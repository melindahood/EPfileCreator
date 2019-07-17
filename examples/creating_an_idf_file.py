# -*- coding: utf-8 -*-New to Spyder? Read our tutorialNew to Spyder? Read our tutorial
"""
Created on Mon Jun  4 22:30:35 2018

@author: mkj32
"""

#Version 8.9

from EPfileCreator.epfunctions_idealload_v890 import create_idf_file

from EPfileCreator.epfunctions_shadingsensitivity import modify_idf_shading

from EPfileCreator.epfunctions_globalsensitivity import modify_IDF_global


input_file_path = r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/SensitivityAnalysis/Shading_SA'

input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Shading_SA'

input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190710_1Y_MM'

iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
pathnameto_eppy = r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Energy Plus/IdealLoads'

pathnameto_eppy =r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/SensitivityAnalysis/Shading_SA'

baselineIDF =  pathnameto_eppy+r'/School_ShadingSA.idf'


#create_idf_file(input_file_path=input_file_path,
#                iddfile=iddfile,
#                pathnameto_eppy=pathnameto_eppy, 
#                nbiterations=3)
#create_idf_file(input_file_path=input_file_path,
#                iddfile=iddfile, 
#                nbiterations=5,
#                baselineIDF = baselineIDF,
#                versionIDF = "v890")
#modify_idf_shading(input_file_path=input_file_path,
#                iddfile=iddfile, 
#                nbiterations=100)
#modify_idf_shading_2(input_file_path=input_file_path,
#                iddfile=iddfile, 
#                nbiterations=100)

sensitivityfilename ="InputParams_SensitivityAnalysis_N_500.csv"
sensitivityfilename= "InputParams_SA_Min_Max.csv"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=18,
                sa_fname = sensitivityfilename,
                nbbatches=6)

# Divide 100 iterations into 4 batches, so we can run simulations in parallel.

#%% #Version 8.6
#
#from EPfileCreator.epfunctions_idealload_v890 import create_idf_file
#
#input_file_path = r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Code'
#iddfile = "C:/software/EnergyPlusV8-6-0/Energy+.idd"
#pathnameto_eppy = r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Energy Plus/IdealLoads'
#
#baselineIDF =  pathnameto_eppy+r'/baseline_V860.idf'
#
#
##create_idf_file(input_file_path=input_file_path,
##                iddfile=iddfile,
##                pathnameto_eppy=pathnameto_eppy, 
##                nbiterations=3)
#create_idf_file(input_file_path=input_file_path,
#                iddfile=iddfile, 
#                nbiterations=1,
#                baselineIDF = baselineIDF)
#
#
#create_idf_file(input_file_path,
#                iddfile, 
#               10,
#                baselineIDF)


#%% 
#from EPfileCreator.epfunctions_idealload_v890 import printversion
#printversion("v890")
