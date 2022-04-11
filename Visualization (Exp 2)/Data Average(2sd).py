#-*- coding: utf-8 -*-
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy, os
from numpy import asarray
from scipy import stats

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
    #threshold_X = stdRatio_X - m_X

    std0_X.append(m_X[0])
    std1_X.append(m_X[1])
    std2_X.append(m_X[2])
    std3_X.append(m_X[3])
    std4_X.append(m_X[4])
    std5_X.append(m_X[5])
    std6_X.append(m_X[6])
    
    m_O = expData_Threshold_EMSO.m.values
    stdRatio_O = expData_Threshold_EMSO.stdRatio.values
    #threshold_O = stdRatio_O - m_O

    std0.append(m_O[0])
    std1.append(m_O[1])
    std2.append(m_O[2])
    std3.append(m_O[3])
    std4.append(m_O[4])
    std5.append(m_O[5])
    std6.append(m_O[6])
    
enableEMS = [std0, std1, std2, std3, std4, std5, std6]
disableEMS = [std0_X, std1_X, std2_X, std3_X, std4_X, std5_X, std6_X]
stdList = [0.05, 0.1, 0.15, 0.2, 0.4, 0.7, 1]

#Converting
def Convert(stdRes):
    for m_res, std in zip(stdRes, stdList):
        for idx in range(0, len(m_res)):
            m_res[idx] = std - m_res[idx]

Convert(enableEMS)
Convert(disableEMS)


#Trimming
EMSO_err = []
EMSO = []
for std in enableEMS:
    stds = np.array(std)

    mean = np.mean(stds, axis=0)
    sd = np.std(stds, axis=0)

    final_list = [x for x in std if (x > mean - 2 * sd)]
    final_list = [x for x in final_list if (x < mean + 2 * sd)]

    finstd = np.array(final_list)
    finstd = std #no 2sd

    mean = np.mean(finstd, axis=0)
    EMSO.append(mean)
    EMSO_err.append(stats.sem(finstd, axis=0))
    
EMSX_err = []
EMSX = []
for std in disableEMS:
    stds = np.array(std)

    mean = np.mean(stds, axis=0)
    sd = np.std(stds, axis=0)

    final_list = [x for x in std if (x > mean - 2 * sd)]
    final_list = [x for x in final_list if (x < mean + 2 * sd)]

    finstd = np.array(final_list)
    finstd = std #no 2sd

    mean = np.mean(finstd, axis=0)
    EMSX.append(mean)
    EMSX_err.append(stats.sem(finstd, axis=0))


#Ploting
cntON_UP = np.array(EMSO) + np.array(EMSO_err)
cntON_DOWN = np.array(EMSO) - np.array(EMSO_err)

cntOFF_UP = np.array(EMSX) + np.array(EMSX_err)
cntOFF_DOWN = np.array(EMSX) - np.array(EMSX_err)


plt.errorbar(stdRatio_O, EMSO, EMSO_err, color='maroon', marker='.',linewidth=1.5, elinewidth=0.5, capsize=3, capthick=0.5)
plt.errorbar(stdRatio_X, EMSX, EMSX_err,color='steelblue', marker='.', linewidth=1.5, elinewidth=0.5, capsize=3, capthick=0.5)

plt.legend(['EMS ON', 'EMS OFF'], loc=2)

plt.fill_between(stdRatio_O, cntON_DOWN, cntON_UP, alpha=0.1, color='maroon')
plt.fill_between(stdRatio_X, cntOFF_DOWN, cntOFF_UP, alpha=0.1,color='steelblue')
plt.xticks(np.arange(0, 1.1, 0.1))

plt.xlabel('Standard C/D ratio', fontsize=11)
plt.ylabel('Difference threshold (C/D ratio)', fontsize=11)

plt.show()
plt.savefig('Average MLP.png', dpi=300)
plt.clf()


