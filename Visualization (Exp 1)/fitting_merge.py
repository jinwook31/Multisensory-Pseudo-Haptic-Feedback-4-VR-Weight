#-*- coding: utf-8 -*-
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy, os
import scipy as sy
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
weightData = expData_trial.loc[:,['Delay Rate', 'EMS Status', 'Weight Felt']]

perception = weightData.pivot_table('Weight Felt', index='Delay Rate', columns='EMS Status', aggfunc='mean')

idx = perception.index.tolist()
val = perception.values.tolist()
listData = [["delayRate","emsOFF","emsON"]]
for i in range(0, len(idx)):
    #print(val[i])
    listData.append([idx[i], val[i][0], val[i][1]])
    emsON.append(val[i][0])
    emsOFF.append(val[i][1])
    
#Sigmoid
def func(x, a, b):
    return 1. / (1. + np.exp(-a*(x-b)))

par0 = sy.array([0., 1.])

popt_OFF, pcov_OFF = curve_fit(func, idx, emsOFF)
print(popt_OFF)
popt_ON, pcov_ON = curve_fit(func, idx, emsON)
print(popt_ON)


#plt.scatter(idx, emsOFF, s=10, facecolors='none', edgecolors='firebrick')
plt.plot(idx, func(np.asarray(idx), *popt_OFF), color='firebrick', linewidth=1.5)
#plt.scatter(idx, emsON, s=10, facecolors='none', edgecolors='lightskyblue')
plt.plot(idx, func(np.asarray(idx), *popt_ON), color='lightskyblue', linewidth=1.5)


##ERROR BAR##
onSEM = [0.072,0.068,0.08,0.076,0.032,0.024,0.017]
offSEM = [0.046,0.049,0.053,0.067,0.071,0.069,0.07]

cntON_UP = np.array(emsON) + np.array(onSEM)
cntON_DOWN = np.array(emsON) - np.array(onSEM)

cntOFF_UP = np.array(emsOFF) + np.array(offSEM)
cntOFF_DOWN = np.array(emsOFF) - np.array(offSEM)

#plt.scatter(idx, emsOFF, s=10, facecolors='none', edgecolors='firebrick')
#plt.errorbar(idx, func(np.asarray(idx), *popt_OFF), yerr = offSEM, color='maroon', linewidth=1.5, elinewidth=0.5, capsize=3, capthick=0.5)
#plt.scatter(idx, emsON, s=10, facecolors='none', edgecolors='lightskyblue')
#plt.errorbar(idx, func(np.asarray(idx), *popt_ON), yerr = onSEM, color='steelblue', linewidth=1.5, elinewidth=0.5, capsize=3, capthick=0.5)

plt.errorbar(idx, emsON, yerr = onSEM, color='steelblue', marker='.',linewidth=1.5, elinewidth=0.5, capsize=3, capthick=0.5, linestyle='None')
plt.errorbar(idx, emsOFF, yerr = offSEM, color='maroon', marker='.', linewidth=1.5, elinewidth=0.5, capsize=3, capthick=0.5, linestyle='None')

plt.legend(['EMS ON', 'EMS OFF'], loc=1)

#plt.fill_between(idx, cntON_DOWN, cntON_UP, alpha=0.1)
#plt.fill_between(idx, cntOFF_DOWN, cntOFF_UP, alpha=0.1)

plt.axhline(y=0.5, color='g', linestyle='--', linewidth=0.7)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.xticks(np.arange(0, 1.1, 0.1))

plt.xlabel('C/D Ratio',fontsize=11)
plt.ylabel('Probability of weight perception', fontsize=11)
#plt.savefig('./Fig/fitting_merged.png', dpi=300)
plt.show()

