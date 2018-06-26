## ArcGIS_Example.R - This script does the following (1) performs latin hypercube sampling to assist 
##                    in the scenario generation activities and (2) applies the sdtoolkit function which
##                    uses PRIM to undertake scenario discovery and illuminate vulnerabilities
##                    (i.e. candidate scenarios) in the data.


## LATIN HYPERCUBE SAMPLING
## DATABASE WITH LATIN HYPERCUBE SAMPLING
## Reference: ftp://cran.r-project.org/pub/R/web/packages/lhs/lhs.pdf
install.packages("lhs")
library(lhs)

## DEFINE THE SEED VALUE FOR RANDOM CALCULATIONS 
## Used for repeatable calculations. Number can be anything - assume 100.
set.seed(100)

## 7 variables, 300 scenarios
LHS_basic <- randomLHS(5000,7)
LHS_basic

## LHS_basic[,1] is mean SLR and between 0 and 2m
SLR_max = 1
SLR_min = 0
LHS_basic[,1] = round((LHS_basic[,1]*(SLR_max-SLR_min)/(1-0))+SLR_min,digit=2)

## LHS_basic[,2] is change in rainfall intensity and between -10% and 30% (24-hour rainfall intensity)
rain_max = 30
rain_min = -10
LHS_basic[,2] = round((LHS_basic[,2]*(rain_max-rain_min)/(1-0))+rain_min,digit=1)


## LHS_basic[,3] is the maximum CONTENTS damage per 4m2 for a residential house (give DEM size 2mx2m=4m2)
maxcontents_max = 2500
maxcontents_min = 500
LHS_basic[,3] = round((LHS_basic[,3]*(maxcontents_max-maxcontents_min)/(1-0))+maxcontents_min,digit=2)
  
## LHS_basic[,4] is the maximum STRUCTURAL damage per 4m2 for a residential house (give DEM size 2mx2m=4m2)
maxstructural_max = 10000
maxstructural_min = 4000
LHS_basic[,4] = round((LHS_basic[,4]*(maxstructural_max-maxstructural_min)/(1-0))+maxstructural_min,digits=0)

## LHS_basic[,5] is the damage index at 10cm inundation - based on vulnerability curves
## Variable reflects the change in damage index for 10cm flood
df_10cm_max = -0.1
df_10cm_min = 0.1
LHS_basic[,5] = round((LHS_basic[,5]*(df_10cm_max-df_10cm_min)/(1-0))+df_10cm_min,digits=2)

## LHS_basic[,6] is the Bruun Factor - range based on rules of thumb
## Variable reflects the horizontal recession responses for change in sea-level
bruun_fact_max = 100
bruun_fact_min = 10
LHS_basic[,6] = round((LHS_basic[,6]*(bruun_fact_max-bruun_fact_min)/(1-0))+bruun_fact_min,digits=0)

## LHS_basic[,7] is the Average ppeople per house in the suburb (ABS data)
av_ppl_house_max = 3
av_ppl_house_min = 2
LHS_basic[,7] = round((LHS_basic[,7]*(av_ppl_house_max-av_ppl_house_min)/(1-0))+av_ppl_house_min,digits=1)

## LHS_basic[,3] is change in average annual house value and between -10 to +10%
## aah_max = 10
## aah_min = -10
## LHS_basic[,3] = round(LHS_basic[,3]*(((aah_max-aah_min)/(1-0))+aah_min),digits=0)

## LHS_basic[,4] is change in % loss in houses at inundation of 10cm water and between 0 and +25%
## vuln_max = 25
## vuln_min = 0
## LHS_basic[,4] = round(LHS_basic[,4]*(((vuln_max-vuln_min)/(1-0))+vuln_min),digits=0)

DF <- data.frame(LHS_basic)
## Add a column for scenario number
DF$Scenario <- seq.int(nrow(DF))
## Reorder
DF <- DF[c(8,1,2,3,4,5,6,7)]
head(DF)
names(DF)<- c("Scenario","SLR","Rainfall", "maxcontents", "maxstructure", "df10cm","bruun_factor","Av_ppl")
head(DF)

par(mfrow=c(2,4))
plot(LHS_basic[,1],LHS_basic[,2], xlab="SLR (m)", ylab="Rainfall (%)")
plot(LHS_basic[,2],LHS_basic[,3], xlab="Rainfall (%)", ylab="Max contents damage ($/4m2)")
plot(LHS_basic[,3],LHS_basic[,4], xlab="Max contents damage ($/4m2)", ylab="Max structural damage ($/4m2)")
plot(LHS_basic[,4],LHS_basic[,5], xlab="Max structural damage ($/4m2)", ylab="Damage factor error (%)")
plot(LHS_basic[,5],LHS_basic[,6], xlab="Damage factor error (%)", ylab="Bruun Factor")
plot(LHS_basic[,6],LHS_basic[,7], xlab="Bruun Factor", ylab="Average People/House")
plot(LHS_basic[,7],LHS_basic[,1], xlab="Average People/House", ylab="SLR (m)")

## Export data to csv
setwd('C:/Users/tdramm/Desktop/GIS/Results')
write.csv(DF, file ="2017-05-11_5000Case_Generation.csv")

##_______________________________________________________________________________________
## FOR LOOP
## Look up the original csv and create a data frame
Scenario_Data<-read.csv('Scenarios.csv')

## For Loop
for(i in Scenario_Data$X){
  Scenario_Data$Output<-(Scenario_Data$SLR*4)+10*(Scenario_Data$Rainfall)+(Scenario_Data$Groundwater)
}

##Results add to Database
Scenario_Data


##_______________________________________________________________________________________
##_______________________________________________________________________________________
##_______________________________________________________________________________________
## WATER ELEVATION GRAPHS
setwd('P:\PhD 2015\8. Journal and Conference Papers\04 Evaluating Adaptation with Values (model example)')
water_el = read.csv("Water_elevation_relationships.csv")
head(water_el)

## Formatting: http://www.statmethods.net/advgraphs/parameters.html

par(mfrow=c(1,2))
plot(water_el$AEP, water_el$Average.w.e..extent., pch =19, ylim = c(-0.1,1.5), main = paste("(a) Average peak flood water","\nelevation change"), ylab = "Incremental rise from 20% AEP elevation (m)", xlab = "Exceedance Probability")
par(new=T)
plot(water_el$AEP, water_el$Plus.30..rain, xlab ="",ylab="",ylim = c(-0.1,1.5))
par(new=T)
plot(water_el$AEP, water_el$Less.10..rain, xlab ="",ylab="",ylim = c(-0.1,1.5))
lines(water_el$AEP, water_el$Average.w.e..extent.)
lines(water_el$AEP, water_el$Plus.30..rain, lty = 3)
lines(water_el$AEP, water_el$Less.10..rain, lty = 4)
## Legend: https://www.r-bloggers.com/adding-a-legend-to-a-plot/
legend (5,1.5,c("No change to rainfall (baseline)","30% rainfall increase","10% rainfall decrease"),lty=c(1,3,4),lwd=c(2.5,2.5,2.5),col=c("black","black","black"))

plot(water_el$AEP, water_el$Average.w.e..houses., pch =19, ylim = c(-0.1,1.5), main = paste("(b) Average peak flood water","\nelevation change","\n(flooded houses only)"), ylab = "Incremental rise from 20% AEP elevation (m)", xlab = "Exceedance Probability")
par(new=T)
plot(water_el$AEP, water_el$Plus.30..rain.1, xlab ="",ylab="",ylim = c(-0.1,1.5))
par(new=T)
plot(water_el$AEP, water_el$Less.10..rain.1, xlab ="",ylab="",ylim = c(-0.1,1.5))
lines(water_el$AEP, water_el$Average.w.e..houses.)
lines(water_el$AEP, water_el$Plus.30..rain.1, lty = 3)
lines(water_el$AEP, water_el$Less.10..rain.1, lty = 4)
legend (5,1.5,c("No change to rainfall (baseline)","30% rainfall increase","10% rainfall decrease"),lty=c(1,3,4),lwd=c(2.5,2.5,2.5),col=c("black","black","black"))




# Operationalising flooding to roads
op_pts = read.csv("Operational_points.csv")
head(op_pts)

DEM_pt1 = 1.96
DEM_pt2 = 2.0

par(mfrow=c(1,2))
plot(op_pts$AEP, op_pts$pt1.elevation, pch =19, ylim = c(1.5,3.5), main = paste("Average peak flood water","\nelevation change (point 1)"), ylab = "Incremental rise from 20% AEP elevation (m)", xlab = "Exceedance Probability")
lines(op_pts$AEP, op_pts$pt1.elevation)
par(new=T)
plot(op_pts$AEP, op_pts$X10p_rain, xlab ="",ylab="",ylim = c(1.5,3.5))
lines(op_pts$AEP, op_pts$X10p_rain, lty = 3)
abline(h=DEM_pt1,lty=4,lwd=3,col=554)
## Legend: https://www.r-bloggers.com/adding-a-legend-to-a-plot/
legend (5,3.5,c("Baseline (current)","10% rainfall increase", "DEM"),lty=c(1,3, 4),lwd=c(2.5,2.5, 2.5),col=c("black","black", "red"))

plot(op_pts$AEP, op_pts$pt2.elevation, pch =19, ylim = c(1.5,2.5), main = paste("Average peak flood water elevation change"), ylab = "Incremental water elevation rise from 20% AEP flood (m)", xlab = "Exceedance Probability")
lines(op_pts$AEP, op_pts$pt2.elevation)
par(new=T)
plot(op_pts$AEP, op_pts$X10p_rain.1, xlab ="",ylab="",ylim = c(1.5,2.5))
lines(op_pts$AEP, op_pts$X10p_rain.1, lty = 3)
abline(h=DEM_pt2,lty=4,lwd=3,col=554)
## Legend: https://www.r-bloggers.com/adding-a-legend-to-a-plot/
legend (8,2.5,c("Baseline (current)","4.8% rainfall increase", "DEM"),lty=c(1,3, 4),lwd=c(2.5,2.5, 2.5),col=c("black","black", "red"))




##_______________________________________________________________________________________
##_______________________________________________________________________________________
##_______________________________________________________________________________________
## ROBUST DECISION MAKING (RDM) USING THE PATIENT RULE INDUCTION METHOD (PRIM)
## https://cran.r-project.org/web/packages/sdtoolkit/sdtoolkit.pdf
## page 10: Patient Rule Induction Method Adapted for Scenario Discovery
install.packages("sdtoolkit")
library(sdtoolkit)

## Set working directory and read in csv file
setwd('C:/Users/tdramm/Desktop/GIS/Results')
test = read.csv("2017-05-25CaseStudyResults.csv")
head(test)

## Define thresholds
AAD_thresh = 650000
AAPE_thresh = 23.5
Beach_thresh = 5

## Number of values that meet risk threshold
sum(test$Av.Annual.Damages<AAD_thresh)
## Number of values that do NOT meet risk threshold
sum(test$Av.Annual.Damages>=AAD_thresh)

sum(test$Av.People.Exposed<AAPE_thresh)
sum(test$Av.People.Exposed>=AAPE_thresh)
sum(test$Average.Beach.Width<Beach_thresh)
sum(test$Average.Beach.Width>=Beach_thresh)

## Plot of results
## Format ref: http://www.statmethods.net/advgraphs/parameters.html
par(mfrow=c(2,1))
plot(test$Av.People.Exposed,test$Av.Annual.Damages,main="(a) Risk to AAPE and AAD", xlab = "AAPE (ppl/year)",ylab="AAD ($/year)", pch = 20, xlim=c(0,50),ylim=c(0,2000000))
abline(v=AAPE_thresh,lty=4,lwd=3,col=554)
abline(h=AAD_thresh,lty=4,lwd=3,col=554)
plot(test$Average.Beach.Width,test$Av.Annual.Damages,main="(b) Risk to Average Beach Width and AAD", xlab = "Beach Width (m)",ylab="AAD ($/year)", pch = 20, xlim=c(0,30),ylim=c(0,2000000))
abline(v=Beach_thresh,lty=4,lwd=3,col=554)
abline(h=AAD_thresh,lty=4,lwd=3,col=554)
#plot(test$Average.Beach.Width,test$Av.People.Exposed,main="(c) Risk to Average Beach Width and AAPE", xlab = "Beach Width (m)",ylab="AAPE (ppl/year)", pch = 20, xlim=c(0,30),ylim=c(0,50))
#abline(v=Beach_thresh,lty=4,lwd=3,col=554)
#abline(h=AAPE_thresh,lty=4,lwd=3,col=554)
par(mfrow=c(1,1))


## Visual - Scatter plot and Correlation
par(mfrow=c(3,2))
plot(Av.Annual.Damages~SLR,data=test, xlab="SLR (m)", ylab="AAD ($/year)")
abline(lm(test$Av.Annual.Damages~test$SLR),lty=4,lwd=3,col=554)
plot(Av.Annual.Damages~Rainfall,data=test, xlab="Rainfall intensity (%)", ylab="AAD ($/year)")
abline(lm(test$Av.Annual.Damages~test$Rainfall),lty=4,lwd=3,col=554)
plot(Av.Annual.Damages~maxcontents,data=test, xlab="Maximum contents damage ($)", ylab="AAD ($/year)")
abline(lm(test$Av.Annual.Damages~test$maxcontents),lty=4,lwd=3,col=554)
plot(Av.Annual.Damages~maxstructure,data=test, xlab="Maximum structural damage ($)", ylab="AAD ($/year)")
abline(lm(test$Av.Annual.Damages~test$maxstructure),lty=4,lwd=3,col=554)
plot(Av.Annual.Damages~df10cm,data=test, xlab="Damage at 10cm inundation", ylab="AAD ($/year)")
abline(lm(test$Av.Annual.Damages~test$df10cm),lty=4,lwd=3,col=554)
## Correlation
cor(test[,c(4,5,6,7,8)], test[,32])
par(mfrow=c(1,1))

par(mfrow=c(3,1))
plot(Av.People.Exposed~SLR,data=test, xlab="SLR (m)", ylab="AAPE (ppl/year)")
abline(lm(test$Av.People.Exposed~test$SLR),lty=4,lwd=3,col=554)
plot(Av.People.Exposed~Rainfall,data=test, xlab="Rainfall intensity (%)", ylab="AAPE (ppl/year)")
abline(lm(test$Av.People.Exposed~test$Rainfall),lty=4,lwd=3,col=554)
plot(Av.People.Exposed~Av_ppl,data=test, xlab="Av.People.per.dwelling", ylab="AAPE (ppl/year)")
abline(lm(test$Av.People.Exposed~test$Av_ppl),lty=4,lwd=3,col=554)
cor(test[,c(4,5,10)], test[,33])
par(mfrow=c(1,1))

par(mfrow=c(2,1))
plot(Average.Beach.Width~SLR,data=test, xlab="SLR (m)", ylab="Average.Beach.Width (m)")
abline(lm(test$Average.Beach.Width~test$SLR),lty=4,lwd=3,col=554)
plot(Average.Beach.Width~bruun_factor,data=test, xlab="Bruun Factor", ylab="Average.Beach.Width (m)")
abline(lm(test$Average.Beach.Width~test$bruun_factor),lty=4,lwd=3,col=554)
cor(test[,c(4,9)], test[,14])
par(mfrow=c(1,1))


## Show histogram of the results
## Referene on formatting: https://www.r-bloggers.com/how-to-make-a-histogram-with-basic-r/
par(mfrow=c(3,1))
max(test$Av.Annual.Damages)
hist(test$Av.Annual.Damages,breaks=c(seq(0,2000000,100000)), main = "Historgram of AAD outcomes", xlab = "AAD ($/year)")
##Show threshold on histogram
##Could also do a horizontal line
abline(v=AAD_thresh,lty=2,lwd=3,col=30)

max(test$Av.People.Exposed)
hist(test$Av.People.Exposed,breaks=c(seq(0,50,1)),main = "Historgram of AAPE outcomes", xlab = "AAPE (people/year)")
abline(v=AAPE_thresh,lty=2,lwd=3,col=30)

max(test$Average.Beach.Width)
hist(test$Average.Beach.Width,breaks=c(seq(0,30,2)),main = "Historgram of average beach width outcomes", xlab = "width (m)")
abline(v=Beach_thresh,lty=2,lwd=3,col=30)

par(mfrow=c(1,3))
boxplot(test$Av.Annual.Damages, xlab="AAD", ylab = "$/year")
boxplot(test$Av.People.Exposed, xlab = "AAPE", ylab = "ppl/year")
boxplot(test$Average.Beach.Width, xlab = "beach width", ylab = "m")
par(mfrow=c(1,1))


## AAD PRIM ANALYSIS
## Select input columns
inputs=test[,c(4,5,6,7,8)]
head(inputs)
## Select output columns
output=test[,32]
head(output)

##Run sd toolkit
##Look at smaller number of pass/fails - i.e. only small number pass so interrogate this (i.e. <AAD)
##If < uses, y values less than thresh will be 1's (cases of interest), all values graeter 0's
sdprim(inputs, output, thresh=AAD_thresh,threshtype="<",peel_crit = 1)

## AAPE
inputs=test[,c(4,5,10)]
head(inputs)
output=test[,33]
head(output)
sdprim(inputs, output, thresh=AAPE_thresh,threshtype="<",peel_crit = 1)

## BEACH WIDTH
inputs=test[,c(4,9)]
head(inputs)
output=test[,14]
head(output)
sdprim(inputs, output, thresh=Beach_thresh,threshtype=">",peel_crit = 1)





##_______________________________________________________________________________________
## Classification and regression tree (CART) EXAMPLE
## Classification with trees
## rpart package
## https://cran.r-project.org/web/packages/rpart/rpart.pdf

install.packages("rpart")
library(rpart)

setwd('C:/Users/tdramm/Desktop/GIS/Results')
test = read.csv("2017-03-04scenarioresults.csv")
head(test)

## predictor variables
inputs=test[,c(4,5,7,8)]
head(inputs)
output=test[,20]
head(output)

require(rpart)

test.rpart = rpart(Av.Annual.Damages ~ SLR + Rainfall + maxdam + df10cm, data = test)
plotcp(test.rpart)
printcp(test.rpart)
summary(test.rpart)

test.rpart2 = prune (test.rpart, cp = 0.02)
plot(test.rpart2, uniform = TRUE, main = "Classification tree for AAD (move left to left branch if cond. true)")
text(test.rpart2, use.n = TRUE, cex = 0.75)

