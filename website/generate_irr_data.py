import random
import csv
import numpy_financial as npf

def generate_irr(num_rows, num_periods):
    table = []
    for _ in range(num_rows):
        present_values = [random.uniform(1000, 10000) for _ in range(num_periods)]

        present_values[0] *= -1

        irr = round(npf.irr(present_values), 3)
        
        present_values.append(irr)
        table.append(present_values)

    return table

num_rows = 20

num_periods = 5

random_table = generate_irr(num_rows, num_periods)

csv_file = "irr.csv"

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(random_table)

