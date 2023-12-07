# import argparse
import pandas as pd
# import numpy as np
from .formatting import string_format, string_format_fill
from .local_main import *
from .domain_knowledge import domain_knowledge_formula, fill_domain_knowledge
from .cluster import sepncluster

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

def helper(file_path):

    file_root = file_path[:file_path.find(".csv")]
    output_path = file_root + "_output.csv"
    
    data = load_csv(file_path)

    data = cleaning(data)
    # print(data)
    
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
        print("here at string processing")
        # Convert all the numeric values into string
        data = data.astype(str)
        method, extra = string_format(data)
        # print(method, extra)
        # assert(False)        
        if method in ['extract', 'concat', 'refactoring']:
            data = string_format_fill(data, method=method, extra=extra)

    # if method == None:
    #     nums, units, clusters =sepncluster(data)
    #     print(clusters)
        
    # Domain knowledge
    if method == None:
        # print("domain")
        f, key, v = domain_knowledge_formula(data)
        if f:
            data = fill_domain_knowledge(data, key, v)
            method = "domain knowledge"
        else:
            print("It is too hard to infer potential relationship from the given columns.")
            return 0

    if header:
        data = pd.DataFrame([header_names]).append(data)
        data = data.reset_index(drop=True)
    # print(example)
    # example = check(example, file_root+"_expected.csv")
    # print(example)
    # example.to_csv(output_path, index=False, header = False)
    if method == None:
        return None
    return data