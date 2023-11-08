# This method tries to find a formula that fit in the table. 
# The formula will be in the form of w1 * col1 + w2 * col2 = col3, where w1 and
# w2 will be integer. 
# Return False in the first return value, if the formula doesn't apply to the
# table
def weighted_sum(table):
    examples = table[2].dropna()
    count = len(examples)
    n1 = table[0][0]
    n2 = table[1][0]
    result0 = table[2][0]
    trial, w1, w2 = find_weight(n1, n2, result0, 0)  
    cont = True 
    
    while trial and cont:
        for i in range(1, count):
            result = table[2][i]
            i1 = table[0][i]
            i2 = table[1][i]
            if (w2 == -1):
                w = (result - i1 * w1) / i2
                if (w.is_integer()):
                    w2 = w
                else:
                    trial, w1, w2 = find_weight(n1, n2, result0, w1)
                    break
            if (i1 * w1 + i2 * w2 == result):
                if i == (count-1):
                    cont = False
                continue
            trial, w1, w2 = find_weight(n1, n2, result0, w1)
            break

    return trial, w1, w2


# This is a helper for the method weighted_sum.
# Given the two values (n1, n2) and their arithmetic result, we want to find a
# formula such that n1 * w1 + n2 * w2 = result, and w1 > w1_bound.
def find_weight(n1, n2, result, w1_bound):
    w1 = w1_bound + 1
    w2 = 1
    trial = False

    if (n1 == 0):
        w = result / n2
        if (not (w).is_integer()):
            return trial, w1, w2
        elif w1 <= 100:
            return True, w1, w
        else:
            return trial, w1, w2
        
    if (n2 == 0):
        w = result / n1
        if (not (w).is_integer()):
            return trial, w1, w2
        elif w <= w1_bound:
            return trial, w1, w2
        return True, w, -1
        
    while (w1 <= (result / n1)):
        if (not ((result - w1 * n1) / n2).is_integer()):
            w1 += 1
        else:
            w2 = (int) (result - w1 * n1) / n2
            trial = True
            break
    
    return trial, w1, w2


def fill_weighted_sum(table, trial, w1, w2):
    if not trial:
        raise Exception("not weight_sum formula")
    
    row_num = table.shape[0]
    examples = table[2].dropna()
    num = len(examples)

    new = table.copy()

    for i in range(num, row_num):
        weighted = w1 * table[0][i] + w2 * table[1][i]
        new.iloc[i, 2] = weighted

    return new

