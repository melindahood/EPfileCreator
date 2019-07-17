# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 17:39:24 2019

@author: mkj32
"""

from eppy.useful_scripts import idfdiff
from eppy.modeleditor import IDF

file1 = 'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190611_IDF_SA_Batch_A/2019-06-11_SA_run_0.idf'
file2 = 'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/CosimulationFiles/GlobalSA_BaselineIDF.idf'
file3 = 'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190606_OneDayJuly_TryAgain/2019-06-06_SA_run_0.idf'

iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"

idf1 = IDF(file1)
idf2 = IDF(file2)
idf3 = IDF(file3)
idfdiff.idfdiffs(idf1,idf3)
