from plot_common import output_graph

# results of N = 5, 10, 15, 20
Ns = [5, 10, 15, 20]

large_dataset_precisions = {
    'SKBPR-BCIPF': (Ns, [0.0401, 0.0321, 0.0281, 0.0259], [0.0004, 0.0003, 0.0002, 0.0001], [0.0002, 0.0002, 0.0004, 0.0003]),
    'SKBPR-BCIPF-FB': (Ns, [0.0370, 0.0283, 0.0242, 0.0219], [0.0001, 0.0002, 0.0002, 0.0001], [0.0003, 0.0001, 0.0003, 0.0001]),
}

large_dataset_recalls = {
    'SKBPR-BCIPF': (Ns, [0.0955, 0.1286, 0.1522, 0.1726], [0.0007, 0.0012, 0.0013, 0.0006], [0.0009, 0.0013, 0.0017, 0.0008]),
    'SKBPR-BCIPF-FB': (Ns, [0.0974, 0.1309, 0.1546, 0.1752], [0.0008, 0.0012, 0.0013, 0.0006], [0.0009, 0.0012, 0.0017, 0.0008]),
}

if __name__ == '__main__':
    precision_axis = [0, 25, 0.010, 0.050]
    recall_axis = [0, 25, 0.04, 0.25]
    # draw precision and recall on on graph
    # omit results of small datasets
    mixed_datasets = [
        ('Precision', 'Large', precision_axis, large_dataset_precisions),
        ('Recall', 'Large', recall_axis, large_dataset_recalls),
    ]
    output_graph(mixed_datasets, 'output/fallback_precision_recall.png')
