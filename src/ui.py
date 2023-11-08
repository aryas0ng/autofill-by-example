### This python file is able to take the scv file to process as an argument
### and auto fill the file. It will also display a few examples of the final 
### output to make sure the results are the same as the user's expectation. 

import argparse
import pandas as pd
# from ez_numeric_2cols import ez_rel, ez_rel_fill
from formatting import string_format, string_format_fill
from main import autofill,check

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
    method, cand = None, -1
    # method, cand = ez_rel(data)
    if cand == -1:
        method, cand = string_format(data)
    if method == None:
        print("It is too hard to infer potential relationship from the given columns.")
        return 0 
    else:
        # if method in ['+', '-1', '-2','*','/1','/2','max','min','avg']:
        #     example = ez_rel_fill(example, method=method)
        if method in ['extract', 'concat', 'refactoring', 'complex']:
            example = string_format_fill(data, method=method)
        else:
            example = autofill(data)
    
    check(example, file_root+"_expected.scv")
    example.to_csv(output_path, index=False)
    print("Done! The out put is stored in", output_path)
    return 0

main()