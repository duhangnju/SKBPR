import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# results of N = 5, 10, 15, 20
Ns = [5, 10, 15, 20]

small_dataset_precisions = {
    'Hottest': ('ro-', [0.0368, 0.0342, 0.0300, 0.0284]),
    'SKBPR-BC': ('go-', [0.0558, 0.0486, 0.0439, 0.0420]),
    'SKBPR-BCIPF': ('bo-', [0.0583, 0.0502, 0.0457, 0.0430]),
}

large_dataset_precisions = {
    'Hottest': ('ro-', [0.0217, 0.0156, 0.0135, 0.0132]),
    'SKBPR-BC': ('go-', [0.0363, 0.0295, 0.0264, 0.0243]),
    'SKBPR-BCIPF': ('bo-', [0.0398, 0.0321, 0.0282, 0.0259]),
}

small_dataset_recalls = {
    'Hottest': ('ro-', [0.1064, 0.1556, 0.2033, 0.2374]),
    'SKBPR-BC': ('go-', [0.1115, 0.1659, 0.2103, 0.2532]),
    'SKBPR-BCIPF': ('bo-', [0.1167, 0.1781, 0.2273, 0.2652]),
}

large_dataset_recalls = {
    'Hottest': ('ro-', [0.0523, 0.0745, 0.0943, 0.0981]),
    'SKBPR-BC': ('go-', [0.0832, 0.1136, 0.1386, 0.1561]),
    'SKBPR-BCIPF': ('bo-', [0.0942, 0.1289, 0.1517, 0.1732]),
}

def output_dataset(fig, title, labels, pos, dataset, axis):
    ax = fig.add_subplot(pos)
    for method, config in dataset.iteritems():
        fmt, data = config
        # plot data with lines
        ax.plot(Ns, data, fmt)
        for n, d in zip(Ns, data):
            # show precise number
            ax.text(n, d, '%.4f' % d)

    xlabel, ylabel = labels
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.axis(axis)# doesn't care about y-axis range
    plt.grid(True)

def output_measure_graph(measure, axis, datasets, filename):
    fig = plt.figure()
    labels = ('N', measure)
    ds_number = len(datasets)
    for i, config in enumerate(datasets, 1):
        name, dataset = config
        title = '%s Plot - %s Dataset' % (measure, name)
        output_dataset(fig, title, labels, '1%d%d' % (ds_number, i), dataset, axis)
    fig.savefig(filename)

if __name__ == '__main__':
    precision_axis = [0, 25, 0.010, 0.060]
    precision_datasets = [
        ('Small', small_dataset_precisions),
        ('Large', large_dataset_precisions),
    ]
    output_measure_graph('Precision', precision_axis, precision_datasets, 'output/basic_precision.png')
    recall_axis = [0, 25, 0.04, 0.30]
    recall_datasets = [
        ('Small', small_dataset_recalls),
        ('Large', large_dataset_recalls),
    ]
    output_measure_graph('Recall', recall_axis, recall_datasets, 'output/basic_recall.png')
