import math 
import numpy_financial as npf
import numpy as np

def irr(table):
    row_num, col_num = table.shape
    
    table.replace('nan', np.nan, inplace=True)
    examples = table[col_num-1].dropna()
    num = len(examples)

    for i in range(num):
        try:
            present_values = []
            for j in range(col_num-1):
                present_values.append(table.iloc[i, j])
            
            irr = float(table.iloc[i, col_num-1])

            calculate = round(npf.irr(present_values), 3)

            if not math.isclose(calculate, irr , rel_tol = 0.01):
                return False
        except ValueError:
            return False

    return True


def fill_irr(table):
    row_num, col_num = table.shape
    
    filled = table.copy()

    for i in range(row_num):
        present_values = []
        for j in range(col_num-1):
            present_values.append(table.iloc[i, j])

        calculate = round(npf.irr(present_values), 3)

        filled.iloc[i, col_num-1] = calculate

    return filled
