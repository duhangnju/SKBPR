import config
from tester import Tester

if __name__ == '__main__':
    print 'Running tests on database [%s]' % config.DB_NAME

    dbm = config.DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    try:
        # set up recommender
        word_segmenter = config.WordSegmenter()
        recommenders = [R(config.N, dbm, word_segmenter, M()) for R, M in config.Recommenders]

        # set up tester
        splitter = config.Splitter(dbm, config.K)
        evaluator = config.Evaluator()
        tester = Tester(dbm, recommenders, splitter, evaluator)

        # fire!
        tester.run()
    finally:
        dbm.close()
