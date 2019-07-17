# EPfileCreator
Creates Energy Plus files for input into greenhouse energy simulator


This set of files uses mostly the eppy package to create input files for EnergyPlus.

The functions allow an iterative way to add similar attributes across different zones by iterating through a list of zones, as well as through an uncertainty spreadsheet where parameters can vary (e.g. air change per hour).

The sensitiviy analysis functions allow to create several IDF files with different parameters according to the variables desired to be studied.
The functions are written specifically for my application and need to be modified if the user has different zones, or wishes to analyse different sensitivity parameters.

I recommend looking at the eppy help available here: https://pythonhosted.org/eppy/Main_Tutorial.html for more information on how to access different substructures within an idf file.

The examples folder contains the files used to call the functions created. In this way, the user could run several IDF simulations and save the outputs in Python.

