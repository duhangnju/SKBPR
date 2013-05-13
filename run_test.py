import config
from tester import Tester
from splitter import KFoldSplitter
from database import DatabaseManager
from word_segment import SpaceWordSegmenter
from evaluator import ConfusionMatrixEvaluator
from recommender import KeywordRecommender, BCIPFMeasure

if __name__ == '__main__':
    dbm = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    try:
        # set up recommender
        word_segmenter = SpaceWordSegmenter()
        rmeasure = BCIPFMeasure()
        recommender = KeywordRecommender(config.N, dbm, word_segmenter, rmeasure)

        # set up tester
        splitter = KFoldSplitter(dbm, config.K)
        evaluator = ConfusionMatrixEvaluator()
        tester = Tester(dbm, recommender, splitter, evaluator)

        # fire!
        tester.run()
    finally:
        dbm.close()
