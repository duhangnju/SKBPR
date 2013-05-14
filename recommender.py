"""
Keyword Recommenders.
"""

import math
from utils import timeit
from collections import defaultdict

class HottestRecommender(object):
    def __init__(self, limit, dbm, *ignored):
        """
        @param dbm a DatabaseManager
        @param limit the (maximal) number of recommended products at a time
        """
        self.limit = limit
        self.dbm = dbm
        self.recommend_list = []

    def __str__(self):
        return 'Hottest Recommender[N=%d]' % self.limit

    def use_keywords(self):
        return False

    @timeit
    def preprocess(self, query_train_table):
        for row in self.dbm.get_rows('''SELECT pageinfo, COUNT(id) count FROM visit
            WHERE pagetype = 'product' AND pageinfo != '' AND userid IN (
                SELECT user_id FROM %s
            ) GROUP BY pageinfo ORDER BY count DESC LIMIT %d''' % (query_train_table, self.limit)):
            self.recommend_list.append((row['pageinfo'], row['count']))
        #print self.recommend_list

    def recommend(self, query):
        return self.recommend_list


class KeywordRecommender(object):
    def __init__(self, limit, dbm, ws, rm):
        """
        Make sure to source rec_tables.sql before using this class.
        @param dbm a DatabaseManager
        @param ws a WordSegmenter
        @param rm a RelevanceMeasure
        """
        self.limit = limit
        self.dbm = dbm
        self.ws = ws
        self.rm = rm
        self._related_product_cache = {}

    def __str__(self):
        return 'Keyword Recommender with %s[N=%d]' % (self.rm, self.limit)

    def use_keywords(self):
        return True

    @timeit
    def preprocess(self, query_train_table):
        # empty cache so that cache from last round does not interfere with next round
        self._related_product_cache = {}

        self.dbm.begin()
        self.dbm.query('TRUNCATE TABLE keyword');
        self.dbm.query('TRUNCATE TABLE keyword_product_weight');

        # build keyword-product and product-keyword mapping
        keyword_count = defaultdict(int)
        keyword_product_count = defaultdict(lambda: defaultdict(int))

        for qrow in self.dbm.get_rows('SELECT id, query FROM %s' % query_train_table):
            # GROUP_CONCAT returns a comma-separeted string
            products = [(qprow['product_name'], qprow['sequences']) for qprow in self.dbm.get_rows('SELECT product_name, GROUP_CONCAT(sequence) AS sequences FROM query_product WHERE query_id = %s GROUP BY product_name', (qrow['id'],))]

            keywords = self.ws.segment(qrow['query'])
            for kw in keywords:
                keyword_count[kw] += 1

            for p, sequences in products:
                # get product sequence in this session
                sequences = map(int, sequences.split(','))
                count = self.get_browse_count(sequences)
                # update keyword_product_count
                for kw in keywords:
                    keyword_product_count[kw][p] += count

        # construct product_keyword_count
        # it's actually equivalent to keyword_product_count, but can let compute
        # related_product_count faster
        product_keyword_count = defaultdict(dict)
        for kw, dt in keyword_product_count.iteritems():
            for p, c in dt.iteritems():
                product_keyword_count[p][kw] = c

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

    def get_browse_count(self, sequences):
        """Multiple browses in a session always count 1."""
        return 1

    def recommend(self, query):
        keywords = self.ws.segment(query)
        product_weight = defaultdict(float)
        # gather product weights
        for kw in keywords:
            for product, weight in self.__fetch_related_products(kw):
                product_weight[product] += weight

        # convert dict to list for sorting
        product_weight_list = [item for item in product_weight.iteritems()]
        product_weight_list.sort(key=lambda t: t[1], reverse=True)
        return product_weight_list[:self.limit]

    def __fetch_related_products(self, keyword):
        if not self._related_product_cache.has_key(keyword):
            self._related_product_cache[keyword] = [(row['product'], row['weight']) for row in self.dbm.get_rows('SELECT product, weight FROM keyword_product_weight WHERE keyword = %s', (keyword,))]
        return self._related_product_cache[keyword]


class RelevanceMeasure(object):
    def get_relevance(self, keyword, product, count, related_product_count, related_keyword_count, all_product_count):
        raise NotImplemented


class BCMeasure(RelevanceMeasure):
    def get_relevance(self, keyword, product, count, *ignored):
        return count

    def __str__(self):
        return 'BC'


class BCIPFMeasure(RelevanceMeasure):
    def get_relevance(self, keyword, product, count, related_product_count, related_keyword_count, all_product_count):
        ipf = math.log(1.0 * all_product_count / related_product_count)
        return count * ipf

    def __str__(self):
        return 'BC-IPF'


if __name__ == '__main__':
    import config
    from database import DatabaseManager
    from word_segment import SpaceWordSegmenter
    dbm = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    try:
        word_segmenter = SpaceWordSegmenter()
        rmeasure = BCIPFMeasure()
        recommender = KeywordRecommender(10, dbm, word_segmenter, rmeasure)
        recommender.preprocess('query_train')
    finally:
        dbm.close()
