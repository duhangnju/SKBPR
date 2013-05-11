"""
Query Extraction Stuff.
"""

from urllib import unquote
import urlparse

def load_stop_words(filename):
    """Load a set of stop words from a file.
    One word each line."""
    # you are using CPython, don't you?
    # http://stackoverflow.com/a/11027437/1240620
    stopwords = {w.strip() for w in open(filename)}
    return stopwords


class QueryExtractor(object):
    # possible query parame in descending order of possibility
    QUERY_PARAMS = ['q', 'p', 'query', 'wd', 'searchFor', 'text']

    def __init__(self, stopwords=None):
        self.stopwords = stopwords or set()

    def extract_query(self, url, escaped=False, delimiter=' '):
        if escaped:
            url = unquote(url)

        query_string = urlparse.urlparse(url).query
        queries = urlparse.parse_qs(query_string)

        query_val = ''
        for q in self.QUERY_PARAMS:
            if queries.has_key(q):
                # use the first value, as there could be more than one
                query_val = queries[q][0]
                break

        # remove stop words
        valid_keywords = []
        for word in query_val.split():
            if word and word not in self.stopwords:
                valid_keywords.append(word)

        return delimiter.join(valid_keywords)
