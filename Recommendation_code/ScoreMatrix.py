import os
import random
import pandas as pd
import numpy as np
from openpyxl import Workbook
import copy

def get_scorematrix():
    return score_list

URL = os.getcwd()  # Excel File Create
path = "./"
file_list = os.listdir(path)

score_list = [[] for i in range(50)]

for i in range(50):  # result list create
    for j in range(23):
        name = "G" + str(j+1)
        score_list[i].append([round((random.uniform(-1,2)),3),name])

df = pd.DataFrame(score_list)  # List -> DataFrame

df.to_excel('ScoreMatrix.xlsx')  # Create Excel