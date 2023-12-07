from itertools import permutations, product
import pandas as pd

from .bmi import bmi, fill_bmi
from .bmr import bmr, fill_bmr
from .bai import bai, fill_bai
from .irr import irr, fill_irr

def wh_perm(num):
    cols = list(permutations(range(0, num)))
    
    wh_units = [["kg", "lb"], ["cm", "in"]]
    units = list(product(*wh_units))

    combined = []
    for i in cols:
        for j in units:
            temp = i + j 
            combined.append(temp)
    return [list(t) for t in combined]

def hh_perm(num):
    cols = list(permutations(range(0, num)))

    h_units = [["cm", "in"], ["cm", "in"]]
    units = list(product(*h_units))

    combined = []
    for i in cols:
        for j in units: 
            temp = i + j
            combined.append(temp)
    return [list(t) for t in combined]


def domain_knowledge_formula(table):
    row_num, col_num = table.shape
    
    examples = table[col_num-1].dropna()
    num = len(examples)

    if (pd.api.types.is_numeric_dtype(table.iloc[0][0])):
        examples = table[:][:num]
    else:
        examples = table[:][1:num]

    domain_knowledge = {}

    domain_knowledge[irr] = []

    bmi_combined = wh_perm(2)
    domain_knowledge[bmi] = bmi_combined

    bmr_combined = wh_perm(4)
    domain_knowledge[bmr] = bmr_combined

    bai_combined = hh_perm(2)
    domain_knowledge[bai] = bai_combined
    # print(bai_combined)
    
    for key, value in domain_knowledge.items():
        if value == []:
            formula = key(examples)
            if formula:
                return formula, key, []
        for v in value:
            # print(v)
            formula = key(examples, *v)
            if formula:
                return formula, key, v
    
    return False, None, None


def fill_domain_knowledge(table, key, v):
    filled = None

    if key == irr:
        filled = fill_irr(table)
    elif key == bmi:
        filled = fill_bmi(table, *v)
    elif key == bmr:
        filled = fill_bmr(table, *v)
    elif key == bai:
        filled = fill_bai(table, *v)
    return filled

