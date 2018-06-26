# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 16:26:03 2017

@author: tdramm

O1_PROTECT_RDM.py -     The script...                  
                        
                   
"""

###############################################################################
# IMPORT PACKAGES
# Import arcpy module
import arcpy 
# Pandas module used for importing csv as data frame and making float data type
import pandas as pd
# For TableToNumPyArray used with raster data
import numpy as np
# Import math package for 'exp' function (extreme sea levels)
#import math
# Import time package
import time
# Import MatPlotLib package
#import matplotlib.pyplot as plt
# Import datetime package
import datetime

## Set up the date. Useful for adding date to csv file names with results
date_list = []
today = datetime.date.today()
date_list.append(today)
date_string = str(date_list[0])
#date_string = today.strftime('%Y'+"_"+'%m'+"_"+'%d')
print "Trial run for " + date_string

###############################################################################
# SET UP LICENSES AND WORKING ENVIRONMENT
# Check ArcGIS out license
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension("3D")
# Set Geoprocessing overwrite option
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = "C:\\Users\\tdramm\\Desktop\\GIS_LE\\ScratchCaseTwo.gbd"
arcpy.env.workspace = "C:\\Users\\tdramm\\Desktop\\GIS_LE\\CaseTwo.gdb"
# Set raster snapping"
arcpy.env.snapRaster = "C:\\Users\\tdramm\\Desktop\\GIS_LE\\CaseTwo.gdb\\AOI_dem1m"
# Set Geoprocessing environments for analysis (Left, Bottom, Right, Top)
# Same extent as AOI_dem1m; coordinate systems same as inputs by default; coordinates as Xmin, Ymin, Xmax, Ymax
arcpy.env.extent = "584953 5805832 590779 5808569"
# Make cell size 1m to speed up processing (make 2m if too slow to process)
arcpy.env.cellSize = "1"
arcpy.env.mask = ""

###############################################################################
# SET-UP TIMER FOR CODE - START CLOCK
t0 = time.clock()   # Starts clock times

###############################################################################
# CONSTANT VALUES
CONDITION_TRUE = "1"
#MHHW 0.433m above AHD in study area
MHHW_ADJUST = "0.433" #Ref BOM Email (Bullock Island) [MSL = 0.085mAHD; MHHW = 0.433mAHD)] 

max_car_depth = "0.15"

# Define input path and output path to geodatabase
inpath = "C:\\Users\\tdramm\\Desktop\\GIS_LE\\CaseTwo.gdb\\"
outpath = inpath

Area_of_Interest = inpath + "AOI_box"

# Define local variables
AOI_dem1m = inpath + "AOI_dem1m"
Esp_Hwy = inpath + "Esp_Hwy"
MHHW_dem1m = "MHHW_dem1m"
slr_surface = "slr_surface"
slr_surf_mhhw = "slr_surf_mhhw"
slr_extent = "slr_extent"
slr_ext_con = "slr_ext_con"
slrgroup = "slrgroup"
slr_poly = "slr_poly"
max_slr_poly = "max_slr_poly"
diffslr = "diffslr"
slrdepth = "slrdepth"
rd_flood_seg = "rd_flood_seg"
roads = "roads"
roads_sel = inpath + "road_select"
sealedroad = "sealedroad"
sealed = "sealed"
LessThan0_15 = "LessThan0_15"
rd_dep_con = "rd_dep_con"
rd_dep_poly = "rd_dep_poly"
bld_area_mer = inpath + "Bld_area_mer"

###############################################################################
# CONVERT DEM DATA FROM AHD (Australian Height Datum) to MHHW (Mean Higher High Water) LEVEL
# Source = [TBA] MHHW = 0.668m AHD (assumed - TBC)
# Process: Minus (Clean DEM data - convert from AHD to MHHW)1
#arcpy.gp.Minus_sa(AOI_dem1m, MHHW_ADJUST, MHHW_dem1m)

###############################################################################
# IMPORT CASES GENERATED USING LHS
#Alternative is to import csv file as a dataframe
#Refer LE_RDM_Analysis.R script
cases = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\2018-02-28_5000Case_Generation.csv')
cases.head()

## Define prior values for key factors
cases = cases[0:1]    #Note [31:32] a good one to test
cases

###############################################################################
# SET UP UNCERTAIN FACTORS  CASE FACTORS
## https://www.python.org/dev/peps/pep-0008/#global-variable-names
## Function and global variable names should be lowercase, with words seperated by underscore
## Constants written in CAPTIAL_LETTERS_SEPERATED_WITH_UNDERSCORES

## Baseline lake levels mAHD (Grayson et al., 2004)
AEP_PT_ONE_BL = 2.2
AEP_PT_TWO_BL = 2.1
AEP_PT_FIVE_BL = 2.0
AEP_ONE_BL = 1.8
AEP_TWO_BL = 1.6
AEP_FIVE_BL = 1.3
AEP_TEN_BL = 1.2
AEP_TWENTY_BL = 1.05
AEP_FORTY_BL = 0.9
AEP_SIXTY_BL = 0.85
AEP_NINETY_BL = 0.77 #Note impacts to propoerties with floor level up to 0.5m above this (see D.I. lookup table)
MHHW_BULLOCK_IS = 0.43 # MHHW for Bullock Island

#BL_AAD_risk = 1000000    #Assume this is the tolerable risk TO BE CONFIRMED
#m_str_bl = 1820         #TO BE CONFIRMED
#m_con_bl = 140          #TO BE CONFIRMED

# Plot - References: https://matplotlib.org/users/pyplot_tutorial.html
#plt.plot((0.1,0.2,0.5,1,2,5,10,20),(AEP_PT_ONE_BL,AEP_PT_TWO_BL,AEP_PT_FIVE_BL,AEP_ONE_BL,AEP_TWO_BL,AEP_FIVE_BL,AEP_TEN_BL,AEP_TWENTY_BL ),'bs')
#plt.plot((0.1,0.2,0.5,1,2,5,10,20),(AEP_PT_ONE_BL,AEP_PT_TWO_BL,AEP_PT_FIVE_BL,AEP_ONE_BL,AEP_TWO_BL,AEP_FIVE_BL,AEP_TEN_BL,AEP_TWENTY_BL ))
#plt.xlabel('AEP(%)')
#plt.ylabel('Lake water level (m AHD)')
#plt.title('AEP vs Lake Water Level at Lakes Entrance')
#plt.axis([0,20,0,2.5])  # define x-axis range (0 to 20) and y-axis range (0 to 2.5)
#plt.grid(True)

## Bring in structural damage and contents damage lookup tables
vuln_model_str = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\Vulnerability_Models\\Lookup\\GA_vuln_structural.csv')
vuln_model_con = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\Vulnerability_Models\\Lookup\\GA_vuln_contents.csv')
aape_lookup = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\2018-03-02 AAPE_Lookup.csv')

###############################################################################
## Define before looping through
## Lists to be appended to cases dataframe
#RDM_SLR = []
#RDM_APOLY = []
#RDM_BPOLY = []
#RDM_CPOLY = []
#RDM_CSTAR = []
#RDM_TSTAR = []
#RDM_RSEA = []
#RDM_DI = []
#RDM_STR = []    #+/- 10%
#RDM_CON = []    #+/- 10%
#RDM_SLR_PROJ = []
#RDM_RSTR = []
#RDM_RCON = []
#RDM_R = []
#RDM_RNET_S = []     # Net (r - r_str) / (1 + r_str)
#RDM_RNET_C = []     # Net (r - r_con) / (1 + r_con)
#RDM_TLEADA = []
#RDM_LCAPA = []
#RDM_MOPA = []
#RDM_PLIFEA = []
CASE = []
#YYYY = []
#SIGNPOST =[]
#NPV_A = []
#SIGN_A =[]

###############################################################################
# STRESS TEST THE EXISTING SYSTEM (SENSITIVITIES TO UNCERTAIN FACTORS)

# Set up to save figure
#fig = plt.figure()


AEP_PT_ONE_IMP = []
AEP_PT_TWO_IMP = []
AEP_PT_FIVE_IMP = []
AEP_ONE_IMP = []
AEP_TWO_IMP = []
AEP_FIVE_IMP = []
AEP_TEN_IMP = []
AEP_TWENTY_IMP = []
AEP_FORTY_IMP = []
AEP_SIXTY_IMP = []
AEP_NINETY_IMP = []

NO_HOUSES_PT_ONE = []
NO_HOUSES_PT_TWO = []
NO_HOUSES_PT_FIVE = []
NO_HOUSES_ONE = []
NO_HOUSES_TWO = []
NO_HOUSES_FIVE = []
NO_HOUSES_TEN = []
NO_HOUSES_TWENTY = []
NO_HOUSES_FORTY = []
NO_HOUSES_SIXTY = []
NO_HOUSES_NINETY = []

SUM_HOUSES_PT_ONE = []
SUM_HOUSES_PT_TWO = []
SUM_HOUSES_PT_FIVE = []
SUM_HOUSES_ONE = []
SUM_HOUSES_TWO = []
SUM_HOUSES_FIVE = []
SUM_HOUSES_TEN = []
SUM_HOUSES_TWENTY = []
SUM_HOUSES_FORTY = []
SUM_HOUSES_SIXTY = []
SUM_HOUSES_NINETY = []

NO_PPL_PT_ONE = []
NO_PPL_PT_TWO = []
NO_PPL_PT_FIVE = []
NO_PPL_ONE = []
NO_PPL_TWO = []
NO_PPL_FIVE = []
NO_PPL_TEN = []
NO_PPL_TWENTY = []
NO_PPL_FORTY = []
NO_PPL_SIXTY = []
NO_PPL_NINETY = []

SUM_PPL_PT_ONE = []
SUM_PPL_PT_TWO = []
SUM_PPL_PT_FIVE = []
SUM_PPL_ONE = []
SUM_PPL_TWO = []
SUM_PPL_FIVE = []
SUM_PPL_TEN = []
SUM_PPL_TWENTY = []
SUM_PPL_FORTY = []
SUM_PPL_SIXTY = []
SUM_PPL_NINETY = []

Road_length_SLR = []

AAD = []
AAPE = []

for index, i in cases.iterrows():
    slr = i['slr']
    r_sea = i['r_sea']                  # Sea-level response factor
    m_str = i['m_str']                  # shift in maximum structural damage to building fabric (%)
    m_con = i['m_con']                  # shift in maximum contents damage (%)
    a_ppl = i['a_ppl']                  # % change in average people per dwelling (pp/dwelling)
    d_i = i['d_i']                      # damage index shift at 10cm inundation
    case = i['Case']                    # case number
    
#    slr = 0            #BASELINE    
#    r_sea = 0.9           #BASELINE
#    m_str = 0           #BASELINE
#    m_con = 0           #BASELINE
#    a_ppl = 0           #BASELINE
#    d_i = 0             #BASELINE

   
    print "-------------------------------------"    
    print "Case " +str(case)+":"
    print "Sea level rise = " +str(slr) +"m"
    print "Sea level response factor = " +str(r_sea)    
    print "Change in maximum structural replacement values = " +str(m_str) +" (decimal %)"
    print "Change in maximum contents replacement values (residential) = " +str(m_con) +" (decimal %)"   
    print "Change in average people per dwelling = " +str(a_ppl) +" (decimal %)"    
    print "Damage index uncertainty adjustment = " +str(d_i) +" (decimal %)"       
    print "-------------------------------------"    

###############################################################################
## 4. Analyse impacts for each year in the realisation
    
    ## Create dataframe of propoerty stock and key charactersitics
    ## Lists to be appended to annual_MSL dataframe    
    prop_impact = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\Property_Stock_19Feb.csv')
#    prop_impact = prop_impact[0:5]     # For troubleshooting    
#    prop_impact
#    prop_impact['FLR_LVL_2'] = prop_impact['EST_FLR_LVL_R']
    prop_impact['sample'] = 'Y'
    prop_impact.head()
 
##############################################################     
##############################################################
    # DON'T SAMPLE HOUSES IN ZONE 4
    # Create a subset of the proporty database with zone 4 only            
    prop_imp_sub = pd.DataFrame(prop_impact.loc[prop_impact['ZONE']== 'Zone4'])
    sample2 = []
    # Assign new values to the 'sample' column
    for index, i in prop_imp_sub.iterrows():           
        if i['BLD_TYPE'] == 'Residential':
            Count = 'N'
        else:
            Count = 'Y'
        sample2.append(Count)
    prop_imp_sub['samp2'] = sample2
    prop_imp_sub.head()
    # Replace the value in the original dataset 
    for index, j in prop_imp_sub.iterrows():          
        ID = int(j['Arc_ID'])            
        New_sample = prop_imp_sub.loc[prop_imp_sub['Arc_ID'] == ID, 'samp2']         
        prop_impact.loc[prop_impact['Arc_ID'] == ID, 'sample'] = New_sample
#    #Check        
#    prop_impact[850:950]
#    Check1 = ("C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\"+date_string+"_Check_prop_impact.csv")
#    prop_impact.to_csv(Check1) 
    # Only select values to be sampled
    prop_impact = prop_impact.loc[prop_impact['sample'] == 'Y']       
    len(prop_impact)    #Length of the subset
##############################################################       
##############################################################     
 
    # Add the adjusted AEP levels
    prop_impact['0.1%_AEP'] = slr*r_sea + AEP_PT_ONE_BL
    prop_impact['0.2%_AEP'] = slr*r_sea + AEP_PT_TWO_BL
    prop_impact['0.5%_AEP'] = slr*r_sea + AEP_PT_FIVE_BL
    prop_impact['1%_AEP'] = slr*r_sea + AEP_ONE_BL
    prop_impact['2%_AEP'] = slr*r_sea + AEP_TWO_BL
    prop_impact['5%_AEP'] = slr*r_sea + AEP_FIVE_BL
    prop_impact['10%_AEP'] = slr*r_sea + AEP_TEN_BL
    prop_impact['20%_AEP'] = slr*r_sea + AEP_TWENTY_BL
    prop_impact['40%_AEP'] = slr*r_sea + AEP_FORTY_BL
    prop_impact['60%_AEP'] = slr*r_sea + AEP_SIXTY_BL
    prop_impact['90%_AEP'] = slr*r_sea + AEP_NINETY_BL   
    prop_impact
      
    FLD_DEP_PT_ONE = []
    FLD_DEP_PT_TWO = []
    FLD_DEP_PT_FIVE = []
    FLD_DEP_ONE = []
    FLD_DEP_TWO = []
    FLD_DEP_FIVE = []
    FLD_DEP_TEN = []
    FLD_DEP_TWENTY = []
    FLD_DEP_FORTY = []
    FLD_DEP_SIXTY = []
    FLD_DEP_NINETY = []
    
    DI_STR_PT_ONE = []
    DI_STR_PT_TWO = []
    DI_STR_PT_FIVE = []
    DI_STR_ONE = []
    DI_STR_TWO = []
    DI_STR_FIVE = []
    DI_STR_TEN = []
    DI_STR_TWENTY = []
    DI_STR_FORTY = []
    DI_STR_SIXTY = []
    DI_STR_NINETY = []
    
    DI_CON_PT_ONE = []
    DI_CON_PT_TWO = []
    DI_CON_PT_FIVE = []
    DI_CON_ONE = []
    DI_CON_TWO = []
    DI_CON_FIVE = []
    DI_CON_TEN = []
    DI_CON_TWENTY = []
    DI_CON_FORTY = []
    DI_CON_SIXTY = []
    DI_CON_NINETY = []    
    
    STR_DAM_PT_ONE = []
    STR_DAM_PT_TWO = []
    STR_DAM_PT_FIVE = []
    STR_DAM_ONE = []
    STR_DAM_TWO = []
    STR_DAM_FIVE = []
    STR_DAM_TEN = []
    STR_DAM_TWENTY = []
    STR_DAM_FORTY = []
    STR_DAM_SIXTY = []
    STR_DAM_NINETY = []    
    
    CON_DAM_PT_ONE = []
    CON_DAM_PT_TWO = []
    CON_DAM_PT_FIVE = []
    CON_DAM_ONE = []
    CON_DAM_TWO = []
    CON_DAM_FIVE = []
    CON_DAM_TEN = []
    CON_DAM_TWENTY = []
    CON_DAM_FORTY = []
    CON_DAM_SIXTY = []
    CON_DAM_NINETY = []
    
    TOTAL_DAM_PT_ONE = []
    TOTAL_DAM_PT_TWO = []
    TOTAL_DAM_PT_FIVE = []
    TOTAL_DAM_ONE = []
    TOTAL_DAM_TWO = []
    TOTAL_DAM_FIVE = []
    TOTAL_DAM_TEN = []
    TOTAL_DAM_TWENTY = []
    TOTAL_DAM_FORTY = []
    TOTAL_DAM_SIXTY = []
    TOTAL_DAM_NINETY = []

    NO_HOUSES_PT_ONE = []
    NO_HOUSES_PT_TWO = []
    NO_HOUSES_PT_FIVE = []
    NO_HOUSES_ONE = []
    NO_HOUSES_TWO = []
    NO_HOUSES_FIVE = []    
    NO_HOUSES_TEN = []
    NO_HOUSES_TWENTY = []
    NO_HOUSES_FORTY = []
    NO_HOUSES_SIXTY = []
    NO_HOUSES_NINETY = []
    
    NO_PPL_PT_ONE = []
    NO_PPL_PT_TWO = []
    NO_PPL_PT_FIVE = []
    NO_PPL_ONE = []
    NO_PPL_TWO = []
    NO_PPL_FIVE = []
    NO_PPL_TEN = []
    NO_PPL_TWENTY = []
    NO_PPL_FORTY = []
    NO_PPL_SIXTY = []
    NO_PPL_NINETY = []

#    prop_impact['0.1%_AEP'] = i['aep_pt_one']
#    prop_impact['0.2%_AEP'] = i['aep_pt_two']    
#    prop_impact['0.5%_AEP'] = i['aep_pt_five']
#    prop_impact['1%_AEP'] = i['aep_one']
#    prop_impact['2%_AEP'] = i['aep_two']
#    prop_impact['5%_AEP'] = i['aep_five']
#    prop_impact['10%_AEP'] = i['aep_ten']
#    prop_impact['20%_AEP'] = i['aep_twenty']    
#    prop_impact
            
       # Iterate through the rows in the propoerty stock database to assess 
       # impacts for a given realisation
    for index, k in prop_impact.iterrows():     
        
        crest = 2.5 # Add in crest height (mAHD) for 1:200 year flood + 30cm freeboard + 20cm sea level rise
        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['0.1%_AEP'] < crest: # conditions
            damage_index_str_pt_one = 0
            damage_index_con_pt_one = 0
        else:
            flood_depth_pt_one = round(k['0.1%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_PT_ONE.append(flood_depth_pt_one)
            if flood_depth_pt_one < -0.5:
                damage_index_str_pt_one = 0
                damage_index_con_pt_one = 0
            else:
                damage_index_str_pt_one = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_pt_one,k['VULN_MODEL']]) + d_i
                damage_index_con_pt_one = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_pt_one,k['VULN_MODEL']]) + d_i
            damage_index_str_pt_one = np.clip(damage_index_str_pt_one, 0, 1)
            damage_index_con_pt_one = np.clip(damage_index_con_pt_one, 0, 1)
        DI_STR_PT_ONE.append(damage_index_str_pt_one)
        str_damage_pt_one = damage_index_str_pt_one * k['REP_VAL_2']*(1+m_str)
        STR_DAM_PT_ONE.append(str_damage_pt_one)
        DI_CON_PT_ONE.append(damage_index_con_pt_one)
        con_damage_pt_one = damage_index_con_pt_one * k['CON_VAL']*(1+m_con)
        CON_DAM_PT_ONE.append(con_damage_pt_one)
        total_value_pt_one = str_damage_pt_one + con_damage_pt_one
        TOTAL_DAM_PT_ONE.append(total_value_pt_one)
        if k['EST_FLR_LVL_R'] < k['0.1%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_PT_ONE.append(House_flood)       
     #   NO_PPL_PT_ONE.append(People)        
       
        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['0.2%_AEP'] < crest:
            damage_index_str_pt_two = 0
            damage_index_con_pt_two = 0        
        else:
            flood_depth_pt_two = round(k['0.2%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_PT_TWO.append(flood_depth_pt_two)
            if flood_depth_pt_two < -0.5:
                damage_index_str_pt_two = 0
                damage_index_con_pt_two = 0
            else:
                damage_index_str_pt_two = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_pt_two,k['VULN_MODEL']]) + d_i
                damage_index_con_pt_two = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_pt_two,k['VULN_MODEL']]) + d_i
            damage_index_str_pt_two = np.clip(damage_index_str_pt_two, 0, 1)
            damage_index_con_pt_two = np.clip(damage_index_con_pt_two, 0, 1)
        DI_STR_PT_TWO.append(damage_index_str_pt_two)
        str_damage_pt_two = damage_index_str_pt_two * k['REP_VAL_2']*(1+m_str)
        STR_DAM_PT_TWO.append(str_damage_pt_two)
        DI_CON_PT_TWO.append(damage_index_con_pt_two)
        con_damage_pt_two = damage_index_con_pt_two * k['CON_VAL']*(1+m_con)
        CON_DAM_PT_TWO.append(con_damage_pt_two)
        total_value_pt_two = str_damage_pt_two + con_damage_pt_two
        TOTAL_DAM_PT_TWO.append(total_value_pt_two)
        if k['EST_FLR_LVL_R'] < k['0.2%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_PT_TWO.append(House_flood)
#        NO_PPL_PT_TWO.append(People)
        
        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['0.5%_AEP'] < crest:
            damage_index_str_pt_five = 0
            damage_index_con_pt_five = 0      
        else:
            flood_depth_pt_five = round(k['0.5%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_PT_FIVE.append(flood_depth_pt_five)
            if flood_depth_pt_five < -0.5:
                damage_index_str_pt_five = 0
                damage_index_con_pt_five = 0
            else:
                damage_index_str_pt_five = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_pt_five,k['VULN_MODEL']]) + d_i
                damage_index_con_pt_five = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_pt_five,k['VULN_MODEL']]) + d_i
            damage_index_str_pt_five = np.clip(damage_index_str_pt_five, 0, 1)
            damage_index_con_pt_five = np.clip(damage_index_con_pt_five, 0, 1)        
        DI_STR_PT_FIVE.append(damage_index_str_pt_five)
        str_damage_pt_five = damage_index_str_pt_five * k['REP_VAL_2']*(1+m_str)
        STR_DAM_PT_FIVE.append(str_damage_pt_five)
        DI_CON_PT_FIVE.append(damage_index_con_pt_five)
        con_damage_pt_five = damage_index_con_pt_five * k['CON_VAL']*(1+m_con)
        CON_DAM_PT_FIVE.append(con_damage_pt_five)
        total_value_pt_five = str_damage_pt_five + con_damage_pt_five
        TOTAL_DAM_PT_FIVE.append(total_value_pt_five)
        if k['EST_FLR_LVL_R'] < k['0.5%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_PT_FIVE.append(House_flood)
#        NO_PPL_PT_FIVE.append(People)
      
 
        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['1%_AEP'] < crest:
            damage_index_str_one = 0
            damage_index_con_one = 0
        else:
            # Calculate the flood depth (sea level - house floor level)
            # Round to 1-digit for use in lookup table
            flood_depth_one = round(k['1%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_ONE.append(flood_depth_one)
               #Lookup table - looks up damage index based upon flood depth and 
               #vulnerability model assigned to the property
            if flood_depth_one < -0.5:
                damage_index_str_one =  0
                damage_index_con_one =  0
            else:
                damage_index_str_one = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_one,k['VULN_MODEL']]) + d_i
                #Look up damage index for contents (insured, saved goods)
                damage_index_con_one = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_one,k['VULN_MODEL']]) + d_i
                # Clip out any damage index values less than zero or more than 1 (as adjusted by D_I value)
        damage_index_str_one = np.clip(damage_index_str_one, 0, 1)
        damage_index_con_one = np.clip(damage_index_con_one, 0, 1)
        DI_STR_ONE.append(damage_index_str_one)
        #Calculate structural damage (building fabric; insured]
        str_damage_one = damage_index_str_one * k['REP_VAL_2']*(1+m_str)
        STR_DAM_ONE.append(str_damage_one)
        DI_CON_ONE.append(damage_index_con_one)
        #Calculate contents damage
        con_damage_one = damage_index_con_one * k['CON_VAL']*(1+m_con)
        CON_DAM_ONE.append(con_damage_one)
        #Calculate total damages (strutural and contents)
        total_value_one = str_damage_one + con_damage_one
        TOTAL_DAM_ONE.append(total_value_one)
        ### EXTRA - number of houses in 1% floodplain
        if k['EST_FLR_LVL_R'] < k['1%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_ONE.append(House_flood)
#        NO_PPL_ONE.append(People)
    
        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['2%_AEP'] < crest:
            damage_index_str_two = 0
            damage_index_con_two = 0
        else:
            flood_depth_two = round(k['2%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_TWO.append(flood_depth_two)
            if flood_depth_two < -0.5:
                damage_index_str_two = 0
                damage_index_con_two = 0
            else:
                damage_index_str_two = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_two,k['VULN_MODEL']]) + d_i
                damage_index_con_two = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_two,k['VULN_MODEL']]) + d_i
        damage_index_str_two = np.clip(damage_index_str_two, 0, 1)
        damage_index_con_two = np.clip(damage_index_con_two, 0, 1)
        DI_STR_TWO.append(damage_index_str_two)
        str_damage_two = damage_index_str_two * k['REP_VAL_2']*(1+m_str)
        STR_DAM_TWO.append(str_damage_two)
        DI_CON_TWO.append(damage_index_con_two)     
        con_damage_two = damage_index_con_two * k['CON_VAL']*(1+m_con)
        CON_DAM_TWO.append(con_damage_two)
        total_value_two = str_damage_two + con_damage_two
        TOTAL_DAM_TWO.append(total_value_two)
        if k['EST_FLR_LVL_R'] < k['2%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_TWO.append(House_flood)      
#        NO_PPL_TWO.append(People)
      
        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['5%_AEP'] < crest:
            damage_index_str_five = 0
            damage_index_con_five = 0
        else:
            flood_depth_five = round(k['5%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_FIVE.append(flood_depth_five)
            if flood_depth_five < -0.5:
                damage_index_str_five = 0
                damage_index_con_five = 0
            else:
                damage_index_str_five = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_five,k['VULN_MODEL']]) + d_i
                damage_index_con_five = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_five,k['VULN_MODEL']]) + d_i
        damage_index_str_five = np.clip(damage_index_str_five, 0, 1)
        damage_index_con_five = np.clip(damage_index_con_five, 0, 1)
        DI_STR_FIVE.append(damage_index_str_five)
        str_damage_five = damage_index_str_five * k['REP_VAL_2']*(1+m_str)
        STR_DAM_FIVE.append(str_damage_five)
        DI_CON_FIVE.append(damage_index_con_five)     
        con_damage_five = damage_index_con_five * k['CON_VAL']*(1+m_con)
        CON_DAM_FIVE.append(con_damage_five)
        total_value_five = str_damage_five + con_damage_five
        TOTAL_DAM_FIVE.append(total_value_five)
        if k['EST_FLR_LVL_R'] < k['5%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_FIVE.append(House_flood)        
#        NO_PPL_FIVE.append(People)        
        
        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['10%_AEP'] < crest:
            damage_index_str_ten = 0
            damage_index_con_ten = 0
        else:
            flood_depth_ten = round(k['10%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_TEN.append(flood_depth_ten)
            if flood_depth_ten < -0.5:
                damage_index_str_ten = 0
                damage_index_con_ten = 0
            else:
                damage_index_str_ten = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_ten,k['VULN_MODEL']]) + d_i
                damage_index_con_ten = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_ten,k['VULN_MODEL']]) + d_i
        damage_index_str_ten = np.clip(damage_index_str_ten, 0, 1)
        damage_index_con_ten = np.clip(damage_index_con_ten, 0, 1)
        DI_STR_TEN.append(damage_index_str_ten)
        str_damage_ten = damage_index_str_ten * k['REP_VAL_2']*(1+m_str)
        STR_DAM_TEN.append(str_damage_ten)
        DI_CON_TEN.append(damage_index_con_ten)     
        con_damage_ten = damage_index_con_ten * k['CON_VAL']*(1+m_con)
        CON_DAM_TEN.append(con_damage_ten)
        total_value_ten = str_damage_ten + con_damage_ten
        TOTAL_DAM_TEN.append(total_value_ten)
        if k['EST_FLR_LVL_R'] < k['10%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_TEN.append(House_flood)    
#        NO_PPL_TEN.append(People)
    
        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['20%_AEP'] < crest:
            damage_index_str_twenty = 0
            damage_index_con_twenty = 0        
        else:
            flood_depth_twenty = round(k['20%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_TWENTY.append(flood_depth_twenty)
            if flood_depth_twenty < -0.5:
                damage_index_str_twenty = 0
                damage_index_con_twenty = 0
            else:
                damage_index_str_twenty = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_twenty,k['VULN_MODEL']]) + d_i
                damage_index_con_twenty = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_twenty,k['VULN_MODEL']]) + d_i  
        damage_index_str_twenty = np.clip(damage_index_str_twenty, 0, 1)
        damage_index_con_twenty = np.clip(damage_index_con_twenty, 0, 1)
        DI_STR_TWENTY.append(damage_index_str_twenty)
        str_damage_twenty = damage_index_str_twenty * k['REP_VAL_2']*(1+m_str)
        STR_DAM_TWENTY.append(str_damage_twenty)                  
        DI_CON_TWENTY.append(damage_index_con_twenty)
        con_damage_twenty = damage_index_con_twenty * k['CON_VAL']*(1+m_con)
        CON_DAM_TWENTY.append(con_damage_twenty)
        total_value_twenty = str_damage_twenty + con_damage_twenty
        TOTAL_DAM_TWENTY.append(total_value_twenty)
        if k['EST_FLR_LVL_R'] < k['20%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_TWENTY.append(House_flood)
#        NO_PPL_TWENTY.append(People)

        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['40%_AEP'] < crest:
            damage_index_str_forty = 0
            damage_index_con_forty = 0        
        else:
            flood_depth_forty = round(k['40%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_FORTY.append(flood_depth_forty)
            if flood_depth_forty < -0.5:
                damage_index_str_forty = 0
                damage_index_con_forty = 0
            else:
                damage_index_str_forty = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_forty,k['VULN_MODEL']]) + d_i
                damage_index_con_forty = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_forty,k['VULN_MODEL']]) + d_i  
        damage_index_str_forty = np.clip(damage_index_str_forty, 0, 1)
        damage_index_con_forty = np.clip(damage_index_con_forty, 0, 1)
        DI_STR_FORTY.append(damage_index_str_forty)
        str_damage_forty = damage_index_str_forty * k['REP_VAL_2']*(1+m_str)
        STR_DAM_FORTY.append(str_damage_forty)                  
        DI_CON_FORTY.append(damage_index_con_forty)
        con_damage_forty = damage_index_con_forty * k['CON_VAL']*(1+m_con)
        CON_DAM_FORTY.append(con_damage_forty)
        total_value_forty = str_damage_forty + con_damage_forty
        TOTAL_DAM_FORTY.append(total_value_forty)
        if k['EST_FLR_LVL_R'] < k['40%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_FORTY.append(House_flood)
#        NO_PPL_FORTY.append(People)

        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['60%_AEP'] < crest:
            damage_index_str_sixty = 0
            damage_index_con_sixty = 0        
        else:
            flood_depth_sixty = round(k['60%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_SIXTY.append(flood_depth_sixty)
            if flood_depth_sixty < -0.5:
                damage_index_str_sixty = 0
                damage_index_con_sixty = 0
            else:
                damage_index_str_sixty = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_sixty,k['VULN_MODEL']]) + d_i
                damage_index_con_sixty = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_sixty,k['VULN_MODEL']]) + d_i  
        damage_index_str_sixty = np.clip(damage_index_str_sixty, 0, 1)
        damage_index_con_forty = np.clip(damage_index_con_sixty, 0, 1)
        DI_STR_SIXTY.append(damage_index_str_sixty)
        str_damage_sixty = damage_index_str_sixty * k['REP_VAL_2']*(1+m_str)
        STR_DAM_SIXTY.append(str_damage_sixty)                  
        DI_CON_SIXTY.append(damage_index_con_sixty)
        con_damage_sixty = damage_index_con_sixty * k['CON_VAL']*(1+m_con)
        CON_DAM_SIXTY.append(con_damage_sixty)
        total_value_sixty = str_damage_sixty + con_damage_sixty
        TOTAL_DAM_SIXTY.append(total_value_sixty)
        if k['EST_FLR_LVL_R'] < k['60%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_SIXTY.append(House_flood)
#        NO_PPL_SIXTY.append(People)

        if k['ZONE'] == ('Zone1' or 'Zone2' or 'Zone 3') and k['90%_AEP'] < crest:
            damage_index_str_ninety = 0
            damage_index_con_ninety = 0        
        else:
            flood_depth_ninety = round(k['90%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_NINETY.append(flood_depth_ninety)
            if flood_depth_ninety < -0.5:
                damage_index_str_ninety = 0
                damage_index_con_ninety = 0
            else:
                damage_index_str_ninety = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_ninety,k['VULN_MODEL']]) + d_i
                damage_index_con_ninety = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_ninety,k['VULN_MODEL']]) + d_i  
        damage_index_str_ninety = np.clip(damage_index_str_ninety, 0, 1)
        damage_index_con_ninety = np.clip(damage_index_con_ninety, 0, 1)
        DI_STR_NINETY.append(damage_index_str_ninety)
        str_damage_ninety = damage_index_str_ninety * k['REP_VAL_2']*(1+m_str)
        STR_DAM_NINETY.append(str_damage_ninety)                  
        DI_CON_NINETY.append(damage_index_con_ninety)
        con_damage_ninety = damage_index_con_ninety * k['CON_VAL']*(1+m_con)
        CON_DAM_NINETY.append(con_damage_ninety)
        total_value_ninety = str_damage_ninety + con_damage_ninety
        TOTAL_DAM_NINETY.append(total_value_ninety)
        if k['EST_FLR_LVL_R'] < k['90%_AEP']:
            House_flood = 1
#            People = k['AV_PPL_DWL']*(1+a_ppl)
        else:
            House_flood = 0
#            People = 0
        NO_HOUSES_NINETY.append(House_flood)
#        NO_PPL_NINETY.append(People)


#    Property_outfile_one = "C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\"+date_string+"_Prop_Impact.csv"
#    prop_impact.to_csv(Property_outfile_one) 


    ## CALCULATING THE AVERAGE ANNUAL PEOPLE EXPOSED   
    fld_lvl_pt_one = slr*r_sea + AEP_PT_ONE_BL
    fld_lvl_pt_two = slr*r_sea + AEP_PT_TWO_BL
    fld_lvl_pt_five = slr*r_sea + AEP_PT_FIVE_BL
    fld_lvl_one = slr*r_sea + AEP_ONE_BL
    fld_lvl_two = slr*r_sea + AEP_TWO_BL
    fld_lvl_five = slr*r_sea + AEP_FIVE_BL
    fld_lvl_ten = slr*r_sea + AEP_TEN_BL
    fld_lvl_twenty = slr*r_sea + AEP_TWENTY_BL
    fld_lvl_forty = slr*r_sea + AEP_FORTY_BL
    fld_lvl_sixty = slr*r_sea + AEP_SIXTY_BL
    fld_lvl_ninety = slr*r_sea + AEP_NINETY_BL
    
    fld_pt_one_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_pt_one,2), 'OP1_AAPE'])
    ppl_pt_one = fld_pt_one_lookup*(1+a_ppl)
    NO_PPL_PT_ONE.append(ppl_pt_one)
       
    fld_pt_two_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_pt_two,2), 'OP1_AAPE'])
    ppl_pt_two = fld_pt_two_lookup*(1+a_ppl)
    NO_PPL_PT_TWO.append(ppl_pt_two)

    fld_pt_five_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_pt_five,2), 'OP1_AAPE'])
    ppl_pt_five = fld_pt_five_lookup*(1+a_ppl)
    NO_PPL_PT_FIVE.append(ppl_pt_five)    
    
    fld_one_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_one,2), 'OP1_AAPE'])
    ppl_one = fld_one_lookup*(1+a_ppl)
    NO_PPL_ONE.append(ppl_one)    
    
    fld_two_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_two,2), 'OP1_AAPE'])
    ppl_two = fld_two_lookup*(1+a_ppl)
    NO_PPL_TWO.append(ppl_two)    
    
    fld_five_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_five,2), 'OP1_AAPE'])
    ppl_five = fld_five_lookup*(1+a_ppl)
    NO_PPL_FIVE.append(ppl_five)     
    
    fld_ten_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_ten,2), 'OP1_AAPE'])
    ppl_ten = fld_ten_lookup*(1+a_ppl)
    NO_PPL_TEN.append(ppl_ten)     
    
    fld_twenty_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_twenty,2), 'OP1_AAPE'])
    ppl_twenty = fld_twenty_lookup*(1+a_ppl)
    NO_PPL_TWENTY.append(ppl_twenty) 
       
    fld_forty_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_forty,2), 'OP1_AAPE'])
    ppl_forty = fld_forty_lookup*(1+a_ppl)
    NO_PPL_FORTY.append(ppl_forty)

    fld_sixty_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_sixty,2), 'OP1_AAPE'])
    ppl_sixty = fld_sixty_lookup*(1+a_ppl)
    NO_PPL_SIXTY.append(ppl_sixty)

    fld_ninety_lookup = float(aape_lookup.loc[aape_lookup['Flood_level']==round(fld_lvl_ninety,2), 'OP1_AAPE'])
    ppl_ninety = fld_ninety_lookup*(1+a_ppl)
    NO_PPL_NINETY.append(ppl_ninety)


    #Sum the total damages for all properties affected
    AEP_pt_one_impact = sum(TOTAL_DAM_PT_ONE)
    AEP_PT_ONE_IMP.append(AEP_pt_one_impact)
    AEP_pt_two_impact = sum(TOTAL_DAM_PT_TWO)
    AEP_PT_TWO_IMP.append(AEP_pt_two_impact)  
    AEP_pt_five_impact = sum(TOTAL_DAM_PT_FIVE)
    AEP_PT_FIVE_IMP.append(AEP_pt_five_impact)  
    AEP_one_impact = sum(TOTAL_DAM_ONE)
    AEP_ONE_IMP.append(AEP_one_impact)
    AEP_two_impact = sum(TOTAL_DAM_TWO)
    AEP_TWO_IMP.append(AEP_two_impact)
    AEP_five_impact = sum(TOTAL_DAM_FIVE)
    AEP_FIVE_IMP.append(AEP_five_impact)
    AEP_ten_impact = sum(TOTAL_DAM_TEN)
    AEP_TEN_IMP.append(AEP_ten_impact)  
    AEP_twenty_impact = sum(TOTAL_DAM_TWENTY)
    AEP_TWENTY_IMP.append(AEP_twenty_impact)   
    AEP_forty_impact = sum(TOTAL_DAM_FORTY)
    AEP_FORTY_IMP.append(AEP_forty_impact)   
    AEP_sixty_impact = sum(TOTAL_DAM_SIXTY)
    AEP_SIXTY_IMP.append(AEP_sixty_impact)       
    AEP_ninety_impact = sum(TOTAL_DAM_NINETY)
    AEP_NINETY_IMP.append(AEP_ninety_impact)         
        
    #Sum the total number of houses impacts     
    House_pt_one_impact = sum(NO_HOUSES_PT_ONE)
    SUM_HOUSES_PT_ONE.append(House_pt_one_impact)  
    House_pt_two_impact = sum(NO_HOUSES_PT_TWO)
    SUM_HOUSES_PT_TWO.append(House_pt_two_impact)  
    House_pt_five_impact = sum(NO_HOUSES_PT_FIVE)
    SUM_HOUSES_PT_FIVE.append(House_pt_five_impact)  
    House_one_impact = sum(NO_HOUSES_ONE)
    SUM_HOUSES_ONE.append(House_one_impact)  
    House_two_impact = sum(NO_HOUSES_TWO)
    SUM_HOUSES_TWO.append(House_two_impact)  
    House_five_impact = sum(NO_HOUSES_FIVE)
    SUM_HOUSES_FIVE.append(House_five_impact)  
    House_ten_impact = sum(NO_HOUSES_TEN)
    SUM_HOUSES_TEN.append(House_ten_impact)  
    House_twenty_impact = sum(NO_HOUSES_TWENTY)
    SUM_HOUSES_TWENTY.append(House_twenty_impact)  
    House_forty_impact = sum(NO_HOUSES_FORTY)
    SUM_HOUSES_FORTY.append(House_forty_impact)    
    House_sixty_impact = sum(NO_HOUSES_SIXTY)
    SUM_HOUSES_SIXTY.append(House_sixty_impact)    
    House_ninety_impact = sum(NO_HOUSES_NINETY)
    SUM_HOUSES_NINETY.append(House_ninety_impact)    
    
    #Sum the total number of people
    People_pt_one_impact = sum(NO_PPL_PT_ONE)
    SUM_PPL_PT_ONE.append(People_pt_one_impact)
    People_pt_two_impact = sum(NO_PPL_PT_TWO)
    SUM_PPL_PT_TWO.append(People_pt_two_impact)
    People_pt_five_impact = sum(NO_PPL_PT_FIVE)
    SUM_PPL_PT_FIVE.append(People_pt_five_impact)
    People_one_impact = sum(NO_PPL_ONE)
    SUM_PPL_ONE.append(People_one_impact)
    People_two_impact = sum(NO_PPL_TWO)
    SUM_PPL_TWO.append(People_two_impact)
    People_five_impact = sum(NO_PPL_FIVE)
    SUM_PPL_FIVE.append(People_five_impact)
    People_ten_impact = sum(NO_PPL_TEN)
    SUM_PPL_TEN.append(People_ten_impact)
    People_twenty_impact = sum(NO_PPL_TWENTY)
    SUM_PPL_TWENTY.append(People_twenty_impact)
    People_forty_impact = sum(NO_PPL_FORTY)
    SUM_PPL_FORTY.append(People_forty_impact)
    People_sixty_impact = sum(NO_PPL_SIXTY)
    SUM_PPL_SIXTY.append(People_sixty_impact)    
    People_ninety_impact = sum(NO_PPL_NINETY)
    SUM_PPL_NINETY.append(People_ninety_impact)    
    
#################################################################################    
#    #ARCMAP Analysis to determine lineal meters of esplanade untrafficable 
#    arcpy.gp.CreateConstantRaster_sa(slr_surface, slr, "FLOAT", "1", "584953 5805832 590779 5808569")
#    # Process: Calculate Statistics
#    arcpy.CalculateStatistics_management(AOI_dem1m, "1", "1", "", "OVERWRITE", inpath + "AOI_box")    
#    # Process: Plus - create the MHHW surface by adding onto MSL level
#    arcpy.Plus_3d(slr_surface,MHHW_ADJUST,slr_surf_mhhw)
#    # Process: Less Than Equal.Evaluate if DEM lower than water elevation. If yes, value of 1.
#    arcpy.gp.LessThanEqual_sa(AOI_dem1m, slr_surf_mhhw, slr_extent)
#    # Process: Con. If cell has value of 1, then keep
#    arcpy.gp.Con_sa(slr_extent, CONDITION_TRUE, slr_ext_con, "", "Value =1")
#    ## Process: Region Group - assigns a number to each connected region for cells (i.e. with value 1 from Con)
#    ## As per NOAA inundation mapping guidance (NOAA, 2017)
##    #arcpy.gp.RegionGroup_sa(slr_ext_con, slrgroup, "EIGHT", "WITHIN", "NO_LINK", "")
#    ### NOTE assumed hydraulic connectivity through base, pipes, etc... not just overland
#    # Process: Raster to Polygon
#    arcpy.RasterToPolygon_conversion(slr_ext_con, slr_poly, "SIMPLIFY", "Value")
#    ## Process: Select - Max polygon
##    ##arcpy.Select_analysis(slr_poly, max_slr_poly, "Shape_Area=(SELECT MAX(Shape_Area) FROM slr_poly)")
#    # Process: Minus (2)
#    arcpy.Minus_3d(slr_surf_mhhw, AOI_dem1m, diffslr)
#    # Process: Extract by Mask
#    arcpy.gp.ExtractByMask_sa(diffslr, slr_poly, slrdepth)
#    # Process: Less Than Equal.Evaluate if DEM lower than water elevation. If yes, value of 1.
#    arcpy.gp.LessThanEqual_sa(slrdepth, max_car_depth, LessThan0_15)
#    # Process: Con. If cell has value of 0, then keep
#    arcpy.gp.Con_sa(LessThan0_15, CONDITION_TRUE, rd_dep_con, "", "Value =0")
#    # Process: Raster to Polygon
#    arcpy.RasterToPolygon_conversion(rd_dep_con, rd_dep_poly, "SIMPLIFY", "Value")
#    # Process: Clip
#    arcpy.Clip_analysis(roads_sel, rd_dep_poly, rd_flood_seg, "")    
#    # Process: Summary Statistics (2)
#    arr_road = arcpy.da.TableToNumPyArray(rd_flood_seg,"Shape_Length")
#    Public_road = arr_road["Shape_Length"].sum()
#    print "The length of the esplanade impacted by nuisance flooding is " + str(round(Public_road,1))+"m"
#    # Add results 
#    Road_length_SLR.append(Public_road) 
#    print "-------------------------------------"     


cases['0.1%_AEP_IMP'] = AEP_PT_ONE_IMP
cases['0.2%_AEP_IMP'] = AEP_PT_TWO_IMP
cases['0.5%_AEP_IMP'] = AEP_PT_FIVE_IMP
cases['1%_AEP_IMP'] = AEP_ONE_IMP
cases['2%_AEP_IMP'] = AEP_TWO_IMP
cases['5%_AEP_IMP'] = AEP_FIVE_IMP
cases['10%_AEP_IMP'] = AEP_TEN_IMP
cases['20%_AEP_IMP'] = AEP_TWENTY_IMP
cases['40%_AEP_IMP'] = AEP_FORTY_IMP
cases['60%_AEP_IMP'] = AEP_SIXTY_IMP
cases['90%_AEP_IMP'] = AEP_NINETY_IMP

cases['Houses_0.1%'] = SUM_HOUSES_PT_ONE
cases['Houses_0.2%'] = SUM_HOUSES_PT_TWO
cases['Houses_0.5%'] = SUM_HOUSES_PT_FIVE
cases['Houses_1%'] = SUM_HOUSES_ONE
cases['Houses_2%'] = SUM_HOUSES_TWO
cases['Houses_5%'] = SUM_HOUSES_FIVE
cases['Houses_10%'] = SUM_HOUSES_TEN
cases['Houses_20%'] = SUM_HOUSES_TWENTY
cases['Houses_40%'] = SUM_HOUSES_FORTY
cases['Houses_60%'] = SUM_HOUSES_SIXTY
cases['Houses_90%'] = SUM_HOUSES_NINETY

cases['0.1%_AEP_PPL'] = SUM_PPL_PT_ONE
cases['0.2%_AEP_PPL'] = SUM_PPL_PT_TWO
cases['0.5%_AEP_PPL'] = SUM_PPL_PT_FIVE
cases['1%_AEP_PPL'] = SUM_PPL_ONE
cases['2%_AEP_PPL'] = SUM_PPL_TWO
cases['5%_AEP_PPL'] = SUM_PPL_FIVE
cases['10%_AEP_PPL'] = SUM_PPL_TEN
cases['20%_AEP_PPL'] = SUM_PPL_TWENTY
cases['40%_AEP_PPL'] = SUM_PPL_FORTY
cases['60%_AEP_PPL'] = SUM_PPL_SIXTY
cases['90%_AEP_PPL'] = SUM_PPL_NINETY


###############################################################################      
#cases["Road Impact"]=Road_length_SLR
###############################################################################      

for index, z in cases.iterrows():
    a = z['0.1%_AEP_IMP']
    b = z['0.2%_AEP_IMP']
    c = z['0.5%_AEP_IMP']
    d = z['1%_AEP_IMP']
    e = z['2%_AEP_IMP']
    f = z['5%_AEP_IMP']
    g = z['10%_AEP_IMP']
    h = z['20%_AEP_IMP']
    i = z['40%_AEP_IMP']
    j = z['60%_AEP_IMP']
    k = z['90%_AEP_IMP']
    
    l = z['0.1%_AEP_PPL']
    m = z['0.2%_AEP_PPL']
    n = z['0.5%_AEP_PPL']
    o = z['1%_AEP_PPL']
    p = z['2%_AEP_PPL']
    q = z['5%_AEP_PPL']
    r = z['10%_AEP_PPL']
    s = z['20%_AEP_PPL']
    t = z['40%_AEP_PPL']
    u = z['60%_AEP_PPL']
    v = z['90%_AEP_PPL']    
    
    aad =  float(np.trapz([a,b,c,d,e,f,g,h,i,j,k],x=[0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.4,0.6,0.9]))
    aape = float(np.trapz([l,m,n,o,p,q,r,s,t,u,v],x=[0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.4,0.6,0.9]))
    #    aad = np.trapz([a,b,c,d],x=[0.01,0.02,0.05,0.1])
    AAD.append(aad)
    AAPE.append(aape)

cases["AAD"]=AAD
cases['AAPE'] = AAPE
cases

## NOTE THIS IS THE FILE IN THE LAST YEAR OF THE LAST ANNUAL_MSL SCENARIO
#Property_outfile_one = "C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\"+date_string+"_Prop_Impact_op1.csv"
#prop_impact.to_csv(Property_outfile_one) 

Cases_outfile_one = ("C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\"+date_string+"_Case_Results_RDM_OPTION1_BARRIER.csv")
cases.to_csv(Cases_outfile_one) 



t1 = time.clock()
tdiff = t1 - t0
tmin = tdiff/60
thour = tmin/60
print "It took %.3f seconds for this code to run" % (tdiff) + " (%.2f mins " % (tmin) + "/ %.2f hours)" % (thour) +" to run " + str(case)+" scenarios"