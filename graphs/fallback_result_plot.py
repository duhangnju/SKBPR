from plot_common import output_graph

# results of N = 5, 10, 15, 20
Ns = [5, 10, 15, 20]

small_dataset_precisions = {
    'SKBPR-BCIPF': (Ns, [0.0583, 0.0502, 0.0457, 0.0430]),
    'SKBPR-BCIPF-FB': (Ns, [0.0511, 0.0414, 0.0370, 0.0336]),
}

large_dataset_precisions = {
    'SKBPR-BCIPF': (Ns, [0.0398, 0.0321, 0.0282, 0.0259]),
    'SKBPR-BCIPF-FB': (Ns, [0.0368, 0.0275, 0.0231, 0.0206]),
}

small_dataset_recalls = {
    'SKBPR-BCIPF': (Ns, [0.1167, 0.1781, 0.2273, 0.2652]),
    'SKBPR-BCIPF-FB': (Ns, [0.1207, 0.1867, 0.2398, 0.2809]),
}

large_dataset_recalls = {
    'SKBPR-BCIPF': (Ns, [0.0942, 0.1289, 0.1517, 0.1732]),
    'SKBPR-BCIPF-FB': (Ns, [0.0960, 0.1320, 0.1555, 0.1781]),
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
