"""
Process raw data.
"""

import config
from utils import timeit
from query_extract import load_stop_words, QueryExtractor

class RawDataPreprocessor(object):
    """Populate query, product, query_product tables.
    Make sure to source tables.sql before using this class."""

    def __init__(self, dbm):
        self.dbm = dbm
        stopwords = None
        if hasattr(config, 'stopwords'):
            stopwords = load_stop_words(config.stopwords)
        self.query_extractor = QueryExtractor(stopwords)

    def run(self):
        self.__populate_query_table()
        self.__populate_product_table()
        self.__populate_query_product_table()

    @timeit
    def __populate_query_table(self):
        self.dbm.begin()
        self.dbm.query('TRUNCATE TABLE query');
        for row in self.dbm.get_rows("SELECT userid, refer FROM user WHERE refer IS NOT NULL AND refer != '' AND refer != 'null'"):
            visit_count = self.dbm.get_value("SELECT count(id) visit_count FROM visit WHERE userid = %s AND pagetype = 'product'", (row['userid'],))
            if visit_count > 0:
                query = self.query_extractor.extract_query(row['refer'], escaped=True)
                if query:
                    try:
                        self.dbm.query("INSERT INTO query (user_id, query) VALUES (%s, %s)", (row['userid'], query))
                    except:
                        print 'Error', query
        self.dbm.commit()

    @timeit
    def __populate_product_table(self):
        self.dbm.begin()
        self.dbm.query('TRUNCATE TABLE product');
        self.dbm.query("INSERT INTO product (name) SELECT DISTINCT(pageinfo) FROM visit WHERE pagetype = 'product'")
        self.dbm.commit()

    @timeit
    def __populate_query_product_table(self):
        self.dbm.begin()
        self.dbm.query('TRUNCATE TABLE query_product');
        for qrow in self.dbm.get_rows("SELECT id, user_id FROM query"):
            sequence = 1
            for vrow in self.dbm.get_rows("SELECT pageinfo FROM visit WHERE pagetype = 'product' AND userid = %s ORDER BY time ASC", (qrow['user_id'],)):
                order_count = self.dbm.get_value("SELECT count(id) order_count FROM orderrecord WHERE userid = %s AND item = %s", (qrow['user_id'], vrow['pageinfo']))
                # the bought field can actually be updated with one query
                bought = 2 if order_count > 0 else 0
                self.dbm.insert("INSERT INTO query_product (query_id, product_name, bought, sequence) VALUES (%s, %s, %s, %s)", (qrow['id'], vrow['pageinfo'], bought, sequence))
                sequence += 1
        self.dbm.commit()

if __name__ == '__main__':
    from database import DatabaseManager
    dbm = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    try:
        preprocessor = RawDataPreprocessor(dbm)
        preprocessor.run()
    finally:
        dbm.close()
