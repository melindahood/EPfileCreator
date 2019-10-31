# -*- coding: utf-8 -*-New to Spyder? Read our tutorialNew to Spyder? Read our tutorial
"""
Created on Mon Jun  4 22:30:35 2018

@author: mkj32
"""
#%% Load the packages necessary
#Version 8.9

from EPfileCreator.epfunctions_idealload_v890 import create_idf_file

from EPfileCreator.epfunctions_shadingsensitivity import modify_idf_shading

from EPfileCreator.epfunctions_globalsensitivity import modify_IDF_global

#%%

input_file_path = r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/SensitivityAnalysis/Shading_SA'

input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Shading_SA'

input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190710_1Y_MM'

iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
pathnameto_eppy = r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Energy Plus/IdealLoads'

sensitivityfilename ="InputParams_SensitivityAnalysis_N_500.csv"
pathnameto_eppy =r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Cosimulation/SensitivityAnalysis/Shading_SA'

baselineIDF =  pathnameto_eppy+r'/School_ShadingSA.idf'


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190818_1Y_MM'
sensitivityfilename= "InputParams_SA_Min_Max_2.csv"
iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"


modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=18,
                sa_fname = sensitivityfilename,
                nbbatches=6)

# Add variables and config file in each folder
#%% For the July LHS ========================


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190930_July_LHS_400'
sensitivityfilename= r"InputParams_SensitivityAnalysis_N_400.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename=r"Run_Cosim_Batch_JulySRC.m"
monthprefix="July"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=400,
                sa_fname = sensitivityfilename,
                nbbatches=40,
                start_month=7, end_month=7,m_file=matlab_filename,
                monthprefix=monthprefix)


#%% For the January LHS ========================


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190930_Jan_LHS_400'
sensitivityfilename= r"InputParams_SensitivityAnalysis_N_400.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename=r"Run_Cosim_Batch_JanSRC.m"
monthprefix="Jan"

modify_IDF_global(input_file_path=input_file_path,iddfile=iddfile, 
                nbiterations=400,
                sa_fname = sensitivityfilename,
                nbbatches=40,
                start_month=1, end_month=1,m_file=matlab_filename, 
                monthprefix=monthprefix)
#%% For theYEAR LONG LHS  ========================


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20191003_1Y_LHS_400'
sensitivityfilename= r"InputParams_SensitivityAnalysis_N_400.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename=r"Run_Cosim_Batch_1YSRC.m"
monthprefix="1Y"

modify_IDF_global(input_file_path=input_file_path,iddfile=iddfile, 
                nbiterations=400,
                sa_fname = sensitivityfilename,
                nbbatches=50,
                start_month=1, end_month=1,m_file=matlab_filename, 
                monthprefix=monthprefix)

#%% For the July MORRIS METHOD ======================


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190913_July_Morris'
sensitivityfilename= r"InputParam_Morris_N_120.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename=r"Run_Cosim_Batch_JulyMorris.m"
monthprefix="July"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=120,
                sa_fname = sensitivityfilename,
                nbbatches=30,
                start_month=7, end_month=7,m_file=matlab_filename,monthprefix=monthprefix)

#%% For the January MORRIS METHOD ======================


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190913_January_Morris'
sensitivityfilename= r"InputParam_Morris_N_120.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename=r"Run_Cosim_Batch_JanMorris.m"
monthprefix="Jan"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=120,
                sa_fname = sensitivityfilename,
                nbbatches=30,
                start_month=1, end_month=1,m_file=matlab_filename,monthprefix=monthprefix)

#%% For the parametric study


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190930_ParamChange'
sensitivityfilename= r"InputParams_ChangeExperiment.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename=r"Run_Cosim_Batch_1YParamStudy.m"
monthprefix="1Y"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=17,
                sa_fname = sensitivityfilename,
                nbbatches=17,
                start_month=1, end_month=12,m_file=matlab_filename,monthprefix=monthprefix)
#%% For the parametric study 2 : =heating


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20191004_1Year_HeatingChange'
sensitivityfilename= r"InputParams_ChangeHeatingGH.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename=r"Run_Cosim_Batch_1YP_HeatingChange.m"
monthprefix="1Y"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=17,
                sa_fname = sensitivityfilename,
                nbbatches=17,
                start_month=1, end_month=12,m_file=matlab_filename,monthprefix=monthprefix)

#%% For the parametric study 2 : =heating and more crops


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20191006_ParamChange_morecrops'
sensitivityfilename= r"InputParams_ChangeExperiment_morecrops.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename=r"Run_Cosim_Batch_1YParamStudy_morecrops.m"
monthprefix="1Y"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=25,
                sa_fname = sensitivityfilename,
                nbbatches=25,
                start_month=1, end_month=12,m_file=matlab_filename,monthprefix=monthprefix)

#%% For the one year lHS


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20191008_1Year_SRC'
sensitivityfilename= r"InputParams_SensitivityAnalysis_N_450.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename=r"Run_Cosim_Batch_1Y_LHS.m"
monthprefix="1Y"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=450,
                sa_fname = sensitivityfilename,
                nbbatches=90,
                start_month=1, end_month=12,m_file=matlab_filename,monthprefix=monthprefix)


#%% For the one year Morris


# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20191017_1Year_Morris'
sensitivityfilename= r"Morris_inputs_N_150.csv"
iddfile = r"C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename1=r"Run_Cosim_Batch_1Y_Morris_C1.m"
matlab_filename2=r"Run_Cosim_Batch_1Y_Morris_C2.m"
monthprefix="1Y"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=150,
                sa_fname = sensitivityfilename,
                nbbatches=50,
                start_month=1, end_month=12,m_file1=matlab_filename1,m_file2=matlab_filename2,monthprefix=monthprefix)


#%% For renewd min max

# Input files for 1 year analysis - Min Max
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20191030_1Y_MM'
sensitivityfilename= "InputParams_SA_Min_Max.csv"
iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
matlab_filename1=r"Run_Cosim_Batch_1Y_MM_C1.m"
matlab_filename2=r"Run_Cosim_Batch_1Y_MM_C2.m"
monthprefix="1Y"
modify_IDF_global(input_file_path=input_file_path,
                iddfile=iddfile, 
                nbiterations=18,
                sa_fname = sensitivityfilename,
                nbbatches=18,
                start_month=1, end_month=12,m_file1=matlab_filename1,m_file2=matlab_filename2,monthprefix=monthprefix)




#%% Other code
# Divide 100 iterations into 4 batches, so we can run simulations in parallel.

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


#from EPfileCreator.epfunctions_idealload_v890 import printversion
#printversion("v890")


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
    fname = base_filename+"\\Text_Cosim_Command_line_run_C1.txt"
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
    fname = base_filename1+"\\Text_Cosim_Command_line_run_C2.txt"
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
nbbatches=40
letters_batch = list(itertools.islice(excel_cols(), nbbatches))


# January LHS
base_filename = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20190930_Jan_LHS_400\20190930_Jan_Batch'
f= open("C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190930_Jan_LHS_400/Text_Cosim_Command_line_run.txt","w+")
create_command_file(f,nbbatches, letters_batch,base_filename,monthname="Jan")

# July LHS
base_filename = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20190930_July_LHS_400\20191001_July_Batch'
f= open("C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190930_July_LHS_400/Text_Cosim_Command_line_run.txt","w+")
create_command_file(f,nbbatches, letters_batch,base_filename,monthname="July")


# January Morris
base_filename = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20190913_January_Morris\20190924_Jan_Batch'
f= open("C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190913_January_Morris/Text_Cosim_Command_line_run.txt","w+")
create_command_file(f,nbbatches, letters_batch,base_filename,monthname="Jan")

# July Morris
base_filename = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20190913_July_Morris\20190925_July_Batch'
f= open("C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190913_July_Morris/Text_Cosim_Command_line_run.txt","w+")
create_command_file(f,nbbatches, letters_batch,base_filename,monthname="July")



# 1 YEar param C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190930_ParamChange
base_filename = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20190930_ParamChange'
batchdate = '\\20190930_1Y_Batch'
create_command_file(f,17,base_filename,monthname="1Y")


# 1 YEar param C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190930_ParamChange
base_filename = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20191004_1Year_HeatingChange'
batchdate = '\\20191005_1Y_Batch'
create_command_file(17,base_filename,batchdate,monthname="1Y")

# 1 YEar param C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20190930_ParamChange
base_filename = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20191006_ParamChange_morecrops'
batchdate = '\\20191006_1Y_Batch'
create_command_file(25,base_filename,batchdate,monthname="1Y")


# 1 YEar LHS
base_filename = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20191008_1Year_SRC'
batchdate = '\\20191010_1Y_Batch'
create_command_file(90,base_filename,batchdate,monthname="1Y")

# 1 YEar LHS
base_filename1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20191008_1Year_SRC'
base_filename2 = r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA\20191008_1Year_SRC'

batchdate = '\\20191010_1Y_Batch'
create_command_file_3(90,base_filename1,base_filename2,batchdate,monthname="1Y")


# 1 YEar Morris
base_filename1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20191017_1Year_Morris'
base_filename2 = r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA\20191017_1Year_Morris'

batchdate = '\\20191020_1Y_Batch'
create_command_file(50,base_filename1,batchdate,monthname="1Y")
create_command_file_2(50,base_filename1,base_filename2,batchdate,monthname="1Y")


# 1 YEar MM
base_filename1 = r'C:\Users\mkj32\OneDrive - UIS\SensitivityAnalysis\Global_SA\20191030_1Y_MM'
base_filename2 = r'C:\Users\mkj32\OneDrive - University of Cambridge\SensitivityAnalysis\Global_SA\20191030_1Y_MM'

batchdate = '\\20191030_1Y_Batch'
create_command_file(18,base_filename1,batchdate,monthname="1Y")
create_command_file_2(18,base_filename1,base_filename2,batchdate,monthname="1Y")

#%%# Modify the matlab file in each folder
input_file_path = r'C:/Users/mkj32/OneDrive - UIS/SensitivityAnalysis/Global_SA/20191008_1Year_SRC'
m_file=r"Run_Cosim_Batch_1Y_LHS_comp2.m"


letters_batch = list(itertools.islice(excel_cols(), 90))
import shutil
for batch in letters_batch:
    #print(batch)
    cosim_file_path =  input_file_path +"/CosimulationFiles/"+m_file 
    cosim_new_file_path = base_filename +batchdate+batch + "\\Run_Cosim_Batch_"+batch+"_C3.m"
    
    shutil.copy(cosim_file_path, cosim_new_file_path)

            
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
