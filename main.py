"""
This file handles runs the actual program.

It imports all the other modules.

The final output contains two parts:
    1. In the console, there is a dictionary mapping the years to a list containing change in
    global mean sea level change by each factor.

    The 0th index of the list is the global mean sea level change due to the ocean heat capacity.
    The 1st index of the list is the global mean sea level change due to melting glaciers.
    The 2nd index of the list is the global mean sea level change due to melting ice sheets.

    2. A window opens where the Pygame simulation is running.

This file is Copyright (c) 2020 Yousuf Hassan, Aaditya Mandal, Faraz Hossein, and Dinkar Verma.
"""

if __name__ == '__main__':
    import computations
    import simulation
    from pprint import pprint

    # Perform all the computations.
    data = computations.read_csv('Datasets/global_mean_sea_level.csv')
    data_1993_2020 = computations.mean_sea_level_change(data)
    data_2021_2080 = computations.predict_2021_2080(data_1993_2020['2020'])
    data_2081_2100 = computations.predict_2081_2100(data_2021_2080['2080'])

    # The variable below is the dictionary of the total data.
    combined_data = computations.combine_data(data_1993_2020, data_2021_2080, data_2081_2100)

    # Print the contributions from each factor to the console.
    pprint(computations.factor_contribution(combined_data))

    # Code for running the simulation.
    simulation.run_simulation()
