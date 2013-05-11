import config
import unittest
import MySQLdb.cursors
from database import DatabaseManager

class CursorTypeTest(unittest.TestCase):
    def test_cursor_type(self):
        dbm = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
        get_cursor_type = dbm._DatabaseManager__get_cursor_type
        self.assertEqual(get_cursor_type(use_dict=True), MySQLdb.cursors.DictCursor)
        self.assertEqual(get_cursor_type(use_dict=False), MySQLdb.cursors.Cursor)
        dbm.close()

    def test_cursor_type_large(self):
        dbm = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME, large_scale=True)
        get_cursor_type = dbm._DatabaseManager__get_cursor_type
        self.assertEqual(get_cursor_type(use_dict=True), MySQLdb.cursors.SSDictCursor)
        self.assertEqual(get_cursor_type(use_dict=False), MySQLdb.cursors.SSCursor)
        dbm.close()


class DatabaseManagerTest(unittest.TestCase):
    def setUp(self):
        self.dbm = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)

    def tearDown(self):
        self.dbm.close()

    def table_exists(self, table_name):
        __query = self.dbm._DatabaseManager__query
        cursor = __query('SHOW TABLES LIKE %s', (table_name))
        return cursor.rowcount == 1

    def test_query(self):
        random_table_name = 'gmucrjcx'
        self.assertFalse(self.table_exists(random_table_name))
        self.dbm.query('CREATE TABLE %s (id integer)' % (random_table_name))
        self.assertTrue(self.table_exists(random_table_name))
        self.dbm.query('DROP TABLE %s' % (random_table_name))
        self.assertFalse(self.table_exists(random_table_name))

    def test_insert_and_get_value(self):
        random_table_name = 'ghgsnimb'
        count_query = 'SELECT COUNT(*) FROM %s' % (random_table_name)
        self.dbm.query('CREATE TABLE %s (id integer PRIMARY KEY AUTO_INCREMENT)' % (random_table_name))
        self.assertEqual(self.dbm.get_value(count_query), 0)
        self.assertTrue(self.dbm.insert('INSERT INTO %s VALUES (NULL)' % (random_table_name)) > 0)
        self.assertEqual(self.dbm.get_value(count_query), 1)
        self.assertTrue(self.dbm.insert('INSERT INTO %s VALUES (NULL)' % (random_table_name)) > 0)
        self.assertEqual(self.dbm.get_value(count_query), 2)
        self.dbm.query('DROP TABLE %s' % (random_table_name))


if __name__ == '__main__':
    unittest.main()
