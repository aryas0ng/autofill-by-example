import math

def bmi(table, w, h, w_unit, h_unit):
    row_num, col_num = table.shape

    if col_num != 3:
        return False
    
    examples = table[col_num-1].dropna()
    num = len(examples)

    for i in range(num):
        height = float(table.iloc[i,h])
        weight = float(table.iloc[i,w])
        bmi = float(table.iloc[i,2])
        
        if w_unit == "lb":
            weight *= 0.453592

        if h_unit == "in":
            height = height * 2.54 / 100
        elif h_unit == 'cm':
            height /= 100
        
        if not math.isclose(weight / (height ** 2), bmi , rel_tol = 0.01):
            # print(height, weight)
            return False
        
    return True


def fill_bmi(table, w, h, w_unit, h_unit):
    row_num, col_num = table.shape

    if col_num != 3:
        return None
    
    filled = table.copy()

    for i in range(row_num):
       try:
        height = float(table.iloc[i,h])
        weight = float(table.iloc[i,w])

        if w_unit == "lb":
            weight *= 0.453592

        if h_unit == "in":
            height = height * 2.54 / 100
        elif h_unit == 'cm':
            height /= 100

        temp = weight / (height ** 2)
        filled.iloc[i, 2] = round(temp, 1)
       except ValueError:
         return None

    return filled
