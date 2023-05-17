import copy
import json
from statistics import mean

import numpy as np
from numpy import std

from tp4.pca_plots import plot_biplot
from tp4.tools import standardize_data, csv_to_dict

def main():
    countries, labels, country_data = csv_to_dict("./europe.csv")
    standarized_country_data = standardize_data(country_data)

    # np.float64 is required to build correlation matrix
    data_values = np.array(list(standarized_country_data.values())).astype(np.float64)
    labels.pop(0) # Pop 'Country' label, is unncesary for this plot
    plot_biplot(data_values, countries, labels)

if __name__ == '__main__':
    main()
