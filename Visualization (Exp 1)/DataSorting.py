#-*- coding: utf-8 -*-
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy, os
from numpy import asarray

emsList = ['ON','OFF']
smEffect = [0.05, 0.1, 0.15, 0.2, 0.4, 0.7, 1.0]

for emsStatus in emsList:
    ems = pd.read_csv('./ems' + emsStatus + '.csv')
    pivot = ems.groupby(['partiNum', 'delayRate'])['weightFelt'].mean().astype(float)
    pivot = pivot.unstack('delayRate').reset_index()
    pivot.to_csv('./ems' + emsStatus + '_reordered.csv', sep=',', na_rep='NaN', float_format = '%.2f')
    
