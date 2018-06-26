# -*- coding: utf-8 -*-
"""
Spyder Editor

Created in Jan 2018

@author: tdramm

CaseTwo_PRIM.py -   The script uses the patient rule induction method as part 
                    of scenario discovrey to describe adaptation tipping
                    points.
                    
                    It uses the results output from the CaseStudyTwo_RDM.py 
                    script.
                          
"""

import pandas as pd
import prim
#import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

##Package details: https://github.com/Project-Platypus/PRIM

###############################################################################
##NO POLICY OPTION

Table = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\2018-03-07_Case_Results_RDM.csv')
Table

##Method 1 using the PRIM package
##https://github.com/julierozenberg/excel_model_Tijen/blob/master/scenario%20discovery.ipynb
inputs1 = Table.loc[:,['r_sea','m_str','d_i','m_con','slr']]
#inputs1 = Table.loc[:,['r_sea','m_str','m_con','slr']]
inputs1
inputs2 = Table.loc[:,['r_sea','a_ppl','slr']]
inputs2
outputs = Table.loc[:,['AAD','AAPE']]
outputs

sns.distplot(outputs.AAD)
sns.distplot(outputs.AAPE)
sns.pairplot(outputs)

outputs['AAD_bin'] = np.where(outputs['AAD']<3700000, 1, 0) #Assing binary
sum(outputs['AAD_bin'])

outputs['AAPE_bin'] = np.where(outputs['AAPE']<94, 1, 0) #Assing binary
sum(outputs['AAPE_bin'])
# Look at smaller number of pass/fails - i.e. only small number are under threshold, so interrogate this
# If '<' used, y values less than thresh will be 1's (cases of interest), all values graeter 0's


##https://github.com/Project-Platypus/PRIM/blob/master/README.md
# AAPE OBJECTIVE
# In this instance we are interested in cases where the response is greater than 0.5
# (as indicated by the "threshold" and "threshold_type" arguments)
p = prim.Prim(inputs2, outputs.AAPE_bin, threshold=0.5, threshold_type=">")
box = p.find_box()
box.show_tradeoff()
plt.show()

box.select(42)
print(box)
box.show_details()

# AAD OBJECTIVE
p = prim.Prim(inputs1, outputs.AAD_bin, threshold=0.5, threshold_type=">")
box = p.find_box()
box.show_tradeoff()
plt.show()

box.select(42)
print(box)
box.show_details()



###############################################################################
##OPTION 1: PROTECT

Table_op1 = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\2018-03-11_Case_Results_RDM_OPTION1_BARRIER.csv')
Table_op1
inputs1op1 = Table_op1.loc[:,['r_sea','m_str','d_i','m_con','slr']]
inputs1op1
inputs2op1 = Table_op1.loc[:,['r_sea','a_ppl','slr']]
inputs2op1
outputsop1 = Table_op1.loc[:,['AAD','AAPE']]
outputsop1

sns.distplot(outputsop1.AAD)
sns.distplot(outputsop1.AAPE)
sns.pairplot(outputsop1)

outputsop1['AAD_bin'] = np.where(outputsop1['AAD']<3700000, 1, 0) #Assing binary
sum(outputsop1['AAD_bin'])

outputsop1['AAPE_bin'] = np.where(outputsop1['AAPE']<94, 1, 0) #Assing binary
sum(outputsop1['AAPE_bin'])

# AAPE OBJECTIVE
p = prim.Prim(inputs2op1, outputsop1.AAPE_bin, threshold=0.5, threshold_type=">")
box = p.find_box()
box.show_tradeoff()
plt.show()

box.select(13)
print(box)
box.show_details()

# AAD OBJECTIVE
p = prim.Prim(inputs1op1, outputsop1.AAD_bin, threshold=0.5, threshold_type=">")
box = p.find_box()
box.show_tradeoff()
plt.show()

box.select(25)
print(box)
box.show_details()



###############################################################################
##OPTION 2: NEW BUILDING REGULATIONS

Table_op2 = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\2018-03-16_Case_Results_RDM_OPTION2_BLDREG.csv')
Table_op2
inputs1op2 = Table_op2.loc[:,['r_sea','m_str','d_i','m_con','slr']]
inputs1op2
inputs2op2 = Table_op2.loc[:,['r_sea','a_ppl','slr']]
inputs2op2
outputsop2 = Table_op2.loc[:,['AAD','AAPE']]
outputsop2

sns.distplot(outputsop2.AAD)
sns.distplot(outputsop2.AAPE)
sns.pairplot(outputsop2)

outputsop2['AAD_bin'] = np.where(outputsop2['AAD']<3700000, 1, 0) #Assing binary
sum(outputsop2['AAD_bin'])

outputsop2['AAPE_bin'] = np.where(outputsop2['AAPE']<94, 1, 0) #Assing binary
sum(outputsop2['AAPE_bin'])

# AAPE OBJECTIVE
p = prim.Prim(inputs2op2, outputsop2.AAPE_bin, threshold=0.5, threshold_type=">")
box = p.find_box()
box.show_tradeoff()
plt.show()

box.select(15)
print(box)
box.show_details()

# AAD OBJECTIVE
p = prim.Prim(inputs1op2, outputsop2.AAD_bin, threshold=0.5, threshold_type=">")
box = p.find_box()
box.show_tradeoff()
plt.show()

box.select(16)
print(box)
box.show_details()



###############################################################################
##OPTION 3: LAND USE CHANGES

Table_op3 = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\2018-03-13_Case_Results_RDM_OPTION3_LAND.csv')
Table_op3
inputs1op3 = Table_op3.loc[:,['r_sea','m_str','d_i','m_con','slr']]
inputs1op3
inputs2op3 = Table_op3.loc[:,['r_sea','a_ppl','slr']]
inputs2op3
outputsop3 = Table_op3.loc[:,['AAD','AAPE']]
outputsop3

sns.distplot(outputsop3.AAD)
sns.distplot(outputsop3.AAPE)
sns.pairplot(outputsop3)

outputsop3['AAD_bin'] = np.where(outputsop3['AAD']<3700000, 1, 0) #Assing binary
sum(outputsop3['AAD_bin'])

outputsop3['AAPE_bin'] = np.where(outputsop3['AAPE']<94, 1, 0) #Assing binary
sum(outputsop3['AAPE_bin'])

# AAPE OBJECTIVE
p = prim.Prim(inputs2op3, outputsop3.AAPE_bin, threshold=0.5, threshold_type=">")
box = p.find_box()
box.show_tradeoff()
plt.show()

box.select(17)
print(box)
box.show_details()

# AAD OBJECTIVE
p = prim.Prim(inputs1op3, outputsop3.AAD_bin, threshold=0.5, threshold_type=">")
box = p.find_box()
box.show_tradeoff()
plt.show()

box.select(38)
print(box)
box.show_details()


###############################################################################
##OPTION 4: RETREAT

Table_op4 = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\zzCODE_TESTING\\2018-03-15_Case_Results_RDM_OPTION4_RETREAT.csv')
Table_op4
inputs1op4 = Table_op4.loc[:,['r_sea','m_str','d_i','m_con','slr']]
inputs1op4
inputs2op4 = Table_op4.loc[:,['r_sea','a_ppl','slr']]
inputs2op4
outputsop4 = Table_op4.loc[:,['AAD','AAPE']]
outputsop4

sns.distplot(outputsop4.AAD)
sns.distplot(outputsop4.AAPE)
sns.pairplot(outputsop4)

outputsop4['AAD_bin'] = np.where(outputsop4['AAD']<3700000, 1, 0) #Assing binary
sum(outputsop4['AAD_bin'])

outputsop4['AAPE_bin'] = np.where(outputsop4['AAPE']<94, 1, 0) #Assing binary
sum(outputsop4['AAPE_bin'])

# AAPE OBJECTIVE
p = prim.Prim(inputs2op4, outputsop4.AAPE_bin, threshold=0.5, threshold_type=">")
box = p.find_box()
box.show_tradeoff()
plt.show()

box.select(17)
print(box)
box.show_details()

# AAD OBJECTIVE
p = prim.Prim(inputs1op4, outputsop4.AAD_bin, threshold=0.5, threshold_type=">")
box = p.find_box()
box.show_tradeoff()
plt.show()

box.select(16)
print(box)
box.show_details()






###############################################################################
##Method 2 using the EMA_Workbench package


#https://github.com/quaquel/EMAworkbench/blob/master/ema_workbench/examples/prim_wcm_example.py
#from ema_workbench.analysis import prim
#
#
#
###SET SEED TEST
#import numpy as np
#from pyDOE import lhs
#
#uncertainties_list = pd.read_csv('C:\\Users\\tdramm\\Desktop\\GIS_LE\\Uncertainties_list.csv')
#uncertainties_list
#
#numUncertainties=len(uncertainties_list)
#numCases=1000
#np.random.seed(seed=10)
#
#lhsample = lhs(numUncertainties,numCases)
#lhsample

## THIS SHOULD WORK...



