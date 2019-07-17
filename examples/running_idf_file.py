# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 14:59:54 2018

@author: mkj32
"""
import sys, os
from eppy.modeleditor import IDF
#from eppy import modeleditor

import datetime # to add date and time of file created
#from eppy.results import readhtml # the eppy module with functions to read the html

import csv
import pandas as pd


pathnameto_eppy =r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/SensitivityAnalysis/Shading_SA'
sys.path.append(pathnameto_eppy)
 
# Create a new folder for the date so that they can be saved in a clean way
now = datetime.datetime.now()
newpath = pathnameto_eppy +'/' + now.strftime('%Y%m%d')+"_" +"Shading" +"/Runs"
if not os.path.exists(newpath):
    os.mkdir(newpath)
os.chdir(newpath)


iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
IDF.setiddname(iddfile)

#%% Set the file name and path

rundate = now.strftime('%Y%m%d')
folderpath =input_file_path +"/" + now.strftime('%Y%m%d')+"_" +"Shading" 
dirs = os.listdir( folderpath )

energyoutputs = []
for file in dirs:
    idfrun = file[10:-4]
    runnumber = idfrun[-2:]
       

       
    idfname = folderpath +'/'+ file
    epwfile = "C:/EnergyPlusV8-9-0/WeatherData/GBR_London.Gatwick.037760_IWEC.epw"
    idf = IDF(idfname, epwfile)
    

    #% Run the idf file
    
    idf.run(output_directory=newpath, 
            output_prefix = rundate + idfrun + '_',
            expandobjects=True,
            readvarsESO=True)
    
    #results are in this folder:
    # file:///C:/Users/mkj32/eplustbl.htm
    
    #% Read outputs
    
    csvfname =newpath'/'+ rundate+ idfrun + '_tbl.csv'
    with open(csvfname,'r') as table:
       # TotalSiteEnergy = myreader[14]
        data =list(csv.reader(table))
        TotalSiteEnergy = data[14][2]
        EnergyPerArea = data[14][3]
        BuildingArea = data[41][2]
        ElectricityUse = data[64][2]
        DistrictHeating = data[64][6]
        
    
    #Append to big csv file of outputs
    energyoutputs.append({
            'RunNumber':runnumber,
            'TotalSiteEnergy':TotalSiteEnergy,
            'EnergyPerArea':EnergyPerArea,
            'BuildingArea':BuildingArea,
            'ElectricityUse':ElectricityUse,
            'DistrictHeating':DistrictHeating,
            })
    
    print(energyoutputs)
    
#%% Save as csv file for future analysis

energy_df = pd.DataFrame(energyoutputs)
energy_df.to_csv(pathnameto_eppy+'/Energy Use results/Energy Use of Schools.csv',index=False )


#%% When want to run specific files
##%%
#dirs = [
#'2018-07-17_school_run_3.idf',
#
#'2018-07-17_school_run_6.idf',
#
#'2018-07-17_school_run_10.idf',
#]
#
##%%
#file=dirs[1]
#    idfrun = file[10:-4]
#    runnumber = idfrun[-2:]
##%%
#
#energyoutputs = []
#   #%% Load IDF 