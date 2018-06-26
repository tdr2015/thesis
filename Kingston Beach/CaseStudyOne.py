# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 09:20:53 2017

@author: tdramm

PilotTwo.py -   The script estimates the average annual number of people 
                exposed to flooding, the average annual monetary impacts to 
                private dwellings for different coastal inundation 
                events and the average beach width (Kingston Beach) for 
                changing sea-levels. Different scenarios reflect 
                combinations of uncertain parameters. The inundation events 
                considered includes (1) permanent sea-level rise (i.e. loss) 
                and (2) temporary riverine flooding (Browns River). The script 
                calls upon the ArcPy module to apply geoprocessing tools for 
                undertaking spatial analysis. Open source data sets from 
                TheLIST are used, and the results of the analysis are exported
                in .csv file. Analysis using Scenario Discovery (i.e. Robust 
                decision making) can then be undertaken.

"""


###############################################################################
# IMPORT PACKAGES
# Import arcpy module
import arcpy
# Pandas module used for importing csv as data frame and making float data type
import pandas as pd
# For TableToNumPyArray used with raster data
import numpy as np
# import math package for 'exp' function (extreme sea levels)
import math
# Import time package
import time

###############################################################################
# SET UP LICENSES AND WORKING ENVIRONMENT
# Check ArcGIS out license
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension("3D")
# Set Geoprocessing overwrite option
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = "C:\\Users\\tdramm\\Desktop\\GIS\\ScratchConcept.gbd"
arcpy.env.workspace = "C:\\Users\\tdramm\\Desktop\\GIS\\Concept.gdb"
# Set raster snapping"
arcpy.env.snapRaster = "C:\\Users\\tdramm\\Desktop\\GIS\\Concept.gdb\\ldrclip2m"
# Set Geoprocessing environments for analysis (Left, Bottom, Right, Top)
# Same extent as MWHS_ldrclip2m; coordinate systems same as inputs by default; coordinates as Xmin, Ymin, Xmax, Ymax
arcpy.env.extent = "524950 5239950 527847 5243050"
# Make cell size 2m to speed up processing
arcpy.env.cellSize = "2"
arcpy.env.mask = ""

###############################################################################
# SET-UP TIMER FOR CODE - START CLOCK
## Timer
t0 = time.clock()

###############################################################################
# CONSTANT VALUES
CONDITION_TRUE = "1"
#MHWS 0.62m above AHD in study area (Kingborough Council)
MHWS_ADJUST = "0.62"
# Maximum damage per 4m2 (NEXIS Building Exposure database (Mar 2016 prices) = [Residential footprint]/[Structural Value])
#MAX_DAMAGE = "5750"
#MAX_CONTENTS_DAMAGE = float(1050)
CORRECTION_TWO = "0.4"
CORRECTION_FIVE = "0.8"
# ABS data (Quickstats) says average of 2.3 people per househould
# http://www.censusdata.abs.gov.au/census_services/getproduct/census/2011/quickstat/SSC60179?opendocument&navpos=220
AV_PPL_HOUSE = 2.3
# Initial script argument (parameter for sea-level constant raster)
#CONSTANT_SLR = arcpy.GetParameterAsText(0)
#if CONSTANT_SLR == '#' or not CONSTANT_SLR:
#    CONSTANT_SLR = "2" # provide a default value if unspecified

# LOCAL VARIABLES (on desktop C:)
# Define input path and output path to geodatabase
inpath = "C:\\Users\\tdramm\\Desktop\\GIS\\Concept.gdb\\"
outpath = inpath

# Define local variables
Area_of_Interest = "in_memory\\{6E39D316-8734-4301-A45A-25836C63FEC1}"
ldrclip2m = inpath + "ldrclip2m"
T2DLanduse_Buildings = inpath+"T2DLanduse_Buildings"
interim_planning_scheme_zoning_statewide = inpath+"interim_planning_scheme_zoning_statewide"
list_transport_segments_kingborough = inpath+"list_transport_segments_kingborough"
beachtrans1 = inpath + "beachtrans1"
beachtrans2 = inpath + "beachtrans2"
beachtrans3 = inpath + "beachtrans3"
beachtrans4 = inpath + "beachtrans4"
beachtrans5 = inpath + "beachtrans5"

MWHS_ldrclip2m = "MWHS_ldrclip2m"
slr_surface = "slr_surface"
slr_extent = "slr_extent"
slr_ext_con = "slr_ext_con"
slrgroup = "slrgroup"
slr_poly = "slr_poly"
max_slr_poly = "max_slr_poly"
beachwid1 ="beachwid1"
beachwid2 ="beachwid2"
beachwid3 ="beachwid3"
beachwid4 ="beachwid4"
beachwid5 ="beachwid5"
Buildings = "Buildings"
diffslr = "diffslr"
slrdepth = "slrdepth"
#Selected = T2DLanduse_Buildings
private_houses = "private_houses"
houserisk = "houserisk"
private_land = "private_land"
privland = "privland"
privateland = "privateland"
public_road = "public_road"
roads = "roads"
sealedroad = "sealedroad"
sealed = "sealed"
diffslr = "diffslr"
house_loss = "house_loss"
slr_bruun = "slr_bruun"  

fld_extent = "fld_extent"
fld_ext_con = "fld_ext_con"
fld_poly = "fld_poly"
fld_poly_sel = "fld_poly_sel"
max_fld_poly = "max_fld_poly"
difffld = "difffld"
flddepth = "flddepth"
houserisk1 = "houserisk1"
house_dam1 = "house_dam1"

fld_extent2 = "fld_extent2"
fld_ext_con2 = "fld_ext_con2"
fld_poly2 = "fld_poly2"
fld_poly_sel2 = "fld_poly_sel2"
max_fld_poly2 = "maz_fld_poly2"
difffld2 = "difffld2"
flddepth2 = "flddepth2"
houserisk2 = "houserisk2"
house_dam2 = "house_dam2"

fld_extent5 = "fld_extent5"
fld_ext_con5 = "fld_ext_con5"
fld_poly5 = "fld_poly5"
fld_poly_sel5 = "fld_poly_sel5"
max_fld_poly5 = "max_fld_poly5"
difffld5 = "difffld5"
flddepth5 = "flddepth5"
houserisk5 = "houserisk5"
house_dam5 = "house_dam5"

fld_extent20 = "fld_extent20"
fld_ext_con20 = "fld_ext_con20"
fld_poly20 = "fld_poly20"
fld_poly_sel20 = "fld_poly_sel20"      
max_fld_poly20 = "max_fld_poly20"      
difffld20 = "difffld20"
flddepth20 = "flddepth20"
houserisk20 = "houserisk20"
house_dam20 = "house_dam20"


#leveedem2m = inpath + "leveedem2m"

##OPTION 1 - LEVEE 
#zzfldext_op1 = inpath +"zzfldext_op1"
#zzzfldext_op1 = inpath + "zzzfldext_op1"
#zzfldpoly_op1 = inpath + "zzfldpoly_op1"
#fldpolya_op1 = inpath + "fldpolya_op1"
#fldpoly_op1 = inpath + "fldpoly_op1"
#difffld_op1 = inpath + "difffld_op1"  
#flddepth_op1 = inpath+ "flddepth_op1"
#houserisk1_op1 = inpath + "houserisk1_op1"
#temphouse1_op1 = inpath + "temphouse1_op1"
#flddamarray_op1 = inpath + "flddamarray_op1"

#zzfldext2_op1 = inpath +"zzfldext2_op1"
#zzzfldext2_op1 = inpath + "zzzfldext2_op1"
#zzfldpoly2_op1 = inpath + "zzfldpoly2_op1"
#fldpoly2a_op1 = inpath + "fldpoly2a_op1"
#fldpoly2_op1 = inpath + "fldpoly2_op1"
#difffld2_op1 = inpath + "difffld2_op1"  
#flddepth2_op1 = inpath+ "flddepth2_op1"
#houserisk2_op1 = inpath + "houserisk2_op1"
#temphouse2_op1 = inpath + "temphouse2_op1"
#flddamarray2_op1 = inpath + "flddamarray2_op1"
#
#zzfldext3_op1 = inpath +"zzfldext3_op1"
#zzzfldext3_op1 = inpath + "zzzfldext3_op1"
#zzfldpoly3_op1 = inpath + "zzfldpoly3_op1"
#fldpoly3a_op1 = inpath + "fldpoly3a_op1"
#fldpoly3_op1 = inpath + "fldpoly3_op1"
#difffld3_op1 = inpath + "difffld3_op1"  
#flddepth3_op1 = inpath+ "flddepth3_op1"
#houserisk3_op1 = inpath + "houserisk3_op1"
#temphouse3_op1 = inpath + "temphouse3_op1"
#flddamarray3_op1 = inpath + "flddamarray3_op1"


###############################################################################
# HAZARD BASELINE: Current water elevation rasters for different flood events
# (Hazard modelling done externally)

spline1aep = inpath + "Spline_BL_1" 
spline2aep = inpath + "Spline_BL_2"
spline5aep = inpath + "Spline_BL_5"
spline20aep = inpath + "Spline_BL_20"
#spline1aep = inpath + "zzBL1test" 
#spline2aep = inpath + "zzBL2test"
#spline5aep = inpath + "zzBL5test"
#spline20aep = inpath + "zzBL20test"

#BR2010one = inpath+"BR2010one"
#BR2010two = inpath+"BR2010two"
#BR2010five = inpath+"BR2010five"
#flood1ca=inpath+"flood1ca"
#flood2ca=inpath+"flood2ca"
#flood5ca=inpath+"flood3ca"
#Create new Browns River flood rasters (AEP 1%, 2%, 5%)
#ADJUTS FOR SMWH Datum (AHD - 0.62)
#arcpy.gp.Minus_sa(flood1c, Input_raster_or_constant_value_2, flood1ca)
#arcpy.gp.Minus_sa(flood2c, Input_raster_or_constant_value_2, flood2ca)
#arcpy.gp.Minus_sa(flood5c, Input_raster_or_constant_value_2, flood5ca)

###############################################################################
# DEFINE FUNCTIONS TO BE USED
# Fuction to create new rasters that take into account sea level rise and
# change rainfall intensity
# inras is the current day (baseline) raster
# Create a standard empty raster (1551 rows x 1449 columns; equivalent to 
# 2m x 2m cells in MWHS_ldrclip2m extent)
rastext = inpath+"rastext"
arcpy.gp.CreateConstantRaster_sa(rastext, 0, "FLOAT", "2", "524950 5239950 527847 5243050")
#If BL_1_Spline being used, need to change array

inras = arcpy.RasterToNumPyArray(rastext,nodata_to_value=0)
# Amend the raster shape
#inras = inras[:1550,:1449]
#inras.shape
nrows = inras.shape[0]
ncols = inras.shape[1] 
# create new array to store new values
newras = np.zeros((nrows,ncols), dtype=np.float32)
def RasterScenario(inras,SLRscn,Rainfallscn):
    for k in range(nrows):
        for l in range(ncols):
            val = inras[k,l] + 0.01*SLRscn + 0.01*Rainfallscn
            # Assign new value to new array that can be used for output
            newras[k,l] = val


#newras = np.zeros((nrows,ncols), dtype=np.float32)
#def RasterScenario(inras,SLRscn,Rainfallscn):
#    for k in range(nrows):
#        for l in range(ncols):
#            if SLRscn<= 1:
#                val = inras[k,l] + 0.01*SLRscn + 0.01*Rainfallscn
#            else:
#                val = inras[k,l] + 0.24*SLRscn + 0.01*Rainfallscn
#            # Assign new value to new array that can be used for output
#            newras[k,l] = val

#
#SLRscn = 2
#Rainfallscn = 10
#InBL5scn = arcpy.RasterToNumPyArray(flood5c) 
#RasterScenario(InBL5scn, SLRscn, Rainfallscn)
#newras.sum()
#np.amax(newras)
#newras[230,500]

nrowsv = newras.shape[0]
ncolsv = newras.shape[1]  
rastvul = np.zeros((nrowsv,ncolsv), dtype=np.float32)

# Vulnerability curve estimated from Geosciences Australia
def RasterDamage (newras,MAX_DAMAGE,dften):
    for m in range(nrowsv):
        for n in range(ncolsv):
            if 0 < newras[m,n] <= 3:
                val2 = 0.3831*math.pow((newras[m,n]),0.2)*MAX_DAMAGE + dften
            elif newras[m,n] > 3:
                val2 = (0.54)*MAX_DAMAGE + dften
            else:
                val2 = 0
            # Assign new value to new array that can be used for output
            rastvul[m,n] = val2

# Vulnerability curve estimated from Geosciences Australia
# POTENTIAL LOSSES
# Depth < 0.1m (approx slab on ground height) = 0
def ContentDamage (newras,MAX_CONTENTS_DAMAGE,dften):
    for m in range(nrowsv):
        for n in range(ncolsv):
            if  0.1 < newras[m,n] <= 3:
                val3 = 0.5443*math.pow((newras[m,n]),0.2761)*MAX_CONTENTS_DAMAGE + dften
            elif newras[m,n] > 3:
                val3 = (0.7)*MAX_CONTENTS_DAMAGE + dften
            else:
                val3 = 0
            rastvul[m,n] = val3

# ACTUAL DAMAGE ESTAIMTE (i.e. goods saved)
#def ContentDamage (newras,MAX_CONTENTS_DAMAGE,dften):
#    for m in range(nrowsv):
#        for n in range(ncolsv):
#            if  0.1 < newras[m,n] <= 3:
#                val3 = 0.2149*math.exp(0.3303*inras[m,n])*MAX_CONTENTS_DAMAGE - dften
#            elif newras[m,n] > 3:
#                val3 = 0.68*MAX_CONTENTS_DAMAGE - dften
#            else:
#                val3 = 0
#            rastvul[m,n] = val3

#def RasterLoss (newras,MAX_DAMAGE):
#    for m in range(nrowsv):
#        for n in range(ncolsv):
#            if newras[m,n] > 0:
#                val4 = MAX_DAMAGE
#            else:
#                val4 = 0
#            # Assign new value to new array that can be used for output
#            rastvul[m,n] = val4


## OPTION 2 - Changing Depth-Damage curve (i.e. <30cm = 0)
#def RasterDamage_Op2 (newras,MAX_DAMAGE,dften):
#    for m in range(nrowsv):
#        for n in range(ncolsv):
#            if newras[m,n] > 0.3:           
#                val3 = 0.2726*math.exp(0.223*inras[m,n])*MAX_DAMAGE - dften
#            else:
#                val3 = 0.05*inras[m,n]*MAX_DAMAGE - dften
#            # Assign new value to new array that can be used for output
#            rastvul[m,n] = val3


###############################################################################
# SCENARIOS: Generated in R Programming Language (for script, see "P:\PhD 2015\11. R Code")
RScenario = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS\\Results\\2017-05-11_5000Case_Generation.csv')
# Slice out first five rows to test [33:34]
RScenario = RScenario[1:3] 
# Convert to float data type
RScenario = pd.DataFrame(RScenario,dtype=float)
RScenario

###############################################################################
# CREATE NEW LISTS TO STORE RESULTS FROM BELOW ANALYSIS (in each scenario)
AEP_one_R_impact = []
AEP_two_R_impact = []
AEP_five_R_impact = []
AEP_twenty_R_impact = []
SLR_House_Loss =[]
SLR_Number_House = []
AAD = []
AV_PPL = []

Private_land_area_SLR = []
Road_length_SLR = []
Av_Beach_Width = []

AEP_one_content = []
AEP_two_content = []
AEP_five_content = []
AEP_twenty_content = []
AEP_one_total = []
AEP_two_total = []
AEP_five_total = []
AEP_twenty_total = []

AEP_one_ppl = []
AEP_two_ppl = []
AEP_five_ppl = []
AEP_twenty_ppl = []

#AEP_one_R_LEVEE = []
#AEP_two_R_LEVEE = []
#AEP_five_R_LEVEE = []
#AAD_LEVEE = []
#EAB_LEVEE = []
#EAB_30cm = []

#AEP_one_R_30cm = []
#AEP_two_R_30cm = []
#AEP_five_R_30cm = []
#AAD_30cm = []
#AAD_EAB_30cm = []

###############################################################################
# CONVERT DEM DATA FROM AHD (Australian Height Datum) to MHWS (Mean High Water Sping) LEVEL
# Source = Kingborough Conucl Flood Study (2017). MWHS = 0.623m AHD
# Process: Minus (Clean DEM data - convert from AHD to MHWS)1
arcpy.gp.Minus_sa(ldrclip2m, MHWS_ADJUST, MWHS_ldrclip2m)

###############################################################################
# IMPACT ANALYSIS
# Impacts analysed for each scenario (Number of houses, area of private land, length of road)
for index, i in RScenario.iterrows():
    # Define uncertain parameters in scenario    
    CONSTANT_SLR = i['SLR']
    SLRscn = CONSTANT_SLR
    Rainfallscn = i['Rainfall']  
    MAX_DAMAGE = i['maxstructure']
    MAX_CONTENTS_DAMAGE = i['maxcontents']
    Scenario = i['Scenario']
    dften = i['df10cm']
    bruun_factor = i['bruun_factor']
    AV_PPL_HOUSE = i['Av_ppl']
 
#    VALUES TO DETERMINE BASELINE AAD AND AAPE
#    CONSTANT_SLR = 0
#    SLRscn = CONSTANT_SLR
#    Rainfallscn = 0  
#    MAX_DAMAGE = 5757
#    MAX_CONTENTS_DAMAGE = 1058
#    dften = 0
#    bruun_factor = 50   
#    AV_PPL_HOUSE = 2.2

#    VALUES TO CROSS-CHECK Scenario: 1% AEP flood + 0.3m SLR + 10% rainfall
#    CONSTANT_SLR = 0.3
#    SLRscn = CONSTANT_SLR
#    Rainfallscn = 10  
#    MAX_DAMAGE = 5757
#    MAX_CONTENTS_DAMAGE = 1058
#    dften = 0
#    bruun_factor = 50   
#    AV_PPL_HOUSE = 2.3

#    VALUES TO CROSS-CHECK Scenario: 1% AEP flood + 1m SLR + 30% rainfall
#    CONSTANT_SLR = 1
#    SLRscn = CONSTANT_SLR
#    Rainfallscn = 30  
#    MAX_DAMAGE = 5757
#    MAX_CONTENTS_DAMAGE = 1058
#    dften = 0
#    bruun_factor = 50   
#    AV_PPL_HOUSE = 2.3

#    VALUES TO CROSS-CHECK Scenario: 2% AEP flood + 0.8m SLR + 15% rainfall
#    CONSTANT_SLR = 0.8
#    SLRscn = CONSTANT_SLR
#    Rainfallscn = 15  
#    MAX_DAMAGE = 5757
#    MAX_CONTENTS_DAMAGE = 1058
#    dften = 0
#    bruun_factor = 50   
#    AV_PPL_HOUSE = 2.3
# 
    print "-------------------------------------"    
    print "Scenario " +str(Scenario)+":"
    print "Sea level rise = " +str(SLRscn) +"m"
    print "Rainfall intensity = " +str(Rainfallscn)+"%"
    print "Maximum house structural value = $" +str(MAX_DAMAGE)+ "/4m2"
    print "Maximum house contents value = $" +str(MAX_CONTENTS_DAMAGE)+ "/4m2"
    print "Bruun factor = " +str(bruun_factor)
    print "Average people per house = " +str(AV_PPL_HOUSE)   
    print "-------------------------------------"    
   
    # SEA LEVEL RISE - PERMANENT LOSSES AT MEAN HIGH WATER SPRING TIDE (MHWS Vertical Datum)
    # Note for Permenent SLR calculations, working in MHWS as datum
    # Process: Create Constant Raster - SLR scenario
    arcpy.gp.CreateConstantRaster_sa(slr_surface, CONSTANT_SLR, "FLOAT", "2", "524950 5239950 527847 5243050")
    # Process: Calculate Statistics
    arcpy.CalculateStatistics_management(MWHS_ldrclip2m, "1", "1", "", "OVERWRITE", Area_of_Interest)    
    # Process: Less Than Equal.Evaluate if DEM lower than water elevation. If yes, value of 1.
    arcpy.gp.LessThanEqual_sa(MWHS_ldrclip2m, slr_surface, slr_extent)
    # Process: Con. If cell has value of 1, then keep
    arcpy.gp.Con_sa(slr_extent, CONDITION_TRUE, slr_ext_con, "", "Value =1")
 
    # NUMBER OF HOUSES LOST AT MWHS ###########################################  
    # Process: Region Group - assigns a number to each connected region for cells (i.e. with value 1 from Con)
    # As per NOAA inundation mapping guidance (NOAA, 2017)
    arcpy.gp.RegionGroup_sa(slr_ext_con, slrgroup, "EIGHT", "WITHIN", "NO_LINK", "")
    # Process: Raster to Polygon
    arcpy.RasterToPolygon_conversion(slrgroup, slr_poly, "SIMPLIFY", "Value")
    # Process: Select - Max polygon
    arcpy.Select_analysis(slr_poly, max_slr_poly, "Shape_Area=(SELECT MAX(Shape_Area) FROM slr_poly)")
    # Process: Select - Private residential dwellings as building type
    arcpy.Select_analysis(T2DLanduse_Buildings, private_houses, "TYPE = 'Residential'")    
      
    # Process: Select Layer By Location
    arcpy.MakeFeatureLayer_management(T2DLanduse_Buildings,"Buildings")
    building_count_result = arcpy.GetCount_management(arcpy.SelectLayerByLocation_management("Buildings", "INTERSECT", max_slr_poly, "", "NEW_SELECTION", "NOT_INVERT"))
    arcpy.MakeFeatureLayer_management(private_houses,"houses")
    house_count = arcpy.GetCount_management(arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_slr_poly, "", "NEW_SELECTION", "NOT_INVERT")) 
    slr_house = int(house_count.getOutput(0))
    # Print output from GetCount process
    print "The number of houses lost is " + str(slr_house) + " (of the " + str(int(building_count_result.getOutput(0))) + " buildings affected)"
    #Add results to seperate list/column
    SLR_Number_House.append(slr_house)     
     
    # AVERAGE BEACH WIDTH (m) #################################################
    if SLRscn == 0:
        Transect1 = arcpy.da.TableToNumPyArray(arcpy.Erase_analysis(beachtrans1,slr_poly, beachwid1, ""),'SHAPE_Length')
        Transect_1_sum = Transect1["SHAPE_Length"].sum()
        Transect2 = arcpy.da.TableToNumPyArray(arcpy.Erase_analysis(beachtrans2,slr_poly, beachwid2, ""),'SHAPE_Length')
        Transect_2_sum = Transect2["SHAPE_Length"].sum()
        Transect3 = arcpy.da.TableToNumPyArray(arcpy.Erase_analysis(beachtrans3,slr_poly, beachwid3, ""),'SHAPE_Length')
        Transect_3_sum = Transect3["SHAPE_Length"].sum()   
        Transect4 = arcpy.da.TableToNumPyArray(arcpy.Erase_analysis(beachtrans4,slr_poly, beachwid4, ""),'SHAPE_Length')
        Transect_4_sum = Transect4["SHAPE_Length"].sum()
        Transect5 = arcpy.da.TableToNumPyArray(arcpy.Erase_analysis(beachtrans5,slr_poly, beachwid5, ""),'SHAPE_Length')
        Transect_5_sum = Transect5["SHAPE_Length"].sum()
        Beach_Width = np.average([Transect_1_sum, Transect_2_sum, Transect_3_sum, Transect_4_sum, Transect_5_sum])
        print "The average beach width is " + str(round(Beach_Width,1)) + "m"         
    else:
    # Process: Buffer - Create the horizontgal recession layer using Bruun factor    
        buff_dist = bruun_factor*SLRscn    
        arcpy.Buffer_analysis(slr_poly,slr_bruun,buff_dist,"FULL","FLAT","","")    
        Transect1 = arcpy.da.TableToNumPyArray(arcpy.Erase_analysis(beachtrans1,slr_bruun, beachwid1, ""),'SHAPE_Length')
        Transect_1_sum = Transect1["SHAPE_Length"].sum()
        Transect2 = arcpy.da.TableToNumPyArray(arcpy.Erase_analysis(beachtrans2,slr_bruun, beachwid2, ""),'SHAPE_Length')
        Transect_2_sum = Transect2["SHAPE_Length"].sum()
        Transect3 = arcpy.da.TableToNumPyArray(arcpy.Erase_analysis(beachtrans3,slr_bruun, beachwid3, ""),'SHAPE_Length')
        Transect_3_sum = Transect3["SHAPE_Length"].sum()   
        Transect4 = arcpy.da.TableToNumPyArray(arcpy.Erase_analysis(beachtrans4,slr_bruun, beachwid4, ""),'SHAPE_Length')
        Transect_4_sum = Transect4["SHAPE_Length"].sum()
        Transect5 = arcpy.da.TableToNumPyArray(arcpy.Erase_analysis(beachtrans5,slr_bruun, beachwid5, ""),'SHAPE_Length')
        Transect_5_sum = Transect5["SHAPE_Length"].sum()
        Beach_Width = np.average([Transect_1_sum, Transect_2_sum, Transect_3_sum, Transect_4_sum, Transect_5_sum])
        print "The average beach width is " + str(round(Beach_Width,1)) + "m"    
    Av_Beach_Width.append(Beach_Width)
      
    # VALUE OF HOUSES LOST AT MWHS ############################################
    # Process: Minus (2)
    arcpy.Minus_3d(slr_surface, MWHS_ldrclip2m, diffslr)
    # Process: Extract by Mask
    arcpy.gp.ExtractByMask_sa(diffslr, max_slr_poly, slrdepth)
    # Process: Select Layer By Location. Select land within inundation extent
    # Land use type is houses
    
    # Process: Make Feature Layer. Needed for extract by mask step 
    arcpy.MakeFeatureLayer_management(arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_slr_poly, "", "NEW_SELECTION", "NOT_INVERT"), houserisk, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Entity Entity VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;Av_ppl_per_dwelling Av_ppl_per_dwelling VISIBLE NONE")
    # Process: Extract by Mask. Extract raster depth cells in land use area
#    arcpy.gp.ExtractByMask_sa(slrdepth, houserisk, house_loss)
    # Apply pre-defined function that applies (1) damage index based on depth; 
    # (2) multiplies damage index by MaxDam
#    tempdamarray = arcpy.RasterToNumPyArray(house_loss,nodata_to_value=0)  
#    RasterLoss(tempdamarray, MAX_DAMAGE)
#    slrlossimp = rastvul.sum()
    house_area = "house_area"
    housearea = "housearea"
    sumhouse = "sumhouse"
    house_area = arcpy.da.TableToNumPyArray(arcpy.Statistics_analysis(houserisk, housearea, "Shape_Area SUM", ""),'SUM_Shape_Area')   
    sumhouse = house_area["SUM_Shape_Area"].sum()    
    # House area in m2; MAX_DAMAGE is per 4m2
    slrlossimp = sumhouse*(MAX_DAMAGE/4)
    # Print output results          
    print "The structural loss to houses is $" + str(float(slrlossimp))
    SLR_House_Loss.append(slrlossimp)
 
    # PERMANENT LOSSES TO PRIVATE LAND (m2) ###################################
    # Process: Select - Residential
    arcpy.Select_analysis(interim_planning_scheme_zoning_statewide, private_land, "ZONE = '10.0 General Residential'")
    # Process: Select Layer By Location
    arcpy.MakeFeatureLayer_management(private_land,"Res")  
    # Process: Intersect
    arcpy.Intersect_analysis("Res #;C:\\Users\\tdramm\\Desktop\\GIS\\Concept.gdb\\max_slr_poly #", privland, "ALL", "", "INPUT")
    # Converts table to NumPy array
    # http://resources.arcgis.com/en/help/main/10.1/index.html#/TableToNumPyArray/018w00000018000000/
    arr = arcpy.da.TableToNumPyArray(arcpy.Statistics_analysis(privland, privateland, "Shape_Area SUM", ""),'SUM_Shape_Area')
    # Print output results
    Private_land = arr["SUM_Shape_Area"].sum()
    print "The loss of private land is " + str(round(Private_land,1)) + "m2"
    # Add results 
    Private_land_area_SLR.append(Private_land)
 
    # PERMANENT LOSS TO SEALED PUBLIC ROAD (m) ################################
    # Process: Intersect        
    arcpy.Intersect_analysis("list_transport_segments_kingborough #; max_slr_poly #", public_road, "ALL", "", "INPUT")
    arcpy.Select_analysis(public_road, sealedroad, "SURFACE_TY = 'Sealed'")
    arcpy.Select_analysis(sealedroad, sealed, "TRANS_TYPE = 'Road'")
    # Process: Summary Statistics (2)
    arr_road = arcpy.da.TableToNumPyArray(arcpy.Statistics_analysis(sealed, roads, "Shape_Length SUM", ""),"SUM_Shape_Length")
    Public_road = arr_road["SUM_Shape_Length"].sum()
    print "The loss of sealed public roads is " + str(round(Public_road,1))+"m"
    # Add results 
    Road_length_SLR.append(Public_road) 
    print "-------------------------------------"     
 

 
    # RIVERINE FLOODING - ANNUAL ANVERAGE DAMAGES (STRUCTURAL) TO HOUSES ######
    # Tidy up all rasters to get water depth and extent
    # 1% AEP raster
    # Concert to numpy arrage to adjudt
    BL1spline = arcpy.RasterToNumPyArray(spline1aep,nodata_to_value=0) 
    # Apply prefedined function to adjust
    RasterScenario(BL1spline, SLRscn, Rainfallscn)
    # Convert back to raster for geoprocessing
    # Derive properties of input raster that will be used for output (e.g. setting coordinate system)
    descData=arcpy.Describe(rastext)
    cellSize=descData.meanCellHeight
    extent=descData.Extent
    HATData=arcpy.Describe(MWHS_ldrclip2m)
    spatialReference=HATData.spatialReference
    pnt=arcpy.Point(extent.XMin,extent.YMin)
    BL1surrogate = arcpy.NumPyArrayToRaster(newras,pnt,cellSize,cellSize)   
    # Raster that has combined flood, SLR, Rainfall scenario inputs    
    # convert numpy array to an ArcGIS raster and save raster to disk
    # Retain projection information. 
    # http://gis.stackexchange.com/questions/37241/how-to-keep-spatial-reference-using-arcpy-rastertonumpyarray    
    BL1surrogate.save("C:\\Users\\tdramm\\Desktop\\GIS\\Concept.gdb\\BL1surrogate") 
    arcpy.DefineProjection_management(BL1surrogate, spatialReference)   
    # Process: Less Than Equal. 
    arcpy.gp.LessThanEqual_sa(ldrclip2m, BL1surrogate, fld_extent)
    # Process: Con. If water elevation higher than DEM, then value of 1
    arcpy.gp.Con_sa(fld_extent, BL1surrogate, fld_ext_con, "", "Value =1")        
    # Process: Raster to Polygon. Extent polygon of raster
    arcpy.RasterToPolygon_conversion(fld_extent, fld_poly, "SIMPLIFY", "Value")    
    # Process: Select - Max polygon
    arcpy.Select_analysis(fld_poly, fld_poly_sel, "gridcode=1")
    arcpy.Select_analysis(fld_poly_sel, max_fld_poly, "Shape_Area=(SELECT MAX(Shape_Area) FROM fld_poly_sel)")
    # Process: Select Layer By Location
    arcpy.MakeFeatureLayer_management(private_houses,"houses")    
    # Process: Select Layer By Location. Select land within inundation extent
    # Process: Minus (2)
    arcpy.Minus_3d(BL1surrogate, ldrclip2m, difffld)
    # Process: Extract by Mask
    arcpy.gp.ExtractByMask_sa(difffld, max_fld_poly, flddepth)
    # Process: Select Layer By Location. Select land within inundation extent
    # Land use type is houses



#*************************
    arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly, "", "NEW_SELECTION", "NOT_INVERT")
    # Process: Make Feature Layer. Needed for extract by mask step 
    arcpy.MakeFeatureLayer_management(private_houses, houserisk1, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Entity Entity VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;Av_ppl_per_dwelling Av_ppl_per_dwelling VISIBLE NONE")
    # Process: Extract by Mask. Extract raster depth cells in landu use area
    arcpy.gp.ExtractByMask_sa(flddepth, arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly, "", "NEW_SELECTION", "NOT_INVERT"), house_dam1)
#*****************************
#    SIMPLER CODE THAN ABOVE FEW LINES
#    test = "test"    
#    arcpy.Intersect_analysis(["private_houses","max_fld_poly"],"test", "ALL", "", "")
#    arcpy.gp.ExtractByMask_sa(flddepth, test, house_dam1)
 # ******************************************************** 

  # Apply funtion
    flddamarray = arcpy.RasterToNumPyArray(house_dam1,nodata_to_value=0)
    RasterDamage(flddamarray, MAX_DAMAGE, dften)
    fldoneimp = rastvul.sum()
    print "The structural damage to houses from a 1% AEP flood is $" + str(float(fldoneimp))
    AEP_one_R_impact.append(rastvul.sum())

    # Contents Loss (if water > 100mm; and approximate depth of the 'slab on ground')
    ContentDamage(flddamarray,MAX_CONTENTS_DAMAGE,dften)     
    fldonecont = rastvul.sum()
    print "The contents damage to houses from a 1% AEP flood is $" + str(float(fldonecont))
    AEP_one_content.append(rastvul.sum())

    # Total structural and contents Loss
    total_damage_one = fldoneimp + fldonecont
    print "The total damage to houses from a 1% AEP flood is $" + str(float(total_damage_one))
    AEP_one_total.append(total_damage_one)
    
    # Count number of people exposed       
    fldone_count = arcpy.GetCount_management(arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly, "", "NEW_SELECTION", "NOT_INVERT")) 
    fldone_house = int(fldone_count.getOutput(0))
    fldone_ppl = AV_PPL_HOUSE * float(fldone_house)
    print "The total number of people exposed in 1% AEP flood is " + str(round(fldone_ppl,0))    
    AEP_one_ppl.append(fldone_ppl)

    print "-------------------------------------"  

      
    #Repeat for 2% AEP raster #################################################
    BL2spline = arcpy.RasterToNumPyArray(spline2aep,nodata_to_value=0) 
    RasterScenario(BL2spline, SLRscn, Rainfallscn)
    descData=arcpy.Describe(rastext)
    cellSize=descData.meanCellHeight
    extent=descData.Extent
    HATData=arcpy.Describe(MWHS_ldrclip2m)
    spatialReference=HATData.spatialReference
    pnt=arcpy.Point(extent.XMin,extent.YMin)
    BL2surrogate = arcpy.NumPyArrayToRaster(newras,pnt,cellSize,cellSize)     
    BL2surrogate.save("C:\\Users\\tdramm\\Desktop\\GIS\\Concept.gdb\\BL2surrogate") 
    arcpy.DefineProjection_management(BL2surrogate, spatialReference) 
    
    arcpy.gp.LessThanEqual_sa(ldrclip2m, BL2surrogate, fld_extent2)
    arcpy.gp.Con_sa(fld_extent2, BL2surrogate, fld_ext_con2, "", "Value =1")        
    arcpy.RasterToPolygon_conversion(fld_extent2, fld_poly2, "SIMPLIFY", "Value")      
    arcpy.Select_analysis(fld_poly2, fld_poly_sel2, "gridcode=1")
    arcpy.Select_analysis(fld_poly_sel2, max_fld_poly2, "Shape_Area=(SELECT MAX(Shape_Area) FROM fld_poly_sel2)")
    arcpy.MakeFeatureLayer_management(private_houses,"houses")    
    arcpy.Minus_3d(BL2surrogate, ldrclip2m, difffld2)
    arcpy.gp.ExtractByMask_sa(difffld2, max_fld_poly2, flddepth2)
    # Process: Select Layer By Location. Select land within inundation extent
    # Land use type is houses
#    arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly2, "", "NEW_SELECTION", "NOT_INVERT")
    # Process: Make Feature Layer. Needed for extract by mask step 
#    arcpy.MakeFeatureLayer_management(Selected, houserisk2, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Entity Entity VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;Av_ppl_per_dwelling Av_ppl_per_dwelling VISIBLE NONE")
    # Process: Extract by Mask. Extract raster depth cells in land uuse area
    arcpy.gp.ExtractByMask_sa(flddepth2, arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly2, "", "NEW_SELECTION", "NOT_INVERT"), house_dam2)
    # Apply funtion
    flddamarray2 = arcpy.RasterToNumPyArray(house_dam2,nodata_to_value=0)
    rastvul = np.zeros((nrowsv,ncolsv), dtype=np.float32)    
    RasterDamage(flddamarray2, MAX_DAMAGE, dften)
    aeptwoimp = rastvul.sum()
    print "The structural damage to houses from a 2% AEP flood is $" + str(float(aeptwoimp))
    AEP_two_R_impact.append(rastvul.sum())
        
    ContentDamage(flddamarray2,MAX_CONTENTS_DAMAGE,dften)     
    fldtwocont = rastvul.sum()
    print "The contents damage to houses from a 2% AEP flood is $" + str(float(fldtwocont))
    AEP_two_content.append(rastvul.sum())   
   
    total_damage_two = aeptwoimp + fldtwocont
    print "The total damage to houses from a 2% AEP flood is $" + str(float(total_damage_two))
    AEP_two_total.append(total_damage_two)   
 
    fldtwo_count = arcpy.GetCount_management(arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly2, "", "NEW_SELECTION", "NOT_INVERT")) 
    fldtwo_house = int(fldtwo_count.getOutput(0))
    fldtwo_ppl = AV_PPL_HOUSE * float(fldtwo_house)
    print "The total number of people exposed in 2% AEP flood is " + str(round(fldtwo_ppl,0))    
    AEP_two_ppl.append(fldtwo_ppl)
   
    print "-------------------------------------"     
        
    #Repeat for 5% AEP raster
    BL5spline = arcpy.RasterToNumPyArray(spline5aep,nodata_to_value=0) 
    RasterScenario(BL5spline, SLRscn, Rainfallscn)
    descData=arcpy.Describe(rastext)
    cellSize=descData.meanCellHeight
    extent=descData.Extent
    HATData=arcpy.Describe(MWHS_ldrclip2m)
    spatialReference=HATData.spatialReference
    pnt=arcpy.Point(extent.XMin,extent.YMin)
    BL5surrogate = arcpy.NumPyArrayToRaster(newras,pnt,cellSize,cellSize)     
    BL5surrogate.save("C:\\Users\\tdramm\\Desktop\\GIS\\Concept.gdb\\BL5surrogate") 
    arcpy.DefineProjection_management(BL5surrogate, spatialReference) 
      
    arcpy.gp.LessThanEqual_sa(ldrclip2m, BL5surrogate, fld_extent5)
    arcpy.gp.Con_sa(fld_extent5, BL5surrogate, fld_ext_con5, "", "Value =1")        
    arcpy.RasterToPolygon_conversion(fld_extent5, fld_poly5, "SIMPLIFY", "Value")      
    arcpy.Select_analysis(fld_poly5, fld_poly_sel5, "gridcode=1")
    arcpy.Select_analysis(fld_poly_sel5, max_fld_poly5, "Shape_Area=(SELECT MAX(Shape_Area) FROM fld_poly_sel5)")    
    # Process: Select Layer By Location
    arcpy.MakeFeatureLayer_management(private_houses,"houses")    
    # Process: Select Layer By Location. Select land within inundation extent
    # Process: Minus (2)
    arcpy.Minus_3d(BL5surrogate, ldrclip2m, difffld5)
    # Process: Extract by Mask
    arcpy.gp.ExtractByMask_sa(difffld5, max_fld_poly5, flddepth5)
    # Process: Select Layer By Location. Select land within inundation extent
    # Land use type is houses
#    arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly5, "", "NEW_SELECTION", "NOT_INVERT")
    # Process: Make Feature Layer. Needed for extract by mask step 
    arcpy.MakeFeatureLayer_management(arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly5, "", "NEW_SELECTION", "NOT_INVERT"), houserisk5, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Entity Entity VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;Av_ppl_per_dwelling Av_ppl_per_dwelling VISIBLE NONE")
    # Process: Extract by Mask. Extract raster depth cells in landu use area
    arcpy.gp.ExtractByMask_sa(flddepth5, houserisk5, house_dam5)
    # Apply funtion
    flddamarray5 = arcpy.RasterToNumPyArray(house_dam5,nodata_to_value=0)
    rastvul = np.zeros((nrowsv,ncolsv), dtype=np.float32)    
    RasterDamage(flddamarray5, MAX_DAMAGE, dften)
    aepfiveimp = rastvul.sum()
    print "The structural damage to houses from a 5% AEP flood is $" + str(float(aepfiveimp))
    AEP_five_R_impact.append(rastvul.sum())
   
    ContentDamage(flddamarray5,MAX_CONTENTS_DAMAGE,dften)     
    fldfivecont = rastvul.sum()
    print "The contents damage to houses from a 5% AEP flood is $" + str(float(fldfivecont))
    AEP_five_content.append(rastvul.sum()) 

    total_damage_five = aepfiveimp + fldfivecont
    print "The total damage to houses from a 5% AEP flood is $" + str(float(total_damage_five))
    AEP_five_total.append(total_damage_five) 

    fldfive_count = arcpy.GetCount_management(arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly5, "", "NEW_SELECTION", "NOT_INVERT")) 
    fldfive_house = int(fldfive_count.getOutput(0))
    fldfive_ppl = AV_PPL_HOUSE * float(fldfive_house)
    print "The total number of people exposed in 5% AEP flood is " + str(round(fldfive_ppl,0))    
    AEP_five_ppl.append(fldfive_ppl)

    print "-------------------------------------"     

    #Repeat for 20% AEP raster
    BL20spline = arcpy.RasterToNumPyArray(spline20aep,nodata_to_value=0) 
    RasterScenario(BL20spline, SLRscn, Rainfallscn)
    descData=arcpy.Describe(rastext)
    cellSize=descData.meanCellHeight
    extent=descData.Extent
    HATData=arcpy.Describe(MWHS_ldrclip2m)
    spatialReference=HATData.spatialReference
    pnt=arcpy.Point(extent.XMin,extent.YMin)
    BL20surrogate = arcpy.NumPyArrayToRaster(newras,pnt,cellSize,cellSize)     
    BL20surrogate.save("C:\\Users\\tdramm\\Desktop\\GIS\\Concept.gdb\\BL20surrogate") 
    arcpy.DefineProjection_management(BL20surrogate, spatialReference) 
         
    arcpy.gp.LessThanEqual_sa(ldrclip2m, BL20surrogate, fld_extent20)
    arcpy.gp.Con_sa(fld_extent20, BL20surrogate, fld_ext_con20, "", "Value =1")        
    arcpy.RasterToPolygon_conversion(fld_extent20, fld_poly20, "SIMPLIFY", "Value")      
    arcpy.Select_analysis(fld_poly20, fld_poly_sel20, "gridcode=1")
    arcpy.Select_analysis(fld_poly_sel20, max_fld_poly20, "Shape_Area=(SELECT MAX(Shape_Area) FROM fld_poly_sel20)")    
    # Process: Select Layer By Location
    arcpy.MakeFeatureLayer_management(private_houses,"houses")    
    # Process: Select Layer By Location. Select land within inundation extent
    # Process: Minus (2)
    arcpy.Minus_3d(BL20surrogate, ldrclip2m, difffld20)
    # Process: Extract by Mask
    arcpy.gp.ExtractByMask_sa(difffld20, max_fld_poly20, flddepth20)
    # Process: Select Layer By Location. Select land within inundation extent
    # Land use type is houses
#    arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly5, "", "NEW_SELECTION", "NOT_INVERT")
    # Process: Make Feature Layer. Needed for extract by mask step 
    arcpy.MakeFeatureLayer_management(arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly20, "", "NEW_SELECTION", "NOT_INVERT"), houserisk20, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Entity Entity VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;Av_ppl_per_dwelling Av_ppl_per_dwelling VISIBLE NONE")
    # Process: Extract by Mask. Extract raster depth cells in landu use area
    arcpy.gp.ExtractByMask_sa(flddepth20, houserisk20, house_dam20)
    # Apply funtion
    flddamarray20 = arcpy.RasterToNumPyArray(house_dam20,nodata_to_value=0)
    rastvul = np.zeros((nrowsv,ncolsv), dtype=np.float32)    
    RasterDamage(flddamarray20, MAX_DAMAGE, dften)
    aeptwentyimp = rastvul.sum()
    print "The structural damage to houses from a 20% AEP flood is $" + str(float(aeptwentyimp))
    AEP_twenty_R_impact.append(rastvul.sum())
   
    ContentDamage(flddamarray20,MAX_CONTENTS_DAMAGE,dften)     
    fldtwentycont = rastvul.sum()
    print "The contents damage to houses from a 20% AEP flood is $" + str(float(fldtwentycont))
    AEP_twenty_content.append(rastvul.sum()) 

    total_damage_twenty = aeptwentyimp + fldtwentycont
    print "The total damage to houses from a 20% AEP flood is $" + str(float(total_damage_twenty))
    AEP_twenty_total.append(total_damage_twenty) 

    fldtwenty_count = arcpy.GetCount_management(arcpy.SelectLayerByLocation_management("houses", "INTERSECT", max_fld_poly20, "", "NEW_SELECTION", "NOT_INVERT")) 
    fldtwenty_house = int(fldtwenty_count.getOutput(0))
    fldtwenty_ppl = AV_PPL_HOUSE * float(fldtwenty_house)
    print "The total number of people exposed in 20% AEP flood is " + str(round(fldtwenty_ppl,0))    
    AEP_twenty_ppl.append(fldtwenty_ppl)
  
        


    print "*************************************"

###############################################################################
# ADD RESULT LISTS INTO THE DATA FRAME
RScenario["Number Houses Lost"] = SLR_Number_House
RScenario["Permanent Houses Loss"] = SLR_House_Loss
RScenario["Private Land Impact"]=Private_land_area_SLR
RScenario["Average Beach Width"] = Av_Beach_Width
RScenario["Road Impact"]=Road_length_SLR
RScenario["1% AEP structure"] = AEP_one_R_impact
RScenario["2% AEP structure"] = AEP_two_R_impact
RScenario["5% AEP structure"] = AEP_five_R_impact
RScenario["20% AEP structure"] = AEP_twenty_R_impact
RScenario["1% AEP contents"] = AEP_one_content
RScenario["2% AEP contents"] = AEP_two_content
RScenario["5% AEP contents"] = AEP_five_content
RScenario["20% AEP contents"] = AEP_twenty_content
RScenario["1% AEP total damage"] = AEP_one_total
RScenario["2% AEP total damage"] = AEP_two_total
RScenario["5% AEP total damage"] = AEP_five_total
RScenario["20% AEP total damage"] = AEP_twenty_total
RScenario["1% AEP ppl exposed"] = AEP_one_ppl
RScenario["2% AEP ppl exposed"] = AEP_two_ppl
RScenario["5% AEP ppl exposed"] = AEP_five_ppl
RScenario["20% AEP ppl exposed"] = AEP_twenty_ppl


#RScenario['1% AEP - LEVEE'] = AEP_one_R_LEVEE
#RScenario['2% AEP - LEVEE'] = AEP_two_R_LEVEE
#RScenario['5% AEP - LEVEE'] = AEP_five_R_LEVEE
#RScenario['1% AEP - 30cm barrier'] = AEP_one_R_30cm
#RScenario['2% AEP - 30cm barrier'] = AEP_two_R_30cm
#RScenario['5% AEP - 30cm barrier'] = AEP_five_R_30cm
RScenario

###############################################################################
## ANNUAL AVERAGE DAMAGES (AAD): APPLY TRAPEZOIDAL RULE TO DETERMINE AREA UNDER CURVE
## Trapezoidal Rule Reference on SciPy: https://docs.scipy.org/doc/numpy-1.9.1/reference/generated/numpy.trapz.html
## Consider improvin gby using log scales (i.e. better approximate - i.e. reduces chance of overestimation (ref. Fig 2, AECOM Australia, 2012: 13)
## math.log10(x,10)
for index, k in RScenario.iterrows():
    a = k['1% AEP total damage']
    b = k['2% AEP total damage']
    c = k['5% AEP total damage']
    d = k['20% AEP total damage']

    e = k['1% AEP ppl exposed']
    f = k['2% AEP ppl exposed']
    g = k['5% AEP ppl exposed']
    h = k['20% AEP ppl exposed']

#    d = k['1% AEP - LEVEE']
#    e = k['2% AEP - LEVEE']
#    f = k['5% AEP - LEVEE']
#    
#    g = k['1% AEP - 30cm barrier']
#    h = k['2% AEP - 30cm barrier']
#    i = k['5% AEP - 30cm barrier']
    

    aad = np.trapz([a,b,c,d],x=[0.01,0.02,0.05,0.2])
    AAD.append(aad)

    av_ppl = np.trapz([e,f,g,h],x=[0.01,0.02,0.05,0.2])
    AV_PPL.append(av_ppl)

#    aad_levee = np.trapz([d,e,f],x=[0.01,0.02,0.05])    
#    AAD_LEVEE.append(aad_levee)
#
#    aad_30cm = np.trapz([g,h,i],x=[0.01,0.02,0.05])    
#    AAD_30cm.append(aad_30cm)
#
#    EAB_op1 = aad - aad_levee
#    EAB_LEVEE.append(EAB_op1)
#    
#    EAB_op2 = aad - aad_30cm    
#    EAB_30cm.append(EAB_op2)
    
#print "The Average Annual Damage cost of flooding to houses is $" + str(float(aad))

# Baseline AAD - assume SLR = 0; Rainfall = 0; MAX_DAMAGE = 1500/m2 or 6000/4m2 (AAD=$188k)

RScenario["Av Annual Damages"]=AAD
RScenario["Av People Exposed"]=AV_PPL
#RScenario['AAD - Levee']=AAD_LEVEE
#RScenario['AAD - 30cm']=AAD_30cm
#RScenario['EAB - Levee']=EAB_LEVEE
#RScenario['EAB - 30cm']=EAB_30cm
RScenario





###############################################################################
# STOP TIMER AND OUTPUT TIME TAKEN TO RUN CODE
t1 = time.clock()
tdiff = t1 - t0
print "It took %.3f seconds for this code to run" % (tdiff)

###############################################################################
# Write results to csv file
outfile = "C:\\Users\\tdramm\\Desktop\\GIS\\Results\\2017-09-04CaseStudyResults.csv"
RScenario.to_csv(outfile)

