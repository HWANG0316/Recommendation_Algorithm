import os
import random
import pandas as pd
import numpy as np
from openpyxl import Workbook
import copy

URL = os.getcwd()  # Excel File Create
path = "./"
file_list = os.listdir(path)

GAME_NAME = []
result_list = [[] for i in range(50)]

GAME_NAME.append("  ")
for i in range(1, 24):
    GAME_NAME.append("G" + str(i))


for i in range(50):  # result list create
    for j in range(23):
        if random.random() > 0.5:
            success = "T"
        else:
            success = "F"

        none_rand = random.random()

        if none_rand > 0.9:
            result_list[i].append([round(random.random(), 3), "0", 0])
        elif none_rand > 0.8 :
            result_list[i].append([round(random.random(), 3), success, 0])
        else:
            result_list[i].append([round(random.random(), 3), success, int(1 + (random.random()) * 3)])

df = pd.DataFrame(result_list)  # List -> DataFrame
df.columns = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12", "G13", "G14", "G15", "G16",
              "G17", "G18", "G19", "G20", "G21", "G22", "G23"]
index_list = []

for i in range(1, 51):  # DataFrame Column Add
    index_list.append("U" + str(i))

df.index = index_list

df.to_excel('ResultMatrix.xlsx')  # Create Excel


def get_df():
    return df

def get_gamename():
    return GAME_NAME