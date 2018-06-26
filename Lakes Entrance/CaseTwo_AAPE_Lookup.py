# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:28:59 2018

@author: tdramm

CaseTwo_AAPE_Lookup.py -    The script uses develops a table of the average     
                            annual people exposed and number of buildings at 
                            which floodwater reaches the property. The script
                            calls upon the arcpy module to undertake a sequence
                            of geoprocessing steps to undertake the analysis.
                            
                            The lookup table procuded is called upon in the 
                            CaseStudyTwo_RDM.py and the CaseStudyTwo_DAPP.py
                            scrips

"""


###############################################################################
# IMPORT PACKAGES
# Import arcpy module
import arcpy 
# Pandas module used for importing csv as data frame and making float data type
import pandas as pd
# For TableToNumPyArray used with raster data
import numpy as np
# Import time package
import time
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
##MHHW 0.433m above AHD in study area
#MHHW_ADJUST = "0.433" #Ref BOM Email (Bullock Island) [MSL = 0.085mAHD; MHHW = 0.433mAHD)] 
#
#max_car_depth = "0.15"

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
slr_poly2 = "slr_poly2"
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
bld_all_ret = inpath + "build_z1234_r"
bld_all_comm = inpath + "build_z1234_c"
bld_234_ret = inpath + "build_z234_r"
bld_234_lan = inpath + "build_z234_c"
bld_4_ret = inpath + "build_z4_ret"
bld_4_land = inpath + "build_z4_com"
bld_1_ret = inpath + "build_z1_ret"
bld_1_land = inpath + "build_z1_com"
dem1m_infill = inpath + "dem1m_infill"
protect_dem1m = inpath + "protect_dem1m"
slr_extent_inf = inpath + "slr_extent_inf"
slr_ext_con_inf = inpath + "slr_ext_con_inf"
slr_poly_inf = inpath + "slr_poly_inf"
max_slr_poly_2 = inpath + "max_slr_poly_2"
protec_dem1m = inpath +"protec_dem1m"
slr_extent_p = "slr_extent_p"
slr_ext_con_p = "slr_ext_con_p"
    
###############################################################################
## Baseline lake levels mAHD (Grayson et al., 2004)
#AEP_PT_ONE_BL = 2.2
#AEP_PT_TWO_BL = 2.1
#AEP_PT_FIVE_BL = 2.0
#AEP_ONE_BL = 1.8
#AEP_TWO_BL = 1.6
#AEP_FIVE_BL = 1.3
#AEP_TEN_BL = 1.2
#AEP_TWENTY_BL = 1.05

NO_PPL = []
NO_PPL_OP4= []
NO_PPL_OP3= []
NO_PPL_OP2= []
NO_PPL_OP1= []

PROP_FLD_BASE = []
PROP_FLD_OP4 = []
PROP_FLD_OP3 = []
PROP_FLD_OP2 = []
PROP_FLD_OP1 = []


index = np.arange(0, 5.01, 0.01)
#index = np.arange(1.3, 1.31, 0.01)
#index = np.arange(0, 5.01, 0.5)

columns = []
AAPE_lookup = pd.DataFrame(index=index, columns=columns, dtype=np.float32)
AAPE_lookup['Flood_level'] = index

for index, i in AAPE_lookup.iterrows():
    slr = i['Flood_level']
 
    arcpy.gp.CreateConstantRaster_sa(slr_surface, slr, "FLOAT", "1", "584953 5805832 590779 5808569")
    arcpy.CalculateStatistics_management(AOI_dem1m, "1", "1", "", "OVERWRITE", inpath + "AOI_box")    
##    arcpy.Plus_3d(slr_surface,MHHW_ADJUST,slr_surf_mhhw)
    arcpy.gp.LessThanEqual_sa(AOI_dem1m, slr_surface, slr_extent)
    arcpy.gp.Con_sa(slr_extent, CONDITION_TRUE, slr_ext_con, "", "Value =1")
    arcpy.RasterToPolygon_conversion(slr_ext_con, slr_poly, "SIMPLIFY", "Value")

    # No policy
    arcpy.MakeFeatureLayer_management(bld_area_mer,"property")    
    Select_prop = arcpy.SelectLayerByLocation_management("property","INTERSECT",slr_poly,"", "NEW_SELECTION", "NOT_INVERT")
    PROP_count = arcpy.GetCount_management(Select_prop)
    fld_prop_count = int(PROP_count.getOutput(0))
    PROP_FLD_BASE.append(fld_prop_count)       
    Sum_ppl = arcpy.da.TableToNumPyArray(Select_prop,'AV_PPL_DWL')
    PPL_sum = Sum_ppl["AV_PPL_DWL"].sum()
    NO_PPL.append(PPL_sum)

    ### LOG HOUSE ID of those properties exposed to flooding
    slr_name = int(slr*100)
    House_ID = arcpy.da.TableToNumPyArray(Select_prop,'Arc_ID')
    HousesID = pd.DataFrame(House_ID)    
    Log_outfile = ("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\"+str(slr_name)+"_houses_no_pol.csv")
    HousesID.to_csv(Log_outfile) 

    # OPTION 4: Retreat All
    arcpy.MakeFeatureLayer_management(bld_all_ret,"prop_op4")    
    Select_op4 = arcpy.SelectLayerByLocation_management("prop_op4","INTERSECT",slr_poly,"", "NEW_SELECTION", "NOT_INVERT")
    PROP_count = arcpy.GetCount_management(Select_op4)
    fld_prop_count = int(PROP_count.getOutput(0))
    PROP_FLD_OP4.append(fld_prop_count)       
    Sum_ppl_op4 = arcpy.da.TableToNumPyArray(Select_op4,'AV_PPL_DWL')
    PPL_sum_op4 = Sum_ppl_op4["AV_PPL_DWL"].sum()
    NO_PPL_OP4.append(PPL_sum_op4)

    # OPTION 3: Change land use in zones 1, 2, 3, 4 to commercial only, not residential
    arcpy.MakeFeatureLayer_management(bld_all_comm,"prop_op3")    
    Select_op3 = arcpy.SelectLayerByLocation_management("prop_op3","INTERSECT",slr_poly,"", "NEW_SELECTION", "NOT_INVERT")
    PROP_count = arcpy.GetCount_management(Select_op3)
    fld_prop_count = int(PROP_count.getOutput(0))
    PROP_FLD_OP3.append(fld_prop_count)       
    Sum_ppl_op3 = arcpy.da.TableToNumPyArray(Select_op3,'AV_PPL_DWL')
    PPL_sum_op3 = Sum_ppl_op3["AV_PPL_DWL"].sum()
    NO_PPL_OP3.append(PPL_sum_op3)

    # OPTION 2: Change building requirements, infill land
    arcpy.gp.LessThanEqual_sa(dem1m_infill, slr_surface, slr_extent_inf)
    arcpy.gp.Con_sa(slr_extent_inf, CONDITION_TRUE, slr_ext_con_inf, "", "Value =1")
    arcpy.RasterToPolygon_conversion(slr_ext_con_inf, slr_poly_inf, "SIMPLIFY", "Value")       
    arcpy.MakeFeatureLayer_management(bld_area_mer,"prop_op2")    
    Select_op2 = arcpy.SelectLayerByLocation_management("prop_op2","INTERSECT",slr_poly_inf,"", "NEW_SELECTION", "NOT_INVERT")
    PROP_count = arcpy.GetCount_management(Select_op2)
    fld_prop_count = int(PROP_count.getOutput(0))
    PROP_FLD_OP2.append(fld_prop_count)       
    Sum_ppl_op2 = arcpy.da.TableToNumPyArray(Select_op2,'AV_PPL_DWL')
    PPL_sum_op2 = Sum_ppl_op2["AV_PPL_DWL"].sum()
    NO_PPL_OP2.append(PPL_sum_op2)
    
#    OPTION 1: Protect and change land use in zone 4
#     Hydraulic connectivity via overland flow as per NOAA inundation mapping guidance (NOAA, 2017)   
    arcpy.CalculateStatistics_management(protect_dem1m, "1", "1", "", "OVERWRITE", inpath + "AOI_box")        
    arcpy.gp.LessThanEqual_sa(protec_dem1m, slr_surface, slr_extent_p)
    arcpy.gp.Con_sa(slr_extent_p, CONDITION_TRUE, slr_ext_con_p, "", "Value =1")
    arcpy.gp.RegionGroup_sa(slr_ext_con_p, slrgroup, "EIGHT", "WITHIN", "NO_LINK", "")
    arcpy.RasterToPolygon_conversion(slrgroup, slr_poly2, "SIMPLIFY", "Value")
    arcpy.Select_analysis(slr_poly2, max_slr_poly_2, "Shape_Area=(SELECT MAX(Shape_Area) FROM slr_poly2)")
#    arcpy.MakeFeatureLayer_management(bld_4_land,"prop_op1")    
    arcpy.MakeFeatureLayer_management(bld_area_mer,"prop_op1")    
    Select_op1 = arcpy.SelectLayerByLocation_management("prop_op1","INTERSECT",max_slr_poly_2,"", "NEW_SELECTION", "NOT_INVERT") 
    PROP_count = arcpy.GetCount_management(Select_op1)
    fld_prop_count = int(PROP_count.getOutput(0))
    PROP_FLD_OP1.append(fld_prop_count)       
    Sum_ppl_op1= arcpy.da.TableToNumPyArray(Select_op1,'AV_PPL_DWL')
    PPL_sum_op1 = Sum_ppl_op1["AV_PPL_DWL"].sum()
    NO_PPL_OP1.append(PPL_sum_op1)

    ### LOG HOUSE ID of those properties exposed to flooding
    slr_name = int(slr*100)
    House_ID = arcpy.da.TableToNumPyArray(Select_op1,'Arc_ID')
    HousesID = pd.DataFrame(House_ID)    
    Log_outfile = ("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\Log\\Option1\\"+str(slr_name)+"_houses_op_one.csv")
    HousesID.to_csv(Log_outfile) 


AAPE_lookup['NO_OP_Prop_exp'] = PROP_FLD_BASE
AAPE_lookup['NO_OP_AAPE'] = NO_PPL
AAPE_lookup['OP1_Prop_exp'] = PROP_FLD_OP1
AAPE_lookup['OP1_AAPE'] = NO_PPL_OP1
AAPE_lookup['OP2_Prop_exp'] = PROP_FLD_OP2
AAPE_lookup['OP2_AAPE'] = NO_PPL_OP2
AAPE_lookup['OP3_Prop_exp'] = PROP_FLD_OP3
AAPE_lookup['OP3_AAPE'] = NO_PPL_OP3
AAPE_lookup['OP4_Prop_exp'] = PROP_FLD_OP4
AAPE_lookup['OP4_AAPE'] = NO_PPL_OP4
AAPE_lookup
 
AAPE_outfile_one = ("C:\\Users\\tdramm\\Desktop\\GIS_LE\\AAPE_Lookup\\"+date_string+" AAPE_Lookup.csv")
AAPE_lookup.to_csv(AAPE_outfile_one) 

t1 = time.clock()
tdiff = t1 - t0
tmin = tdiff/60
thour = tmin/60
print "It took %.3f seconds for this code to run" % (tdiff) + " (%.2f mins " % (tmin) + "/ %.2f hours)" % (thour) +" to run " 