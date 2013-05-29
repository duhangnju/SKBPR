from plot_common import output_graph

# results of N = 5, 10, 15, 20
Ns = [5, 10, 15, 20]

small_dataset_precisions = {
    'Hottest': (Ns, [0.0360, 0.0342, 0.0296, 0.0277], [0.0003, 0.0000, 0.0006, 0.0003], [0.0014, 0.0001, 0.0007, 0.0002]),
    'SKBPR-BC': (Ns, [0.0552, 0.0484, 0.0442, 0.0422], [0.0015, 0.0009, 0.0011, 0.0006], [0.0013, 0.0006, 0.0009, 0.0004]),
    'SKBPR-BCIPF': (Ns, [0.0572, 0.0502, 0.0459, 0.0434], [0.0016, 0.0010, 0.0009, 0.0005], [0.0011, 0.0005, 0.0005, 0.0004]),
}

large_dataset_precisions = {
    'Hottest': (Ns, [0.0217, 0.0149, 0.0132, 0.0130], [0.0001, 0.0003, 0.0000, 0.0000], [0.0005, 0.0008, 0.0003, 0.0002]),
    'SKBPR-BC': (Ns, [0.0366, 0.0297, 0.0263, 0.0244], [0.0004, 0.0003, 0.0002, 0.0002], [0.0002, 0.0003, 0.0003, 0.0003]),
    'SKBPR-BCIPF': (Ns, [0.0401, 0.0321, 0.0281, 0.0259], [0.0004, 0.0003, 0.0002, 0.0001], [0.0002, 0.0002, 0.0004, 0.0003]),
}

small_dataset_recalls = {
    'Hottest': (Ns, [0.1256, 0.1567, 0.2122, 0.2569], [0.0212, 0.0013, 0.0141, 0.0098], [0.0031, 0.0003, 0.0079, 0.0067]),
    'SKBPR-BC': (Ns, [0.1105, 0.1664, 0.2104, 0.2517], [0.0040, 0.0016, 0.0023, 0.0011], [0.0025, 0.0014, 0.0034, 0.0020]),
    'SKBPR-BCIPF': (Ns, [0.1157, 0.1790, 0.2268, 0.2669], [0.0025, 0.0014, 0.0014, 0.0025], [0.0017, 0.0011, 0.0009, 0.0015]),
}

large_dataset_recalls = {
    'Hottest': (Ns, [0.0526, 0.0792, 0.0979, 0.1003], [0.0009, 0.0037, 0.0029, 0.0021], [0.0002, 0.0016, 0.0004, 0.0004]),
    'SKBPR-BC': (Ns, [0.0844, 0.1139, 0.1367, 0.1559], [0.0011, 0.0010, 0.0010, 0.0006], [0.0011, 0.0011, 0.0006, 0.0004]),
    'SKBPR-BCIPF': (Ns, [0.0955, 0.1286, 0.1522, 0.1726], [0.0007, 0.0012, 0.0013, 0.0006], [0.0009, 0.0013, 0.0017, 0.0008]),
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
