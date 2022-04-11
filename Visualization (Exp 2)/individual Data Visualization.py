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
    if f.find('.csv') != -1:
        dataList.append(f)
dataList = sorted(dataList, key=lambda dataList:dataList[20])  #P로 정렬

stdList = [0.05, 0.1, 0.15, 0.2, 0.4, 0.7, 1]
countPN = 1

#Pre-Processing
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

    #Draw Graph
    #plt.plot(stdRatio_O, threshold_O, marker='o')
    #plt.plot(stdRatio_X, threshold_X, marker='x')
    plt.plot(stdRatio_O, m_O, marker='o')
    plt.plot(stdRatio_X, m_X, marker='x')
    plt.xlabel('Delay Rate')
    plt.ylabel('Differential Threshold')
    plt.title('./Fig/P0'+ str(countPN) + ' Differential Threshold for C/D Ratio')
    plt.legend(['EMS ON', 'EMS OFF'], loc=1)
    #plt.show()
    plt.savefig('P0'+ str(countPN) + '_Threshold.png', dpi=300)
    plt.clf()

    for std in stdList:
        expData_std = expData[expData.stdRatio == std]
        
        expData_std_EMSO = expData_std[expData_std.EMS == 1]
        expData_std_EMSO  = expData_std_EMSO.loc[:, ['stdRatio', 'trialNumber','stim', 'isCorrect']]

        expData_std_EMSX = expData_std[expData_std.EMS == 0]
        expData_std_EMSX  = expData_std_EMSX.loc[:, ['stdRatio', 'trialNumber','stim', 'isCorrect']]

        trialNum_EMSO = expData_std_EMSO.trialNumber.values+1
        stim_EMSO = expData_std_EMSO.stim.values

        trialNum_EMSX = expData_std_EMSX.trialNumber.values+1
        stim_EMSX = expData_std_EMSX.stim.values

        plt.plot(trialNum_EMSO, stim_EMSO, marker='o', color='steelblue')
        plt.plot(trialNum_EMSX, stim_EMSX, marker='x', color='maroon')
        plt.axhline(y=m_O[stdList.index(std)], color='steelblue', linestyle='--')
        plt.axhline(y=m_X[stdList.index(std)], color='maroon', linestyle='--')
        #plt.xlim(0.5, 18.5)
        plt.xticks(np.arange(1, 19, 1))

        plt.xlabel('Trials')
        plt.ylabel('C/D ratio applied to another cube')
        plt.legend(['EMS ON', 'EMS OFF'], loc=1)
        #plt.title(str(std) + ' Maximum Likelihood Procedure')
        #plt.show()
        plt.savefig('./Fig/P0'+ str(countPN) + '_' + str(std) + '_MLP.png', dpi=300)
        plt.clf()
    
    countPN += 1

