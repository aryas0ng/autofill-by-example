### This is a file that contains functions that help identify if there is
### a formatting pattern.
from string import punctuation
import pandas as pd 
import math

def string_format(example, fill_col=1, cand=0):
    example = pd.DataFrame(example)
    # user input examples
    valid = []
    for i in range(len(example[fill_col])):
        if example[fill_col][i] != 'NaN' or example[fill_col][i] != "nan" or example[fill_col][i] != "0":
            valid.append(example[fill_col][i])
    # number of user input examples
    number = len(valid)
    start1 = str(example[0][0]).strip()
    start2 = str(valid[0]).strip()
    try:
        start2 = str(int(float(start2)))
    except:
        pass
    # print(start1, start2)
    cands = ['extract', 'concat', 'refactoring', 'complex']
    pos = start1.find(start2)
    # if start2 is in start1 --> extracting task
    if pos != -1:
        check = True
        context = [None, None]
        if pos == 0:
            context[0] = "B"
        if pos+len(start2) == len(start1):
            context[1] = "E"
        if context[0] == None:
            context[0] = start1[pos-1]
        if context[1] == None:
            context[1] = start1[pos+len(start2)]
        for i in range(1,len(valid)):
            try:
                valid[i] = str(int(float(valid[i])))
            except:
                pass
            if valid[i] == "nan":
                break
            if context[0] == "B" and context[1] == "E":
                if str(valid[i]) != str(example[0][i]):
                    check = False 
                    break
            elif context[0] == "B":
                rightidx = example[0][i].find(context[1])
                if str(valid[i]) != str(example[0][i][:rightidx]):
                    check = False
                    break
            elif context[1] == "E":
                leftidx = example[0][i].rfind(context[0])
                if str(valid[i]) != str(example[0][i][leftidx+1:]):
                    print(str(valid[i]),str(example[0][i][leftidx+1:]) )
                    check = False 
                    break
            else:
                leftidx = example[0][i].find(context[0])
                rightidx = example[0][i].rfind(context[1])
                if valid[i] != example[0][i][leftidx+1:rightidx]:
                    check = False
                    break
        if check:
            return "extract", context
    # if start1 is in start2 --> concatenating task
    pos = start2.find(start1)
    if pos != -1:
        check = True
        tagging = ""
        if pos == 0:
            leftidx = len(start1)
            tagging = start2[leftidx:]
        else:
            tagging = start2[:pos]
        for i in range(1, len(valid)):
            if pos == 0:
                if valid[i] != example[0][i] and valid[i] != example[0][i] + tagging:
                    check = False
                    break
            else:
                if valid[i] != example[0][i] and valid[i] != tagging + example[0][i]:
                    check = False
                    break
        tagpos = 0
        if pos != 0:
            tagpos = 1
        if check:
            return "concat", (tagging, tagpos)
        
    check = True
    start2seg = []
    pointer = 0
    flag = False #if num
    if start2[0] not in punctuation:
        start2seg.append("")
    for i in range(len(start2)):
        if start2[i] not in punctuation and flag:
            flag = False
            start2seg.append(start2[pointer:i])
        elif start2[i] in punctuation and not flag:
            flag = True
            pointer = i
    if start2[-1] not in punctuation:
        start2seg.append("")
    for i in range(1, len(valid)):
        
        pointer = 0 
        flag = False # if punc
        localseg = []
        local = ""
        for j in range(len(example[0][i])):
            if example[0][i][j] in punctuation and not flag:
                flag = True
                localseg.append(example[0][i][pointer:j])
            elif example[0][i][j] not in punctuation and flag:
                pointer = j 
                flag = False
        if example[0][i][-1] not in punctuation:
            localseg.append(example[0][i][pointer:])
        localseg.append("")
        print(start2seg, localseg)
        for k in range(len(start2seg)):
            local += start2seg[k]
            local += localseg[k]
        if local != valid[i]:
            check = False
            break
    if check:
        return "refactor", start2seg
    
    return None, None

def string_format_fill(example, fill_col=1, method="", extra=None):
    example = pd.DataFrame(example)
    # user input examples
    valid = []
    for i in range(len(example[fill_col])):
        if example[fill_col][i] != 'NaN' or example[fill_col][i] != "nan" or example[fill_col][i] != "0":
            valid.append(example[fill_col][i])
    if method == "extract":
        context = extra
        for i in range(len(example[0])):
            if context[0] == "B" and context[1] == "E":
                example[1][i] = str(example[0][i])
            elif context[0] == "B":
                rightidx = example[0][i].find(context[1])
                example[1][i] = str(example[0][i][:rightidx])
            elif context[1] == "E":
                leftidx = example[0][i].rfind(context[0])
                example[1][i] = str(example[0][i][leftidx+1:])
            else:
                leftidx = example[0][i].find(context[0])
                rightidx = example[0][i].rfind(context[1])
                example[1][i] = example[0][i][leftidx+1:rightidx]

    elif method == "concat":
        tagging, tagpos = extra
        for i in range(len(example[0])):
            if tagging in example[0][i]:
                example[1][i] = example[0][i]
            elif tagpos == 0:
                example[1][i] = example[0][i]+tagging
            elif tagpos == 1:
                example[1][i] = tagging+example[0][i]

    elif method == "refactor":
        punclist = extra
        for i in range(len(example[0])):
            pointer = 0 
            flag = False # if punc
            localseg = []
            local = ""
            for j in range(len(example[0][i])):
                if example[0][i][j] in punctuation and not flag:
                    flag = True
                    localseg.append(example[0][i][pointer:j])
                elif example[0][i][j] not in punctuation and flag:
                    pointer = j 
                    flag = False
            if example[0][i][-1] not in punctuation:
                localseg.append(example[0][i][pointer:])
            localseg.append("")
            for k in range(len(punclist)):
                local += punclist[k]
                local += localseg[k]
            example[1][i] = local

    return example