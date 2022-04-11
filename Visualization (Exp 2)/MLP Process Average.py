#-*- coding: utf-8 -*-
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy, os

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
#countPN = 1

#Pre-Processing
totalEMSO = np.empty((0, 18), float)
totalEMSX = np.empty((0, 18), float)
for participant in dataList:
    expData = pd.read_csv(path_dir + participant)
    totalEachTrial = expData.shape[0] / ( len(stdList) * 2)

    expData_Threshold = expData[expData.trialNumber == totalEachTrial-1]

    expData_Threshold_EMSO = expData_Threshold[expData_Threshold.EMS == 1]
    expData_Threshold_EMSO = expData_Threshold_EMSO.loc[:,['stdRatio', 'm', 'EMS']]
    expData_Threshold_EMSO = expData_Threshold_EMSO.sort_values(by=['stdRatio'])

    expData_Threshold_EMSX = expData_Threshold[expData_Threshold.EMS == 0]
    expData_Threshold_EMSX = expData_Threshold_EMSX.loc[:,['stdRatio', 'm', 'EMS']]
    expData_Threshold_EMSX = expData_Threshold_EMSX.sort_values(by=['stdRatio'])
    
    m_X = expData_Threshold_EMSX.m.values
    stdRatio_X = expData_Threshold_EMSX.stdRatio.values
    threshold_X = stdRatio_X - m_X
    
    m_O = expData_Threshold_EMSO.m.values
    stdRatio_O = expData_Threshold_EMSO.stdRatio.values
    threshold_O = stdRatio_O - m_O

    #totalEMSO = np.empty((0, 18), float)
    #totalEMSX = np.empty((0, 18), float)
    for std in stdList:
        expData_std = expData[expData.stdRatio == std]
        
        expData_std_EMSO = expData_std[expData_std.EMS == 1]
        expData_std_EMSO  = expData_std_EMSO.loc[:, ['stdRatio', 'trialNumber','stim', 'isCorrect']]

        expData_std_EMSX = expData_std[expData_std.EMS == 0]
        expData_std_EMSX  = expData_std_EMSX.loc[:, ['stdRatio', 'trialNumber','stim', 'isCorrect']]

        trialNum_EMSO = expData_std_EMSO.trialNumber.values
        stim_EMSO = expData_std_EMSO.stim.values

        trialNum_EMSX = expData_std_EMSX.trialNumber.values
        stim_EMSX = expData_std_EMSX.stim.values

        stim_EMSO = np.array(stim_EMSO)
        stim_EMSX = np.array(stim_EMSX)

        stim_EMSO = np.where(stim_EMSO==0.01, 0, stim_EMSO)
        stim_EMSX = np.where(stim_EMSX==0.01, 0, stim_EMSX)

        print(stim_EMSO)

        stim_EMSO = stim_EMSO/std * 100
        stim_EMSX = stim_EMSX/std * 100

        totalEMSO = np.vstack([totalEMSO, stim_EMSO])
        totalEMSX = np.vstack([totalEMSX, stim_EMSX])


totalEMSO = totalEMSO.mean(axis=0)
totalEMSX = totalEMSX.mean(axis=0)

plt.plot(trialNum_EMSO, totalEMSO, marker='o')
plt.plot(trialNum_EMSX, totalEMSX, marker='x')
plt.xlabel('Trials') # 정수로 표시
plt.ylabel('C/D Ratio')
plt.legend(['EMS ON', 'EMS OFF'], loc=1)
plt.title('Maximum Likelihood Procedure')
plt.savefig('./MLP Fig/total_MLP.png', dpi=300)
plt.clf()

