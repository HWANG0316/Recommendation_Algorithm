import os
import random
import pandas as pd
import datetime
from openpyxl import load_workbook
import numpy as np

def get_keywordMatrix():
    return keyword_matrix

def isNan(num):
    return num == num

keyword_matrix = [[] for i in range(23)]
df = pd.read_excel('keyword_matrix.xlsx')

for i in range(len(keyword_matrix)):
    keyword_matrix[i].append("G" + str(i+1))

for i in range(len(df.values)):

    temp = list(df.values[i])

    for j in range(1, len(temp)):
        if isNan(temp[j]):
            keyword_matrix[i].append(temp[j])

#for i in range(len(keyword_matrix)):
    #print(keyword_matrix[i])