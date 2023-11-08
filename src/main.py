import pandas as pd

from multiple_rows import *
from weighted_col import *
from empty_entries import *
from tailing import * 

def load_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    return df


def autofill(file_path):
    table = load_csv(file_path)

    # remove ending empty cols
    table = tailing(table)

    # remove empty entries, especially for numeric table
    empty, zeroes, table = remove_empty_entries(table)

    # simple operations

    # multiple rows operation
    op, result = multiple_row_sum_avg(table)
    if result != -1:
        return fill_multiple_row_sum_avg(table, op, result)

    # print(table)
    # filter operations
    col, op = filter_sum_avg(table)
    if op != "":
        return fill_filter_sum_avg(table, col, op)

    trial = filter_count(table)
    if trial:
        return fill_filter_count(table, trial)
    
    # weighted sum operation
    trial, w1, w2 = weighted_sum(table)
    if trial:
        return fill_weighted_sum(table, trial, w1, w2)

    return table
    

def check(filled, expected):
    expected = load_csv(expected)
    # print(expected.compare(filled))
    pd.testing.assert_frame_equal(expected, filled, check_dtype = False, atol = 0.01)
