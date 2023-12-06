### This python file is able to take the scv file to process as an argument
### and auto fill the file. It will also display a few examples of the final 
### output to make sure the results are the same as the user's expectation. 

import argparse
import pandas as pd
import numpy as np

from formatting import string_format, string_format_fill
from local_main import *
from domain_knowledge import domain_knowledge_formula, fill_domain_knowledge

def load_csv(file_path):
    df = pd.read_csv(file_path, header = None)
    return df


# Function to update a CSV file with new data
def update_csv(file_path, df):
    df.to_csv(file_path, index=False)


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

    # header
    header = False
    header_names = None
    if data.iloc[0,0] in ["weight", "height", "age_sv"]:
        header = True
        header_names = data.iloc[0,:]
        data = data.iloc[1:, :]
        data = data.reset_index(drop=True)
    

    num = True
    formula = False
    op = ""
    method = None

    # check if all the entries are numeric
    if not pd.api.types.is_numeric_dtype(data.iloc[0]):
        num = False

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
    
    if num:
        formula, data = autofill(data)
        op = 'numeric'
        method = 'numeric'


    # Mixed column types: filter column is string, other column is numeric
    if not formula:
        col, op = filter_sum_avg(data)
        if op != "":
            data = fill_filter_sum_avg(data, col, op)
            method = 'mixed'


    # the numeric formula doesn't apply to the table
    if op == "":
        # Convert all the numeric values into string
        data = data.astype(str)

        method, cand = string_format(data)
        # if method == None:
        #     print("It is too hard to infer potential relationship from the given columns.")
        #     return 0 
        # else:
        if method in ['extract', 'concat', 'refactoring', 'complex']:
            data = string_format_fill(data, method=method)


    # Domain knowledge
    if method == None:
        # print("domain")
        f, key, v = domain_knowledge_formula(data)
        if f:
            data = fill_domain_knowledge(data, key, v)
        else:
            print("It is too hard to infer potential relationship from the given columns.")
            return 0


    if header:
        data = pd.DataFrame([header_names]).append(data)
        data = data.reset_index(drop=True)

    data = check(data, file_root+"_expected.csv", header)

    data.to_csv(output_path, index=False, header = False)
    print("Done! The output is stored in", output_path)
    return 0

main()