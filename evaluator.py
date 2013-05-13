"""
Evaluate recommendations.
"""

class ConfusionMatrixEvaluator(object):
    """Evaluate result's precision and recall."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.results = []

    def round_start(self):
        """Reset data for new round."""
        self.precisions = []
        self.recalls = []

    def evaluate(self, actual_result, test_result):
        """
        @param actual_results the set of actual products
        @param test_results the set of calculated products
        """
        correct_count = float(len(actual_result & test_result))
        precision = correct_count / len(test_result) if test_result else 0.0
        self.precisions.append(precision)
        recall = correct_count / len(actual_result) if actual_result else 0.0
        self.recalls.append(recall)

    def round_end(self):
        avg_precision = sum(self.precisions) / len(self.precisions)
        avg_recall = sum(self.recalls) / len(self.recalls)
        self.results.append((avg_precision, avg_recall))

    def summary(self):
        print# empty line
        all_precision = 0.0
        all_recall = 0.0
        for i, result in enumerate(self.results, 1):
            precision, recall = result
            print 'Round %2d: precision: %.4f | recall: %.4f' % (i, precision, recall)
            all_precision += precision
            all_recall += recall

        n = len(self.results)
        print ' Average: precision: %.4f | recall: %.4f' % (all_precision/n, all_recall/n)
