"""
Keyword Recommenders.
"""

import math
import config
from utils import timeit
from collections import defaultdict

class KeywordRecommender(object):
    def __init__(self, dbm, ws, rm):
        """
        Make sure to source rec_tables.sql before using this class.
        @param dbm a DatabaseManager
        @param ws a WordSegmenter
        @param rm a RelevanceMeasure
        """
        self.dbm = dbm
        self.ws = ws
        self.rm = rm

    @timeit
    def preprocess(self):
        self.dbm.begin()
        self.dbm.query('TRUNCATE TABLE keyword');
        self.dbm.query('TRUNCATE TABLE keyword_product_weight');

        # build keyword-product and product-keyword mapping
        keyword_count = defaultdict(int)
        keyword_product_count = defaultdict(lambda: defaultdict(int))
        product_keyword_count = defaultdict(lambda: defaultdict(int))

        for qrow in self.dbm.get_rows('SELECT id, query FROM query'):
            # TODO: consider sequence
            products = [qprow['p_name'] for qprow in self.dbm.get_rows('SELECT DISTINCT(product_name) p_name FROM query_product WHERE query_id = %s', (qrow['id'],))]

            keywords = self.ws.segment(qrow['query'])
            for kw in keywords:
                keyword_count[kw] += 1

                for p in products:
                    keyword_product_count[kw][p] += 1
                    product_keyword_count[p][kw] += 1

        # calculate keyword-product relevance
        all_product_count = self.dbm.get_value('SELECT COUNT(DISTINCT product_name) FROM query_product')
        for keyword, count in keyword_count.iteritems():
            self.dbm.insert('INSERT INTO keyword (keyword, count) VALUES (%s, %s)', (keyword, count))
            related_product_count = sum(keyword_product_count[keyword].values())

            for product, count in keyword_product_count[keyword].iteritems():
                related_keyword_count = sum(product_keyword_count[product].values())
                # delegate to sub-classes
                relevance = self.rm.get_relevance(keyword, product, count, related_product_count, related_keyword_count, all_product_count)
                self.dbm.insert('INSERT INTO keyword_product_weight (keyword, product, weight) VALUES (%s, %s, %s)', (keyword, product, relevance))

        self.dbm.commit()


class RelevanceMeasure(object):
    def get_relevance(self, keyword, product, count, related_product_count, related_keyword_count):
        raise NotImplemented


class BCMeasure(RelevanceMeasure):
    def get_relevance(self, keyword, product, count, related_product_count, related_keyword_count, all_product_count):
        return count


class BCIPFMeasure(RelevanceMeasure):
    def get_relevance(self, keyword, product, count, related_product_count, related_keyword_count, all_product_count):
        ipf = math.log(1.0 * all_product_count / related_product_count)
        return count * ipf

if __name__ == '__main__':
    from database import DatabaseManager
    from word_segment import SpaceWordSegmenter
    dbm = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    try:
        word_segmenter = SpaceWordSegmenter()
        rmeasure = BCIPFMeasure()
        recommender = KeywordRecommender(dbm, word_segmenter, rmeasure)
        recommender.preprocess()
    finally:
        dbm.close()
