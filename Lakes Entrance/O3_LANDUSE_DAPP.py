# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 10:35:47 2018

@author: tdramm

03_LANDUSE_DAPP.py -   The 


                         
"""

import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

###############################################################################
#Clock setup
t0 = time.clock()   # Starts clock times

###############################################################################
## Set up the date. Useful for adding date to csv file names with results
date_list = []
today = datetime.date.today()
date_list.append(today)
date_string = str(date_list[0])
#date_string = today.strftime('%Y'+"_"+'%m'+"_"+'%d')
print "Trial run for " + date_string

###############################################################################
#Import the uncertain factors
cases_dapp = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\2018-02-28_5000Case_Generation.csv')
#cases_dapp = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\2018-01-23_Case_Results_RDM.csv')
#cases_dapp = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\2018-02-28_Case_Results_RDM.csv')
cases_dapp.head()

## Define prior values for key factors
cases_dapp = cases_dapp[0:500]    #Note [31:32] a good one to test
cases_dapp

## Baseline lake levels mAHD (Grayson et al., 2004)
aep_pt_one_bl = 2.2
aep_pt_two_bl = 2.1
aep_pt_five_bl = 2.0
aep_one_bl = 1.8
aep_two_bl = 1.6
aep_five_bl = 1.3
aep_ten_bl = 1.2
aep_twenty_bl = 1.05
aep_forty_bl = 0.9
aep_sixty_bl = 0.85
aep_ninety_bl = 0.77 #Note impacts to propoerties with floor level up to 0.5m above this (see D.I. lookup table)
MHHW_BULLOCK_IS = 0.43 # MHHW for Bullock Island


BL_AAD_risk = 3700000 #SAY (100% is 3.2mil, 50% is 2.4mil)
BL_AAPE_risk = 94 #say (100% is 82.4, 50% is 30.9)
BL_Esp_lvl = 0.7
year_imp = 2030 #2050 (median from DAPP less 20 years) is the year of implementing

## Bring in structural damage and contents damage lookup tables
vuln_model_str = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\Vulnerability_Models\\Lookup\\GA_vuln_structural.csv')
vuln_model_con = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\Vulnerability_Models\\Lookup\\GA_vuln_contents.csv')
#vuln_model_str = pd.read_csv('C:\\Users\\Tim\\Desktop\\TEMP_slr\\GA_vuln_structural.csv')
#vuln_model_con = pd.read_csv('C:\\Users\\Tim\\Desktop\\TEMP_slr\\GA_vuln_contents.csv')
aape_lookup = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\2018-03-02 AAPE_Lookup.csv')

###############################################################################
# Define the sea level rise model / function
def slr_model (a_poly, b_poly, c_poly, t_star, c_star):
    for index, i in annual_MSL.iterrows():
        year_i= i['Year']        
        if year_i < t_star:
            msl_i = a_poly + b_poly*year_i + c_poly*(math.pow(year_i,2))
        else:
            msl_i = a_poly + b_poly*year_i + c_poly*(math.pow(year_i,2))+c_star*(year_i - t_star)
        msl.append(msl_i)
###############################################################################

## Define lists for the cases_dapp dataframe before looping through
## Lists to be appended to cases_dapp dataframe
DAPP_LSUB = []
DAPP_APOLY = []
DAPP_BPOLY = []
DAPP_CPOLY = []
DAPP_CSTAR = []
DAPP_TSTAR = []
DAPP_SLR_PROJ = []
DAPP_RSTR = []
DAPP_RCON = []
DAPP_R = []
DAPP_RNET_S = []     # Net (r - r_str) / (1 + r_str)
DAPP_RNET_C = []     # Net (r - r_con) / (1 + r_con)
DAPP_TLEADA = []
DAPP_LCAPA = []
DAPP_MOPA = []
DAPP_PLIFEA = []
CASE = []
YYYY = []
SIGNPOST =[]
SIGNPOST_AAPE =[]
SIGNPOST_ESP =[]
#NPV_A = []
#SIGN_A =[]



###############################################################################
# Set up to save figure
fig = plt.figure()

for index, i in cases_dapp.iterrows():
    r_sea = i['r_sea']                  # Sea-level response factor    
    l_sub = i['l_sub']                  # rate of vertical land movement (mm/year)
    a_poly = i['a_poly']                # coefficient a, current sea level (mm)
    b_poly = i['b_poly']                # coefficient b, rate of sea level rise (mm/year)
    c_poly = i['c_poly']                # coefficient c, sea level rise acceleration (mm2/year)
    c_star = i['c_star']                # rate of abrupt sea level rise (mm/year)
    t_star = i['t_star']                # year of abrupt sea level rise (years from today)
    r_str = i['r_str']                  # rate of annual growth (real $) in replacement cost - structural (%/year)
    r_con = i['r_con']                  # rate of annual growth (real $) in contents value (%/year)
    r_ppl = i['r_ppl']                  # rate of annual growth in household composition
    r = i['r']                          # discount rate (%/year)
#    t_lead_pol_a = i['t_lead_pol_a']    # policy lead time (years)
#    l_cap_pol_a = i['l_cap_pol_a']      # upfront capital investment ($)
#    m_op_pol_a = i['m_op_pol_a']        # annual maintenance cost ($/year)
#    p_life_pol_a = i['p_life_pol_a']    # effective policy lifetime (years)
    case = i['Case']                    # case number
    rate_op = int(i['rate_op3'])

#    d_i = i['d_i']                      # damage index shift at 10cm inundation
#    m_str = i['m_str']                  # shift in maximum structural damage to building fabric (%)
#    m_con = i['m_con']                  # shift in maximum contents damage (%)
#    a_ppl = i['a_ppl']                  # % change in average people per dwelling (pp/dwelling)
    
#    r_sea = 0.9                 # Baseline   
#    l_sub = 0                   # Baseline
#    a_poly = 0                  # Baseline
#    b_poly = 3                  # Baseline
#    c_poly = 0                  # Baseline
#    c_star = 0                  # Baseline
#    t_star = 0                  # Baseline
#    r_str = 0                   # Baseline
#    r_con = 0                   # Baseline
#    r_ppl = 0                   # Baseline

    print "-------------------------------------"    
    print "Case " +str(case)+":"
    print "Coefficient a = " +str(a_poly) +"(mm)"
    print "Coefficient b = " +str(b_poly) +"(mm/yr)"
    print "Coefficient c = " +str(c_poly) +"(mm2/yr)"
    print "Coefficient c* = " +str(c_star) +"(mm2/yr)"
    print "Coefficient t* = " +str(t_star) +"(years from present)"
    print "Annual rate of change in structural replacement cost, r_str = " +str(r_str) +"(decimal %/year)"
    print "Annual rate of change in contents replacement cost, r_con = " +str(r_con) +"(decimal %/year)"
    print "Annual rate of change in household composition, r_ppl = " +str(r_ppl) +"(decimal %/year)"

###############################################################################
    # Set-up lists for the annual_MSL dataframe
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

#    NO_HOUSES_PT_ONE = []
#    NO_HOUSES_PT_TWO = []
#    NO_HOUSES_PT_FIVE = []
    NO_HOUSES_ONE = []
#    NO_HOUSES_TWO = []
#    NO_HOUSES_FIVE = []
#    NO_HOUSES_TEN = []
#    NO_HOUSES_TWENTY = []
#    
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
    
#    NO_PPL_PT_ONE = []
#    NO_PPL_PT_TWO = []
#    NO_PPL_PT_FIVE = []
#    NO_PPL_ONE = []
#    NO_PPL_TWO = []
#    NO_PPL_FIVE = []
#    NO_PPL_TEN = []
#    NO_PPL_TWENTY = []
    
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
    
    AAD = []
    AAPE = []
    AAH = []

###############################################################################
## 3. Generate time-series realisation
    year = []                   # list of years up to (t_lead + p_policy)
    mean_sea_level = []         # annual mean sea level relative to baseline (mm)      
   
#    timeframe = int(t_lead_pol_a + p_life_pol_a)
    timeframe=90
    year = range(0,timeframe +1,5)
    
    columns = []                # Set up emply list
    index = range(0,timeframe + 1,5)
    annual_MSL = pd.DataFrame(index = index, columns = columns, dtype=np.float32)
    annual_MSL['Year'] = year
    annual_MSL = pd.DataFrame(annual_MSL,dtype=float)
    # Create column referenced to current year
#    annual_MSL['Year_Date'] = annual_MSL['Year'] + 2017 
    annual_MSL['Year_Date'] = annual_MSL['Year'] + 2010

    # Run the model with default input values    
    msl = []
    slr_model(a_poly,b_poly,c_poly,t_star,c_star)
    msl

    annual_MSL['SLR_proj_mm'] = msl
    annual_MSL['SLR_proj_m'] = annual_MSL['SLR_proj_mm'] / 1000
#    # Apply rule of thumb
#    annual_MSL['Rule_of_thumb (m)'] = annual_MSL['SLR_proj_m']*r_sea
    annual_MSL

    # ADD IN INPUTS
    annual_MSL['l_sub'] = l_sub*annual_MSL['Year']/1000         #convert to m
    annual_MSL['a_poly'] = a_poly
    annual_MSL['b_poly'] = b_poly
    annual_MSL['c_poly'] = c_poly
    annual_MSL['c_star'] = c_star
    annual_MSL['t_star'] = t_star 
    annual_MSL['r_sea'] = r_sea
#    annual_MSL['d_i'] = d_i
    
    # Add the adjusted AEP levels
    annual_MSL['aep_pt_one'] = aep_pt_one_bl + annual_MSL['SLR_proj_m']*r_sea - annual_MSL['l_sub']
    annual_MSL['aep_pt_two'] = aep_pt_two_bl + annual_MSL['SLR_proj_m']*r_sea - annual_MSL['l_sub']
    annual_MSL['aep_pt_five'] = aep_pt_five_bl + annual_MSL['SLR_proj_m']*r_sea - annual_MSL['l_sub']
    annual_MSL['aep_one'] = aep_one_bl + annual_MSL['SLR_proj_m']*r_sea - annual_MSL['l_sub']
    annual_MSL['aep_two'] = aep_two_bl + annual_MSL['SLR_proj_m']*r_sea - annual_MSL['l_sub']
    annual_MSL['aep_five'] = aep_five_bl + annual_MSL['SLR_proj_m']*r_sea - annual_MSL['l_sub']
    annual_MSL['aep_ten'] = aep_ten_bl + annual_MSL['SLR_proj_m']*r_sea - annual_MSL['l_sub']
    annual_MSL['aep_twenty'] = aep_twenty_bl + annual_MSL['SLR_proj_m']*r_sea- annual_MSL['l_sub']
    annual_MSL['aep_forty'] = aep_forty_bl + annual_MSL['SLR_proj_m']*r_sea- annual_MSL['l_sub']    
    annual_MSL['aep_sixty'] = aep_sixty_bl + annual_MSL['SLR_proj_m']*r_sea- annual_MSL['l_sub']    
    annual_MSL['aep_ninety'] = aep_ninety_bl + annual_MSL['SLR_proj_m']*r_sea- annual_MSL['l_sub']
        
    # Add the rates
    annual_MSL['rate_str'] = r_str * annual_MSL['Year']  # annual growth rate (linear)
    annual_MSL['rate_con'] = r_con * annual_MSL['Year']
    annual_MSL 
    
    ###############################################################################
    ## 4. Analyse impacts for each year in the realisation
    ###############################################################################
 
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
    
#    DI_STR_PT_ONE = []
#    DI_STR_PT_TWO = []
#    DI_STR_PT_FIVE = []
#    DI_STR_ONE = []
#    DI_STR_TWO = []
#    DI_STR_FIVE = []
#    DI_STR_TEN = []
#    DI_STR_TWENTY = []
#    
#    DI_CON_PT_ONE = []
#    DI_CON_PT_TWO = []
#    DI_CON_PT_FIVE = []
#    DI_CON_ONE = []
#    DI_CON_TWO = []
#    DI_CON_FIVE = []
#    DI_CON_TEN = []
#    DI_CON_TWENTY = []
    
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
   
#    sub_annual_MSL = annual_MSL
#    sub_annual_MSL
    
    prop_impact = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\Property_Stock_19Feb.csv')   
    #    prop_impact = pd.read_csv('C:\\Users\\Tim\\Desktop\\TEMP_slr\\Property_Stock_19Jan.csv')
        
    #    prop_impact = prop_impact[0:100]     # For troubleshooting    
    #    prop_impact
    
    prop_impact['sample'] = 'N' #Counter to know if property has been sampled yet
    prop_impact.head()
#    agg_ppl = 0             

    # Iterate through the rows in the realisation over the timeframe
    for index, j in annual_MSL.iterrows():
                    
        #        prop_impact['Con_Value'] = prop_impact['FLR_AREA'] * prop_impact['STOREYS'] * j['rate_con']
        prop_impact['0.1%_AEP'] = j['aep_pt_one']
        prop_impact['0.2%_AEP'] = j['aep_pt_two']    
        prop_impact['0.5%_AEP'] = j['aep_pt_five']
        prop_impact['1%_AEP'] = j['aep_one']
        prop_impact['2%_AEP'] = j['aep_two']
        prop_impact['5%_AEP'] = j['aep_five']
        prop_impact['10%_AEP'] = j['aep_ten']
        prop_impact['20%_AEP'] = j['aep_twenty']     
        prop_impact['40%_AEP'] = j['aep_forty']     
        prop_impact['60%_AEP'] = j['aep_sixty']     
        prop_impact['90%_AEP'] = j['aep_ninety']     
        prop_impact    


    ##############################################################     
    ##############################################################
        # DON'T SAMPLE RESIDENTIAL HOUSES IN ZONE 1, 2, 3, 4
        prop_imp_sub = pd.DataFrame(prop_impact.loc[(prop_impact['ZONE']== 'Zone4') | (prop_impact['ZONE']== 'Zone3') | (prop_impact['ZONE']== 'Zone2') | (prop_impact['ZONE']== 'Zone1')])  
        prop_imp_sub2 = pd.DataFrame(prop_imp_sub.loc[prop_imp_sub['BLD_TYPE'] == 'Residential'])    #Select residential properties   
        prop_imp_samp = prop_imp_sub2.loc[prop_imp_sub2['sample']=='N'] ##Select remianing propoerties that have not been sampled
            
        if j['Year_Date'] <= year_imp:    #i.e. retreat does not commence until 2030     
#        if 2035 < year_imp:    #i.e. retreat does not commence until 2030     
            prop_impact = prop_impact              
        else:
            # Create a subset of the proporty database with zone 4 only            
            nn = rate_op # Average number of houses retreating per 5 years
    
            if len(prop_imp_sub2.index) < nn: #Rate of properties retreated
                nn = len(prop_imp_sub2.index)
            else:
                nn = nn
        
            #Randomly sample 4 properties
            if nn > 0:
                prop_imp_sub_sel = pd.DataFrame(prop_imp_samp.sample(nn)) #Sample from remaining properties that have not yet been sampled
                sample3 =[]
                for index, x in prop_imp_sub_sel.iterrows():
                    Count = 'Y'
                    sample3.append(Count)         
                prop_imp_sub_sel['samp3'] = sample3
#                prop_imp_sub.head()
    
            # Replace the value in the original dataset 
                for index, y in prop_imp_sub_sel.iterrows():          
                    ID = int(y['Arc_ID'])            
                    New_sample_rate = prop_imp_sub_sel.loc[prop_imp_sub_sel['Arc_ID'] == ID, 'samp3']         
                    prop_impact.loc[prop_impact['Arc_ID'] == ID, 'sample'] = New_sample_rate #Change sampled to 'Y'
                
#                agg_ppl = agg_ppl + sum(prop_imp_sub_sel['AV_PPL_DWL'])
                
            else:
                prop_impact = prop_impact            
    
            
            prop_impact = prop_impact.loc[prop_impact['sample'] == 'N'] #Take subset of the properties which have not been retreated (i.e. 'N')             
            # len(prop_impact) # Length of subset
    ##############################################################       
    ##############################################################            

        year_ppl = int(j['Year'])
        str_adj = j['rate_str']
        con_adj = j['rate_con']
       
        slr_proj = j['SLR_proj_m']
#        rate_str = j['rate_str']
#        rate_con = j['rate_con'] 
        yr_yyyy = int(j['Year_Date'])
        case = int(case)      
            
        # clear the contents to avoid duplication in the next iteration
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
        
#        prop_impact = prop_impact[0:10]     # For troubleshooting
        # Iterate through the rows in the propoerty stock database to assess 
        # impacts for a given realisation
        for index, k in prop_impact.iterrows():            
            flood_depth_pt_one = round(k['0.1%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_PT_ONE.append(flood_depth_pt_one)
            if flood_depth_pt_one < -0.5:
                damage_index_str_pt_one = 0
                damage_index_con_pt_one = 0
            else:
                damage_index_str_pt_one = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_pt_one,k['VULN_MODEL']])
                damage_index_con_pt_one = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_pt_one,k['VULN_MODEL']])
            damage_index_str_pt_one = np.clip(damage_index_str_pt_one, 0, 1)
            damage_index_con_pt_one = np.clip(damage_index_con_pt_one, 0, 1)
            DI_STR_PT_ONE.append(damage_index_str_pt_one)
            str_damage_pt_one = damage_index_str_pt_one * k['REP_VAL_2']*(1+str_adj) #NEED TO ADD increasing rate
            STR_DAM_PT_ONE.append(str_damage_pt_one)
            DI_CON_PT_ONE.append(damage_index_con_pt_one)
            con_damage_pt_one = damage_index_con_pt_one * k['CON_VAL']*(1+con_adj)
            CON_DAM_PT_ONE.append(con_damage_pt_one)
            total_value_pt_one = str_damage_pt_one + con_damage_pt_one
            TOTAL_DAM_PT_ONE.append(total_value_pt_one)
            if k['EST_FLR_LVL_R'] < k['0.1%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)
            NO_HOUSES_PT_ONE.append(House_flood)       
#            NO_PPL_PT_ONE.append(People)
           
            flood_depth_pt_two = round(k['0.2%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_PT_TWO.append(flood_depth_pt_two)
            if flood_depth_pt_two < -0.5:
                damage_index_str_pt_two = 0
                damage_index_con_pt_two = 0
            else:
                damage_index_str_pt_two = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_pt_two,k['VULN_MODEL']])
                damage_index_con_pt_two = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_pt_two,k['VULN_MODEL']])
            damage_index_str_pt_two = np.clip(damage_index_str_pt_two, 0, 1)
            damage_index_con_pt_two = np.clip(damage_index_con_pt_two, 0, 1)
            DI_STR_PT_TWO.append(damage_index_str_pt_two)
            str_damage_pt_two = damage_index_str_pt_two * k['REP_VAL_2']*(1+str_adj)
            STR_DAM_PT_TWO.append(str_damage_pt_two)
            DI_CON_PT_TWO.append(damage_index_con_pt_two)
            con_damage_pt_two = damage_index_con_pt_two * k['CON_VAL']*(1+con_adj)
            CON_DAM_PT_TWO.append(con_damage_pt_two)
            total_value_pt_two = str_damage_pt_two + con_damage_pt_two
            TOTAL_DAM_PT_TWO.append(total_value_pt_two)
            if k['EST_FLR_LVL_R'] < k['0.2%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)            
            NO_HOUSES_PT_TWO.append(House_flood)
#            NO_PPL_PT_TWO.append(People)
            
            flood_depth_pt_five = round(k['0.5%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_PT_FIVE.append(flood_depth_pt_five)
            if flood_depth_pt_five < -0.5:
                damage_index_str_pt_five = 0
                damage_index_con_pt_five = 0
            else:
                damage_index_str_pt_five = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_pt_five,k['VULN_MODEL']])
                damage_index_con_pt_five = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_pt_five,k['VULN_MODEL']])
            damage_index_str_pt_five = np.clip(damage_index_str_pt_five, 0, 1)
            damage_index_con_pt_five = np.clip(damage_index_con_pt_five, 0, 1)        
            DI_STR_PT_FIVE.append(damage_index_str_pt_five)
            str_damage_pt_five = damage_index_str_pt_five * k['REP_VAL_2']*(1+str_adj)
            STR_DAM_PT_FIVE.append(str_damage_pt_five)
            DI_CON_PT_FIVE.append(damage_index_con_pt_five)
            con_damage_pt_five = damage_index_con_pt_five * k['CON_VAL']*(1+con_adj)
            CON_DAM_PT_FIVE.append(con_damage_pt_five)
            total_value_pt_five = str_damage_pt_five + con_damage_pt_five
            TOTAL_DAM_PT_FIVE.append(total_value_pt_five)
            if k['EST_FLR_LVL_R'] < k['0.5%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)
            NO_HOUSES_PT_FIVE.append(House_flood)
#            NO_PPL_PT_FIVE.append(People)
          
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
                damage_index_str_one = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_one,k['VULN_MODEL']])
                #Look up damage index for contents (insured, saved goods)
                damage_index_con_one = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_one,k['VULN_MODEL']])
                # Clip out any damage index values less than zero or more than 1 (as adjusted by D_I value)
            damage_index_str_one = np.clip(damage_index_str_one, 0, 1)
            damage_index_con_one = np.clip(damage_index_con_one, 0, 1)
            DI_STR_ONE.append(damage_index_str_one)
            #Calculate structural damage (building fabric; insured]
            str_damage_one = damage_index_str_one * k['REP_VAL_2']*(1+str_adj)
            STR_DAM_ONE.append(str_damage_one)
            DI_CON_ONE.append(damage_index_con_one)
            #Calculate contents damage
            con_damage_one = damage_index_con_one * k['CON_VAL']*(1+con_adj)
            CON_DAM_ONE.append(con_damage_one)
            #Calculate total damages (strutural and contents)
            total_value_one = str_damage_one + con_damage_one
            TOTAL_DAM_ONE.append(total_value_one)
            ### EXTRA - number of houses in 1% floodplain
            if k['EST_FLR_LVL_R'] < k['1%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)            
            NO_HOUSES_ONE.append(House_flood)
#            NO_PPL_ONE.append(People)
        
        # Repeat for AEP 2%, 5%, 10%
            flood_depth_two = round(k['2%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_TWO.append(flood_depth_two)
            if flood_depth_two < -0.5:
                damage_index_str_two = 0
                damage_index_con_two = 0
            else:
                damage_index_str_two = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_two,k['VULN_MODEL']])
                damage_index_con_two = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_two,k['VULN_MODEL']])
            damage_index_str_two = np.clip(damage_index_str_two, 0, 1)
            damage_index_con_two = np.clip(damage_index_con_two, 0, 1)
            DI_STR_TWO.append(damage_index_str_two)
            str_damage_two = damage_index_str_two * k['REP_VAL_2']*(1+str_adj)
            STR_DAM_TWO.append(str_damage_two)
            DI_CON_TWO.append(damage_index_con_two)     
            con_damage_two = damage_index_con_two * k['CON_VAL']*(1+con_adj)
            CON_DAM_TWO.append(con_damage_two)
            total_value_two = str_damage_two + con_damage_two
            TOTAL_DAM_TWO.append(total_value_two)
            if k['EST_FLR_LVL_R'] < k['2%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)            
            NO_HOUSES_TWO.append(House_flood)      
#            NO_PPL_TWO.append(People)
#          
            flood_depth_five = round(k['5%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_FIVE.append(flood_depth_five)
            if flood_depth_five < -0.5:
                damage_index_str_five = 0
                damage_index_con_five = 0
            else:
                damage_index_str_five = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_five,k['VULN_MODEL']])
                damage_index_con_five = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_five,k['VULN_MODEL']])
            damage_index_str_five = np.clip(damage_index_str_five, 0, 1)
            damage_index_con_five = np.clip(damage_index_con_five, 0, 1)
            DI_STR_FIVE.append(damage_index_str_five)
            str_damage_five = damage_index_str_five * k['REP_VAL_2']*(1+str_adj)
            STR_DAM_FIVE.append(str_damage_five)
            DI_CON_FIVE.append(damage_index_con_five)     
            con_damage_five = damage_index_con_five * k['CON_VAL']*(1+con_adj)
            CON_DAM_FIVE.append(con_damage_five)
            total_value_five = str_damage_five + con_damage_five
            TOTAL_DAM_FIVE.append(total_value_five)
            if k['EST_FLR_LVL_R'] < k['5%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)            
            NO_HOUSES_FIVE.append(House_flood)        
#            NO_PPL_FIVE.append(People)        
#            
            flood_depth_ten = round(k['10%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_TEN.append(flood_depth_ten)
            if flood_depth_ten < -0.5:
                damage_index_str_ten = 0
                damage_index_con_ten = 0
            else:
                damage_index_str_ten = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_ten,k['VULN_MODEL']])
                damage_index_con_ten = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_ten,k['VULN_MODEL']])
            damage_index_str_ten = np.clip(damage_index_str_ten, 0, 1)
            damage_index_con_ten = np.clip(damage_index_con_ten, 0, 1)
            DI_STR_TEN.append(damage_index_str_ten)
            str_damage_ten = damage_index_str_ten * k['REP_VAL_2']*(1+str_adj)
            STR_DAM_TEN.append(str_damage_ten)
            DI_CON_TEN.append(damage_index_con_ten)     
            con_damage_ten = damage_index_con_ten * k['CON_VAL']*(1+con_adj)
            CON_DAM_TEN.append(con_damage_ten)
            total_value_ten = str_damage_ten + con_damage_ten
            TOTAL_DAM_TEN.append(total_value_ten)
            if k['EST_FLR_LVL_R'] < k['10%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)            
            NO_HOUSES_TEN.append(House_flood)    
#            NO_PPL_TEN.append(People)
        
            flood_depth_twenty = round(k['20%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_TWENTY.append(flood_depth_twenty)
            if flood_depth_twenty < -0.5:
                damage_index_str_twenty = 0
                damage_index_con_twenty = 0
            else:
                damage_index_str_twenty = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_twenty,k['VULN_MODEL']])
                damage_index_con_twenty = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_twenty,k['VULN_MODEL']])  
            damage_index_str_twenty = np.clip(damage_index_str_twenty, 0, 1)
            damage_index_con_twenty = np.clip(damage_index_con_twenty, 0, 1)
            DI_STR_TWENTY.append(damage_index_str_twenty)
            str_damage_twenty = damage_index_str_twenty * k['REP_VAL_2']*(1+str_adj)
            STR_DAM_TWENTY.append(str_damage_twenty)                  
            DI_CON_TWENTY.append(damage_index_con_twenty)
            con_damage_twenty = damage_index_con_twenty * k['CON_VAL']*(1+con_adj)
            CON_DAM_TWENTY.append(con_damage_twenty)
            total_value_twenty = str_damage_twenty + con_damage_twenty
            TOTAL_DAM_TWENTY.append(total_value_twenty)
            if k['EST_FLR_LVL_R'] < k['20%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)            
            NO_HOUSES_TWENTY.append(House_flood)
#            NO_PPL_TWENTY.append(People)

            flood_depth_forty = round(k['40%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_FORTY.append(flood_depth_forty)
            if flood_depth_forty < -0.5:
                damage_index_str_forty = 0
                damage_index_con_forty = 0
            else:
                damage_index_str_forty = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_forty,k['VULN_MODEL']])
                damage_index_con_forty = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_forty,k['VULN_MODEL']])  
            damage_index_str_forty = np.clip(damage_index_str_forty, 0, 1)
            damage_index_con_forty = np.clip(damage_index_con_forty, 0, 1)
            DI_STR_FORTY.append(damage_index_str_forty)
            str_damage_forty = damage_index_str_forty * k['REP_VAL_2']*(1+str_adj)
            STR_DAM_FORTY.append(str_damage_forty)                  
            DI_CON_FORTY.append(damage_index_con_forty)
            con_damage_forty = damage_index_con_forty * k['CON_VAL']*(1+con_adj)
            CON_DAM_FORTY.append(con_damage_forty)
            total_value_forty = str_damage_forty + con_damage_forty
            TOTAL_DAM_FORTY.append(total_value_forty)
            if k['EST_FLR_LVL_R'] < k['40%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)            
            NO_HOUSES_FORTY.append(House_flood)
#            NO_PPL_FORTY.append(People)

            flood_depth_sixty = round(k['60%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_SIXTY.append(flood_depth_sixty)
            if flood_depth_sixty < -0.5:
                damage_index_str_sixty = 0
                damage_index_con_sixty = 0
            else:
                damage_index_str_sixty = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_sixty,k['VULN_MODEL']])
                damage_index_con_sixty = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_sixty,k['VULN_MODEL']])  
            damage_index_str_sixty = np.clip(damage_index_str_sixty, 0, 1)
            damage_index_con_sixty = np.clip(damage_index_con_sixty, 0, 1)
            DI_STR_SIXTY.append(damage_index_str_sixty)
            str_damage_sixty = damage_index_str_sixty * k['REP_VAL_2']*(1+str_adj)
            STR_DAM_SIXTY.append(str_damage_sixty)                  
            DI_CON_SIXTY.append(damage_index_con_sixty)
            con_damage_sixty = damage_index_con_sixty * k['CON_VAL']*(1+con_adj)
            CON_DAM_SIXTY.append(con_damage_sixty)
            total_value_sixty = str_damage_sixty + con_damage_sixty
            TOTAL_DAM_SIXTY.append(total_value_sixty)
            if k['EST_FLR_LVL_R'] < k['60%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)            
            NO_HOUSES_SIXTY.append(House_flood)
#            NO_PPL_SIXTY.append(People)

            flood_depth_ninety = round(k['90%_AEP']-k['EST_FLR_LVL_R'],1)
            FLD_DEP_NINETY.append(flood_depth_ninety)
            if flood_depth_ninety < -0.5:
                damage_index_str_ninety = 0
                damage_index_con_ninety = 0
            else:
                damage_index_str_ninety = float(vuln_model_str.loc[vuln_model_str['WATER DEPTH (m)']==flood_depth_ninety,k['VULN_MODEL']])
                damage_index_con_ninety = float(vuln_model_con.loc[vuln_model_con['WATER DEPTH (m)']==flood_depth_ninety,k['VULN_MODEL']])  
            damage_index_str_ninety = np.clip(damage_index_str_ninety, 0, 1)
            damage_index_con_ninety = np.clip(damage_index_con_ninety, 0, 1)
            DI_STR_NINETY.append(damage_index_str_ninety)
            str_damage_ninety = damage_index_str_ninety * k['REP_VAL_2']*(1+str_adj)
            STR_DAM_NINETY.append(str_damage_ninety)                  
            DI_CON_NINETY.append(damage_index_con_ninety)
            con_damage_ninety = damage_index_con_ninety * k['CON_VAL']*(1+con_adj)
            CON_DAM_NINETY.append(con_damage_ninety)
            total_value_ninety = str_damage_ninety + con_damage_ninety
            TOTAL_DAM_NINETY.append(total_value_ninety)
            if k['EST_FLR_LVL_R'] < k['90%_AEP']:
                House_flood = 1
#                if k['AV_PPL_DWL'] > 0:
#                    People = k['AV_PPL_DWL']*(1+r_ppl*year_ppl)
#                else:
#                    People = 0
            else:
                House_flood = 0
#                People = 0
#            People = np.clip(People,0,None)            
            NO_HOUSES_NINETY.append(House_flood)
#            NO_PPL_NINETY.append(People)

        
        ## CALCULATING THE AVERAGE ANNUAL PEOPLE EXPOSED
        slr_name = int(100*round(j['aep_pt_one'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner') #Select rows where the Arc_ID matches between prop_impact and those properties affected by flooding at this flood level as determined in ArcGIS
        ppl_pt_one = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl) #sum AV_PPL for hosues remaining and also affected by flooding
        ppl_pt_one = np.clip(ppl_pt_one, 0, None) #clip at zero as your cannot have negative people (e.g. may be needed if negative growth over time)       
        NO_PPL_PT_ONE.append(ppl_pt_one)

        slr_name = int(100*round(j['aep_pt_two'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner')
        ppl_pt_two = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl)
        ppl_pt_two = np.clip(ppl_pt_two, 0, None)
        NO_PPL_PT_TWO.append(ppl_pt_two)
    
        slr_name = int(100*round(j['aep_pt_five'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner')  
        ppl_pt_five = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl)
        ppl_pt_five = np.clip(ppl_pt_five, 0, None)        
        NO_PPL_PT_FIVE.append(ppl_pt_five)    
        
        slr_name = int(100*round(j['aep_one'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner')  
        ppl_one = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl)
        ppl_one = np.clip(ppl_one, 0, None)        
        NO_PPL_ONE.append(ppl_one)    
        
        slr_name = int(100*round(j['aep_two'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner')  
        ppl_two = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl)
        ppl_two = np.clip(ppl_two, 0, None)         
        NO_PPL_TWO.append(ppl_two)    
        
        slr_name = int(100*round(j['aep_five'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner')  
        ppl_five = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl)
        ppl_five = np.clip(ppl_five, 0, None)         
        NO_PPL_FIVE.append(ppl_five)     
        
        slr_name = int(100*round(j['aep_ten'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner')  
        ppl_ten = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl)
        ppl_ten = np.clip(ppl_ten, 0, None)         
        NO_PPL_TEN.append(ppl_ten)     
        
        slr_name = int(100*round(j['aep_twenty'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner')  
        ppl_twenty = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl)
        ppl_twenty = np.clip(ppl_twenty, 0, None)         
        NO_PPL_TWENTY.append(ppl_twenty) 
    
        slr_name = int(100*round(j['aep_forty'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner')  
        ppl_forty = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl)
        ppl_forty = np.clip(ppl_forty, 0, None)         
        NO_PPL_FORTY.append(ppl_forty)
    
        slr_name = int(100*round(j['aep_sixty'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner')  
        ppl_sixty = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl)
        ppl_sixty = np.clip(ppl_sixty, 0, None)         
        NO_PPL_SIXTY.append(ppl_sixty)
    
        slr_name = int(100*round(j['aep_ninety'],2))        
        Comparing_list = pd.read_csv("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
        Merging = pd.merge(prop_impact, Comparing_list, on=['Arc_ID'], how='inner')  
        ppl_ninety = (sum(Merging['AV_PPL_DWL']))*(1+r_ppl*year_ppl)
        ppl_ninety = np.clip(ppl_ninety, 0, None)         
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
        
#        Sum the total number of houses impacts     
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
    
        # clear the contents to avoid duplication in the next iteration
#        TOTAL_DAM_PT_ONE = [] 
#        TOTAL_DAM_PT_TWO = [] 
#        TOTAL_DAM_PT_FIVE = [] 
#        TOTAL_DAM_ONE = []               
#        TOTAL_DAM_TWO = []                  
#        TOTAL_DAM_FIVE = []
#        TOTAL_DAM_TEN = []
#        TOTAL_DAM_PT_TWENTY = [] 
###        NO_HOUSES_PT_ONE = []
###        NO_HOUSES_PT_TWO = []
###        NO_HOUSES_PT_FIVE = []
#        NO_HOUSES_ONE = []
##        NO_HOUSES_TWO = []
##        NO_HOUSES_FIVE = []
##        NO_HOUSES_TEN = []
##        NO_HOUSES_TWENTY = []
##        NO_PPL_PT_ONE = []
##        NO_PPL_PT_TWO = []    
##        NO_PPL_PT_FIVE = []
#        NO_PPL_ONE = []
##        NO_PPL_TWO = []
##        NO_PPL_FIVE = []
#        NO_PPL_TEN = []
#        NO_PPL_TWENTY = []
    
    #Append the results to the time-series realisation
    annual_MSL['0.1%_AEP_IMP'] = AEP_PT_ONE_IMP
    annual_MSL['0.2%_AEP_IMP'] = AEP_PT_TWO_IMP
    annual_MSL['0.5%_AEP_IMP'] = AEP_PT_FIVE_IMP
    annual_MSL['1%_AEP_IMP'] = AEP_ONE_IMP
    annual_MSL['2%_AEP_IMP'] = AEP_TWO_IMP
    annual_MSL['5%_AEP_IMP'] = AEP_FIVE_IMP
    annual_MSL['10%_AEP_IMP'] = AEP_TEN_IMP
    annual_MSL['20%_AEP_IMP'] = AEP_TWENTY_IMP
    annual_MSL['40%_AEP_IMP'] = AEP_FORTY_IMP    
    annual_MSL['60%_AEP_IMP'] = AEP_SIXTY_IMP    
    annual_MSL['90%_AEP_IMP'] = AEP_NINETY_IMP    
    annual_MSL['Houses_0.1%'] = SUM_HOUSES_PT_ONE
    annual_MSL['Houses_0.2%'] = SUM_HOUSES_PT_TWO
    annual_MSL['Houses_0.5%'] = SUM_HOUSES_PT_FIVE
    annual_MSL['Houses_1%'] = SUM_HOUSES_ONE    
    annual_MSL['Houses_2%'] = SUM_HOUSES_TWO
    annual_MSL['Houses_5%'] = SUM_HOUSES_FIVE
    annual_MSL['Houses_10%'] = SUM_HOUSES_TEN
    annual_MSL['Houses_20%'] = SUM_HOUSES_TWENTY
    annual_MSL['Houses_40%'] = SUM_HOUSES_FORTY
    annual_MSL['Houses_60%'] = SUM_HOUSES_SIXTY
    annual_MSL['Houses_90%'] = SUM_HOUSES_NINETY            
    annual_MSL['0.1%_AEP_PPL'] = SUM_PPL_PT_ONE
    annual_MSL['0.2%_AEP_PPL'] = SUM_PPL_PT_TWO
    annual_MSL['0.5%_AEP_PPL'] = SUM_PPL_PT_FIVE
    annual_MSL['1%_AEP_PPL'] = SUM_PPL_ONE
    annual_MSL['2%_AEP_PPL'] = SUM_PPL_TWO
    annual_MSL['5%_AEP_PPL'] = SUM_PPL_FIVE
    annual_MSL['10%_AEP_PPL'] = SUM_PPL_TEN
    annual_MSL['20%_AEP_PPL'] = SUM_PPL_TWENTY   
    annual_MSL['40%_AEP_PPL'] = SUM_PPL_FORTY   
    annual_MSL['60%_AEP_PPL'] = SUM_PPL_SIXTY   
    annual_MSL['90%_AEP_PPL'] = SUM_PPL_NINETY   
   
    for index, z in annual_MSL.iterrows():
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
        
        aa = z['Houses_0.1%']
        ab = z['Houses_0.2%']
        ac = z['Houses_0.5%']
        ad = z['Houses_1%']
        ae = z['Houses_2%']
        af = z['Houses_5%']
        ag = z['Houses_10%']
        ah = z['Houses_20%']
        ai = z['Houses_40%']
        aj = z['Houses_60%']
        ak = z['Houses_90%']    
        
        aad =  float(np.trapz([a,b,c,d,e,f,g,h,i,j,k],x=[0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.4,0.6,0.9]))
        aape = float(np.trapz([l,m,n,o,p,q,r,s,t,u,v],x=[0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.4,0.6,0.9]))

        aah = float(np.trapz([aa,ab,ac,ad,ae,af,ag,ah,ai,aj,ak],x=[0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.4,0.6,0.9]))              
        
        AAD.append(aad)
        AAPE.append(aape)
        AAH.append(aah)
       
    annual_MSL["AAD"]=AAD
    annual_MSL["AAPE"] = AAPE
    annual_MSL["AAH"] = AAH
    annual_MSL
   
          
    ax1 = plt.subplot(411)
    plt.plot(annual_MSL['Year_Date'],annual_MSL['SLR_proj_m'])
#    plt.axhline(y=BL_Esp_lvl, xmin=0, xmax=1, linewidth=1, color = 'k', linestyle = '-.')   
#    plt.text(2020, BL_Esp_lvl+0.2, "ATP = " + str(BL_Esp_lvl) + "m")
    plt.ylabel('SLR (m)',fontsize = 8)
    plt.yticks(np.arange(0,2.6,0.5))
    plt.title('Changing AAD and AAPE risk with time')    
    ax1.set_xticklabels([])
    ax2 = plt.subplot(412)
    plt.plot(annual_MSL['Year_Date'],annual_MSL['AAH'])
    plt.ylabel('AAP (prop/yr)',fontsize = 8)
    plt.yticks(np.arange(0,801,400))
    ax2.set_xticklabels([])
#    ax3 = plt.subplot(413)
#    plt.plot(annual_MSL['Year_Date'],annual_MSL['rate_str'])
#    plt.ylabel('r_str ($/m2)')
#    plt.yticks(np.arange(0,12000,3000))
#    ax3.set_xticklabels([])
    ax3 = plt.subplot(413)
    plt.plot(annual_MSL['Year_Date'],annual_MSL['AAD'])     #PROB NEED TO USE PV_AAD FOR VULN?
    plt.axhline(y=BL_AAD_risk, xmin=0, xmax=1, linewidth=1, color = 'k', linestyle = '-.')
    plt.text(2020, BL_AAD_risk*3, "ATP = $" + str(BL_AAD_risk) + " /yr")
    plt.ylabel('AAD ($/yr)',fontsize = 8)
    plt.yticks(np.arange(0,60000001,20000000))
#    plt.xlim(2010,2120)
#    plt.xlabel('Time (year)')
    ax3.set_xticklabels([])
    ax4 = plt.subplot(414)
    plt.plot(annual_MSL['Year_Date'],annual_MSL['AAPE'])     #PROB NEED TO USE PV_AAD FOR VULN?
    plt.axhline(y=BL_AAPE_risk, xmin=0, xmax=1, linewidth=1, color = 'k', linestyle = '-.')
    plt.text(2020, BL_AAPE_risk*5, "ATP = " + str(BL_AAPE_risk) + " ppl/yr")
    plt.ylabel('AAPE (ppl/yr)',fontsize = 8)
    plt.yticks(np.arange(0,1501,500))
    plt.xlim(2010,2100)
    plt.xlabel('Time (year)') 
   

    BL_slice_trial = annual_MSL[annual_MSL['AAD']<BL_AAD_risk]
    BL_slice_last = BL_slice_trial[-1:]    #Select bottom value - http://www.datacarpentry.org/python-ecology-lesson/02-index-slice-subset/ 
    BL_slice_last
    Case_year = int(BL_slice_last['Year_Date'])
    SIGNPOST.append(Case_year)

    if annual_MSL.loc[annual_MSL['Year']==0, ['AAPE']].ix[0,"AAPE"]>BL_AAPE_risk:
        Case_year_1= 2018
    else:
        BL_slice_trial_1 = annual_MSL[annual_MSL['AAPE']<BL_AAPE_risk]
        BL_slice_last_1 = BL_slice_trial_1[-1:]    #Select bottom value - http://www.datacarpentry.org/python-ecology-lesson/02-index-slice-subset/ 
        BL_slice_last_1
        Case_year_1 = int(BL_slice_last_1['Year_Date'])
    SIGNPOST_AAPE.append(Case_year_1)

    BL_slice_trial_2 = annual_MSL[annual_MSL['SLR_proj_m']<BL_Esp_lvl]
    BL_slice_last_2 = BL_slice_trial_2[-1:]    #Select bottom value - http://www.datacarpentry.org/python-ecology-lesson/02-index-slice-subset/ 
    BL_slice_last_2
    Case_year_2 = int(BL_slice_last_2['Year_Date'])
    SIGNPOST_ESP.append(Case_year_2)

#
## NOTE THIS IS THE FILE IN THE LAST YEAR OF THE LAST ANNUAL_MSL SCENARIO
#Property_outfile_one = "C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\"+date_string+"_Prop_Impact_op3.csv"
#prop_impact.to_csv(Property_outfile_one) 
#
## NOTE THIS IS THE FILE IN THE LAST CASE SCENARIO
#annual_MSL_outfile_two = "C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\"+date_string+"_annual_msl_op3.csv"
#annual_MSL.to_csv(annual_MSL_outfile_two) 

cases_dapp["ATP_AAD"]=SIGNPOST
sign_median = int(np.median(cases_dapp['ATP_AAD']))        # Calculate the median
sign_max = max(cases_dapp['ATP_AAD'])
sign_min = min(cases_dapp['ATP_AAD'])

cases_dapp["ATP_AAPE"]=SIGNPOST_AAPE
sign_median1 = int(np.median(cases_dapp['ATP_AAPE']))        # Calculate the median
sign_max1 = max(cases_dapp['ATP_AAPE'])
sign_min1 = min(cases_dapp['ATP_AAPE'])

cases_dapp["ATP_ESP"]=SIGNPOST_ESP
sign_median2 = int(np.median(cases_dapp['ATP_ESP']))        # Calculate the median
sign_max2 = max(cases_dapp['ATP_ESP'])
sign_min2 = min(cases_dapp['ATP_ESP'])


print "Below is a time-series plot of all cases assessed. The bottom panel is AAD ($/year)."
fig.savefig('C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\'+date_string+'_scenarios_op3'+'.png',dpi=300,bbox_inches='tight')
plt.show()

###############################################################################
## COULD PLOT OPTIONS NEXT TO THIS
print "Below is a box plot of used-by year for each case at which factor describing ATP is reached (risk no longer acceptable)"
fig2 = plt.figure()


#https://matplotlib.org/examples/pylab_examples/subplots_demo.html


ax10 = plt.subplot(121)
plt.boxplot([cases_dapp['ATP_AAD'].values])   # .values added to avoid a "KeyError: 0L"
plt.xticks([1],["Option 3: Land use change"])
plt.ylim(min(cases_dapp['ATP_AAD'])-5)
plt.ylim(2015,2100) # Years
#plt.xlabel('Existing System')
plt.ylabel('Year')
plt.text(1.1, sign_median, "Median = " + str(sign_median), fontsize = 7)
plt.text(1.1, sign_max-2, "Max = " + str(sign_max), fontsize = 7)
plt.text(1.1, sign_min, "Min = " + str(sign_min), fontsize = 7)
plt.text(1.1, np.percentile(cases_dapp["ATP_AAD"],25), "Q1 = " + str(int(np.percentile(cases_dapp["ATP_AAD"],25))), fontsize = 7)
plt.text(1.1, np.percentile(cases_dapp["ATP_AAD"],75), "Q3 = " + str(int(np.percentile(cases_dapp["ATP_AAD"],75))), fontsize = 7)
plt.title('(a) AAD')

ax11 = plt.subplot(122)
plt.boxplot([cases_dapp['ATP_AAPE'].values])   # .values added to avoid a "KeyError: 0L"
plt.xticks([1],["Option 3: Land use change"])
plt.ylim(min(cases_dapp['ATP_AAPE'])-5)
plt.ylim(2015,2100) # Years
#plt.xlabel('Existing System')
#ax11.set_yticklabels([])
#plt.ylabel('Year')
plt.text(1.1, sign_median1-6, "Median = " + str(sign_median1),fontsize = 7)
plt.text(1.1, sign_max1 -2, "Max = " + str(sign_max1), fontsize = 7)
plt.text(1.1, sign_min1, "Min = " + str(sign_min1), fontsize = 7)
plt.text(1.1, np.percentile(cases_dapp["ATP_AAPE"],25), "Q1 = " + str(int(np.percentile(cases_dapp["ATP_AAPE"],25))), fontsize = 7)
plt.text(1.1, np.percentile(cases_dapp["ATP_AAPE"],75)-4, "Q3 = " + str(int(np.percentile(cases_dapp["ATP_AAPE"],75))), fontsize = 7)
plt.title('(b) AAPE')

#ax12 = plt.subplot(133)
#plt.boxplot([cases_dapp['ATP_ESP'].values])   # .values added to avoid a "KeyError: 0L"
#plt.xticks([1],["No policy"])
#plt.ylim(min(cases_dapp['ATP_ESP'])-5)
#plt.ylim(2015,2100) # Years
##plt.xlabel('Existing System')
##ax11.set_yticklabels([])
##plt.ylabel('Year')
#plt.text(1.1, sign_median2, "Median = " + str(sign_median2),fontsize = 7)
#plt.text(1.1, sign_max2 - 3, "Max = " + str(sign_max2), fontsize = 7)
#plt.text(1.1, sign_min2, "Min = " + str(sign_min2), fontsize = 7)
#plt.title('Timing when AAPE unacceptable')

fig2.savefig('C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\'+date_string+'_boxplot_op3'+'.png',dpi=300)
plt.show()


np.percentile(cases_dapp["ATP_AAPE"],25) #25th percentile
np.percentile(cases_dapp["ATP_AAPE"],50) #50th percentile
np.percentile(cases_dapp["ATP_AAPE"],75) #75th percentile

np.percentile(cases_dapp["ATP_AAD"],25)
np.percentile(cases_dapp["ATP_AAD"],50)
np.percentile(cases_dapp["ATP_AAD"],75)

np.percentile(cases_dapp["ATP_ESP"],25)
np.percentile(cases_dapp["ATP_ESP"],50)
np.percentile(cases_dapp["ATP_ESP"],75)

#print "Below is a box plot of used-by year for each case at which factor describing ATP is reached (risk no longer acceptable)"
#fig3 = plt.figure()
#plt.boxplot([cases_dapp['ATP_AAPE'].values])   # .values added to avoid a "KeyError: 0L"
#plt.xticks([1],["Existing System"])
#plt.ylim(min(cases_dapp['ATP_AAPE'])-5)
#plt.ylim(2015,2050) # Years
##plt.xlabel('Existing System')
#plt.ylabel('Year')
#plt.text(1.1, sign_median1, "Median = " + str(sign_median1))
#plt.text(1.1, sign_max1 - 1, "Max = " + str(sign_max1))
#plt.text(1.1, sign_min1, "Min = " + str(sign_min1))
#plt.title('Timing at which AAPE becomes unacceptable')


Cases_outfile_two = "C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\"+date_string+"_Case_Results_DAPP_OPTION3.csv"
cases_dapp.to_csv(Cases_outfile_two) 


t1 = time.clock()
tdiff = t1 - t0
tmin = tdiff/60
thour = tmin/60
print "It took %.3f seconds for this code to run" % (tdiff) + " (%.2f mins " % (tmin) + "/ %.2f hours)" % (thour) +" to run " + str(case)+" scenarios"
