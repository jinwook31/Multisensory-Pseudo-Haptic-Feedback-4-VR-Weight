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


#EMS 기준으로 나누기
emsON = weightData[weightData.EMS == 1]
emsOFF = weightData[weightData.EMS == 0]
emsON.to_csv("./emsON.csv", mode='w', header=True)
emsOFF.to_csv("./emsOFF.csv", mode='w', header=True)

emsStatus = ['emsOFF', 'emsON']

for stat in emsStatus:
    smEffect = [0.005 , 0.05, 0.075, 0.09, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 1]
    val = [[],[],[],[],[],[],[],[],[],[],[],[],[]]

    f = open(stat + '.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    first = True
    for line in rdr:
        if(first):
            first=False
            continue
        val[smEffect.index(float(line[3]))].append(line[2])
    f.close()

    f = open(stat + 'cdRatio effect.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    smEffect = ['{:.3f}_'.format(x) + stat for x in smEffect]
    wr.writerow(smEffect)
    totalParticipantNum = len(val[0]) / 2
    for pNum in range(totalParticipantNum):
        idx = 2 * pNum
        nidx = idx + 1

        trial1 = [val[0][idx], val[1][idx], val[2][idx], val[3][idx],val[4][idx],val[5][idx],val[6][idx],val[7][idx],val[8][idx],val[9][idx],val[10][idx],val[11][idx],val[12][idx]]
        trial2 = [val[0][nidx], val[1][nidx], val[2][nidx], val[3][nidx],val[4][nidx],val[5][nidx],val[6][nidx],val[7][nidx],val[8][nidx],val[9][nidx],val[10][nidx],val[11][nidx],val[12][nidx]]
        trial1 = asarray(list(map(int, trial1)))
        trial2 = asarray(list(map(int, trial2)))

        res = trial1 + trial2
        res = res / 2

        wr.writerow(res)
    f.close()
