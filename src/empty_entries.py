import numpy as np
import pandas as pd
from math import prod

# If there is any empty entry in the table, return True for the first return
# value. Otherwise, return False for the first return value.
# If there are indeed empty entries in the table, and if there are empty entries
# in the example rows (first few rows), it's the filter case. If the overall
# empty entries are over 5% of the total entries in the table, it's also the
# filter case. Otherwise, it is the missing entries case.
# Filter case: the empty entries should be the same value as the nearest
# non-empty entry above it. 
# Missing entries case: fill all the empty entries with 0.
def remove_empty_entries(table):
    col_num = table.shape[1]
    row_num = table.shape[0]
    examples = table[col_num-1].dropna()
    num = len(examples)

    total_entries = prod(table.shape)
    num_zeros = 0

    new = table.copy()
    
    zeroes = True
    empty = False
    for j in range(num):
        for i in range(col_num):
            if (pd.isna(table[i][j])):
                num_zeros += 1
                zeroes = False
                empty = True
                n = table.iloc[j-1, i]
                new.iloc[j, i] = n

    
    for j in range(num, row_num):
        for i in range(col_num-1):
            if (pd.isna(table[i][j])):
                empty = True
                num_zeros += 1
                if not zeroes:
                    # filter case
                    n = new.iloc[j-1, i]
                    new.iloc[j, i] = n
    
    if not zeroes:
        return empty, zeroes, new
    
    perc = num_zeros / total_entries

    if perc == 0:
        return empty, zeroes, new 

    # missing entries case
    if (perc < 0.05):
        for j in range(row_num):
            for i in range(col_num-1):
                if (pd.isna(table[i][j])):
                        new[i][j] = 0
        return empty, zeroes, new
    
    # filter case
    zeroes = False
    for j in range(num, row_num):
        for i in range(col_num-1):
            if (pd.isna(table[i][j])):
                n = new.iloc[j-1, i]
                new.iloc[j, i] = n
    
    return empty, zeroes, new
