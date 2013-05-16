"""
Orchestrate recommender/splitter/evaluators to run a SKBPR test.
"""

class Tester(object):
    def __init__(self, dbm, recommenders, splitter, evaluator):
        self.dbm = dbm
        self.recommenders = recommenders
        self.splitter = splitter
        self.evaluator = evaluator

    def run(self):
        # split only once to ensure the same for all recommenders
        self.splitter.split('query')
        for recommender in self.recommenders:
            self.evaluator.reset()
            self.splitter.reset()
            self.__run(recommender)

    def __run(self, recommender):
        print '\nRunning %s ...' % recommender

        _round = 1
        while self.splitter.more_rounds():
            # advance to next train/test set
            self.splitter.next_round()
            self.evaluator.round_start()
            print 'Round', _round

            # train recommender
            recommender.preprocess('query_train')

            # start test
            for row in self.dbm.get_rows('SELECT id, query from query_test'):
                actual_products = self.get_actual_products(row['id'])
                recommended_products = set(rec[0] for rec in recommender.recommend(row['query']))
                self.evaluator.evaluate(actual_products, recommended_products)

            # let evaluate record result of this round
            self.evaluator.round_end()

            recommender.round_statistics()
            _round += 1

        # output summary of all results
        self.evaluator.summary()

    def get_actual_products(self, query_id):
        return set(row['product_name'] for row in self.dbm.get_rows('SELECT product_name FROM query_product WHERE query_id = %s', (query_id,)))
