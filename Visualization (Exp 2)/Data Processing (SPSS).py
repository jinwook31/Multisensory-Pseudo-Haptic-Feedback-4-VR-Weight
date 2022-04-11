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
#dataList = sorted(dataList, key=lambda dataList:dataList[20])  #P로 정렬

stdList = [0.05, 0.1, 0.15, 0.2, 0.4, 0.7, 1]
countPN = 0

std0 = []
std1 = []
std2 = []
std3 = []
std4 = []
std5 = []
std6 = []

std0_X = []
std1_X = []
std2_X = []
std3_X = []
std4_X = []
std5_X = []
std6_X = []

#Pre-Processing
for participant in dataList:
    expData = pd.read_csv(path_dir + participant)
    totalEachTrial = expData.shape[0] / (len(stdList) * 2)

    expData_Threshold = expData[expData.trialNumber==totalEachTrial-1]

    expData_Threshold_EMSO = expData_Threshold[expData_Threshold.EMS == 1]
    expData_Threshold_EMSO = expData_Threshold_EMSO.loc[:,['stdRatio', 'm', 'EMS']]
    expData_Threshold_EMSO = expData_Threshold_EMSO.sort_values(by=['stdRatio'])

    expData_Threshold_EMSX = expData_Threshold[expData_Threshold.EMS == 0]
    expData_Threshold_EMSX = expData_Threshold_EMSX.loc[:,['stdRatio', 'm', 'EMS']]
    expData_Threshold_EMSX = expData_Threshold_EMSX.sort_values(by=['stdRatio'])
    
    m_X = expData_Threshold_EMSX.m.values
    stdRatio_X = expData_Threshold_EMSX.stdRatio.values
    # threshold_X = stdRatio_X - m_X

    std0_X.append(m_X[0])
    std1_X.append(m_X[1])
    std2_X.append(m_X[2])
    std3_X.append(m_X[3])
    std4_X.append(m_X[4])
    std5_X.append(m_X[5])
    std6_X.append(m_X[6])
    
    m_O = expData_Threshold_EMSO.m.values
    stdRatio_O = expData_Threshold_EMSO.stdRatio.values
    # threshold_O = stdRatio_O - m_O

    std0.append(m_O[0])
    std1.append(m_O[1])
    std2.append(m_O[2])
    std3.append(m_O[3])
    std4.append(m_O[4])
    std5.append(m_O[5])
    std6.append(m_O[6])
    
enableEMS = [std0, std1, std2, std3, std4, std5, std6]
disableEMS = [std0_X, std1_X, std2_X, std3_X, std4_X, std5_X, std6_X]
#dataLists = [enableEMS, disableEMS]

#Converting
def Convert(stdRes):
    for m_res, std in zip(stdRes, stdList):
        for idx in range(0, len(m_res)):
            m_res[idx] = (std - m_res[idx])

Convert(enableEMS)
Convert(disableEMS)
dataLists = [enableEMS, disableEMS]

#stdList = [0.05, 0.1, 0.15, 0.2, 0.4, 0.7, 1]
header = ['0.05_O','0.1_O','0.15_O','0.2_O','0.4_O','0.7_O','1_O','0.05_X','0.1_X','0.15_X','0.2_X','0.4_X','0.7_X','1_X']
f = open('./SPSS/output.csv', 'w', newline='', encoding='utf=8')
wr = csv.writer(f)
wr.writerow(header)

for p in range(0, len(std0)):
    line = []
    for ems in dataLists:
        for cd in ems:
            line.append(cd[p])
    wr.writerow(line)

f.close()


