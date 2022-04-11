#-*- coding: utf-8 -*-
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy, os
from scipy.optimize import curve_fit

#Get File Names
path_dir = './Data/'
file_list = os.listdir(path_dir)
file_list.sort()
dataList = []
for f in file_list:
    if f.find('.csv') is not -1:
        dataList.append(f)
dataList = sorted(dataList, key=lambda dataList:dataList[16])  #P로 정렬

#Sigmoid
def func(x, a, b):
    #return a/pow(x, b)
    return a/x + b

#Pre-Processing
pNum = 1
fittingRes = []
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

    popt_OFF, pcov_OFF = curve_fit(func, idx, emsOFF, maxfev=5000)
    popt_ON, pcov_ON = curve_fit(func, idx, emsON, maxfev=5000)

    fittingRes.append([popt_OFF[0], popt_OFF[1], popt_ON[0], popt_ON[1]])

    #Make Graph
    plt.scatter(idx, emsOFF, color='firebrick', marker='.')
    plt.plot(idx, func(np.asarray(idx), *popt_OFF), color='maroon', linewidth=2)
    plt.scatter(idx, emsON, color='lightskyblue', marker='.')
    plt.plot(idx, func(np.asarray(idx), *popt_ON), color='steelblue', linewidth=2)
    plt.legend(['EMS ON', 'EMS OFF'], loc=1)
    plt.title('Prob of felt weight')
    plt.xlabel('Delay Rate')
    plt.ylabel('Prob')
    #plt.show()
    plt.savefig('./Fig/P'+ str(pNum) + '_weight perception_fitting.png', dpi=300)
    pNum += 1
    plt.clf()


#Res2CSV
f = open('fitting Result.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(["aOFF","bOFF","aON","bON"])
for idx in fittingRes:
    wr.writerow(idx)
f.close()

