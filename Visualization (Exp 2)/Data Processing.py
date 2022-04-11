#-*- coding: utf-8 -*-
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy, os
from numpy import asarray


#Get File Names
path_dir = './'
file_list = os.listdir(path_dir)
file_list.sort()
dataList = []
for f in file_list:
    if f.find('.csv') is not -1:
        dataList.append(f)
dataList = sorted(dataList, key=lambda dataList:dataList[20])  #P로 정렬

stdList = [0.05, 0.1, 0.15, 0.2, 0.4, 0.7, 1]
countPN = 0

EMSO = asarray([0,0,0,0,0,0,0])
EMSX = asarray([0,0,0,0,0,0,0])

#Pre-Processing
for participant in dataList:
    expData = pd.read_csv(path_dir + participant)
    totalEachTrial = expData.shape[0] / (len(stdList) * 2)

    expData_Threshold = expData[expData.trialNumber == totalEachTrial-1]

    expData_Threshold_EMSO = expData_Threshold[expData_Threshold.EMS == 1]
    expData_Threshold_EMSO = expData_Threshold_EMSO.loc[:,['stdRatio', 'm', 'EMS']]
    expData_Threshold_EMSO = expData_Threshold_EMSO.sort_values(by=['stdRatio'])

    expData_Threshold_EMSX = expData_Threshold[expData_Threshold.EMS == 0]
    expData_Threshold_EMSX = expData_Threshold_EMSX.loc[:,['stdRatio', 'm', 'EMS']]
    expData_Threshold_EMSX = expData_Threshold_EMSX.sort_values(by=['stdRatio'])
    
    m_X = expData_Threshold_EMSX.m.values
    stdRatio_X = expData_Threshold_EMSX.stdRatio.values
    threshold_X = (stdRatio_X - m_X) / stdRatio_X
    
    m_O = expData_Threshold_EMSO.m.values
    stdRatio_O = expData_Threshold_EMSO.stdRatio.values
    threshold_O = (stdRatio_O - m_O) / stdRatio_O

    #print(expData_Threshold_EMSO)
    #print(expData_Threshold_EMSX)

    EMS_O = asarray(m_O)
    EMS_X = asarray(m_X)
    
    EMS_O = asarray(threshold_O)
    EMS_X = asarray(threshold_X)

    EMSO = EMSO + EMS_O
    EMSX = EMSX + EMS_X

    countPN += 1


EMSO = EMSO / countPN
EMSX = EMSX / countPN

plt.plot(stdRatio_O, EMSO, marker='o', color='steelblue')
plt.plot(stdRatio_X, EMSX, marker='x', color='maroon')


plt.xlabel('C/D Ratio')
plt.ylabel('Differential Threshold')
plt.legend(['EMS ON', 'EMS OFF'], loc=1)
#plt.title('Average Maximum Likelihood Procedure')
#plt.show()
plt.savefig('Average MLP.png', dpi=300)
plt.clf()