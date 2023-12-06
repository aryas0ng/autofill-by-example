import pandas as pd

# Truncate the extra empty rows and cols in the table
def tailing(table):
    col_num = table.shape[1]
    row_num = table.shape[0]

    while col_num > 0:
        col = True
        for i in range(row_num):
            if not pd.isna(table[col_num-1][i]):
                col = False
                break
        if col: 
            table = table.drop(col_num-1, axis = 1)

        col_num -= 1

    col_num = table.shape[1]

    # Remove empty rows
    table = table.dropna(how='all')
    table = table.reset_index(drop=True)
    
    return table
