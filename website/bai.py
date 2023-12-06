import math 
import numpy as np

def bai(example, c_col, h_col, c_unit, h_unit):
    row_num, col_num = example.shape

    if col_num != 3:
        return False
    
    example.replace('nan', np.nan, inplace=True)
    examples = example[col_num-1].dropna()
    num = len(examples)

    for i in range(num):
        try:
            hip_circ = float(example.iloc[i,c_col])
            height = float(example.iloc[i,h_col])
            bai = float(example.iloc[i, 2])

            if c_unit == "in":
                hip_circ *= 2.54

            if h_unit == "in":
                height = height * 2.54 / 100
            elif h_unit == "cm":
                height /= 100

        except ValueError:
            return False
        
        calculate = ((hip_circ / height) ** 1.5) - 18

        if not math.isclose(calculate, bai , rel_tol = 0.01):
            # print(hip_circ, height, bai, calculate)
            return False
        
    return True


def fill_bai(table,  c_col, h_col, c_unit, h_unit):
    row_num, col_num = table.shape

    if col_num != 3:
        return None
    
    filled = table.copy()

    for i in range(row_num):
        try:
            hip_circ = float(table.iloc[i,c_col])
            height = float(table.iloc[i,h_col])

            if c_unit == "in":
                hip_circ *= 2.54

            if h_unit == "in":
                height = height * 2.54 / 100
            elif h_unit == "cm":
                height /= 100
            
            calculate = ((hip_circ / height) ** 1.5) - 18
            filled.iloc[i, 2] = calculate

        except ValueError:
            return None
        
    return filled

