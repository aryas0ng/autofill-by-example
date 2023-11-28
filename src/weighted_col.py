from sympy import symbols, Eq, solve

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