# -*- coding: utf-8 -*-
"""
Spyder Editor

This is not a temporary script file.
"""
import csv
import os 
import pandas as pd
from eppy import modeleditor
from eppy.modeleditor import IDF

import eppy.EPlusInterfaceFunctions.parse_idd as parse_idd

import datetime # to add date and time of file created



def create_idf_file(input_file_path,iddfile,nbiterations,
                    pathnameto_eppy = r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Energy Plus'):

    """creates idf based on baseline IDF, and three inputs: file path to baseline
    IDF, pathname to EnergyPlus Package, and nb of iterations to run the simulation 
    i.e. number of simulations based on the uncertainty input file."""

    IDF.setiddname(iddfile)
    
    os.chdir(input_file_path)
    
    idfname_wwr1 = pathnameto_eppy+r'/baseline_mod_WWR_1.idf'
    idfname_wwr2 = pathnameto_eppy+r'/baseline_mod_WWR_2.idf'
    idfname_wwr3 = pathnameto_eppy+r'/baseline_mod_WWR_3.idf'
    
    idf_baseline_wwr = [idfname_wwr1,idfname_wwr2,idfname_wwr3]
    
    
    zonename =  pd.read_csv("zonename.csv")
    allzones =  pd.read_csv("zonetype.csv")
    heatgains = pd.read_csv("heatgains.csv")
    uncertainty = pd.read_csv("uncertainty_NoDaylighting.csv")
    daylighting_refpoints = pd.read_csv("daylightingcontrol_refpoints.csv")
    scheduletime = pd.read_csv("scheduletimes_on_avoiderror.csv") #removed store and toilet equipment schedule as it was already present in basefile
    
    Equipment_sch   = scheduletime[scheduletime.ScheduleType  == "Equipment"]
    Ventilation_sch = scheduletime[scheduletime.ScheduleType  == "Ventilation"]
    Heat_sch        = scheduletime[scheduletime.ScheduleType  == "Heat"]
    
    for runindex, run in uncertainty.head(n=nbiterations).iterrows(): # only run for the first iteration
        wallC, roofC, groundC, Infil = calc_wall_prop(run) # load wall properties from calc_wall_property function
        
        daylighting = run.DaylightingControl
        Schedule = run.schedule
        Boiler = run.BoilerEfficiency
        heating = run.HeatingSP # heating setpoint operative temperature
        ventilation = run.ventilation # 0 means no ventilation while 1 means full ventilation, ventilation schedule only 0 or 1.
        wwr = run.WWR # window wall ratio; wwr 1 means 20, 2 means 40, 3 means 60 only for classroom
        
        ## ..........................IDF FILE BASED ON WWR............................................
        for wwr_test in range(1,4): #creates a dummy value equal to 1, 2 or 3
            if wwr==wwr_test: #checks if the WWR is 1, 2 or 3
                idf1 = IDF(idf_baseline_wwr[wwr_test-1]) # assigns the correct IDF file for the corresponding WWR value
            
            
        ## ..........................MATERIALS.....................................................
        # make four new materials with the specified u values and ratios above
        materials = idf1.idfobjects["MATERIAL"]
        
        for i in range(0,3):
            idf1.newidfobject("MATERIAL") # add three empty materials
        
        for material in materials:
            if material.Name == "":
                material.Roughness     = "MediumRough"
                material.Thickness     = 0.508
                material.Density       = 43
                material.Specific_Heat = 1210
                
        materials[len(materials)-3].Name          = "wall insulation"
        materials[len(materials)-3].Conductivity  = wallC
    
        materials[len(materials)-2].Name          = "ground insulation"
        materials[len(materials)-2].Conductivity  = groundC    
    
        materials[len(materials)-1].Name          = "roof insulation"
        materials[len(materials)-1].Conductivity  = roofC    
        
        # make window glazing:
        windowglazing = idf1.newidfobject("WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM")
        windowglazing.Name                         = "simple window"
        windowglazing.UFactor                      = run.WinU
        windowglazing.Solar_Heat_Gain_Coefficient  = run.WinSHGC
        
        # depending on the type of room, will have different equipment and lighting schedules, but for now will use the ones from heatgains table
    #     if typezone.typecode == 5:
    #     Equipclass = run.EquipmentClass
    #     Equipstaff = run.EquipmentStaff
    #     lightclass = run.LightingClass
    #     lightstaff = run.LightingStaff
    
        ## ..........................INPUT OF CONDITIONAL DAYLIGHTING CONTROLS.....................................................
        # Add branch and branch list information
        ## ..........................INPUT OF CONDITIONAL DAYLIGHTING CONTROLS.....................................................
        # Add branch and branch list information
        if daylighting == 1:
            # Add daylighting control to  idf, conditionally on daylighting being = 1
            for zoneindex, zone in daylighting_refpoints.iterrows():
                print(zoneindex)
                daylighting_control(idf1,zone,zoneindex) # this inputs daylighting control and reference point
                # from the daylighting_controls_on csv file
                
        ## ..........................BOILER PROPERTIES.....................................................
        # Add relevant boiler element
        bhw = idf1.newidfobject("BOILER:HOTWATER")
        bhw.Name                                             = "Boiler1"
        bhw.Fuel_Type                                        = "NaturalGas"
        bhw.Nominal_Capacity                                 = "autosize"
        bhw.Nominal_Thermal_Efficiency                       = Boiler
        bhw.Normalized_Boiler_Efficiency_Curve_Name          = "Boiler1 Efficiency Curve"
        bhw.Design_Water_Outlet_Temperature                  = 81
        bhw.Design_Water_Flow_Rate                           = "autosize" # m3/s
        bhw.Maximum_Part_Load_Ratio                          = 1.1
        bhw.Boiler_Water_Inlet_Node_Name                     = "Boiler1 HW Inlet"
        bhw.Boiler_Water_Outlet_Node_Name                    = "Boiler1 HW Outlet"
        bhw.Water_Outlet_Upper_Temperature_Limit             = 100
        bhw.Boiler_Flow_Mode                                 = "ConstantFlow"
    
        # Boiler and branch properties ..............................................
        branchlist =  idf1.newidfobject("BRANCHLIST")
        branchlist.Name               = "BoilerWater HW Demand Side Branches"
        branchlist.Branch_1_Name      = "BoilerWater HW Demand Inlet Branch"    
        branchlist[branchlist.fieldnames[len(allzones)+3]]       = "BoilerWater HW Demand Bypass Branch"
        branchlist[branchlist.fieldnames[len(allzones)+4]]       = "BoilerWater HW Demand Outlet Branch"    

        connectorsplitter =  idf1.newidfobject("CONNECTOR:SPLITTER")
        connectorsplitter.Name                      = "BoilerWater HW Demand Splitter"
        connectorsplitter.Inlet_Branch_Name         = "BoilerWater HW Demand Inlet Branch"
        connectorsplitter[connectorsplitter.fieldnames[len(allzones)+3]] = "BoilerWater HW Demand Bypass Branch"

        connectormixer =  idf1.newidfobject("CONNECTOR:MIXER")
        connectormixer.Name                     = "BoilerWater HW Demand Mixer"
        connectormixer.Outlet_Branch_Name       = "BoilerWater HW Demand Outlet Branch"        
        connectormixer[connectormixer.fieldnames[len(allzones)+3]]      = "BoilerWater HW Demand Bypass Branch" 

        for k in range(0, len(allzones)):
            branchlist[branchlist.fieldnames[k+3]]               = allzones.zonename[k] + "Baseboard Heat HW Branch"
            connectorsplitter[connectorsplitter.fieldnames[k+3]] = allzones.zonename[k] + "Baseboard Heat HW Branch"
            connectormixer[connectormixer.fieldnames[k+3]]       = allzones.zonename[k] + "Baseboard Heat HW Branch"
       
        ## ..........................ZONE PROPERTIES.....................................................
    
        # Create a for loop with all the info for each zone
        for zoneindex, zone in allzones.iterrows():
            zonename= zone.zonename
            zonetype= zone.type
            typecode= zone.typecode
            for roomindex,hg in heatgains.iterrows():
                zonetype2 = hg.zonetype
                if zonetype ==zonetype2:
                    equip=hg.equipment
                    lighting= hg.lightingW
                    occupancy=hg.occupancy
                    meta=hg.metabolicWPerson
                    latent=hg.LatentGains
                    heating=hg.heating
                    heatingsetback = hg.heatingsetback
                    ventilationrate = hg.ventilation * ventilation / 1000.0 #change unit from l/s to m3/s per person for ventilation
    
                    #schedules:
                    schequip = hg.equipmentSchl
                    schheat= hg.heatSchl
                    schlight= hg.lightSchl
                    schoccu = hg.occupancySchl
                    schventilation = hg.ventilationSchl
    
            #print(zoneindex,zonename, zonetype, typecode, equip,lighting, people,meta,schoccu)
            # Create a new object for the zone:
            idf1.newidfobject("PEOPLE") #everytime you do that you add a new empty material
            idf1.newidfobject("ELECTRICEQUIPMENT") #everytime you do that you add a new empty material
            idf1.newidfobject("LIGHTS") #everytime you do that you add a new empty material
            idf1.newidfobject("ZONEINFILTRATION:DESIGNFLOWRATE") #everytime you do that you add a new empty material
            idf1.newidfobject('ZONEVENTILATION:DESIGNFLOWRATE')
    
            # pop the object out with a given name so that we will be able to assign specific values for each:
            people           = idf1.idfobjects['PEOPLE'][zoneindex]
            lights           = idf1.idfobjects['LIGHTS'][zoneindex]
            elecequip        = idf1.idfobjects['ELECTRICEQUIPMENT'][zoneindex]
            zoneinfildfr     = idf1.idfobjects['ZONEINFILTRATION:DESIGNFLOWRATE'][zoneindex]
            zoneventdfr      = idf1.idfobjects['ZONEVENTILATION:DESIGNFLOWRATE'][zoneindex]
    
            # people:
            people[people.fieldnames[1]] = "Occu" +  zonename #name
            people[people.fieldnames[2]] = zonename # Zone or ZoneList Name"
            people[people.fieldnames[3]] = schoccu
            people[people.fieldnames[4]] = "People/Area"
            people[people.fieldnames[6]] = occupancy #People per Zone Floor Area
            people[people.fieldnames[8]] = latent # Fraction Radiant 
            people[people.fieldnames[9]] = "autocalculate" # sensible heat fraction
            people[people.fieldnames[10]] = zonetype +  "activity" # activity level schedule name
    
            # zone infiltration rate:
            zoneinfildfr[zoneinfildfr.fieldnames[1]] = zonename + "infiltration"
            zoneinfildfr[zoneinfildfr.fieldnames[2]] = zonename # Zone or ZoneList Name
            zoneinfildfr[zoneinfildfr.fieldnames[3]] = "INFIL_SCH" # Schedule Name
            zoneinfildfr[zoneinfildfr.fieldnames[4]] = "AirChanges/Hour" #Design Flow Rate Calculation Method
            zoneinfildfr[zoneinfildfr.fieldnames[8]] = 3 # Air Changes per Hour
    
            # lights:
            lights.Name                             = zonename + "light"
            lights.Zone_or_ZoneList_Name            = zonename
            lights.Schedule_Name                    = schlight
            lights.Design_Level_Calculation_Method  = "Watts/Area"
            lights.Watts_per_Zone_Floor_Area        = lighting
            lights.Fraction_Radiant                 = 0.42
            lights.Fraction_Visible                 = 0.18
    
             # elecequip:
            elecequip.Name                             = zonename + "equip"
            elecequip.Zone_or_ZoneList_Name             = zonename
            elecequip.Schedule_Name                    = schequip
            elecequip.Design_Level_Calculation_Method  = "Watts/Area"
            elecequip.Watts_per_Zone_Floor_Area        = equip
            elecequip.Fraction_Latent                  = 0
            elecequip.Fraction_Radiant                 = 0.5
    
            # VENETILATION DESIGN FLOW RATE
            zoneventdfr.Name                                 = zonename + "ventilation"
            zoneventdfr.Zone_or_ZoneList_Name                = zonename
            zoneventdfr.Schedule_Name                        = schventilation
            zoneventdfr.Design_Flow_Rate_Calculation_Method  = "Flow/Person"
            zoneventdfr.Flow_Rate_per_Person                 = ventilationrate
    
            create_sizing_hvac_objects(idf1, zone) # inputs objects for zone sizing and boiling properties,
            # defined in the function create_sizing_objects
    
            # Water use equipment ...........................
            WUE =  idf1.newidfobject("WATERUSE:EQUIPMENT")
            WUE.Name =  zonename + "DHW"
            WUE.EndUse_Subcategory = "DHW_default"
            WUE.Peak_Flow_Rate = zone.waterflow
            WUE.Flow_Rate_Fraction_Schedule_Name = schoccu
            WUE.Target_Temperature_Schedule_Name = "SHW_default Temp Sched"
            WUE.Hot_Water_Supply_Temperature_Schedule_Name = "Hot Supply Temp Sched"
            WUE.Zone_Name = zonename
            
        # .......................... SCHEDULES FOR EQUIPMENT, LIGHTING, VENTILATION ----------------------
    # Create a for loop to populate schedules for ventilation, heat and equipment. You can change the schedule using the csv file
    # called scheduletimes_on
        schedules_all=idf1.idfobjects['SCHEDULE:COMPACT']
    
        for sch_index, schtype in Equipment_sch.iterrows():
            create_simple_schedule(idf1,schedules_all, schtype, "Fraction")
    
        for sch_index, schtype in Heat_sch.iterrows():
            create_simple_schedule(idf1,schedules_all, schtype, "Temperature")
    
        # .......................... THERMOSTAT FOR HEATING ----------------------
    
        # This for loop creates a Thermostat set point for each Type of Zone (but must not iterate through each zone)
        for roomindex,hg in heatgains.iterrows():
            thermostatsetpoint = idf1.newidfobject("THERMOSTATSETPOINT:SINGLEHEATING")
            thermostatsetpoint.Name = hg.zonetype + "_Heat"
            thermostatsetpoint.Setpoint_Temperature_Schedule_Name = "SecSchl_" + hg.schedulename + "_Heat"
    
        
        # Add to csv file the run number
        print("run=",run.number)
        # Create a new folder for the date so that they can be saved in a clean way
        now = datetime.datetime.now()
        newpath = r"C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Code/" + now.strftime('%Y%m%d')
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        os.chdir(newpath)
        filename = str(now)[:10] + "_school_run_%d.idf" % run.number
        idf1.saveas(filename)
    
        print(filename)



def calc_wall_prop(run):
    """ calculates wall properties from the uncertainty_final inputs csv file"""
    Uwall = run.WallU
    wallC = 0.1422 * Uwall * Uwall * Uwall - 0.1827 * Uwall * Uwall + 0.151 * Uwall - 0.0128
    Uroof = run.RoofU
    roofC = 0.1422 * Uroof * Uroof * Uroof - 0.1827 * Uroof * Uroof + 0.151 * Uroof - 0.0128
    Uground = run.GroundU
    groundC = 0.0073 * Uground * Uground + 0.0489 * Uground + 0.0005
    Infil = run.infiltration
    return wallC, roofC, groundC, Infil

def daylighting_control(idf1, zone, zoneindex):
    idf1.newidfobject("DAYLIGHTING:CONTROLS") #everytime you loop through a zone, you add a new daylighting object
    daylightingcontrol           = idf1.idfobjects['DAYLIGHTING:CONTROLS'][zoneindex]
    daylightingcontrol.Name      = "Daylightingcontrol" + zone.zonename
    daylightingcontrol.Zone_Name = zone.zonename
    daylightingcontrol.Glare_Calculation_Daylighting_Reference_Point_Name = zone.Name_RefPoint_1
    daylightingcontrol.Daylighting_Reference_Point_1_Name = zone.Name_RefPoint_1
    daylightingcontrol.Fraction_of_Zone_Controlled_by_Reference_Point_1 = zone.Fraction_1
    daylightingcontrol.Illuminance_Setpoint_at_Reference_Point_1 = zone.Illum_1
    daylightingcontrol.Daylighting_Reference_Point_2_Name = zone.Name_RefPoint_2
    daylightingcontrol.Fraction_of_Zone_Controlled_by_Reference_Point_2 = zone.Fraction_1
    daylightingcontrol.Illuminance_Setpoint_at_Reference_Point_2 = zone.Illum_1
    for j in range(20,44):
        daylightingcontrol[daylightingcontrol.fieldnames[j]]=""
        
    daylightingrefpoint1   = idf1.newidfobject("DAYLIGHTING:REFERENCEPOINT") #everytime you loop through a zone, you add a new daylighting object
    daylightingrefpoint1.Name = zone.Name_RefPoint_1
    daylightingrefpoint1.Zone_Name = zone.zonename    
    daylightingrefpoint1.XCoordinate_of_Reference_Point = zone.X_1
    daylightingrefpoint1.YCoordinate_of_Reference_Point = zone.Y_1
    daylightingrefpoint1.ZCoordinate_of_Reference_Point = zone.Z_1

    daylightingrefpoint2   =idf1.newidfobject("DAYLIGHTING:REFERENCEPOINT") #everytime you loop through a zone, you add a new daylighting object
    daylightingrefpoint2.Name = zone.Name_RefPoint_2
    daylightingrefpoint2.Zone_Name = zone.zonename    
    daylightingrefpoint2.XCoordinate_of_Reference_Point = zone.X_2
    daylightingrefpoint2.YCoordinate_of_Reference_Point = zone.Y_2
    daylightingrefpoint2.ZCoordinate_of_Reference_Point = zone.Z_2
    
def create_simple_schedule(idf1,schedules_all, schtype,type_limit_name):
    idf1.newidfobject('SCHEDULE:COMPACT')
    schedules = idf1.idfobjects['SCHEDULE:COMPACT'][len(schedules_all)-1]
    schedules.Name = schtype.SecSchl
    schedules.Schedule_Type_Limits_Name = type_limit_name
    schedules.Field_1 = "Through: 12/31"
    # First schedule Through Period
    schedules.Field_2 = "For: "+ schtype.For_1
    schedules.Field_3 = "Until: "+ schtype.TimeOn
    schedules.Field_4 = schtype.ValueOff_1
    schedules.Field_5 = "Until: "+ schtype.TimeOff
    schedules.Field_6 = schtype.ValueOn_1
    schedules.Field_7 = "Until: 24:00" 
    schedules.Field_8 = schtype.ValueOff_1
    # Second schedule Through Period
    schedules.Field_9  = "For: "+ schtype.For_2
    schedules.Field_10 = "Until: "+ schtype.TimeOn
    schedules.Field_11 = schtype.ValueOff_2
    schedules.Field_12 = "Until: "+ schtype.TimeOff
    schedules.Field_13 = schtype.ValueOn_2
    schedules.Field_14 = "Until: 24:00" 
    schedules.Field_15 = schtype.ValueOff_2
    # Last schedule Through Period (all other days)
    schedules.Field_16 = "For: "+ schtype.For_OtherDays
    schedules.Field_17 = "Until: 24:00"
    schedules.Field_18 = schtype.ValueOtherDays
    
def create_sizing_hvac_objects(idf1, zone):
    """creates sizing and hvac components based on the indicated zone"""
    zonename = zone.zonename
    zonetype= zone.type
# .......................... SIZING AND BOILER PROPERTIES///// HVAC ----------------------
    SizingZone =  idf1.newidfobject("SIZING:ZONE")
    SizingZone.Zone_or_ZoneList_Name = zonename
    SizingZone.Zone_Cooling_Design_Supply_Air_Temperature = 12.8
    SizingZone.Zone_Heating_Design_Supply_Air_Temperature = 50

    SizingZone.Zone_Cooling_Design_Supply_Air_Humidity_Ratio = 0.008
    SizingZone.Zone_Heating_Design_Supply_Air_Humidity_Ratio = 0.008
    SizingZone.Design_Specification_Outdoor_Air_Object_Name = "OutdoorAir_Allzones"

    SizingZone.Cooling_Design_Air_Flow_Method     = "Flow/Zone"
    SizingZone.Cooling_Design_Air_Flow_Rate       = 0.001
    SizingZone.Cooling_Minimum_Air_Flow_Fraction  = 0

    SizingZone.Heating_Design_Air_Flow_Method    = "Flow/Zone"
    SizingZone.Heating_Design_Air_Flow_Rate      = 0.001
    SizingZone.Heating_Maximum_Air_Flow_Fraction = 0

    ZoneControl_Thermo =  idf1.newidfobject("ZONECONTROL:THERMOSTAT")
    ZoneControl_Thermo.Name                       = zonename + "Control"
    ZoneControl_Thermo.Zone_or_ZoneList_Name      = zonename
    ZoneControl_Thermo.Control_Type_Schedule_Name = "Zone Control Type Sched"
    ZoneControl_Thermo.Control_1_Object_Type      = "ThermostatSetpoint:SingleHeating"
    ZoneControl_Thermo.Control_1_Name             = zonetype + "_Heat"

    ZoneControl_Thermo_OpT =  idf1.newidfobject("ZONECONTROL:THERMOSTAT:OPERATIVETEMPERATURE")
    ZoneControl_Thermo_OpT.Thermostat_Name               = zonename + "Control"
    ZoneControl_Thermo_OpT.Radiative_Fraction_Input_Mode = "Constant"
    ZoneControl_Thermo_OpT.Fixed_Radiative_Fraction      = 0.5

    ZoneHVAC_Baseboard =  idf1.newidfobject("ZONEHVAC:BASEBOARD:CONVECTIVE:WATER")
    ZoneHVAC_Baseboard.Name                       = zonename + "Baseboard Heat"
    ZoneHVAC_Baseboard.Availability_Schedule_Name = "HVACTemplate-Always 1"
    ZoneHVAC_Baseboard.Inlet_Node_Name            = zonename + "Baseboard HW Inlet"
    ZoneHVAC_Baseboard.Outlet_Node_Name           = zonename + "Baseboard HW Outlet"
    ZoneHVAC_Baseboard.UFactor_Times_Area_Value   = "autosize"
    ZoneHVAC_Baseboard.Maximum_Water_Flow_Rate    = "autosize"

    ZoneHVAC_EqList =  idf1.newidfobject("ZONEHVAC:EQUIPMENTLIST")
    ZoneHVAC_EqList.Name = zonename + "Equipment"
    ZoneHVAC_EqList.Zone_Equipment_1_Object_Type = "ZoneHVAC:Baseboard:Convective:Water"
    ZoneHVAC_EqList.Zone_Equipment_1_Name = zonename + "Baseboard Heat"
    ZoneHVAC_EqList.Zone_Equipment_1_Cooling_Sequence = 1
    ZoneHVAC_EqList.Zone_Equipment_1_Heating_or_NoLoad_Sequence = 1

    ZoneHVAC_EqConnections =  idf1.newidfobject("ZONEHVAC:EQUIPMENTCONNECTIONS")
    ZoneHVAC_EqConnections.Zone_Name  = zonename 
    ZoneHVAC_EqConnections.Zone_Conditioning_Equipment_List_Name  = zonename + "Equipment"
    #ZoneHVAC_EqConnections.Zone_Air_Inlet_Node_or_NodeList_Name   = zonename + "Baseboard HW Inlet"
    ZoneHVAC_EqConnections.Zone_Air_Node_Name                     = zonename + "Zone Air Node"
    #ZoneHVAC_EqConnections.Zone_Return_Air_Node_or_NodeList_Name  = zonename + "Baseboard HW Outlet"

    baseboardbranch =  idf1.newidfobject("BRANCH")
    baseboardbranch.Name                         = zonename + "Baseboard Heat HW Branch"
    baseboardbranch.Component_1_Object_Type      = "ZoneHVAC:Baseboard:Convective:Water"
    baseboardbranch.Component_1_Name             = zonename + "Baseboard Heat"
    baseboardbranch.Component_1_Inlet_Node_Name  = zonename + "Baseboard HW Inlet"
    baseboardbranch.Component_1_Outlet_Node_Name = zonename + "Baseboard HW Outlet"

if __name__ == '__main__':
    input_file_path = r'C:/Users/mkj32/Documents/2016-2019 PhD/School Theoretical/Code'
    iddfile = "C:/EnergyPlusV8-9-0/iddfiles/Energy+V8-9-1.idd"
    create_idf_file(input_file_path,iddfile)