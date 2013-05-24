import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# results of N = 5, 10, 15, 20
Ns = [5, 10, 15, 20]

marker_settings = {
    'Hottest': 'ro-',
    'SKBPR-BC': 'gs-',
    'SKBPR-BCIPF': 'b^-',
    'SKBPR-BCIPF-FB': 'mD-',
}

small_dataset_precisions = {
    'SKBPR-BCIPF': [0.0583, 0.0502, 0.0457, 0.0430],
    'SKBPR-BCIPF-FB': [0.0511, 0.0414, 0.0370, 0.0336],
}

large_dataset_precisions = {
    'SKBPR-BCIPF': [0.0398, 0.0321, 0.0282, 0.0259],
    'SKBPR-BCIPF-FB': [0.0368, 0.0275, 0.0231, 0.0206],
}

small_dataset_recalls = {
    'SKBPR-BCIPF': [0.1167, 0.1781, 0.2273, 0.2652],
    'SKBPR-BCIPF-FB': [0.1207, 0.1867, 0.2398, 0.2809],
}

large_dataset_recalls = {
    'SKBPR-BCIPF': [0.0942, 0.1289, 0.1517, 0.1732],
    'SKBPR-BCIPF-FB': [0.0960, 0.1320, 0.1555, 0.1781],
}

def output_dataset(fig, title, labels, pos, dataset, axis):
    ax = fig.add_subplot(pos)
    for method, data in dataset.iteritems():
        marker = marker_settings[method]
        # plot data with lines
        ax.plot(Ns, data, marker, label=method)
        for n, d in zip(Ns, data):
            # show precise number
            ax.text(n, d, '%.4f' % d)

    xlabel, ylabel = labels
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.axis(axis)# doesn't care about y-axis range
    plt.grid(True)

def output_measure_graph(measure, axis, datasets, filename):
    # default is 8x6, which is so narrow that labels overlap
    # so make it wider
    fig = plt.figure(figsize=(10, 6))# default dpi=72
    labels = ('N', measure)
    ds_number = len(datasets)
    for i, config in enumerate(datasets, 1):
        name, dataset = config
        title = '%s Plot - %s Dataset' % (measure, name)
        output_dataset(fig, title, labels, '1%d%d' % (ds_number, i), dataset, axis)
    fig.savefig(filename)

if __name__ == '__main__':
    precision_axis = [0, 25, 0.010, 0.070]
    precision_datasets = [
        ('Small', small_dataset_precisions),
        ('Large', large_dataset_precisions),
    ]
    output_measure_graph('Precision', precision_axis, precision_datasets, 'output/fallback_precision.png')
    recall_axis = [0, 25, 0.04, 0.35]
    recall_datasets = [
        ('Small', small_dataset_recalls),
        ('Large', large_dataset_recalls),
    ]
    output_measure_graph('Recall', recall_axis, recall_datasets, 'output/fallback_recall.png')
