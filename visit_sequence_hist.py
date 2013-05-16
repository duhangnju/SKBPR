import sys
import math
import config
import numpy as np
import matplotlib.pyplot as plt

SEQ_UPPER_BOUND = 150

if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'sequence_hist.pdf'

    dbm = config.DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    try:
        query = 'SELECT sequence, COUNT(sequence) count FROM query_product WHERE sequence <= %s GROUP BY sequence'
        seq_occur = [(row['sequence'], row['count']) for row in dbm.get_rows(query, (SEQ_UPPER_BOUND,))]

        sequence_range = dbm.get_value('SELECT MAX(sequence)-MIN(sequence)+1 FROM query_product WHERE sequence <= %s', (SEQ_UPPER_BOUND,))
        x_max = sequence_range
        max_occur = max(seq_occur, key=lambda t: t[1])[1]
        y_max = int(1.2 * math.floor(max_occur/1000.0) * 1000)
        arrays = [np.repeat(t[0], t[1]) for t in seq_occur]
        data = np.hstack(arrays)

        fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
        plt.hist(data, bins=sequence_range, facecolor='g', alpha=0.75)
        plt.xlabel('$Sequence$')
        plt.ylabel('$Occurrence$')
        plt.title('$Sequence Occurrence Histogram$')
        plt.axis([0, x_max, 0, y_max])
        plt.grid(True)

        #plt.show()
        fig.savefig(filename)
    finally:
        dbm.close()

