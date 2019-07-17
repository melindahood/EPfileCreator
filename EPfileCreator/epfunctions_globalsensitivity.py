# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:47:41 2019

@author: mkj32
This script modifies the parameters for the global sensitivity analysis made in LHS_space.R
"""


import csv
import os 
import pandas as pd
from eppy import modeleditor
from eppy.modeleditor import IDF

import eppy.EPlusInterfaceFunctions.parse_idd as parse_idd

import datetime # to add date and time of file created



def modify_IDF_global(input_file_path,iddfile,nbiterations,sa_fname,nbbatches):
    """creates idf based on baseline IDF, and three inputs: file path to baseline
    IDF, pathname to EnergyPlus Package, and nb of iterations to run the simulation 
    i.e. number of simulations based on the sensitivity analysis input file."""

# Prepare the idd file and file paths
    IDF.setiddname(iddfile)
    
    os.chdir(input_file_path)
    
    # Name baseline IDF file
    baselineIDF =  input_file_path+r'/CosimulationFiles/GlobalSA_BaselineIDF.idf'
    

# Load all the input files
    sa_inputs =  pd.read_csv(sa_fname)
    
    # now we divide into 4 batches
    #nbiterations=100
    #nbbatches=4
    nbiterations_inbatch = int(nbiterations/nbbatches)
    letters_batch =('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
    batch_index =range(0 , int(nbiterations_inbatch))
    for batch in range(0, nbbatches):
        print("-----------------Batch number is now",batch)
        for runindex in batch_index:
            print("Index number is now",runindex)
            runindex = runindex+nbiterations_inbatch*batch
            print("******Index number is now",runindex)
            
            # Now we can select the correct row from sa_inputs
            run = sa_inputs.iloc[int(runindex),]
            # for runindex, run in sa_inputs.head(n=nbiterations).iterrows(): # only run for the first iteration
        
            print(runindex, run)
            idf1 = IDF(baselineIDF)
            # modify run period
            mofify_run_period(idf1,from_day=1, from_month=1, to_day=31, to_month=12)
            
            
            ## ..........................SHADING.....................................................
            solar_transmittance   = round(run.shading,2)
            solar_reflectance = 0.99-solar_transmittance
            # only one shading control to add:
            # to view the field names use shade.fieldnames
            shade = idf1.idfobjects["WINDOWMATERIAL:SHADE"][0]
            shade.Solar_Transmittance   = solar_transmittance
            shade.Solar_Reflectance   = solar_reflectance
            shade.Visible_Transmittance   = solar_transmittance
            shade.Visible_Reflectance   =  solar_reflectance
            
            ## ..........................ROOFTOP WINDOW.....................................................
            windowsize =round(run.rooftop_window,2)# percentage of rooftop size
            #  max_x = 74.15       max_y = -34.44
            min_x = 38.15
            min_y = -41.44
            new_min_x = min_x + (36-windowsize*36)/2
            new_min_y = min_y + (7-windowsize*7)/2
            new_max_x = min_x + (windowsize*36)
            new_max_y = min_y + (windowsize*7)
            # create window object 
            # count how many windows there are
            nbwindows = len(idf1.idfobjects["FENESTRATIONSURFACE:DETAILED"])
            ghwindow = idf1.idfobjects["FENESTRATIONSURFACE:DETAILED"][nbwindows-1] # select the last window
            
            # identify the fieldnames of the window object
            ghwindow.fieldnames
            # modify the coordinates
            ghwindow.Vertex_1_Xcoordinate = new_min_x
            ghwindow.Vertex_1_Ycoordinate = new_max_y
            
            ghwindow.Vertex_2_Xcoordinate = new_min_x
            ghwindow.Vertex_2_Ycoordinate = new_min_y
            
            ghwindow.Vertex_3_Xcoordinate = new_max_x
            ghwindow.Vertex_3_Ycoordinate = new_min_y
            
            ghwindow.Vertex_4_Xcoordinate = new_max_x
            ghwindow.Vertex_4_Ycoordinate = new_max_y        
            
            ## OCCUPANT DENSITY
            maxpeople = 23
            number_of_people = round(run.occupant_density*maxpeople)
            # modify object 8, index 7 in python
            ghpeople = idf1.idfobjects["PEOPLE"][7]
            ghpeople.Number_of_People=number_of_people
            
            ## AIR MIXING =========================================
            zonemixing = idf1.idfobjects["ZONEMIXING"]
            ach_co_gh = round(run.Airmixing_toGH,2) # from corridor to greenhouse
            zonemixing[0].Air_Changes_per_Hour = ach_co_gh
            ach_gh_cr = round(run.Airmixing_toCR,2) # from greenhouse to classroom
            zonemixing[1].Air_Changes_per_Hour = ach_gh_cr
            
            # if air mixing to classroom too low, add some natural ventilation to classroom:
            crventilation = idf1.idfobjects["ZONEVENTILATION:DESIGNFLOWRATE"][8]
            if ach_gh_cr <4:
                crventilation.Air_Changes_per_Hour = 4-ach_gh_cr
            else:
                crventilation.Air_Changes_per_Hour =0
            
            ## GREENHOUSEVENTILATION
            ghventilation = idf1.idfobjects["ZONEVENTILATION:DESIGNFLOWRATE"][6]
            ach_GH = round(run.Airmixing_toGH,2) # from corridor to greenhouse
            ghventilation.Air_Changes_per_Hour = ach_GH
            
            ## Heating and cooling setpoints
            # modify the scheduled cooling and heating setpoints, objects 72 and 73 respectively
            heatingsched = idf1.idfobjects["SCHEDULE:COMPACT"][71]
            coolingsched = idf1.idfobjects["SCHEDULE:COMPACT"][72]
            # nightheating
            for night_fieldname in [6,10,13,17,20]:
                print(night_fieldname)
                heatingsched[heatingsched.fieldnames[night_fieldname]] = round(run.Heating_SP_GH*0.9,1) #it can get 10% colder at night
                coolingsched[coolingsched.fieldnames[night_fieldname]] = round(run.Cooling_SP_GH*1.1,1) #it can get 10% warmer at night
            for day_fieldname in [8,15]:
                heatingsched[heatingsched.fieldnames[day_fieldname]] = round(run.Heating_SP_GH,1) #it can get 10% colder at night
                coolingsched[coolingsched.fieldnames[day_fieldname]] = round(run.Cooling_SP_GH,1) #it can get 10% warmer at night
            ## CREATE THE IDF FILE
                    # Add to csv file the run number
            print("run=",runindex)
            # Create a new folder for the date so that they can be saved in a clean way
            now = datetime.datetime.now()
            newpath =input_file_path +"/" + now.strftime('%Y%m%d')+"_" +"1Y_MM_Batch_"+letters_batch[batch]
            if not os.path.exists(newpath):
                os.mkdir(newpath)
            os.chdir(newpath)
            filename = str(now)[:10] + "_SA_run_%d.idf" % runindex
            idf1.saveas(filename)
        
            print(filename)

def mofify_run_period(idf1,from_day, from_month, to_day, to_month):
    # modify run period for speed
    runperiod = idf1.idfobjects["RUNPERIOD"][0]
    runperiod.fieldnames
    runperiod.Begin_Month =from_month
    runperiod.Begin_Day_of_Month=from_day
    runperiod.End_Month =to_month
    runperiod.End_Day_of_Month=to_day 

if __name__ == '__main__':
    input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA'
    iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
    nbiterations=2
    modify_IDF_global(input_file_path,iddfile,nbiterations)