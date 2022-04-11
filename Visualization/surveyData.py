#-*- coding: utf-8 -*-
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy, os
from scipy.optimize import curve_fit
import math

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
for participant in dataList:
    if pIndex == 0:
        expData = pd.read_csv(path_dir + participant)
        pIndex += 1
    else:
        csvData = pd.read_csv(path_dir + participant)
        expData = pd.concat([expData, csvData])

expData_trial = expData[expData.isTrial == 1]
weightData = expData_trial.loc[:,['Delay Rate', 'EMS Status','Q1', 'Q2', 'Q3', 'Q4']]

def curved(x, a, b):
    return a / x + b

def lim(x, a, b, c):
    return (x - c) * np.exp(-x * a) + b

questions = ['Q1', 'Q2', 'Q3', 'Q4']
for q in questions:
    evaluation = weightData.pivot_table(q, index='Delay Rate', columns='EMS Status', aggfunc='mean')

    idx = evaluation.index.tolist()
    val = evaluation.values.tolist()
    listData = [["delayRate","emsOFF","emsON"]]
    emsON = []
    emsOFF = []
    for i in range(0, len(idx)):
        #print(val[i])
        listData.append([idx[i], val[i][0], val[i][1]])
        emsON.append(val[i][0])
        emsOFF.append(val[i][1])

    #Draw Graph    
    if q is 'Q1':
        plt.title('Sensory Factor', fontsize=14)
        onSEM = [0.333,0.252,0.218,0.183,0.244,0.204,0.193,0.259,0.304,0.28,0.289,0.319,0.311]
        offSEM = [0.410,0.280,0.272,0.298,0.249,0.277,0.286,0.319,0.320,0.343,0.362,0.380,0.386]

    if q is 'Q2':
        plt.title('Realism Factor', fontsize=14)
        onSEM = [0.351,0.244,0.260,0.236,0.283,0.259,0.254,0.281,0.238,0.336,0.236,0.305,0.311]
        offSEM = [0.382,0.255,0.250,0.319,0.238,0.280,0.298,0.319,0.329,0.351,0.353,0.388,0.370]
        
    if q is 'Q3':
        plt.title('Distraction Factor', fontsize=14)
        onSEM = [0.3,0.38,0.297,0.26,0.282,0.299,0.310,0.365,0.264,0.311,0.352,0.323,0.338]
        offSEM = [0.386,0.34,0.263,0.274,0.272,0.263,0.208,0.197,0.206,0.131,0.185,0.162,0.2]

    if q is 'Q4':
        plt.title('Control Factor', fontsize=14)
        onSEM = [0.246,0.333,0.313,0.291,0.326,0.322,0.243,0.284,0.281,0.222,0.214,0.19,0.203]
        offSEM = [0.366,0.338,0.370,0.311,0.317,0.284,0.273,0.19,0.207,0.126,0.164,0.131,0.2]
    
    cntON_UP = np.array(emsON) + np.array(onSEM)
    cntON_DOWN = np.array(emsON) - np.array(onSEM)

    cntOFF_UP = np.array(emsOFF) + np.array(offSEM)
    cntOFF_DOWN = np.array(emsOFF) - np.array(offSEM)

    plt.errorbar(idx, emsOFF, yerr = offSEM, color='maroon', marker='.',linewidth=1.5, elinewidth=0.5, capsize=3, capthick=0.5)
    plt.errorbar(idx, emsON, yerr = onSEM, color='steelblue', marker='.',linewidth=1.5, elinewidth=0.5, capsize=3, capthick=0.5)

    plt.legend(['EMS ON','EMS OFF'])

    plt.fill_between(idx, cntON_DOWN, cntON_UP, alpha=0.1)
    plt.fill_between(idx, cntOFF_DOWN, cntOFF_UP, alpha=0.1)

    plt.xlabel('C/D Ratio', fontsize=12)
    plt.ylabel('Score average', fontsize=12)
    plt.ylim(0, 7)
    plt.savefig('./Fig/' + q + '_fitting.png', dpi=300)
    #plt.show()
    plt.clf()

    '''
    if q is 'Q1' or q is 'Q2':
        func = curved
    if q is 'Q3' or q is 'Q3':
        func = curved

    popt_OFF, pcov_OFF = curve_fit(func, idx, emsOFF)
    popt_ON, pcov_ON = curve_fit(func, idx, emsON)


    plt.scatter(idx, emsOFF, color='firebrick', marker='.')
    plt.plot(idx, func(np.asarray(idx), *popt_OFF), color='maroon', linewidth=2)
    plt.scatter(idx, emsON, color='lightskyblue', marker='.')
    plt.plot(idx, func(np.asarray(idx), *popt_ON), color='steelblue', linewidth=2)
    plt.legend(['EMS ON', 'EMS OFF'], loc=1)
    plt.title(q)
    plt.xlabel('C/D Ratio')
    plt.ylabel('Score Average')
    plt.savefig('./Fig/Questionnaire '+ q +'_Fitting.png', dpi=300)
    #plt.show()
    plt.clf()
    '''
    

