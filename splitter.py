"""
Stuff which splits dataset into train and test sets.
"""

class KFoldSplitter(object):
    """Splitter that splits a table into k groups of (almost) equal size.
    Before using this splitter, make sure the table to split has a `group_id` column.

    Sample usage:
    >>> splitter.split('query')
    >>> while splitter.more_rounds():
    >>>     splitter.next_round()
    >>>     # use query_traina and query_test
    """

    def __init__(self, dbm, k):
        """
        @param dbm a DatabaseManager
        @param k the number of folds to split into, k should be > 1
        """
        self.dbm = dbm
        self.k = k
        self.current_table = ''
        self.reset()

    def reset(self):
        self.current_round = 1

    def split(self, table):
        """After splitting, 1 <= table.group_id <= k"""
        self.current_table = table
        self.dbm.begin()
        self.dbm.query('UPDATE %s SET group_id = FLOOR(1 + RAND()*%d)' % (table, self.k))
        self.dbm.commit()

    def more_rounds(self):
        return self.current_round <= self.k

    def next_round(self):
        """Prepare table_train and table_test tables.
        They are **actually** views."""
        self.dbm.begin()
        self.dbm.query('CREATE OR REPLACE VIEW %s_test AS SELECT * FROM %s WHERE group_id = %d' % (self.current_table, self.current_table, self.current_round))
        self.dbm.query('CREATE OR REPLACE VIEW %s_train AS SELECT * FROM %s WHERE group_id != %d' % (self.current_table, self.current_table, self.current_round))
        self.dbm.commit()

        # don't forget to increment round otherwise client might get stuck in infinite loop
        self.current_round += 1
