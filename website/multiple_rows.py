import math

# Given the complete first col, the method tries to infer the contents of the
# second col. For each entry in the second col, it looks at at most 10 rows
# including and below the row the entry is at, and find the relationship
# (sum or average) between the entry in the second col and the entries
# including and below the row in the first col.
# Return _, -1 if the formula doesn't fit the table.
def multiple_row_sum_avg(table):
    examples = table[1].dropna()
    count = len(examples)
    result = -1
    op = "sum"
    for j in range(10): # number of rows to consider
        trial = True
        for i in range(count): # loop through examples
            sum = table[0][i]
            for k in range(j):
                sum += table[0][i+k+1]
            avg = sum / (j+1)
            if i == 0 and sum != float(table[1][i]):
                if (math.isclose(avg, table[1][i], rel_tol = 0.01)):
                    op = "avg"
            if op == "sum" and sum != float(table[1][i]):
                trial = False
                break
            if op == "avg" and not (math.isclose(avg, table[1][i], rel_tol = 0.01)):
                trial = False
                break
        if trial:
            result = j+1
            break
    return op, result


def fill_multiple_row_sum_avg(table, op, result):
    col_num = table.shape[1]
    row_num = table.shape[0]
    examples = table[col_num-1].dropna()
    num = len(examples)

    new = table.copy()

    if result == -1:
        raise Exception("not multiple_row_sum_avg formula") 
    
    for i in range(num, row_num):
        sum = table[0][i]
        for j in range(i+1, min(row_num, i+result)):
            sum += table[0][j]
        if op == "sum":
            new.iloc[i, col_num-1] = sum
        elif op == "avg":
            new.iloc[i, col_num-1] = sum / (min(result, row_num-i))
    return new


# The input table contains two complete cols, one is the col to filter, i.e if
# a few  consecutive rows has the same value in the col, we perform certain 
# operation (sum or average) on the entries on the other col.
# Return "" for op, if the formula doesn't apply to the table
def filter_sum_avg(table):
    col_num = table.shape[1]
    if (col_num < 3):
        return 0, ""

    col = 0
    result, op = filter_sum_avg_helper(table, 0)

    if not result:
        result, op = filter_sum_avg_helper(table, 1)
        col = 1
    return col, op


# This is a helper method for filter_sum_avg
# It suppose the col is the filter col, and the remaining col contains entries
# that we do operations on.
def filter_sum_avg_helper(table, col):
    examples = table[2].dropna()
    num = len(examples)
    i = 0
    filter = table[col][0]
    sum = 0
    count = 0
    trial = True
    val = (int) (not col)
    op = "sum"
    while (i < num):
        f = table[col][i]
        elt = float(table[val][i])
        if (f == filter):
            sum += elt 
            count += 1
        else:
            avg = sum / count
            if (filter == table[col][0]):
                if (math.isclose(avg, float(table[2][0]), rel_tol = 0.01)):
                    op = "avg"
            for j in range(count):
                prev = float(table[2][i-j-1])
                if op == "avg" and not (math.isclose(avg, prev, rel_tol = 0.01)):
                    trial = False
                    break
                if op == "sum" and (prev != sum):
                    trial = False
                    break
            filter = f
            count = 1
            sum = elt
        
        if not trial:
            break
        i +=1 

    while (filter == table[col][i]):
        sum += float(table[val][i])
        count += 1
        i += 1

    last = table[2][num-1]
    if op == "sum" and (last != sum):
        trial = False
    
    if op == "avg" and not (math.isclose(sum / count, last, rel_tol = 0.01)):
        trial = False

    if op == "avg" and not trial: 
        op = "sum"
        trial = True
        while (i < num):
            f = table[col][i]
            elt = table[val][i]
            if (f == filter):
                sum += elt 
                count += 1
            else:
                avg = sum / count
                for j in range(count):
                    prev = table[2][i-j-1]
                    if op == "sum" and (prev != sum):
                        trial = False
                        break
                filter = f
                count = 1
                sum = elt
            
            if not trial:
                break
            i +=1 

    if trial:
        return True, op
    else:
        return False, ""


def fill_filter_sum_avg(table, col, op):
    if op == "":
        raise Exception("not filter_sum_avg formula")
    
    col_num = table.shape[1]
    row_num = table.shape[0]
    examples = table[col_num-1].dropna()
    num = len(examples)

    new = table.copy()

    val = (int) (not col)
    cur = table[col][0]
    count = 0
    sum = 0
    for i in range(row_num):
        f = table[col][i]
        if (f == cur):
            sum += table[val][i]
            count += 1
        else:
            for j in range(count):
                if op == "sum":
                    new.iloc[i-j-1, 2] = sum
                elif op == "avg":
                    new.iloc[i-j-1, 2] = sum / count
            sum = table[val][i]
            count = 1
            cur = f
    for j in range(count):
        if op == "sum":
            new.iloc[row_num-j-1, 2] = sum
        elif op == "avg":
            new.iloc[row_num-j-1, 2] = sum / count
    
    return new


# The input table contains one single complete col. The second col counts how
# many consecutive rows has the same value in the first col, and put the count
# in the second col
# Return False if the formula doesn't apply to the table
def filter_count(table):
    examples = table[1].dropna()
    num = len(examples)
    filter = table[0][0]
    count = 0
    trial = True
    for i in range(num):
        f = table[0][i]
        if (f == filter):
            count += 1
        else:
            for j in range(count):
                elt = table[1][i-j-1]
                if (elt != count):
                    trial = False
                    break
            filter = f
            count = 1
    return trial


def fill_filter_count(table, trial):
    if not trial:
        raise Exception("Not filter_count formula")
    
    row_num = table.shape[0]
    new = table.copy()

    cur = table[0][0]
    count = 0
    for i in range(row_num):
        f = table[0][i]
        if (f == cur):
            count += 1
        else:
            for j in range(count):
                new.iloc[i-j-1, 1] = count
            cur = f
            count = 1

    for j in range(count):
        new.iloc[row_num-j-1, 1] = count

    return new
