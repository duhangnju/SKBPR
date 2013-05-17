"""
Process raw data.
Populate query, product, query_product tables with data from user, visit.
"""

from utils import timeit
from query_extract import load_stop_words, QueryExtractor

class RawDataPreprocessor(object):
    """Populate query, product, query_product tables.
    Make sure to source tables.sql before using this class."""

    def __init__(self, dbm, session_duration, stopwords_file=None):
        """
        @param dbm a DatabaseManager
        @param session_duration valid session duration in seconds
        """
        self.dbm = dbm
        self.session_duration = session_duration
        stopwords = None
        if stopwords_file:
            stopwords = load_stop_words(stopwords_file)
        self.query_extractor = QueryExtractor(stopwords)

    def run(self):
        self.__populate_query_table()
        self.__populate_product_table()
        self.__populate_query_product_table()

    @timeit
    def __populate_query_table(self):
        self.dbm.begin()
        self.dbm.query('TRUNCATE TABLE query');

        # get all user with non-empty referrer
        # take care! besides NULL, there's 'null'
        invalid = 0
        for row in self.dbm.get_rows("SELECT userid, refer FROM user WHERE refer IS NOT NULL AND refer != '' AND refer != 'null'"):
            time_row = self.dbm.get_one_row('SELECT vtime - utime AS diff FROM (SELECT MIN(V.time) AS vtime, u.time AS utime FROM visit V JOIN user U ON V.userid = U.userid WHERE U.userid = %s GROUP BY V.userid) T', (row['userid'],))
            if time_row == None or time_row['diff'] != 0:
                # data corrupted: first visit's time is inconsistent in user and visit tables
                # actually we can allow 0 <= diff < THRESHOLD (say 24h), but let't be simple here
                invalid += 1
                continue

            visit_count = self.dbm.get_value("SELECT COUNT(id) visit_count FROM visit WHERE userid = %s AND pagetype = 'product'", (row['userid'],))
            if visit_count == 0:
                # the user needs to visit more than one product page to be valid
                invalid += 1
                continue

            query = self.query_extractor.extract_query(row['refer'], escaped=True)
            # avoid cases when we cannot extract a meaningful query
            if query:
                try:
                    self.dbm.query("INSERT INTO query (user_id, query) VALUES (%s, %s)", (row['userid'], query))
                except:
                    invalid += 1
                    # prevent corrupted unicode string
                    print 'Corrupted string', query

        self.dbm.commit()

        self.query_count = self.dbm.get_value('select COUNT(*) FROM query')
        print 'Query table statistics (inserted/discarded): %d/%d (%.2f%%)' % (self.query_count, invalid, 100.0*self.query_count/(self.query_count+invalid))

    @timeit
    def __populate_product_table(self):
        self.dbm.begin()
        self.dbm.query('TRUNCATE TABLE product');
        self.dbm.query("INSERT INTO product (name) SELECT DISTINCT(pageinfo) FROM visit WHERE pagetype = 'product'")
        self.dbm.commit()

        self.product_count = self.dbm.get_value('select COUNT(*) FROM product')
        max_count = self.dbm.get_value('select COUNT(*) FROM products')
        print '\nProduct table statistics (inserted/maximum): %d/%d (%.2f%%)' % (self.product_count, max_count, 100.0*self.product_count/max_count)

    @timeit
    def __populate_query_product_table(self):
        self.dbm.begin()
        self.dbm.query('TRUNCATE TABLE query_product');
        for qrow in self.dbm.get_rows("SELECT id, user_id FROM query"):
            sequence = 1
            # in __populate_query_table, we guarantee user.time is the same as MIN(visit.time)
            start_time = self.dbm.get_value("SELECT time FROM user WHERE userid = %s", (qrow['user_id'],))
            session_end_time = self.get_session_end(start_time)
            for vrow in self.dbm.get_rows("SELECT pageinfo, pagetype FROM visit WHERE userid = %s AND time <= %s ORDER BY time ASC", (qrow['user_id'], session_end_time)):
                # only consider product visits, but don't filter out others in SQL
                # to get the actual sequence
                if vrow['pagetype'] == 'product':
                    order_count = self.dbm.get_value("SELECT COUNT(id) order_count FROM orderrecord WHERE userid = %s AND item = %s", (qrow['user_id'], vrow['pageinfo']))
                    # the bought field can actually be updated with one query
                    bought = 2 if order_count > 0 else 0
                    self.dbm.insert("INSERT INTO query_product (query_id, product_name, bought, sequence) VALUES (%s, %s, %s, %s)", (qrow['id'], vrow['pageinfo'], bought, sequence))
                sequence += 1

        self.dbm.commit()

        count = self.dbm.get_value('select COUNT(*) FROM query_product')
        max_count = self.query_count * self.product_count
        print '\nQuery-Product table statistics (inserted/maximum): %d/%d (%.2f%%)' % (count, max_count, 100.0*count/max_count)

    def get_session_end(self, start_time):
        """Get session end time.
        @param start_time string of timestamp in milliseconds
        @return string of the same format
        """
        start_ts = int(start_time)
        end_ts = start_ts + self.session_duration * 1000
        return str(end_ts)

if __name__ == '__main__':
    import config
    from database import DatabaseManager
    dbm = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    try:
        swf = None
        if hasattr(config, 'stopwords'):
            swf = config.stopwords
        preprocessor = RawDataPreprocessor(dbm, config.session_duration, stopwords_file=swf)
        preprocessor.run()
    finally:
        dbm.close()
