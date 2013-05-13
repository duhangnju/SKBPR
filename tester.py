"""
Orchestrate recommender/splitter/evaluators to run a SKBPR test.
"""

class Tester(object):
    def __init__(self, dbm, recommender, splitter, evaluator, N):
        self.dbm = dbm
        self.recommender = recommender
        self.splitter = splitter
        self.evaluator = evaluator
        self.N = N

    def run(self):
        self.splitter.split('query')

        _round = 1
        while self.splitter.more_rounds():
            # advance to next train/test set
            self.splitter.next_round()
            self.evaluator.reset()
            print 'Round', _round

            # train recommender
            self.recommender.preprocess('query_train')

            # start test
            for row in self.dbm.get_rows('SELECT id, query from query_test'):
                actual_products = self.get_actual_products(row['id'])
                recommended_products = set(rec[0] for rec in self.recommender.recommend(row['query'], self.N))
                self.evaluator.evaluate(actual_products, recommended_products)

            # get summary of this round
            self.evaluator.summary()
            _round += 1

    def get_actual_products(self, query_id):
        return set(row['product_name'] for row in self.dbm.get_rows('SELECT product_name FROM query_product WHERE query_id = %s', (query_id,)))
