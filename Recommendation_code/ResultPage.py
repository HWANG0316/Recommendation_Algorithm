# User 1 기준

import ResultMatrix
import random
import pandas as pd

resultMatrix = ResultMatrix.get_df()
df = pd.read_excel('ability_matrix.xlsx')

Abilitymatrix = []

stat_list = [[] for i in range(5)]

Successlist = [ [[] for i in range(23)] for i in range(50)]
User_ability = [ [0 for i in range(5)] for i in range(50)]

def printResultpage():
    stat_name = ["수리력", "기억력", "언어능력", "순발력", "공간지각력"]
    print("User[0] Stat (10점 만점)")

    for i in range(5):
        print("%s" % stat_name[i])
        for j in range(int(User_ability[0][i])):
            print("*", end="")
        for k in range(10-int(User_ability[0][i])):
            print("_",end="")

    min_index = User_ability[0].index(min(User_ability[0]))
    print("%s 보완을 위해 G%d게임을 해보세요 !" % (stat_name[min_index], stat_list[min_index][random.randint(0, 4)]))


for i in range(len(df.values)):             # Make Ability list
    Abilitymatrix.append(list(df.values[i][1:]))

for i in range(len(Abilitymatrix)):
    for j in range(len(Abilitymatrix[i])):
        if Abilitymatrix[i][j] == 1:
            stat_list[j].append(i + 1)


for i in range(len(Successlist)):
    for j in range(len(Successlist[i])):
        Successlist[i][j].append(random.randint(1,10)) # Success
        Successlist[i][j].append(random.randint(1,10)) # Fail

        per =round(Successlist[i][j][0] / (Successlist[i][j][0] + Successlist[i][j][1]),3)
        Successlist[i][j].append(per)


sum_count = [[[0 for i in range(2)] for i in range(5)] for i in range(50)]


for i in range(5):
    for j in range(len(Successlist)):
        for k in range(len(Successlist[j])):
            sum_count[j][i][0] = sum_count[j][i][0] + Successlist[j][k][0] * Abilitymatrix[k][i]
            sum_count[j][i][1] = sum_count[j][i][1] + Successlist[j][k][1] * Abilitymatrix[k][i]


for i in range(len(User_ability)):
    for j in range(len(User_ability[i])):
        User_ability[i][j] = round(((sum_count[i][j][0] / (sum_count[i][j][0] + sum_count[i][j][1])) * 10),1)

#printResultpage()

