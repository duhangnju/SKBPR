import numpy as np
import matplotlib.pyplot as plt

marker_settings = {
    'Hottest': 'ro-',
    'SKBPR-BC': 'gs-',
    'SKBPR-BCIPF': 'b^-',
    'SKBPR-BCIPF-FB': 'mD-',
}

def output_dataset(fig, title, labels, pos, dataset, axis):
    ax = fig.add_subplot(pos)
    for method, data in dataset.iteritems():
        marker = marker_settings[method]
        x_data, y_data = data
        # plot data with lines
        ax.plot(x_data, y_data, marker, label=method)
        for n, d in zip(x_data, y_data):
            # show precise number
            ax.text(n, d, '%.4f' % d)

    xlabel, ylabel = labels
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.axis(axis)# doesn't care about y-axis range
    plt.grid(True)

def output_graph(datasets, filename):
    """
    @param datasets list of (Measure, Name, Axes, xy_data)
    @param filename the name of file to write to
    """
    # default is 8x6, which is so narrow that labels overlap
    # so make it wider
    fig = plt.figure(figsize=(10, 6))# default dpi=72
    ds_number = len(datasets)
    for i, config in enumerate(datasets, 1):
        measure, name, axis, dataset = config
        labels = ('N', measure)
        title = '%s Plot - %s Dataset' % (measure, name)
        output_dataset(fig, title, labels, '1%d%d' % (ds_number, i), dataset, axis)
    fig.savefig(filename)
