import pandas as pd

from multiple_rows import *
from weighted_col import *
from empty_entries import *
from tailing import * 
from ez_numeric_2cols import *


def load_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    return df


def cleaning(table):
    # remove ending empty cols
    table = tailing(table)

    # remove empty entries, especially for numeric table
    empty, zeroes, table = remove_empty_entries(table)

    return table


def autofill(table):
    # simple operations
    row_num, col_num = table.shape
    if col_num >= 3:
        method, cand = ez_rel(table)
        if method in ['+', '-1', '-2','*','/1','/2','max','min','avg']:
            table = ez_rel_fill(table, method=method)
            return True, table
    
    # multiple rows operation
    op, result = multiple_row_sum_avg(table)
    if result != -1:
        return True, fill_multiple_row_sum_avg(table, op, result)

    # filter operations
    col, op = filter_sum_avg(table)
    if op != "":
        return True, fill_filter_sum_avg(table, col, op)

    trial = filter_count(table)
    if trial:
        return True, fill_filter_count(table, trial)
    
    # weighted sum operation
    weight = weighted_sum(table)
    if weight != None:
        return True, fill_weighted_sum(table, weight)

    return False, table
    

def check(filled, expected):
    expected = load_csv(expected)
    pd.testing.assert_frame_equal(expected, filled, check_dtype = False, atol = 0.01)

    row_num, col_num = filled.shape
    new_filled = filled.copy()
    for r in range(1, row_num):
        # print(type(expected[col_num-1][r]))
        if isinstance(expected[col_num-1][r], int):
            # print("in")
            try:
                new_filled.iloc[r] = filled.iloc[r].astype(int)
            except ValueError:
                return filled
        elif isinstance(expected[col_num-1][r], np.int_):
            # print("in2")
            try:
                # for i in range(col_num):
                #     new_filled.iloc[r,i] = filled.iloc[r,i].astype(int)
                new_filled.iloc[r, :] = filled.iloc[r].apply(np.int64)
                # print(filled.iloc[r].apply(np.int64))
                # print(int(filled.iloc[r,i]))
                # print(new_filled.iloc[r, :])
            except ValueError:
                return filled
            new_filled = new_filled.astype(int)

    return new_filled

