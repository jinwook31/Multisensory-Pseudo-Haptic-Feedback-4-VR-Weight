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
weightData = expData_trial.loc[:,['Participant Number','Weight Felt', 'Delay Rate', 'EMS Status','Trial Time']]
weightData.columns = ["partiNum", "weightFelt", "delayRate", "EMS", "trialTime"]

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
    smEffect = [0.05, 0.1, 0.15, 0.2, 0.4, 0.7, 1]
    val = [[],[],[],[],[],[],[]]

    f = open(stat + '.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    first = True
    for line in rdr:
        if(first):
            first=False
            continue
        val[smEffect.index(float(line[3]))].append(line[2])
    f.close()

