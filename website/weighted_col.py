from sympy import symbols, Eq, solve
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def load_csv(file_path):
    df = pd.read_csv(file_path, header = None)
    return df

# Function to update a CSV file with new data
def update_csv(file_path, df):
    df.to_csv(file_path, index=False)

# This method tries to find a formula that fit in the table. 
# The formula will be in the form of w1 * col1 + w2 * col2 + ... = lastcol,
# where w1, w2, ... are coefficients. 
# Return the list of coefficients, if the formula exists
# Return None, if the formula doesn't apply to the table
def weighted_sum(table):
    col_num = table.shape[1]
    examples = table[col_num-1].dropna()
    num = len(examples)
    sample = table[:][:num].values.tolist()
    
    return solver(sample)


def solver(rows):
    col_num = len(rows[0])
    col_num -= 1
    if col_num > len(rows):
        return None
    
    # Create variables
    var = {}
    acsii = 97
    for i in range(col_num):
        sym = chr(acsii+i)
        symStr = str(sym)
        var[symStr] = symbols(sym) 
    
    # Create equations
    equations = []
    for i in range(col_num):
        lhs = sum([coeff * var[v] for coeff, v in zip(rows[i][:-1], var)])
        result = rows[i][-1]
        eq = Eq(lhs, result) 
        equations.append(eq)

    sol = solve(equations)

    co = {str(v): sol[var[v]] for v in var}
    coef = [co[v] for v in var]
    
    # Verify coefficients in the remaining rows, if exists
    for i in range(len(rows) - col_num):
        result = rows[col_num+i][-1]
        nums = rows[col_num+i][:-1]
        temp = 0
        for j in range(len(coef)):
            temp += coef[j] * nums[j]
        if temp != result:
            return None

    return coef


# If the weight is None, the table doesn't satisfy the weighted sum formula
# Otherwise, for each row, apply the weight to the corresponding entries, and
# enter the result to the last column.
def fill_weighted_sum(table, weight):
    if weight == None:
        raise Exception("not weighted_sum formula")
    
    col_num = table.shape[1]
    row_num = table.shape[0]
    examples = table[col_num-1].dropna()

    new = table.copy()

    for i in range(row_num):
        result = 0
        for j in range(len(weight)):
            result += weight[j] * table[j][i]
        new.iloc[i,-1] = result

    return new


# Record and plot the execution time of datasets under the weighted sum formula
# with different number of columns 
def weighted_sum_plot():
    number_to_string = {
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine',
        10: 'ten'
    }

    times = []
    for i in range(2,11):
        n = number_to_string.get(i)
        file = "../tests/weighted_sum_of_" + n + "_cols.csv"
        dataset = load_csv(file)

        start_time = time.time()
        result = autofill(dataset)
        end_time = time.time()

        duration = (end_time - start_time) * 1000

        times.append(duration)

    plt.plot(list(range(2, 11)), times)

    plt.xlabel('Number of Columns')
    plt.ylabel('Execution Time (ms)')
    plt.title('Execution Time Plot')

    plt.show()
