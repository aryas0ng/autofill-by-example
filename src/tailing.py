import pandas as pd

# Truncate the extra empty rows and cols in the table
def tailing(table):
    col_num = table.shape[1]
    row_num = table.shape[0]
    col = True
    while col and col_num > 0:
        for i in range(row_num):
            if not pd.isna(table[col_num-1][i]):
                col = False
                break
        if col: 
            col_num -= 1

    row = True
    while row and row_num > 0:
        for j in range(col_num):
            if not pd.isna(table[j][row_num-1]):
                row = False
                break
        if row:
            row_num -= 1
    return table.iloc[:row_num, :col_num]
