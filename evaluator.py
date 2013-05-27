"""
Evaluate recommendations.
"""
import config
from collections import defaultdict

class ConfusionMatrixEvaluator(object):
    """Evaluate result's precision and recall."""

    def __init__(self):
        self.experiment_reset()
        self.reset()

    def experiment_reset(self):
        self.exp_results = defaultdict(list)

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

    def _avg_result(self, results, print_each=False, scale='Round'):
        all_precision = 0.0
        all_recall = 0.0
        for i, result in enumerate(results, 1):
            precision, recall = result
            if print_each:
                print '%s %2d: precision: %.4f | recall: %.4f' % (scale, i, precision, recall)
            all_precision += precision
            all_recall += recall

        n = len(results)
        return all_precision/n, all_recall/n

    def summary(self, recommender, print_result):
        avg_precision, avg_recall = self._avg_result(self.results, config.verbose)
        self.exp_results[str(recommender)].append((avg_precision, avg_recall))

        if print_result:
            print '>Average: precision: %.4f | recall: %.4f' % (avg_precision, avg_recall)

    def grand_summary(self):
        statistics = []
        for recommender, results in self.exp_results.iteritems():
            avg_precision, avg_recall = self._avg_result(results)
            statistics.append((recommender, avg_precision, avg_recall))
        statistics.sort(key=lambda t:t[1], reverse=True)

        for recommender, precision, recall in statistics:
            print 'Precision: %.4f | Recall %.4f -- %s' % (precision, recall, recommender)
