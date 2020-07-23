# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:47:41 2019

@author: mkj32
This script modifies the parameters for the global sensitivity analysis made in LHS_space.R
"""

import shutil
import csv
import os 
import pandas as pd
from eppy import modeleditor
from eppy.modeleditor import IDF
import itertools
import string
import eppy.EPlusInterfaceFunctions.parse_idd as parse_idd

import datetime # to add date and time of file created
from math import sqrt # for square root of window size



def modify_IDF_global(input_file_path,iddfile,nbiterations,sa_fname,nbbatches, start_month, end_month,m_file1,m_file2,monthprefix):
    """creates idf based on baseline IDF, and three inputs: file path to baseline
    IDF, pathname to EnergyPlus Package, and nb of iterations to run the simulation 
    i.e. number of simulations based on the sensitivity analysis input file."""

# Prepare the idd file and file paths
    IDF.setiddname(iddfile)
    
    os.chdir(input_file_path)
    
    # Name baseline IDF file
    baselineIDF =  input_file_path+r'/CosimulationFiles/GlobalSA_BaselineIDF_Cosim.idf'
    

# Load all the input files
    sa_inputs =  pd.read_csv(sa_fname)

    #Planted_area
    # maybe used to modify size on internal mass?
    # 

    # now we divide into 4 batches
    #nbiterations=100
    #nbbatches=4
    nbiterations_inbatch = int(nbiterations/nbbatches)
    #letters_batch =('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
    letters_batch = list(itertools.islice(excel_cols(), nbbatches))
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
            mofify_run_period(idf1,from_day=1, from_month=start_month, to_day=31, to_month=end_month)
            
            
            ## Heating and cooling setpoints  of the greenhouse =============================================
            #Cooling_SP_GH
            #Heating_SP_GH
            # modify the scheduled cooling and heating setpoints, objects 72 and 73 respectively
            heatingsched = idf1.idfobjects["SCHEDULE:COMPACT"][51-1]
            coolingsched = idf1.idfobjects["SCHEDULE:COMPACT"][52-1]
            # nightheating
            for night_fieldname in [6,10,13,17,20]:
                #print(night_fieldname)
                heatingsched[heatingsched.fieldnames[night_fieldname]] = round(run.Heating_SP_GH*0.85,1) #it can get 10% colder at night
                coolingsched[coolingsched.fieldnames[night_fieldname]] = round(run.Cooling_SP_GH*1.1,1) #it can get 10% warmer at night
            for day_fieldname in [8,15]:
                heatingsched[heatingsched.fieldnames[day_fieldname]] = round(run.Heating_SP_GH,1) 
                coolingsched[coolingsched.fieldnames[day_fieldname]] = round(run.Cooling_SP_GH,1) 
    
            
            #shading =======================================================
            #rooftop_window
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
            
            new_min_x = min_x + (36-sqrt(windowsize)*36)/2
            new_min_y = min_y + (7-sqrt(windowsize)*7)/2
            new_max_x = new_min_x + 36*sqrt(windowsize)
            new_max_y = new_min_y + 7*sqrt(windowsize)

            # verification: (new_max_x-new_min_x)*(new_max_y-new_min_y)-252*windowsize
            # create window object 
            # count how many windows there are
            nbwindows = len(idf1.idfobjects["FENESTRATIONSURFACE:DETAILED"])
            ghwindow = idf1.idfobjects["FENESTRATIONSURFACE:DETAILED"][nbwindows-1] # select the last window
            
            # identify the fieldnames of the window object
            #ghwindow.fieldnames
            # modify the coordinates
            ghwindow.Vertex_1_Xcoordinate = new_min_x
            ghwindow.Vertex_1_Ycoordinate = new_max_y
            
            ghwindow.Vertex_2_Xcoordinate = new_min_x
            ghwindow.Vertex_2_Ycoordinate = new_min_y
            
            ghwindow.Vertex_3_Xcoordinate = new_max_x
            ghwindow.Vertex_3_Ycoordinate = new_min_y
            
            ghwindow.Vertex_4_Xcoordinate = new_max_x
            ghwindow.Vertex_4_Ycoordinate = new_max_y 

            #ratio_airmix_GH
            #ratio_airmix_CR

            ## AIR MIXING GREENHOUSE =========================================
            zonemixing = idf1.idfobjects["ZONEMIXING"]
            
            # Greenhouse ventilation rate: - fixing the ventilation rate to 4
            ach_GH = 10# round(run.ACH_GH,2) # total ventilation rate fixed to 10 (varies summer/winter)
            # the ratio of mixing is run.ratio_airmix_GH          
            zonemixing[0].Air_Changes_per_Hour =  ach_GH * run.ratio_airmix_GH 
            ghventilation = idf1.idfobjects["ZONEVENTILATION:DESIGNFLOWRATE"][6]
            ghventilation.Air_Changes_per_Hour = ach_GH * (1- run.ratio_airmix_GH )
#            
#            # Greenhouse ventilation rate: - giving a minimum ventilation rate of 3.75
#            ach_GH = round(run.ACH_GH,2) # total ventilation rate
#            # the ratio of mixing is run.ratio_airmix_GH          
#            zonemixing[0].Air_Changes_per_Hour = run.ratio_airmix_GH 
#            ghventilation = idf1.idfobjects["ZONEVENTILATION:DESIGNFLOWRATE"][6]
#            ghventilation.Air_Changes_per_Hour = ach_GH 
#            
            # AIR MIXING CLASSROOM -------------------------------------
            ACH_CR =4 # round(run.ACH_CR,2) # total ventilation rate
            # the ratio of mixing is run.ratio_airmix_CR         
            zonemixing[1].Air_Changes_per_Hour = ACH_CR *  run.ratio_airmix_CR   
            crventilation = idf1.idfobjects["ZONEVENTILATION:DESIGNFLOWRATE"][8]
            crventilation.Air_Changes_per_Hour = ACH_CR * (1- run.ratio_airmix_CR )


            
            ## CREATE THE IDF FILE ===========================
                    # Add to csv file the run number
            print("run=",runindex)
            # Create a new folder for the date so that they can be saved in a clean way
            now = datetime.datetime.now()
            # monthprefix = "Jan"
            newpath =input_file_path +"/" + now.strftime('%Y%m%d')+"_" +monthprefix+"_Batch"+letters_batch[batch]
            
            if not os.path.exists(newpath):
                os.mkdir(newpath)
            variables_file_path =  input_file_path +"/CosimulationFiles/variables.cfg" 
            shutil.copy(variables_file_path, newpath)
            cosim_file_path1 =  input_file_path +"/CosimulationFiles/"+m_file1 
            cosim_file_path2 =  input_file_path +"/CosimulationFiles/"+m_file2 
            cosim_new_file_path1 = newpath + "/Run_Cosim_"+monthprefix+"_Batch_"+letters_batch[batch]+"_C1.m"
            cosim_new_file_path2 = newpath + "/Run_Cosim_"+monthprefix+"_Batch_"+letters_batch[batch]+"_C2.m"
            shutil.copy(cosim_file_path1, cosim_new_file_path1)
            shutil.copy(cosim_file_path2, cosim_new_file_path2)
            os.chdir(newpath)
            filename = str(now)[:10] + "_SA_run_%d.idf" % runindex
            idf1.saveas(filename)
        
            print(filename)
    
            
def excel_cols():
    n = 1
    while True:
        yield from (''.join(group) for group in itertools.product(string.ascii_uppercase, repeat=n))
        n += 1



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
    
    
#%% Find the area of each zone
#zones = idf1.idfobjects["ZONE"]

