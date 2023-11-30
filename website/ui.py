### This python file is able to take the scv file to process as an argument
### and auto fill the file. It will also display a few examples of the final 
### output to make sure the results are the same as the user's expectation. 

import argparse
import pandas as pd
import numpy as np
# from ez_numeric_2cols import ez_rel, ez_rel_fill
from formatting import string_format, string_format_fill
from local_main import *

def load_csv(file_path):
    df = pd.read_csv(file_path, header = None)
    return df

# Function to update a CSV file with new data
def update_csv(file_path, df):
    df.to_csv(file_path, index=False)

# Function to auto-complete a column based on given examples
# def auto_complete_column(input_data, examples):
#     for i, val in enumerate(input_data):
#         if pd.isna(val):
#             for example in examples:
#                 if val.lower() in example.lower():
#                     input_data[i] = example
#                     break
#     return input_data

def main():
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description='Auto-complete a CSV column based on examples.')
    
    # Add a positional argument for the CSV file
    parser.add_argument('csv_file', help='Path to the CSV file to process')
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Load data from the specified CSV file
    file_path = args.csv_file
    file_root = file_path[:file_path.find(".csv")]
    output_path = file_root + "_output.csv"
    
    data = load_csv(file_path)

    data = cleaning(data)
    # print(data)
    
    formula = False

    num = True
    # print(data.iloc[0])
    if not pd.api.types.is_numeric_dtype(data.iloc[0]):
    # if not pd.to_numeric(data.iloc[0]).all():
        num = False

    # print(num)
    if num:
        new_data = data
        for i in range(data.shape[0]):
            try:
                temp = pd.to_numeric(data.iloc[i])
                new_data.iloc[i] = temp
            except TypeError:
                num = False
                break
        if num:
            data = new_data
    
    # print(num)
    if num:
        # print("here")
        formula, data = autofill(data)
    # print(example)

    # Mixed column types: filter column is string, other column is numeric
    if not formula:
        # print("here")
        col, op = filter_sum_avg(data)
        # print(col, op)
        if op != "":
            data = fill_filter_sum_avg(data, col, op)

    # the numeric formula doesn't apply to the table
    if op == "":
        # Convert all the numeric values into string
        data = data.astype(str)

        # method, cand = ez_rel(data)
        # if cand == -1:
        method, cand = string_format(data)
        if method == None:
            print("It is too hard to infer potential relationship from the given columns.")
            return 0 
        else:
            # if method in ['+', '-1', '-2','*','/1','/2','max','min','avg']:
            #     example = ez_rel_fill(example, method=method)
            if method in ['extract', 'concat', 'refactoring', 'complex']:
                data = string_format_fill(data, method=method)
            # else:
            #     data = autofill(data)
    # print(example)
    data = check(data, file_root+"_expected.csv")
    # print(example)
    data.to_csv(output_path, index=False, header = False)
    print("Done! The output is stored in", output_path)
    return 0

main()