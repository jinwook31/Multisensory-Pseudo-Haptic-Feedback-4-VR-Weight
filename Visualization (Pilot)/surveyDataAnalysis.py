#-*- coding: utf-8 -*-
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy, os
from numpy import asarray

#Get File Names
path_dir = './Data/'
file_list = os.listdir(path_dir)
file_list.sort()
dataList = []
for f in file_list:
    if f.find('.csv') is not -1:
        dataList.append(f)
dataList = sorted(dataList, key=lambda dataList:dataList[16])  #P로 정렬

#Pre-Processing
pIndex = 0
for participant in dataList:
    if pIndex == 0:
        expData = pd.read_csv(path_dir + participant)
        pIndex += 1
    else:
        csvData = pd.read_csv(path_dir + participant)
        expData = pd.concat([expData, csvData])

expData_trial = expData[expData.isTrial == 1]
weightData = expData_trial.loc[:,['Participant Number','Weight Felt', 'Delay Rate', 'EMS Status','Q1', 'Q2', 'Q3', 'Q4','Trial Time']]
weightData.columns = ["partiNum", "weightFelt", "delayRate", "EMS", "Q1", "Q2", "Q3", "Q4", "trialTime"]

#Participant별 집은 평균 시간
grabbedTime = weightData.pivot_table('trialTime', index='partiNum',  aggfunc=[np.mean, np.std])
#print(grabbedTime)

#CSV 출력
weightData.to_csv("./totalData.csv", mode='w', header=True)


questions = ['Q1', 'Q2', 'Q3', 'Q4']
for q in questions:
    smEffect = [0.005 , 0.05, 0.075, 0.09, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 1]
    valON = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
    valOFF = [[],[],[],[],[],[],[],[],[],[],[],[],[]]

    f = open('emsOFF.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    first = True
    for line in rdr:
        if(first):
            first=False
            continue
        valOFF[smEffect.index(float(line[3]))].append(line[questions.index(q) + 5])
    f.close()

    f = open('emsON.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    first = True
    for line in rdr:
        if(first):
            first=False
            continue
        valON[smEffect.index(float(line[3]))].append(line[questions.index(q) + 5])
    f.close()


    f = open('Questionnaire EMS_'+ q + '.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    smEffect_ON = ['ON_{:.3f}'.format(x) for x in smEffect]
    smEffect_OFF = ['OFF_{:.3f}'.format(x) for x in smEffect]
    smEffect_ON.extend(smEffect_OFF)
    wr.writerow(smEffect_ON) #Header
    totalParticipantNum = len(valON[0]) / 2
    for pNum in range(int(totalParticipantNum)):
        idx = 2 * pNum
        nidx = idx + 1

        trial1 = [valON[0][idx], valON[1][idx], valON[2][idx], valON[3][idx],valON[4][idx],valON[5][idx],valON[6][idx],valON[7][idx],valON[8][idx],valON[9][idx],valON[10][idx],valON[11][idx],valON[12][idx],valOFF[0][idx], valOFF[1][idx], valOFF[2][idx], valOFF[3][idx],valOFF[4][idx],valOFF[5][idx],valOFF[6][idx],valOFF[7][idx],valOFF[8][idx],valOFF[9][idx],valOFF[10][idx],valOFF[11][idx],valOFF[12][idx]]
        trial2 = [valON[0][nidx], valON[1][nidx], valON[2][nidx], valON[3][nidx],valON[4][nidx],valON[5][nidx],valON[6][nidx],valON[7][nidx],valON[8][nidx],valON[9][nidx],valON[10][nidx],valON[11][nidx],valON[12][nidx],valOFF[0][nidx], valOFF[1][nidx], valOFF[2][nidx], valOFF[3][nidx],valOFF[4][nidx],valOFF[5][nidx],valOFF[6][nidx],valOFF[7][nidx],valOFF[8][nidx],valOFF[9][nidx],valOFF[10][nidx],valOFF[11][nidx],valOFF[12][nidx]]
        trial1 = asarray(list(map(float, trial1)))
        trial2 = asarray(list(map(float, trial2)))

        res = trial1 + trial2
        res = res / 2

        wr.writerow(res)

        #wr.writerow([valON[0][idx], valON[1][idx], valON[2][idx], valON[3][idx],valON[4][idx],valON[5][idx],valON[6][idx],valON[7][idx],valON[8][idx],valON[9][idx],valON[10][idx],valON[11][idx],valON[12][idx],valOFF[0][idx], valOFF[1][idx], valOFF[2][idx], valOFF[3][idx],valOFF[4][idx],valOFF[5][idx],valOFF[6][idx],valOFF[7][idx],valOFF[8][idx],valOFF[9][idx],valOFF[10][idx],valOFF[11][idx],valOFF[12][idx]])
    f.close()



