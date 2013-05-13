"""
Keyword Recommenders.
"""

import math
import config
from utils import timeit
from collections import defaultdict

class HottestRecommender(object):
    def __init__(self, dbm, limit=10):
        """
        @param dbm a DatabaseManager
        @param limit the (maximal) number of recommended products at a time
        """
        self.dbm = dbm
        self.limit = limit
        self.recommend_list = []

    @timeit
    def preprocess(self, query_train_table):
        for row in self.dbm.get_rows('''SELECT pageinfo, COUNT(id) count FROM visit
            WHERE pagetype = 'product' AND pageinfo != '' AND userid IN (
                SELECT user_id FROM %s
            ) GROUP BY pageinfo ORDER BY count DESC LIMIT %d''' % (query_train_table, self.limit)):
            self.recommend_list.append((row['pageinfo'], row['count']))
        #print self.recommend_list

    def recommend(self, query, limit='discarded'):
        return self.recommend_list


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
    def preprocess(self, query_train_table):
        self.dbm.begin()
        self.dbm.query('TRUNCATE TABLE keyword');
        self.dbm.query('TRUNCATE TABLE keyword_product_weight');

        # build keyword-product and product-keyword mapping
        keyword_count = defaultdict(int)
        keyword_product_count = defaultdict(lambda: defaultdict(int))
        product_keyword_count = defaultdict(lambda: defaultdict(int))

        for qrow in self.dbm.get_rows('SELECT id, query FROM %s' % query_train_table):
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

    def recommend(self, query, limit=10):
        keywords = self.ws.segment(query)
        product_weight = defaultdict(float)
        # gather product weights
        for kw in keywords:
            for product, weight in self.__fetch_related_products(kw):
                product_weight[product] += weight

        # convert dict to list for sorting
        product_weight_list = [item for item in product_weight.iteritems()]
        product_weight_list.sort(key=lambda t: t[1], reverse=True)
        return product_weight_list[:limit]

    def __fetch_related_products(self, keyword):
        # TODO: use generator eliminates the potential to cache
        return ((row['product'], row['weight']) for row in self.dbm.get_rows('SELECT product, weight FROM keyword_product_weight WHERE keyword = %s', (keyword,)))


class RelevanceMeasure(object):
    def get_relevance(self, keyword, product, count, related_product_count, related_keyword_count, all_product_count):
        raise NotImplemented


class BCMeasure(RelevanceMeasure):
    def get_relevance(self, keyword, product, count, *args):
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
        recommender.preprocess('query_train')
    finally:
        dbm.close()
