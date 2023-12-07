import pandas as pd
import numpy as np 

def sep(example,col_fill=2):
  example = pd.DataFrame(example)
  examplenum = pd.DataFrame(example)
  exampleunit = pd.DataFrame(example)
  for i in range(len(example[0])):
    for j in range(0, col_fill):
      pointer = 0
      for k in range(len(example[j][i])):
        print(example[j][i][k])
        if example[j][i][k].isalpha():
          pointer = k
      examplenum[j][i] = float(example[j][i][:pointer])
      exampleunit[j][i] = example[j][i][pointer:]
  return examplenum, exampleunit

def blocking(example, col_fill=2):
  block = {}
  for i in range(len(example[0])):
    for j in range(0, col_fill):
      if example[j][i] not in block:
        block[example[j][i]] = [i]
      else:
        if i not in block[example[j][i]]:
          block[example[j][i]].append(i)
  return block

def jaccard(set1,set2):
  inter = len(set1.intersection(set2))
  union = len(set1.union(set2))
  return inter/union

def all_pairs(block, exampleunit):
  cands = {}
  for key,value in block.items():
    for i in range(len(value)-1):
      set1 = set([exampleunit[0][value[i]], exampleunit[1][value[i]]])
      for j in range(i+1,len(value)):
        set2 = set([exampleunit[0][value[j]], exampleunit[1][value[j]]])
        if (value[i], value[j]) not in cands and (value[j], value[i]) not in cands:
          cands[value[i], value[j]] = jaccard(set1,set2)

  return cands

def afilter(cands, alpha=0.1):
  final = {}
  for key, value in cands.items():
    if value > alpha:
      final[key] = value
  return final

def clustering(cands, lenlst):
  for key, value in cands.items():
    start = 0 
    clusters = [[start]]
    seen = [start]
    for key, value in cands.items():
      a,b =key
      if a == start:
        clusters[0].append(b)
        if b not in seen:
          seen.append(b)
      elif b == start:
        clusters[0].append(a)
        if a not in seen:
          seen.append(a)
  for i in range(lenlst):
    accepted = False
    if i not in seen:
      seen.append(i)
      for clus in clusters:
        vote = 0 
        base = len(clus)
        for c in clus:
          if (c,i) in cands.keys() or (i,c) in cands.keys():
            clus.append(i)
            accepted = True
      if not accepted:
        clusters.append([i])
  return clusters

def sepncluster(example,col_fill=2):
  examplenum, exampleunit = sep(example,col_fill=2)
  block = blocking(exampleunit)
  pairs = all_pairs(block, exampleunit)
  pairs = afilter(pairs)
  clusters = clustering(pairs,len(example[0]))
  return examplenum, exampleunit, clusters