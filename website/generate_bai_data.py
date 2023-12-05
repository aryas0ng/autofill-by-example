import numpy as np
import csv

np.random.seed(42)

num_ppl = 30

# Generate heights in the range [150, 190] (in cm)
heights = np.random.uniform(150, 190, num_ppl)
heights = [round(h, 2) for h in heights]

# Generate hip circumferences based on a normal distribution with mean 100 and sd 10 (in cm)
hip_circ = np.random.normal(100, 10, num_ppl)
hip_circ = [round(h, 2) for h in hip_circ]

# print(heights, hip_circ)

csv_file = "bai.csv"

nested_list = [heights, hip_circ]
transposed_list = list(map(list, zip(*nested_list)))

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(transposed_list)

