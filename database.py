"""
Database Manager.
"""

import MySQLdb
import MySQLdb.cursors

class DatabaseManager(object):
    def __init__(self, host, user, passwd, database, charset='utf8', large_scale=False):
        """Be careful using large_scale=True, SSDictCursor seems not reliable."""
        self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=database, charset=charset)
        self.large_scale = large_scale

    def close(self):
        self.conn.close()

    # put here for better understandability
    cursor_types = {
        True: {
            True: MySQLdb.cursors.SSDictCursor,
            False: MySQLdb.cursors.SSCursor,
        },
        False: {
            True: MySQLdb.cursors.DictCursor,
            False: MySQLdb.cursors.Cursor,
        },
    }

    def __get_cursor_type(self, use_dict):
        return self.cursor_types[self.large_scale][use_dict]

    def __query(self, sql, values=(), use_dict=True):
        """Execute any SQL.
        You can use %s placeholder in sql and fill with values.
        return cursor"""
        cursor = self.conn.cursor(self.__get_cursor_type(use_dict))

        cursor.execute(sql, values)
        return cursor

    def query(self, sql, values=()):
        """Execute any SQL and return affected rows."""
        cursor = self.__query(sql, values)
        return cursor.rowcount

    def insert(self, sql, values=()):
        """Insert a row and return insert id."""
        cursor = self.__query(sql, values)
        return cursor.lastrowid

    def get_rows(self, sql, values=()):
        """[Generator]Get rows of SELECT query."""
        cursor = self.__query(sql, values)

        for i in xrange(cursor.rowcount):
            yield cursor.fetchone()

    def get_value(self, sql, idx=0):
        """Get value of the first row.
        This is handy if you want to retrive COUNT(*)."""
        cursor = self.__query(sql, use_dict=False)
        row = cursor.fetchone()
        return row[idx]
