"""
Orchestrate recommender/splitter/evaluators to run a SKBPR test.
"""
import sys

class Tester(object):
    def __init__(self, dbm, repeat, recommenders, splitter, evaluator):
        self.dbm = dbm
        self.repeat = repeat
        self.recommenders = recommenders
        self.splitter = splitter
        self.evaluator = evaluator

    def run(self):
        self.evaluator.experiment_reset()

        for exp_no in range(1, self.repeat+1):
            print '==============================Experiment %3d==============================' % exp_no

            # split only once to ensure the same for all recommenders
            self.splitter.split('query')
            for recommender in self.recommenders:
                self.evaluator.reset()
                self.splitter.reset()
                self.__run(recommender)

            print '------------------------------Experiment End------------------------------\n'

        self.evaluator.grand_summary()

    def __run(self, recommender):
        print 'Running %s ...' % recommender

        _round = 1
        recommender.reset()
        sys.stdout.write('Rounds: ')
        while self.splitter.more_rounds():
            # advance to next train/test set
            self.splitter.next_round()
            self.evaluator.round_start()

            sys.stdout.write('%d ' % _round)
            sys.stdout.flush()

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

        # go to new line
        print

        # output summary of all results
        recommender.experiment_statistics()
        self.evaluator.summary(recommender, True)
        print

    def get_actual_products(self, query_id):
        return set(row['product_name'] for row in self.dbm.get_rows('SELECT product_name FROM query_product WHERE query_id = %s', (query_id,)))
