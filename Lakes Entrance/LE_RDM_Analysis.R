#############################################################################################################
## LE_RDM_Analysis.R - This script does the following (1) performs latin hypercube sampling (LHS) to assist 
##                     in the case generation activities and (2) applies the sdtoolkit function which
##                     uses PRIM to undertake scenario discovery and illuminate vulnerabilities
##                     (i.e. candidate scenarios) in the data. Note the the LHS script can be run in RStudio, 
##                     however the sdtoolkit can only be run on a PC (Windows) and using the original Windows
##                     R GUI (e.g. R i386 3.2.0 or Rx64 3.2.0).
#############################################################################################################

#############################################################################################################
## 1. LATIN HYPERCUBE SAMPLING
#############################################################################################################

## DATABASE WITH LATIN HYPERCUBE SAMPLING
## Reference: ftp://cran.r-project.org/pub/R/web/packages/lhs/lhs.pdf
install.packages("lhs")
library(lhs)

## DEFINE THE SEED VALUE FOR RANDOM CALCULATIONS 
## Used for repeatable calculations. Number can be anything - assume 100.
set.seed(100)

Cases = read.csv("C:/Users/tdramm/Desktop/GIS_LE/Uncertainties_list.csv")
head(Cases)
Cases


## 20 variables, 5000 scenarios
LHS_basic <- randomLHS(5000,20)
LHS_basic

#setwd("C:/Users/tdramm/Desktop/GIS_LE/zzCODE_TESTING")
#write.csv(LHS_basic, file ="LHS_random_sample_R.csv")

## LHS_basic[,1] is l_sub
l_sub_subset = Cases[1,]
l_sub_max = l_sub_subset$Max
l_sub_min = l_sub_subset$Min
LHS_basic[,1] = round(LHS_basic[,1]*(l_sub_max-l_sub_min)+l_sub_min,digit=2)
LHS_basic[,1]

## LHS_basic[,2] is a_poly
a_poly_subset = Cases[2,]
a_poly_max = a_poly_subset$Max
a_poly_min = a_poly_subset$Min
LHS_basic[,2] = round(LHS_basic[,2]*(a_poly_max-a_poly_min)+a_poly_min,digit=2)
LHS_basic[,2]

## LHS_basic[,3] is b_poly
b_poly_subset = Cases[3,]
b_poly_max = b_poly_subset$Max
b_poly_min = b_poly_subset$Min
LHS_basic[,3] = round(LHS_basic[,3]*(b_poly_max-b_poly_min)+b_poly_min,digit=2)
LHS_basic[,3]

## LHS_basic[,4] is c_poly
c_poly_subset = Cases[4,]
c_poly_max = c_poly_subset$Max
c_poly_min = c_poly_subset$Min
LHS_basic[,4] = round(LHS_basic[,4]*(c_poly_max-c_poly_min)+c_poly_min,digit=3)
LHS_basic[,4]

## LHS_basic[,5] is c_star
c_star_subset = Cases[5,]
c_star_max = c_star_subset$Max
c_star_min = c_star_subset$Min
LHS_basic[,5] = round(LHS_basic[,5]*(c_star_max-c_star_min)+c_star_min,digit=2)
LHS_basic[,5]

## LHS_basic[,6] is t_star
t_star_subset = Cases[6,]
t_star_max = t_star_subset$Max
t_star_min = t_star_subset$Min
LHS_basic[,6] = round(LHS_basic[,6]*(t_star_max-t_star_min)+t_star_min,digit=0)
LHS_basic[,6]

## LHS_basic[,7] is r_sea
r_sea_subset = Cases[7,]
r_sea_max = r_sea_subset$Max
r_sea_min = r_sea_subset$Min
LHS_basic[,7] = round(LHS_basic[,7]*(r_sea_max-r_sea_min)+r_sea_min,digit=2)
LHS_basic[,7]

## LHS_basic[,8] is m_str
m_str_subset = Cases[8,]
m_str_max = m_str_subset$Max
m_str_min = m_str_subset$Min
LHS_basic[,8] = round(LHS_basic[,8]*(m_str_max-m_str_min)+m_str_min,digit=2)
LHS_basic[,8]

## LHS_basic[,9] is m_con
m_con_subset = Cases[9,]
m_con_max = m_con_subset$Max
m_con_min = m_con_subset$Min
LHS_basic[,9] = round(LHS_basic[,9]*(m_con_max-m_con_min)+m_con_min,digit=2)
LHS_basic[,9]

## LHS_basic[,10] is a_ppl
a_ppl_subset = Cases[10,]
a_ppl_max = a_ppl_subset$Max
a_ppl_min = a_ppl_subset$Min
LHS_basic[,10] = round(LHS_basic[,10]*(a_ppl_max-a_ppl_min)+a_ppl_min,digit=2)
LHS_basic[,10]

## LHS_basic[,11] is d_i
d_i_subset = Cases[11,]
d_i_max = d_i_subset$Max
d_i_min = d_i_subset$Min
LHS_basic[,11] = round(LHS_basic[,11]*(d_i_max-d_i_min)+d_i_min,digit=2)
LHS_basic[,11]

## LHS_basic[,12] is r_str
r_str_subset = Cases[12,]
r_str_max = r_str_subset$Max
r_str_min = r_str_subset$Min
LHS_basic[,12] = round(LHS_basic[,12]*(r_str_max-r_str_min)+r_str_min,digit=4)
LHS_basic[,12]


## LHS_basic[,13] is r_con
r_con_subset = Cases[13,]
r_con_max = r_con_subset$Max
r_con_min = r_con_subset$Min
LHS_basic[,13] = round(LHS_basic[,13]*(r_con_max-r_con_min)+r_con_min,digit=4)
LHS_basic[,13]

## LHS_basic[,14] is r_ppl
r_ppl_subset = Cases[14,]
r_ppl_max = r_ppl_subset$Max
r_ppl_min = r_ppl_subset$Min
LHS_basic[,14] = round(LHS_basic[,14]*(r_ppl_max-r_ppl_min)+r_ppl_min,digit=3)
LHS_basic[,14]

## LHS_basic[,15] is r
r_subset = Cases[15,]
r_max = r_subset$Max
r_min = r_subset$Min
LHS_basic[,15] = round(LHS_basic[,15]*(r_max-r_min)+r_min,digit=3)
LHS_basic[,15]

## LHS_basic[,20] is slr
slr_subset = Cases[20,]
slr_subset_max = slr_subset$Max
slr_subset_min = slr_subset$Min
LHS_basic[,16] = round(LHS_basic[,16]*(slr_subset_max-slr_subset_min)+slr_subset_min,digit=2)
LHS_basic[,16]

## LHS_basic[,21] is rate_op1
rate_op1_subset = Cases[21,]
rate_op1_subset_max = rate_op1_subset$Max
rate_op1_subset_min = rate_op1_subset$Min
LHS_basic[,17] = round(LHS_basic[,17]*(rate_op1_subset_max-rate_op1_subset_min)+rate_op1_subset_min,digit=0)
LHS_basic[,17]

## LHS_basic[,22] is rate_op2
rate_op2_subset = Cases[22,]
rate_op2_subset_max = rate_op2_subset$Max
rate_op2_subset_min = rate_op2_subset$Min
LHS_basic[,18] = round(LHS_basic[,18]*(rate_op2_subset_max-rate_op2_subset_min)+rate_op2_subset_min,digit=0)
LHS_basic[,18]

## LHS_basic[,23] is rate_op3
rate_op3_subset = Cases[23,]
rate_op3_subset_max = rate_op3_subset$Max
rate_op3_subset_min = rate_op3_subset$Min
LHS_basic[,19] = round(LHS_basic[,19]*(rate_op3_subset_max-rate_op3_subset_min)+rate_op3_subset_min,digit=0)
LHS_basic[,19]

## LHS_basic[,24] is rate_op4
rate_op4_subset = Cases[24,]
rate_op4_subset_max = rate_op4_subset$Max
rate_op4_subset_min = rate_op4_subset$Min
LHS_basic[,20] = round(LHS_basic[,20]*(rate_op4_subset_max-rate_op4_subset_min)+rate_op4_subset_min,digit=0)
LHS_basic[,20]




DF <- data.frame(LHS_basic)
## Add a column for scenario number
DF$Scenario <- seq.int(nrow(DF))
## Reorder
DF <- DF[c(21,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)]
head(DF)
names(DF)<- c("Case","l_sub","a_poly", "b_poly", "c_poly", "c_star","t_star","r_sea", "m_str", "m_con", "a_ppl", "d_i", "r_str", "r_con", "r_ppl", "r", "slr", "rate_op1", "rate_op2", "rate_op3", "rate_op4")
head(DF)

# Plot  pairs as visualisation to check that sampled parameters are scattered
pairs(~a_poly+b_poly+c_poly+slr, data=DF)
pairs(~c_star+t_star+r_sea, data=DF)
pairs(~+m_str+m_con+r_str+r_con, data=DF)
pairs(~l_sub+a_ppl+r_ppl+d_i, data=DF)
pairs(~rate_op1+rate_op2+rate_op3+rate_op4, data = DF)

## Export data to csv
setwd("C:/Users/tdramm/Desktop/GIS_LE")
write.csv(DF, file ="2018-02-28_5000Case_Generation.csv")



#############################################################################################################
## ROBUST DECISION MAKING (RDM) USING THE PATIENT RULE INDUCTION METHOD (PRIM)
#############################################################################################################

## https://cran.r-project.org/web/packages/sdtoolkit/sdtoolkit.pdf
## page 10: Patient Rule Induction Method Adapted for Scenario Discovery

install.packages("sdtoolkit")
library(sdtoolkit)

## Set working directory and read in csv file
setwd("C:/Users/tdramm/Desktop/GIS_LE/zzCODE_TESTING")
test = read.csv("2018-03-07_Case_Results_RDM.csv")
head(test)

## Define thresholds
##NPV_thresh = 0
#aad_thresh = 2400000
#aape_thresh = 9.3
aad_thresh = 3700000
aape_thresh = 94


test$AAD_bin = ifelse(test$AAD < aad_thresh,1,0)
test$AAPE_bin = ifelse(test$AAPE < aape_thresh,1,0)
head(test)

## Remove NA values from data
test = na.omit(test)
head(test)

## Number of values that meet risk threshold
sum(test$AAD<aad_thresh)
## Number of values that do NOT meet risk threshold
sum(test$AAD>=aad_thresh)

sum(test$AAPE<aape_thresh)
sum(test$AAPE>=aape_thresh)


## Plot of results
## Format ref: http://www.statmethods.net/advgraphs/parameters.html
plot(test$X,test$AAD)
## hist(test$AAD)
plot(test$AAPE,test$AAD, main="Risk to AAPE and AAD", xlab = "AAPE (ppl/year)",ylab="AAD ($/year)", pch = 20)
abline(h=aad_thresh,lty=4,lwd=3,col=554)
abline(v=aape_thresh,lty=4,lwd=3,col=554)

## Show histogram of the results
## Referene on formatting: https://www.r-bloggers.com/how-to-make-a-histogram-with-basic-r/
par(mfrow=c(2,1))
max(test$AAD)
max(test$AAPE)
hist(test$AAD,breaks=c(seq(0,200000000,2000000)), main = "Historgram of AAD outcomes", xlab = "AAD ($/year)")
##Show threshold on histogram
##Could also do a horizontal line
abline(v=aad_thresh,lty=2,lwd=3,col=30)
hist(test$AAPE,breaks=c(seq(0,2000,20)), main = "Historgram of AAPE outcomes", xlab = "AAPE (ppl/year)")
abline(v=aape_thresh,lty=2,lwd=3,col=30)
par(mfrow=c(1,1))

## AAD Visual - Scatter plot and Correlation
par(mfrow=c(3,2))
plot(AAD~r_sea,data=test, xlab="r_sea", ylab="AAD ($/year)")
abline(lm(test$AAD~test$r_sea),lty=4,lwd=3,col=554)
plot(AAD~m_str,data=test, xlab="m_str (%)", ylab="AAD ($/year)")
abline(lm(test$AAD~test$m_str),lty=4,lwd=3,col=554)
plot(AAD~m_con,data=test, xlab="m_con (%)", ylab="AAD ($/year)")
abline(lm(test$AAD~test$m_con),lty=4,lwd=3,col=554)
plot(AAD~d_i,data=test, xlab="d_i", ylab="AAD ($/year)")
abline(lm(test$AAD~test$d_i),lty=4,lwd=3,col=554)
plot(AAD~slr,data=test, xlab="slr (m)", ylab="AAD ($/year)")
abline(lm(test$AAD~test$slr),lty=4,lwd=3,col=554)
## Correlation
cor(test[,c(10,11,12,14,19)], test[,57])
par(mfrow=c(1,1))

## AAPE Visual - Scatter plot and Correlation
par(mfrow=c(2,2))
plot(AAPE~r_sea,data=test, xlab="r_sea", ylab="AAPE (ppl/year)")
abline(lm(test$AAPE~test$r_sea),lty=4,lwd=3,col=554)
plot(AAPE~a_ppl,data=test, xlab="a_ppl (%)", ylab="AAPE (ppl/year)")
abline(lm(test$AAPE~test$a_ppl),lty=4,lwd=3,col=554)
plot(AAPE~slr,data=test, xlab="slr (m)", ylab="AAPE (ppl/year)")
abline(lm(test$AAPE~test$slr),lty=4,lwd=3,col=554)
## Correlation
cor(test[,c(10,13,19)], test[,58])
par(mfrow=c(1,1))

## AAD PRIM ANALYSIS
## Select input columns
inputs=test[,c(10,11,12,14,19)]
head(inputs)
## Select output columns
output=test[,57]
head(output)

inputs2=test[,c(10,13,19)]
head(inputs2)
output2=test[,58]
head(output2)

##Run sd toolkit
##Look at smaller number of pass/fails - i.e. only small number pass so interrogate this (i.e. <AAD)
##If < uses, y values less than thresh will be 1's (cases of interest), all values graeter 0's
##sdprim(inputs, output, thresh=NPV_thresh,threshtype=">=",peel_crit = 1)

## AAD PRIM TEST
sdprim(inputs, output, thresh=aad_thresh,threshtype="<",peel_crit = 1)

#AAPE PRIM TEST
sdprim(inputs2, output2, thresh=aape_thresh,threshtype="<",peel_crit = 1)



