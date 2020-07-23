# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:45:13 2019

@author: mkj32
"""

# -*- coding: utf-8 -*-New to Spyder? Read our tutorialNew to Spyder? Read our tutorial
"""
Created on Mon Jun  4 22:30:35 2018

@author: mkj32
"""
#%% Load the packages necessary
#Version 8.9

from EPfileCreator.epfunctions_idealload_v890 import create_idf_file

from EPfileCreator.epfunctions_shadingsensitivity import modify_idf_shading

from EPfileCreator.epfunctions_globalsensitivity_new import modify_IDF_global


#%% For renewd min max

# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20200418_1Y_MM'
sensitivityfilename= "InputParams_SA_Min_Max_PAR.csv"
iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename1=r"Run_NP_Cosim_Batch_1Y_MM_C1.m"
matlab_filename2=r"Run_NP_Cosim_Batch_1Y_MM_C2.m"
monthprefix="1Y"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=16,
                sa_fname = sensitivityfilename,
                nbbatches=16,
                start_month=1, end_month=12,m_file1=matlab_filename1,m_file2=matlab_filename2,monthprefix=monthprefix)

#%% For renewd min max

# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20200420_1Y_MM_2'
sensitivityfilename= "InputParams_SA_Min_Max_PAR.csv"
iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename1=r"Run_NP_Cosim_Batch_1Y_MM_C1.m"
matlab_filename2=r"Run_NP_Cosim_Batch_1Y_MM_C2.m"
monthprefix="1Y"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=16,
                sa_fname = sensitivityfilename,
                nbbatches=16,
                start_month=1, end_month=12,m_file1=matlab_filename1,m_file2=matlab_filename2,monthprefix=monthprefix)

#%% For the ParamChange - JUlY

# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20191105_ParamChange/July'
sensitivityfilename= r"InputParams_ParamChange.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename1=r"Run_FCosim_Batch_July_PC_C1.m"
matlab_filename2=r"Run_FCosim_Batch_July_PC_C2.m"
monthprefix="July"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=26,
                sa_fname = sensitivityfilename,
                nbbatches=26,
                start_month=7, end_month=7,m_file1=matlab_filename1,m_file2=matlab_filename2,monthprefix=monthprefix)

#%% For the ParamChange - FEB

# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20191105_ParamChange/Feb'
sensitivityfilename= r"InputParams_ParamChange.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename1=r"Run_FCosim_Batch_Feb_PC_C1.m"
matlab_filename2=r"Run_FCosim_Batch_Feb_PC_C2.m"
monthprefix="Feb"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=26,
                sa_fname = sensitivityfilename,
                nbbatches=26,
                start_month=2, end_month=2,m_file1=matlab_filename1,m_file2=matlab_filename2,monthprefix=monthprefix)

#%% For the one year Morris


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20200108_NewMorris'
sensitivityfilename= r"Morris_sample_12T_ordered_new_small.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename1=r"Run_Cosim_Batch_1Y_Morris_NP_C1.m"
matlab_filename2=r"Run_Cosim_Batch_1Y_Morris_NP_C2.m"
monthprefix="1Y"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=84,
                sa_fname = sensitivityfilename,
                nbbatches=84,
                start_month=1, end_month=12,m_file1=matlab_filename1,m_file2=matlab_filename2,monthprefix=monthprefix)



#%% Create list of scripts to run from command line to open matlab
def excel_cols():
    n = 1
    while True:
        yield from (''.join(group) for group in itertools.product(string.ascii_uppercase, repeat=n))
        n += 1
import itertools
import string

list(itertools.islice(excel_cols(), 50))
    

def create_command_file(nbbatches, base_filename,batchdate, monthname):
    fname = base_filename+"\\Text_Cosim_Command_line_run_NP_C1.txt"
    letters_batch = list(itertools.islice(excel_cols(), nbbatches))
    f= open(fname,"w+")
    for i in range(nbbatches):
        letter=letters_batch[i]
        text1 = "matlab -nosplash -r \"run(\'" +base_filename +batchdate
        text2 =text1+letter +"\\Run_Cosim_"+monthname+"_Batch_"+letter+"_C1.m\')\"\r\n"
        print(text2)
        f.write(text2)
    f.close()

def create_command_file_2(nbbatches, base_filename1,base_filename2,batchdate, monthname):
    fname = base_filename1+"\\Text_Cosim_Command_line_run_NP_C2.txt"
    letters_batch = list(itertools.islice(excel_cols(), nbbatches))
    f= open(fname,"w+")
    for i in range(nbbatches):
        letter=letters_batch[i]
        text1 = "matlab -nosplash -r \"run(\'" +base_filename2 +batchdate
        text2 =text1+letter +"\\Run_Cosim_"+monthname+"_Batch_"+letter+"_C2.m\')\"\r\n"
        print(text2)
        f.write(text2)
    f.close()


#%% Create command line files
# 1 YEar param C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190930_ParamChange
base_filename1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20191104_ParamChange_morecrops'
base_filename2 = r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA\20191104_ParamChange_morecrops'

batchdate = '\\20191104_1Y_Batch'
create_command_file(26,base_filename1,batchdate,monthname="1Y")
create_command_file_2(26,base_filename1,base_filename2,batchdate,monthname="1Y")

#%% 1 YEar MM
base_filename1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20200418_1Y_MM'
base_filename2 = r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA\20200418_1Y_MM'

batchdate = '\\20200418_1Y_Batch'
create_command_file(16,base_filename1,batchdate,monthname="1Y")
create_command_file_2(16,base_filename1,base_filename2,batchdate,monthname="1Y")

#%% 1 YEar MM 2
base_filename1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20200420_1Y_MM_2'
base_filename2 = r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA\20200420_1Y_MM_2'

batchdate = '\\20200420_1Y_Batch'
create_command_file(16,base_filename1,batchdate,monthname="1Y")
create_command_file_2(16,base_filename1,base_filename2,batchdate,monthname="1Y")



#%% 1 YEar LHS
base_filename1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20200103_1Y_SRC'
base_filename2 = r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA\20200103_1Y_SRC'

batchdate = '\\20200103_1Y_Batch'
create_command_file(50,base_filename1,batchdate,monthname="1Y")
create_command_file_2(50,base_filename1,base_filename2,batchdate,monthname="1Y")

#%% 1 YEar Morris
base_filename1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20191103_1Y_Morris'
base_filename2 = r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA\20191103_1Y_Morris'

batchdate = '\\20191104_1Y_Batch'
create_command_file(50,base_filename1,batchdate,monthname="1Y")
create_command_file_2(50,base_filename1,base_filename2,batchdate,monthname="1Y")

#%% 1 YEar Morris - NEW!
base_filename1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20200108_NewMorris'
base_filename2 = r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA\20200108_NewMorris'

batchdate = '\\20191104_1Y_Batch'
create_command_file(84,base_filename1,batchdate,monthname="1Y")
create_command_file_2(84,base_filename1,base_filename2,batchdate,monthname="1Y")


#%%##################### 1 month July
path1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA'
path2= r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA'

## July
folder = '\\20191105_ParamChange\July'
base_filename1 = path1 +folder
base_filename2 = path2 +folder

batchdate = '\\20191105_July_Batch'
create_command_file(26,base_filename1,batchdate,monthname="July")
create_command_file_2(26,base_filename1,base_filename2,batchdate,monthname="July")

# Feb:
folder = '\\20191105_ParamChange\Feb'
base_filename1 = path1 +folder
base_filename2 = path2 +folder

batchdate = '\\20191105_Feb_Batch'
create_command_file(26,base_filename1,batchdate,monthname="Feb")
create_command_file_2(26,base_filename1,base_filename2,batchdate,monthname="Feb")



#%%# Modify the matlab file in each folder
which_modifying = r'\20191103_1Y_SRC'
input_file_path = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA'+which_modifying
m_file=r"Run_Cosim_Batch_1Y_SRC_NP_C2.m"

base_filename1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA'+which_modifying
base_filename2 = r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA'+which_modifying
batchdate = '\\20191211_1Y_Batch'

letters_batch = list(itertools.islice(excel_cols(), 50))
import shutil
for batch in letters_batch:
    #print(batch)
    cosim_file_path =  input_file_path +"/CosimulationFiles/"+m_file 
    cosim_new_file_path = base_filename1 +batchdate+batch + "\\Run_Cosim_1Y_Batch_"+batch+"_NP_C2.m"
    
    shutil.copy(cosim_file_path, cosim_new_file_path)

#\\Run_Cosim_"+monthname+"_Batch_"+letter+"_C2.m            
#%% Find divisible factors
            
def factors(chosen, currentnum=None, numbers=None): 
    # Recursion start, always append 1 and start with 2
    if numbers is None:
        numbers = [1]
        currentnum = 2
    # We're at the last value, it's always divisible by itself so
    # append it and return
    if currentnum == chosen:
        numbers.append(currentnum)
        return numbers
    else:
        # Check if the chosen item is divisible by the current number
        if chosen % currentnum == 0:
            numbers.append(currentnum)
        # Always continue with the next number:
        currentnum += 1
        return factors(chosen, currentnum, numbers)
    
chosen = int(input("Enter what you want the factors of: "))
factors(chosen)
