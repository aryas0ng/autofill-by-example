### This is a file that contains functions that help identify the numeric
### relationship across three columns. The value of the third column is dependent 
### on the other two columns. 
import pandas as pd 
import math

def add_helper(row):
    length = row.shape[0]
    sum = 0
    for i in range(length-1):
        sum += row[i]
    
    if math.isclose(sum, row[length-1], abs_tol=0.001):
        return True
    
    return False


def multi_helper(row):
    length = row.shape[0]
    product = 1
    for i in range(length-1):
        product *= row[i]
    
    if math.isclose(product, row[length-1], abs_tol=0.001):
        return True
    
    return False


def ez_rel(example, cand=0):
    fill_col = example.shape[1] - 1

    valid = example[fill_col].dropna()
    number = len(valid)

    if fill_col == 2:
        cands = ['+', '-1', '-2', '*', '/1', '/2', 'max', 'min', 'avg']
    else:
        cands = ['+', '*', 'max', 'min', 'avg']
    
    for i in range(len(cands)):
        cand = i
        pos = True
        for j in range(number):
            if cands[cand] == "+" and (not add_helper(example.iloc[j])):
                pos = False

            elif cands[cand] == "*" and (not multi_helper(example.iloc[j])):
                pos = False

            elif cands[cand] == "max" and (not math.isclose(example.iloc[j].max(), example[fill_col][j], abs_tol=0.001)):
                pos = False 

            elif cands[cand] == "min" and (not math.isclose(example.iloc[j].min(), example[fill_col][j], abs_tol=0.001)):
                pos = False

            elif cands[cand] == "avg" and (not math.isclose(example.iloc[j].mean(), example[fill_col][j], abs_tol=0.001)):
                pos = False  

            elif cands[cand] == "-1" and (not math.isclose(example[0][j]-example[1][j], example[2][j], abs_tol=0.001)):
                pos = False

            elif cands[cand] == "-2" and (not math.isclose(example[1][j]-example[0][j], example[2][j], abs_tol=0.001)):
                pos = False
            
            elif cands[cand] == "/1":
                if example[1][j] == 0:
                    temp = 0
                else:
                    temp = example[0][j] / example[1][j]
                    if math.isinf(temp):
                        temp = 0
                if not math.isclose(temp, example[2][j]):
                    pos = False 

            elif cands[cand]=="/2":
                if example[0][j] == 0:
                    temp = 0
                else:
                    temp = example[1][j] / example[0][j]
                    if math.isinf(temp):
                        temp = 0
                if not math.isclose(temp, example[2][j]):
                    pos = False 

            if not pos:
                break
        
        if pos:
            return cands[cand]

    return None


def ez_rel_fill(example, method):
    fill_col = example.shape[1] - 1
    valid = example[fill_col].dropna()
    number = len(valid)

    filled = example.copy()

    if method == "+":
        for i in range(number, len(example[0])):
             sum = example.iloc[i, :fill_col].sum()
             filled.iloc[i, fill_col] = sum

    elif method == "*":
        for i in range(number, len(example[0])):
            prod = example.iloc[i, :fill_col].prod()
            filled.iloc[i, fill_col] = prod

    elif method == "max":
        for i in range(number, len(example[0])):
            max = example.iloc[i, :fill_col].max()
            filled.iloc[i, fill_col] = max

    elif method == "min":
        for i in range(number, len(example[0])):
            min = example.iloc[i, :fill_col].min()
            filled.iloc[i, fill_col] = min
            
    elif method == "avg":
        for i in range(number, len(example[0])):
            mean = example.iloc[i, :fill_col].mean()
            filled.iloc[i, fill_col] = mean

    elif method == "-1":
        for i in range(number, len(example[0])):
            filled.iloc[i, fill_col] =  example[0][i] - example[1][i]

    elif method == "-2":
        for i in range(number, len(example[0])):
            filled.iloc[i,fill_col] = example[1][i] - example[0][i]

    elif method == "/1":
        for i in range(number, len(example[0])):
            if example[1][i] == 0:
                temp = 0
            else:
                temp = example[0][i] / example[1][i]
                if math.isinf(temp):
                        temp = 0
            filled.iloc[i, fill_col] = temp

    elif method == "/2":
        for i in range(number, len(example[0])):
            if example[0][i] == 0:
                temp = 0
            else: 
                temp = example[1][i] / example[0][i]
                if math.isinf(temp):
                        temp = 0
            filled.iloc[i, fill_col] = temp

    return filled

