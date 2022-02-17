"""
This file handles all the computations of the program.

All the corresponding global mean sea level values are in mm.
The details of each computation is in its function docstring.

This file is Copyright (c) 2020 Yousuf Hassan, Aaditya Mandal, Faraz Hossein, and Dinkar Verma.
"""

import csv
import pprint
from typing import Dict, List
import python_ta


def read_csv(filename: str) -> Dict[str, float]:
    """ Read the csv file and return a dictionary mapping the years to the global mean
    sea levels.
    """
    average_data = {}
    with open(filename) as file:
        reader = csv.reader(file)

        for _ in range(0, 8):  # skip over the first 8 rows
            next(reader)

        for row in reader:
            if row[4] != '':
                average_data[row[0]] = float(row[4])
            elif row[3] != '':
                average_data[row[0]] = float(row[3])
            elif row[2] != '':
                average_data[row[0]] = float(row[2])
            else:
                average_data[row[0]] = float(row[1])

        return average_data


def mean_sea_level_change(csv_data: Dict[str, float]) -> Dict[str, float]:
    """ Calculate the average global mean sea level for each year and return a dictionary
    mapping the years to the average global mean sea levels for that year.

    This function calculates the average global mean sea level by adding all the values
    for a specific year and then dividing it by the total amount of values.


    """
    average_data = {}

    for year in csv_data:
        whole_year = year[0:4]
        if whole_year not in average_data:
            average_data[whole_year] = [csv_data[year]]
        else:
            average_data[whole_year].append(csv_data[year])

    for year in average_data:
        average_data[year] = round(sum(average_data[year]) / len(average_data[year]), 2)

    return average_data


def predict_2021_2080(sea_level_2020: float) -> Dict[str, float]:
    """ Predict the global mean sea level for each year from 2021 to 2080 and return a
    dictionary mapping the years to the global mean sea level for that year.

    According to NASA, the rate of change is 3.3mm per year.
    """
    data_2021 = {'2020': sea_level_2020}

    for year in range(2021, 2081):
        data_2021[str(year)] = round(data_2021[str(year - 1)] + 3.3, 2)

    return data_2021


def predict_2081_2100(sea_level_2080: float) -> Dict[str, float]:
    """ Predict the global mean sea level for each year from 2081 to 2100 and return a
    dictionary mapping the years to the global mean sea level for that year.

    The rate of change is on average 12mm per year from 2080-2100 (Church et al).
    """
    data_2081 = {'2080': sea_level_2080}

    for year in range(2081, 2101):
        data_2081[str(year)] = round(data_2081[str(year - 1)] + 12.0, 2)

    return data_2081


def combine_data(data_1993: Dict[str, float], data_2021: Dict[str, float],
                 data_2081: Dict[str, float]) -> Dict[str, float]:
    """ Return a combination of all three dictionaries.
    """
    data_1993.update(data_2021)
    data_1993.update(data_2081)

    return data_1993


def factor_contribution(total_data: Dict[str, float]) -> Dict[str, List[float]]:
    """Return a dictionary mapping the years to a list containing global mean sea level
    change by each factor.

    The 0th index of the list is the global mean sea level rise due to the ocean heat capacity.
    The 1st index of the list is the global mean sea level rise due to melting glaciers.
    The 2nd index of the list is the global mean sea level rise due to melting ice sheets.

    After performing calculations on Table 13.1, we find that on average, roughly 41% of the global
    mean sea level rise is a result of thermal expansion due to ocean heat contents, 35% is a
    result of melting glaciers, and 24% is a result of melting ice sheets (Church et al. 1151).
    """
    factor_data = {}

    for year in total_data:
        heat_capacity_contribution = round(0.41 * total_data[year], 2)
        glaciers_contribution = round(0.35 * total_data[year], 2)
        ice_sheets_contribution = round(0.24 * total_data[year], 2)
        factor_data[year] = [heat_capacity_contribution, glaciers_contribution,
                             ice_sheets_contribution]

    return factor_data


if __name__ == '__main__':
    data = read_csv('Datasets/global_mean_sea_level.csv')
    data_1993_2020 = mean_sea_level_change(data)
    data_2021_2080 = predict_2021_2080(data_1993_2020['2020'])
    data_2081_2100 = predict_2081_2100(data_2021_2080['2080'])
    combined_data = combine_data(data_1993_2020, data_2021_2080, data_2081_2100)
    pprint.pprint(combined_data)
    pprint.pprint(factor_contribution(combined_data))

    python_ta.check_all(config={
        'extra-imports': ['csv', 'Dict', 'List', 'pprint'],  # the names (strs) of imported modules
        'allowed-io': ['read_csv'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
