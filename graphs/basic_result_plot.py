from plot_common import output_graph

# results of N = 5, 10, 15, 20
Ns = [5, 10, 15, 20]

small_dataset_precisions = {
    'Hottest': (Ns, [0.0368, 0.0342, 0.0300, 0.0284]),
    'SKBPR-BC': (Ns, [0.0558, 0.0486, 0.0439, 0.0420]),
    'SKBPR-BCIPF': (Ns, [0.0583, 0.0502, 0.0457, 0.0430]),
}

large_dataset_precisions = {
    'Hottest': (Ns, [0.0217, 0.0156, 0.0135, 0.0132]),
    'SKBPR-BC': (Ns, [0.0363, 0.0295, 0.0264, 0.0243]),
    'SKBPR-BCIPF': (Ns, [0.0398, 0.0321, 0.0282, 0.0259]),
}

small_dataset_recalls = {
    'Hottest': (Ns, [0.1064, 0.1556, 0.2033, 0.2374]),
    'SKBPR-BC': (Ns, [0.1115, 0.1659, 0.2103, 0.2532]),
    'SKBPR-BCIPF': (Ns, [0.1167, 0.1781, 0.2273, 0.2652]),
}

large_dataset_recalls = {
    'Hottest': (Ns, [0.0523, 0.0745, 0.0943, 0.0981]),
    'SKBPR-BC': (Ns, [0.0832, 0.1136, 0.1386, 0.1561]),
    'SKBPR-BCIPF': (Ns, [0.0942, 0.1289, 0.1517, 0.1732]),
}

if __name__ == '__main__':
    precision_axis = [0, 25, 0.010, 0.070]
    precision_datasets = [
        ('Precision', 'Small', precision_axis, small_dataset_precisions),
        ('Precision', 'Large', precision_axis, large_dataset_precisions),
    ]
    output_graph(precision_datasets, 'output/basic_precision.png')
    recall_axis = [0, 25, 0.04, 0.35]
    recall_datasets = [
        ('Recall', 'Small', recall_axis, small_dataset_recalls),
        ('Recall', 'Large', recall_axis, large_dataset_recalls),
    ]
    output_graph(recall_datasets, 'output/basic_recall.png')
