"""
Evaluate recommendations.
"""

class ConfusionMatrixEvaluator(object):
    """Evaluate result's precision and recall."""

    def __init__(self):
        self.reset()

    def reset(self):
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

    def summary(self):
        avg_precision = sum(self.precisions) / len(self.precisions)
        avg_recall = sum(self.recalls) / len(self.recalls)
        print 'Precision: %.4f, Recall: %.4f' % (avg_precision, avg_recall)
