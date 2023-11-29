import math

def unit_conversion(table):
    row_num, col_num = table.shape
    if (col_num != 2):
        return False, 0

    examples = table[col_num-1].dropna()
    num = len(examples)

    formula = True
    left = table[0][0]
    right = table[1][0]
    unit = right / left
    
    for i in range(1, num):
        left = table[0][i]
        right = table[1][i]
        if not (math.isclose(unit, right / left, rel_tol = 0.01)):
            formula = False
            break

    return formula, unit


def fill_unit_conversion(table, unit):
    row_num, col_num = table.shape
    if (col_num != 2):
        return table
    
    filled = table.copy()
    for i in range(row_num):
        temp = table.iloc[i,0] * unit
        filled.iloc[i,1] = temp

    return filled

