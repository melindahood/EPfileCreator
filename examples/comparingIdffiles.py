# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 17:39:24 2019

@author: mkj32
"""

from eppy.useful_scripts import idfdiff
from eppy.modeleditor import IDF
#must run! 
iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
IDF.setiddname(iddfile)


file1 = 'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190611_IDF_SA_Batch_A/2019-06-11_SA_run_0.idf'
file2 = 'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/CosimulationFiles/GlobalSA_BaselineIDF.idf'
file3 = 'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190606_OneDayJuly_TryAgain/2019-06-06_SA_run_0.idf'


# File from standalone test
file1 = 'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Standalone_Validation/Standalone_rw/GlobalSA_BaselineIDF_Standalone.idf'
# Cosim baseline
file2 = 'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Standalone_Validation/GlobalSA_BaselineIDF_Cosim.idf'
# Unsre
file3 = 'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Standalone_Validation/GlobalSA_BaselineIDF.idf'
file3a = 'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Standalone_Validation/GlobalSA_BaselineIDF_Standalone.idf'


# the one for cosims
file4 = 'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/20190813_Try7_Validation/Aug8Days_replicateGESidpt_wp.idf'

file5 = 'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/20190813_Try7_Validation/Aug8Days_replicateGESidpt_wp_4.idf'
file6 = 'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/20190813_Try7_Validation/GlobalSA_BaselineIDF_Cosim_wp_5.idf'

idf1 = IDF(file1)
idf2 = IDF(file2)
idf3 = IDF(file3)
idf3a = IDF(file3a)

idf4 =IDF(file4)
idf5 =IDF(file5)
idf6 =IDF(file6)
a =idfdiff.idfdiffs(idf1,idf3)

b =idfdiff.idfdiffs(idf2,idf3)

c =idfdiff.idfdiffs(idf1,idf2)

d= idfdiff.idfdiffs(idf2,idf4)
e= idfdiff.idfdiffs(idf2,idf5)
e= idfdiff.idfdiffs(idf2,idf3a)

f=idfdiff.idfdiffs(idf5,idf6)

## why is it not running ====================

file5 = 'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/20190813_Try7_Validation/Aug8Days_replicateGESidpt_wp_4.idf'
file6 = 'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/20190418_Try6_withRoofWindow/June_1Day_replicateGESidpt_wp2.idf'
idf5 =IDF(file5)
idf6 =IDF(file6)
f=idfdiff.idfdiffs(idf5,idf6)

