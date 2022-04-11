#-*- coding: utf-8 -*-
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy, os

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
emsON = []
emsOFF = []
pIndex = 0
pNum = 1
for participant in dataList:
    expData = pd.read_csv(path_dir + participant)

    expData_trial = expData[expData.isTrial == 1]
    weightData = expData_trial.loc[:,['Delay Rate', 'EMS Status', 'Weight Felt']]

    perception = weightData.pivot_table('Weight Felt', index='Delay Rate', columns='EMS Status', aggfunc='mean')

    idx = perception.index.tolist()
    val = perception.values.tolist()
    emsON = []
    emsOFF = []
    listData = [["delayRate","emsOFF","emsON"]]
    for i in range(0, len(idx)):
        #print(val[i])
        listData.append([idx[i], val[i][0], val[i][1]])
        emsON.append(val[i][0])
        emsOFF.append(val[i][1])
        
    #Draw Graph
    plt.plot(idx, emsON)
    plt.plot(idx, emsOFF)
    plt.xlabel('Delay Rate')
    plt.ylabel('Prob')
    plt.title('Prob of felt weight')
    plt.legend(['emsOFF','emsON'])
    plt.savefig('./Fig/P' + str(pNum) + '_weight perception.png', dpi=300)
    pNum += 1
    #plt.show()
    plt.clf()

