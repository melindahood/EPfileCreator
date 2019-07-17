# -*- coding: utf-8 -*-
"""
Created on Fri May 31 19:20:22 2019

@author: mkj32
"""

import csv
import os 
import pandas as pd
from eppy import modeleditor
from eppy.modeleditor import IDF

import eppy.EPlusInterfaceFunctions.parse_idd as parse_idd

import datetime # to add date and time of file created



def modify_idf_shading(input_file_path,iddfile,nbiterations):
    """creates idf based on baseline IDF, and three inputs: file path to baseline
    IDF, pathname to EnergyPlus Package, and nb of iterations to run the simulation 
    i.e. number of simulations based on the sensitivity analysis input file."""

# Prepare the idd file and file paths
    IDF.setiddname(iddfile)
    
    os.chdir(input_file_path)
    
    # Name baseline IDF file
    baselineIDF =  input_file_path+r'/School_ShadingSA.idf'
 
        
# Load all the input files
    shading_inputs =  pd.read_csv("InputParams_Shading_SensitivityAnalysis.csv")
 
    for runindex, run in shading_inputs.head(n=nbiterations).iterrows(): # only run for the first iteration
        
#        print(runindex, run)
        solar_transmittance   = round(run.solar_transmittance,2)
        solar_reflectance = round(run.solar_reflectance,2)
        int_exterior = run.int_exterior
        SP_temp  = run.SP_temp
        
        if round(int_exterior,1) == 1:
            int_exterior ="InteriorShade"
        elif round(int_exterior,1) == 2:
            int_exterior ="ExteriorShade"
    
        idf1 = IDF(baselineIDF)
        
        # modify run period for speed
        runperiod = idf1.idfobjects["RUNPERIOD"][0]
        runperiod.fieldnames
        runperiod.Begin_Month =1
        runperiod.Begin_Day_of_Month=1
        runperiod.End_Month =1
        runperiod.End_Day_of_Month=30       
        ## ..........................SHADING.....................................................
        # extract the shading control object to modify in the IDF file
        shadingcontrol = idf1.idfobjects["WINDOWPROPERTY:SHADINGCONTROL"][0] #use [0] to select the first and here only one
        
        # view the field names currently with:
#        for fieldname in shadingcontrol.fieldnames:
#            print("%s = %s" % (fieldname, shadingcontrol[fieldname]) )
            
        #modify for the correct fieldnames (View fieldname with shadingcontrol.fieldnames)
        shadingcontrol.Shading_Type = int_exterior
        shadingcontrol.Setpoint = SP_temp
        
        shadingconstruction= idf1.idfobjects["CONSTRUCTION"]
        shadingconstruction= idf1.idfobjects["CONSTRUCTION"][len(shadingconstruction)-1]
        if int_exterior =="ExteriorShade":
            shadingconstruction.Outside_Layer = "MEDIUM REFLECT - MEDIUM TRANS SHADE"
            shadingconstruction.Layer_2 = "CLEAR 3MM"
            shadingconstruction.Layer_3 = "AIR 6MM"
            shadingconstruction.Layer_4 = "CLEAR 3MM"        
        
        # in this sensitivity study we only want to change 4 params 
        # only one shading control to add:
        # to view the field names use shade.fieldnames
        shade = idf1.idfobjects["WINDOWMATERIAL:SHADE"][0]
        shade.Solar_Transmittance   = solar_transmittance
        shade.Solar_Reflectance   = solar_reflectance
        shade.Visible_Transmittance   = solar_transmittance
        shade.Visible_Reflectance   =  solar_reflectance
        
                # Add to csv file the run number
        print("run=",runindex)
        # Create a new folder for the date so that they can be saved in a clean way
        now = datetime.datetime.now()
        newpath =input_file_path +"/" + now.strftime('%Y%m%d')+"_" +"Shading_WinterMonth" 
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        os.chdir(newpath)
        filename = str(now)[:10] + "_SA_run_%d.idf" % runindex
        idf1.saveas(filename)
    
        print(filename)


def modify_idf_shading_2(input_file_path,iddfile,nbiterations):
    """creates idf based on baseline IDF, and three inputs: file path to baseline
    IDF, pathname to EnergyPlus Package, and nb of iterations to run the simulation 
    i.e. number of simulations based on the sensitivity analysis input file."""

# Prepare the idd file and file paths
    IDF.setiddname(iddfile)
    
    os.chdir(input_file_path)
    
    # Name baseline IDF file
    baselineIDF =  input_file_path+r'/School_ShadingSA.idf'
 
        
# Load all the input files
    shading_inputs =  pd.read_csv("InputParams_Shading_SensitivityAnalysis_2.csv")
 
    for runindex, run in shading_inputs.head(n=nbiterations).iterrows(): # only run for the first iteratiom
        idf1 = IDF(baselineIDF)
        
        # modify run period for speed
        runperiod = idf1.idfobjects["RUNPERIOD"][0]
        runperiod.fieldnames
        runperiod.Begin_Month =7
        runperiod.Begin_Day_of_Month=1
        runperiod.End_Month =7
        runperiod.End_Day_of_Month=3        
#        print(runindex, run)
        solar_transmittance   = round(run.solar_transmittance,2)
        int_exterior = run.int_exterior
        SP_temp  = run.SP_temp
        
        if round(int_exterior,1) == 1:
            int_exterior ="InteriorShade"
        elif round(int_exterior,1) == 2:
            int_exterior ="ExteriorShade"
    
        if solar_transmittance ==1:
            shading_name="HR-LT"
            solar_r = 0.8
            solar_t =0.1
        elif solar_transmittance ==2:
            shading_name="MR-MT"
            solar_r = 0.4
            solar_t =0.5
        elif solar_transmittance ==3:
            shading_name="MR-LT"
            solar_r = 0.5
            solar_t =0.1
        elif solar_transmittance ==4:
            shading_name="LR-HT"
            solar_r = 0.2
            solar_t =0.7
        elif solar_transmittance ==5:
            shading_name="LR-MT"
            solar_r = 0.2
            solar_t =0.4            
        ## ..........................SHADING.....................................................
        # extract the shading control object to modify in the IDF file
        shadingcontrol = idf1.idfobjects["WINDOWPROPERTY:SHADINGCONTROL"][0] #use [0] to select the first and here only one
        
        # view the field names currently with:
#        for fieldname in shadingcontrol.fieldnames:
#            print("%s = %s" % (fieldname, shadingcontrol[fieldname]) )
            
        #modify for the correct fieldnames (View fieldname with shadingcontrol.fieldnames)
        shadingcontrol.Shading_Type = int_exterior
        shadingcontrol.Setpoint = SP_temp
        
        shadingconstruction= idf1.idfobjects["CONSTRUCTION"]
        shadingconstruction= idf1.idfobjects["CONSTRUCTION"][len(shadingconstruction)-1]
        if int_exterior =="ExteriorShade":
            shadingconstruction.Outside_Layer = shading_name
            shadingconstruction.Layer_2 = "CLEAR 3MM"
            shadingconstruction.Layer_3 = "AIR 6MM"
            shadingconstruction.Layer_4 = "CLEAR 3MM"
        elif int_exterior =="InteriorShade":
            shadingconstruction.Outside_Layer = "CLEAR 3MM"
            shadingconstruction.Layer_2 = "AIR 6MM"
            shadingconstruction.Layer_3 = "CLEAR 3MM"            
            shadingconstruction.Layer_4 = shading_name

        # otherwise leave as is (for interior shade)
    
        #modify 
        
        # in this sensitivity study we only want to change 4 params 
        # only one shading control to add:
        # to view the field names use shade.fieldnames
        shade = idf1.idfobjects["WINDOWMATERIAL:SHADE"][0]
        shade.Name = shading_name
        shade.Solar_Transmittance   = solar_t
        shade.Solar_Reflectance   = solar_r
        shade.Visible_Transmittance   = solar_t
        shade.Visible_Reflectance   = solar_r
        
                # Add to csv file the run number
        print("run=",runindex)
        # Create a new folder for the date so that they can be saved in a clean way
        now = datetime.datetime.now()
        newpath =input_file_path +"/" + now.strftime('%Y%m%d')+"_" +"Shading_2" 
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        os.chdir(newpath)
        filename = str(now)[:10] + "_SA_run_%d.idf" % runindex
        idf1.saveas(filename)
    
        print(filename)


if __name__ == '__main__':
    input_file_path = r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/SensitivityAnalysis/Shading_SA'
    iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
    nbiterations=5
    modify_idf_shading(input_file_path,iddfile,nbiterations)