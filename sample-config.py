"""
Configuration for SKBPR.
Edit and save as config.py
"""

# Database
DB_HOST = 'localhost'
DB_NAME = 'Your database'
DB_USER = 'Your username'
DB_PASSWORD = 'Your password'
DB_CHARSET = 'utf8'

# Tables
TABLES = {
    'QUERY': 'query',
    'ITEM': 'product',
    'QUERY_ITEM': 'query_product',
}

# Test config
from splitter import KFoldSplitter
from database import DatabaseManager
from word_segment import SpaceWordSegmenter
from evaluator import ConfusionMatrixEvaluator
from recommender import KeywordRecommender, HottestRecommender, BCIPFMeasure

# Top-N
N = 5
# for KFoldSplitter
K = 10
# Variations
Splitter = KFoldSplitter
WordSegmenter = SpaceWordSegmenter
RelevanceMeasure = BCIPFMeasure
Evaluator = ConfusionMatrixEvaluator
Recommenders = (KeywordRecommender, HottestRecommender)

# Misc
stopwords = 'stopwords'
