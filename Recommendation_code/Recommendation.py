import os
import random
import sys
from optparse import OptionParser
import pandas as pd
import numpy as np
from numpy import insert
from openpyxl import Workbook
import copy

# get data from other .py files # dependency occurred
import apriori
import ResultMatrix
import ScoreMatrix
import KeywordMatrix
import ResultPage

df = ResultMatrix.get_df()
GAME_NAME = ResultMatrix.get_gamename()
score_list = ScoreMatrix.get_scorematrix()
#print(score_list)
keyword_list=KeywordMatrix.get_keywordMatrix()

df_to_list = []
for i in range(len(df.values)):  # DataFrame -> List
    df_to_list.append(list(copy.deepcopy(df.values[i])))

prefer_candi_list = [[] for i in range(len(df_to_list))]  # Candidate List declare(Prefer)
prefer_candi_name_list = [[] for i in range(len(df_to_list))]

User_prefer_Name_list = []  # User prfer Game Name List
User_prefer_value_list = []  # User prefer Game value list

recommend_level_up = [[] for i in range(len(df_to_list))]  # Level up Please
recommend_level_down = [[] for i in range(len(df_to_list))]  # Level down Please
recommend_practice = [[] for i in range(len(df_to_list))]  # Practice Please
recommend_not_prefer = [[] for i in range(len(df_to_list))]  # Not Prefer But I recommend

def makeStandardGame():

    for i in range(len(df_to_list)):  # Candidate List Create
        count = 0
        temp = copy.deepcopy(df_to_list[i])

        for j in range(len(df_to_list[0])):  # Name Add to List
            temp[j].append(GAME_NAME[j + 1])

        temp = sorted(temp)  # Sorting Temp
        recommend_not_prefer[i].append(temp[0])  # Not Prefer Game List append
        recommend_not_prefer[i].append(temp[1])
        recommend_not_prefer[i].append(temp[2])

        for j in range(len(df_to_list[0])):

            df_to_list[i][j].append(GAME_NAME[j + 1])

            if 'T' in df_to_list[i][j] and (df_to_list[i][j][2] == 3 or df_to_list[i][j][2] == None):  # 기준 게임 찾기 위해서
                prefer_candi_list[i].append(copy.deepcopy(df_to_list[i][j]))
                prefer_candi_list[i][count].append(GAME_NAME[j + 1])
                count = count + 1

            elif 'T' in df_to_list[i][j] and (df_to_list[i][j][2] == 1 or df_to_list[i][j][2] == 2):  # Level up Game List
                recommend_level_up[i].append(df_to_list[i][j])

            elif 'F' in df_to_list[i][j] and (df_to_list[i][j][2] == 1 or df_to_list[i][j][2] == 2):  # Practice Game List
                recommend_practice[i].append(df_to_list[i][j])

            elif 'F' in df_to_list[i][j] and df_to_list[i][j][2] == 3:  # Level down Game List
                recommend_level_down[i].append(df_to_list[i][j])

            elif df_to_list[i][j][1] == None:
                pass

        if len(prefer_candi_list[i]) == 0:  # if len(prefer_candi_list[i]) == 0
            prefer_candi_list[i].append(temp[len(temp) - 1])
            prefer_candi_list[i][count].append(temp[len(temp) - 1][3])

    count = 0
    for i in range(len(prefer_candi_list)):  # Prefer Game Value and Name list Create
        temp = copy.deepcopy(prefer_candi_list[i])
        temp = sorted(temp, reverse=True)

        if len(prefer_candi_list[i]) == 0:
            User_prefer_Name_list.append("  ")
        else:
            User_prefer_value_list.append(prefer_candi_list[i][0])
            User_prefer_Name_list.append(User_prefer_value_list[count][3])
            count = count + 1

    df["기준게임"] = User_prefer_Name_list  # Column Add
    #엑셀에 writing은 아직 하지 않음.

# recommend 1. A Priori algorithm 결과로 좋아하는 게임 추천하기.

def recommend_apriori():

    #for apriori
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                             dest='input',
                             help='filename containing csv',
                             default=None)
    optparser.add_option('-s', '--minSupport',
                             dest='minS',
                             help='minimum support value',
                             default=0.5,
                             type='float')
    optparser.add_option('-c', '--minConfidence',
                             dest='minC',
                             help='minimum confidence value',
                             default=0.7,
                             type='float')

    (options, args) = optparser.parse_args()

    inFile = 'correlation.csv'
    options.input = inFile
    if options.input is None:
            inFile = sys.stdin
    elif options.input is not None:
            inFile = apriori.dataFromFile(options.input)
    else:
            print('No dataset filename specified, system with exit\n')
            sys.exit('System will exit')

    minSupport = options.minS
    minConfidence = options.minC

    #items, rules 결과가 담긴 변수
    items, rules = apriori.runApriori(inFile, minSupport, minConfidence)

    q_list=[]
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: {0} ==> {1} , {2}".format(str(pre), str(post), confidence))
        if "G17" in pre:
            q_list=q_list+(list(post))

    #q_list에서 중복된 게임은 제거
    q_list = set(q_list)
    print("User1의 기준 게임 : " + User_prefer_Name_list[0] )
    print("\n\nq_list : ")
    print(q_list)

    if len(q_list) == 0: #기준게임이 p집합 안에 없는 경우 - keyword matrix 사용 후 score순으로 정렬
        
        print("\n!!! q_list is empty !!!")
        five_intersection_lens=get_keyword_set()
        
        #score순으로 정렬하여 3개만 추천
        for i in range(len(five_intersection_lens)):
            for j in range(len(score_list)):
                if(five_intersection_lens[i][0]==score_list[0][j][1]):
                    five_intersection_lens[i].insert(0,score_list[0][j][0])
                    break

        five_intersection_lens = sorted(five_intersection_lens, reverse=True)

        print("\nfive_intersection_lens with score : ")
        print("1st : " + five_intersection_lens[0][1]+ "\n2st : "+five_intersection_lens[1][1]+"\n3st : "+five_intersection_lens[2][1])
        
    else :#기준게임이 p집합 안에 있는 경우 - score 5개 뽑기
        
        print("\n!!! q_list is not empty !!!")
        high_score=get_high_score()
        qq_list=['G13', 'G17']
        intersection_set=set(q_list) & set(high_score) #교집합
        print("\nThe intersection set : ")
        print (intersection_set)
        complementary_set=set(q_list) ^ set(high_score) #대칭 차집합
        print("\nThe complementary_set : ")
        print(complementary_set)

#score가 가장 높은 것 5개 추출
def get_high_score():

    #print("score_list with game name")
    #print(score_list)

    tmp = copy.deepcopy(score_list)
    tmp = sorted(tmp[0], reverse=True)  # Sorting tmp

    high_score=[]
    high_score.append(tmp[0][1])
    high_score.append(tmp[1][1])
    high_score.append(tmp[2][1])
    high_score.append(tmp[3][1])
    high_score.append(tmp[4][1])

    print("\nhigh_score lsit : ")
    print(high_score)

    return high_score

#기준게임의 키워드를 포함하는 집합 추출
def get_keyword_set():

    print("keyword matrix import")

    #기준게임의 키워드 뽑기
    for i in range(len(keyword_list)):
        if(User_prefer_Name_list[0]==keyword_list[i][0]):
            standard_keyword = keyword_list[i]
            print("standard_keyword : ")
            print(standard_keyword)

    #keyword를 많이 포함하는 순서로  다른 게임들 Search

    intersection_lens=[[] for i in range(len(keyword_list)) ]
    for i in range(len(keyword_list)):

        if(standard_keyword[0]==keyword_list[i][0]): #자기 자신과의 비교는 피한다.
            continue
        else:
            intersection =list(set(standard_keyword) & set(keyword_list[i]))
            #print("intersection : ")
            #print(intersection)

            intersection.append(keyword_list[i][0])
            #print("intersection with gamename: ")
            #print(intersection)

            intersection_lens[i].append(len(intersection))
            intersection_lens[i]+=intersection

    print("\nintersection_lens : ")
    print(intersection_lens)
    
    #정렬
    intersection_lens = sorted(intersection_lens, reverse=True)
    print("\nsorted intersection_lens : ")
    print(intersection_lens)

    #상위 5개의 게임
    five_intersection_lens=[[], [], [], [], []]

    five_intersection_lens[0].append(intersection_lens[0][len(intersection_lens[0])-1])
    five_intersection_lens[1].append(intersection_lens[1][len(intersection_lens[1])-1])
    five_intersection_lens[2].append(intersection_lens[2][len(intersection_lens[2])-1])
    five_intersection_lens[3].append(intersection_lens[3][len(intersection_lens[3])-1])
    five_intersection_lens[4].append(intersection_lens[4][len(intersection_lens[4])-1])

    print("\nfive_intersection_lens : ")
    print(five_intersection_lens)

    return five_intersection_lens


# recommend 2. 경우의 수를 랜덤하게 추천하기.
def recommend_cases():

    rand_number = random.randint(1, 4)  # 4 case 중 무작위로 random하게 추천하기 위한 random_number

    if rand_number == 1:  # level down list copy
        recommend_list = copy.deepcopy(recommend_level_down)
        message = "난이도를 낮춰서 플레이해보세요."
    elif rand_number == 2:
        recommend_list = copy.deepcopy(recommend_level_up)
        message = "난이도를 올려서 플레이해보세요."
    elif rand_number == 3:
        recommend_list = copy.deepcopy(recommend_practice)
        message = "조금 더 연습해보시는 건 어때요?"
    elif rand_number == 4:
        recommend_list = copy.deepcopy(recommend_not_prefer)
        message = "오랜만에 해보시는 건 어떨까요?"

    rand_number = random.randint(0, len(recommend_list[0]) - 1)  # recommend list 안에서 무작위로 추천하기 위한 random_number
    print(recommend_list[0][rand_number][3] + " 게임을 " + message)

# recommend 3. 능력보완 추천하기.
def recommend_ability():
    ResultPage.printResultpage()

#함수 호출하여 프로그램 실행
makeStandardGame()
#recommend_apriori()
#recommend_cases()
recommend_ability()