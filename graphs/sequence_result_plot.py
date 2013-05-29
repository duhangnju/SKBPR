from plot_common import output_graph

# results of N = 5, 10, 15, 20
Ns = [5, 10, 15, 20]

large_dataset_precisions = {
    'SKBPR-BC': (Ns, [0.0366, 0.0297, 0.0263, 0.0244], [0.0004, 0.0003, 0.0002, 0.0002], [0.0002, 0.0003, 0.0003, 0.0003]),
    'SKBPR-BC-SEQ': (Ns, [0.0363, 0.0293, 0.0260, 0.0241], [0.0001, 0.0002, 0.0003, 0.0002], [0.0003, 0.0002, 0.0003, 0.0002]),
}

large_dataset_recalls = {
    'SKBPR-BC': (Ns, [0.0844, 0.1139, 0.1367, 0.1559], [0.0011, 0.0010, 0.0010, 0.0006], [0.0011, 0.0011, 0.0006, 0.0004]),
    'SKBPR-BC-SEQ': (Ns, [0.0855, 0.1154, 0.1384, 0.1578], [0.0005, 0.0006, 0.0007, 0.0006], [0.0007, 0.0006, 0.0009, 0.0010]),
}

if __name__ == '__main__':
    precision_axis = [0, 25, 0.020, 0.040]
    recall_axis = [0, 25, 0.06, 0.20]
    # draw precision and recall on on graph
    # omit results of small datasets
    mixed_datasets = [
        ('Precision', 'Large', precision_axis, large_dataset_precisions),
        ('Recall', 'Large', recall_axis, large_dataset_recalls),
    ]
    output_graph(mixed_datasets, 'output/sequence_precision_recall.png')
