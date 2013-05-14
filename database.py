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
        Note: it's the call's responsibility to call .close() on the returned cursor
        @return cursor"""
        cursor = self.conn.cursor(self.__get_cursor_type(use_dict))

        cursor.execute(sql, values)
        return cursor

    def query(self, sql, values=()):
        """Execute any SQL and return affected rows."""
        cursor = self.__query(sql, values)
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def begin(self):
        self.query('BEGIN')

    def commit(self):
        self.query('BEGIN')

    def insert(self, sql, values=()):
        """Insert a row and return insert id."""
        cursor = self.__query(sql, values)
        lastrowid = cursor.lastrowid
        cursor.close()
        return lastrowid

    def batch_insert(self, sql, values):
        """Insert many rows at a time."""
        cursor = self.conn.cursor()
        cursor.executemany(sql, values)
        cursor.close()

    def get_one_row(self, sql, values=(), return_tuple=False):
        """Get one row of SELECT query.
        Tip: setting return_tuple=True returns tuple so you can unpack with ease.
        """
        cursor = self.__query(sql, values, use_dict=not return_tuple)
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_rows(self, sql, values=()):
        """[Generator]Get rows of SELECT query."""
        cursor = self.__query(sql, values)

        for i in xrange(cursor.rowcount):
            yield cursor.fetchone()

        cursor.close()

    def get_value(self, sql, values=(), idx=0):
        """Get value of the first row.
        Does not check for empty row, so ensure the result is not empty.
        This is handy if you want to retrive COUNT(*)."""
        cursor = self.__query(sql, values, use_dict=False)
        row = cursor.fetchone()
        cursor.close()
        return row[idx]
