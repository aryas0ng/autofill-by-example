### This is a file that contains functions that help identify the numeric
### relationship across three columns. The value of the third column is dependent 
### on the other two columns. 
import pandas as pd 
import math
def ez_rel(example, fill_col=2, cand=0):
    valid = example[fill_col].dropna()
    number = len(valid)
    cands = ['+', '-1', '-2','*','/1','/2','max','min','avg']
    for i in range(len(cands)):
        cand = i
        pos = True
        for j in range(number):
            if cands[cand]=="+" and (not math.isclose(example[0][j]+example[1][j], example[2][j], abs_tol=0.001)):
                pos = False
            elif cands[cand]=="-1" and (not math.isclose(example[0][j]-example[1][j], example[2][j], abs_tol=0.001)):
                pos = False
            elif cands[cand]=="-2" and (not math.isclose(example[1][j]-example[0][j], example[2][j], abs_tol=0.001)):
                pos = False
            elif cands[cand]=="*" and (not math.isclose(example[0][j]*example[1][j], example[2][j], abs_tol=0.001)):
                pos = False
            elif cands[cand]=="/1":
                try:
                    temp = example[0][j]/example[1][j]
                    if math.isinf(temp):
                        temp = 0
                except ZeroDivisionError:
                    temp = 0
                if not math.isclose(temp, example[2][j]):
                    pos = False 
            elif cands[cand]=="/2":
                try:
                    temp = example[1][j]/example[0][j]
                    if math.isinf(temp):
                        temp = 0
                except ZeroDivisionError:
                    temp = 0
                if not math.isclose(temp, example[2][j]):
                    pos = False 
            elif cands[cand]=="max" and (not math.isclose(max(example[0][j], example[1][j]), example[2][j], abs_tol=0.001)):
                pos = False 
            elif cands[cand]=="min" and (not math.isclose(min(example[0][j], example[1][j]), example[2][j], abs_tol=0.001)):
                pos = False
            elif cands[cand]=="avg" and (not math.isclose((example[0][j]+example[1][j])/2, example[2][j], abs_tol=0.001)):
                pos = False        
            if not pos:
                break
        if pos:
            return cands[cand], cand
    return None, -1

def ez_rel_fill(example, fill_col=2, method="+"):
    valid = example[fill_col].dropna()
    number = len(valid)
    if method == "+":
        for i in range(number, len(example[0])):
            example[fill_col][i] = example[0][i]+example[1][i]
    elif method == "*":
        for i in range(number, len(example[0])):
            example[fill_col][i] = example[0][i]*example[1][i]
    elif method == "/1":
        for i in range(number, len(example[0])):
            try:
                temp = example[0][i]/example[1][i]
                if math.isinf(temp):
                        temp = 0
            except ZeroDivisionError:
                temp = 0
            example[fill_col][i] = temp
    elif method == "/2":
        for i in range(number, len(example[0])):
            try:
                temp = example[1][i]/example[0][i]
                if math.isinf(temp):
                        temp = 0
            except ZeroDivisionError:
                temp = 0
            example[fill_col][i] = temp
    elif method == "-1":
        for i in range(number, len(example[0])):
            example[fill_col][i] =  example[0][i]-example[1][i]
    elif method == "-2":
        for i in range(number, len(example[0])):
            example[fill_col][i] = example[1][i]-example[0][i]
    elif method == "max":
        for i in range(number, len(example[0])):
            example[fill_col][i] = max(example[1][i], example[0][i])
    elif method == "min":
        for i in range(number, len(example[0])):
            example[fill_col][i] = min(example[0][i], example[1][i])
    elif method == "avg":
        for i in range(number, len(example[0])):
            example[fill_col][i] = (example[0][i]+example[1][i])/2.0
    return example