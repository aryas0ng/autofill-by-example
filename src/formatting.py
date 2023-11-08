### This is a file that contains functions that help identify if there is
### a formatting pattern
from string import punctuation
import pandas as pd 
import math
def string_format(example, fill_col=1, cand=0):
    example = pd.DataFrame(example)
    # print(fill_col, example.shape)
    print(example)
    print(example.iloc[:,fill_col])
    # print(type(example))
    valid = example.iloc[:,fill_col].dropna()
    number = len(valid)
    start1 = str(example[0][0]).strip()
    start2 = str(valid[0]).strip()
    cands = ['extract', 'concat', 'refactoring', 'complex']
    pos = start1.find(start2)
    cand = 0 
    okay = True
    if pos != -1:
        context= [None, None]
        if pos==0:
            context[0]='start'
        else:
            context[0]=start1[pos-1]
        if pos+len(start2)==len(start1):
            context[1]='end'
        else:
            context[1]=start1[pos+len(start2)]  
        for i in range(1,number):
            start1 = example[0][i]
            start2 = valid[i]
            if context[0] == 'start':
                temp = start1[0:start1.find(context[1])]
                if temp != start2:
                    okay = False
                    break
            elif context[1] == 'end':
                temp = start1[start1.rfind(context[0])+1:]
                if temp != start2:
                    okay = False
                    break
            else:
                left = start1.find(context[0])
                right = start1.rfind(context[1])
                
                temp = start1[left+1:right]
                while temp != start2 and left < right:
                    right = start1.rfind(context[1], 0, right)
                    temp = start1[left+1:right]
                if temp == start2:
                    break
                right = start1.rfind(context[1])
                temp = start1[left+1:right]
                while temp != start2 and left < right:
                    left = start1.find(context[0], left+1)
                    temp = start1[left+1:right]
                if temp == start2:
                    break
                okay = False
                break
        if okay:
            return cands[cand], cand
    cand = 1 
    okay = True
    pos = start2.find(start1)
    if pos != -1:
        before = start2[:pos]
        after = start2[pos+len(start1):]
        for i in range(1, number):
            start1 = example[0][i]
            start2 = valid[i]
            if before+start1+after != start2 and start1 != start2:
                okay = False 
                break 
        if okay:
            return cands[cand], cand  
    cand = 2
    okay = True 
    origin = start1.lower()
    origin_lst = []
    goal = start2.lower()
    goal_lst = []
    ifpunc = False
    if goal[0] not in punctuation:
        goal_lst.append("")
        ifpunc = False
    else:
        goal_lst.append(goal[0])
        ifpunc = True
    for i in range(1,len(goal)):
        if goal[i] in punctuation and ifpunc:
            goal_lst[-1] += goal[i]
        elif goal[i] in punctuation and not ifpunc:
            goal_lst.append(goal[i])
            ifpunc = True
        elif goal[i] not in punctuation and ifpunc:
            ifpunc = False
    if not ifpunc: goal_lst.append("")
    
    for i in range(number):
        origin_lst = []
        origin = example[0][i]
        ifchar = False
        for char in origin:
            if char in punctuation and ifchar:
                ifchar = False
            elif char not in punctuation and not ifchar:
                origin_lst.append(char)
                ifchar = True
            elif char not in punctuation and ifchar:
                origin_lst[-1] += char
        print(goal_lst, origin_lst)
        assert(len(origin_lst)+1 == len(goal_lst))
        fused = ""
        for j in range(len(goal_lst)-1):
            fused += goal_lst[j]
            fused += origin_lst[j]
            
        fused += goal_lst[-1]
        print(valid[i], fused)
        if fused != valid[i]:
            okay = False
            break 
    if okay:
        return cands[cand], cand
        
    return None,-1


def string_format_fill(example, fill_col=1, method=""):
    valid = example[fill_col].dropna()
    number = len(valid)
    if method == 'extract':
      start1 = str(example[0][0]).strip()
      start2 = str(valid[0]).strip()
      pos = start1.find(start2)
      context= [None, None]
      if pos==0:
          context[0]='start'
      else:
          context[0]=start1[pos-1]
      if pos+len(start2)==len(start1):
          context[1]='end'
      else:
          context[1]=start1[pos+len(start2)]  
  
      if context[0] == 'start':
          for j in range(number, len(example[0])):
              example[fill_col][j] = example[0][j][0:start1.find(context[1])]
          
      elif context[1] == 'end':
          for j in range(number, len(example[0])):
              example[fill_col][j] = example[0][j][start1.rfind(context[0])+1:]

      else:
          for j in range(number, len(example[0])):
              left = start1.find(context[0])
              right = start1.rfind(context[1])
              example[fill_col][j] = example[0][j][left+1:right]
            
    elif method == 'concat':
        start1 = str(example[0][0]).strip()
        start2 = str(valid[0]).strip()
        pos = start2.find(start1)
        before = start2[:pos]
        after = start2[pos+len(start1):]
        for j in range(number, len(example[0])):
            example[fill_col][j] = before + example[0][j] + after
    
    elif method == "refactoring":
        start1 = str(example[0][0]).strip()
        start2 = str(valid[0]).strip()
        ifpunc = False
        goal = start2.lower()
        goal_lst = [] 
        if goal[0] not in punctuation:
            goal_lst.append("")
            ifpunc = False
        else:
            goal_lst.append(goal[0])

        ifpunc = True
        
        for i in range(1,len(goal)):
          if goal[i] in punctuation and ifpunc:
              goal_lst[-1] += goal[i]
          elif goal[i] in punctuation and not ifpunc:
              goal_lst.append(goal[i])
              ifpunc = True
          elif goal[i] not in punctuation and ifpunc:
              ifpunc = False
        if not ifpunc: goal_lst.append("")

        for j in range(number, len(example)):
            origin = example[0][j].lower()
            origin_lst = []
            ifchar = False
            for char in origin:
                if char in punctuation and ifchar:
                    ifchar = False
                elif char not in punctuation and not ifchar:
                    origin_lst.append(char)
                    ifchar = True
                elif char not in punctuation and ifchar:
                    origin_lst[-1] += char
            # print(goal_lst, origin_lst)
            # assert(len(origin_lst)+1 == len(goal_lst))
            fused = ""
            for i in range(len(goal_lst)-1):
                fused += goal_lst[i]
                fused += origin_lst[i]
            example[fill_col][j] = fused
    
    return example
