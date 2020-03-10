import ROOT
import os
import pdb
import numpy
from numpy import median
import optparse

parser=optparse.OptionParser()
(options,args)=parser.parse_args()


# Open ROOT file
rootFile=ROOT.TFile(args[0],'OPEN')

# Make dictionary of histograms of limit/limitErr
#masses=[1000+100*i for i in xrange(0,9)]
masses=numpy.arange(1000,4600,100)
#masses=numpy.arange(1200,4600,100)
tree=rootFile.Get('limit')

# Get limits, erros, and ratios
limit={mass:[] for mass in masses}
limitErr={mass:[] for mass in masses}
limitRatio={mass:[] for mass in masses}
#largePulls={mass:{} for mass in masses}
for event in tree:
  if event.quantileExpected<0:
    mass=event.mh
    if event.limitErr>0.1:
      continue
    limit[mass].append(event.limit)
    limitErr[mass].append(event.limitErr)
    if event.limitErr!=0:
      limitRatio[mass].append(event.limit/event.limitErr)
      #if limitRatio[mass]>5:


# Get median values
limitRatioMedian={}
for mass in masses:
  limitRatioMedian[mass]=median(limitRatio[mass])

# Make plot of median as a function of mass
binsMass=len(masses)+2
plotMaxMassX=1.25*(max(masses))
plotMinMassX=1.25*(min(masses))
binsMedian=100
plotMaxMedianY=1.25*max(limitRatioMedian.values())
plotMinMedianY=1.25*min(limitRatioMedian.values())
medianPlot=ROOT.TH2D('medianPlot','medianPlot;M_{X} (GeV);median(limit/limitErr)',binsMass,plotMinMassX,plotMaxMassX,binsMedian,plotMaxMedianY,plotMinMedianY)

# Make plot of median as a function of limitErr
plotMaxErrX=1.25*(max(limitErr[min(masses)]))
#plotMinErrX=1.25*(min(limitErr[min(masses)]))
plotMinErrX=0
for mass in masses:
  plotMaxErrXTemp=1.25*(max(limitErr[mass]))
  plotMinErrXTemp=1.25*(min(limitErr[mass]))
  if plotMaxErrXTemp>plotMaxErrX:
    plotMaxErrX=plotMaxErrXTemp
  if plotMinErrXTemp<plotMinErrX:
    plotMinErrX=plotMinErrXTemp
medianLimErrPlot=ROOT.TH2D('limVsLimErrPlot','limVsLimErrPlot;limErr;median(limit/limitErr)',binsMedian,plotMinErrX,plotMaxErrX,binsMedian,plotMaxMedianY,plotMinMedianY)

# Fill plots
for mass in masses:
  medianPlot.Fill(mass,limitRatioMedian[mass])
  for err in limitErr[mass]:
    medianLimErrPlot.Fill(err,limitRatioMedian[mass])

#pdb.set_trace()

fileOut=ROOT.TFile('medianPlot.root','RECREATE')
fileOut.cd()
medianPlot.Write()
medianLimErrPlot.Write()
fileOut.Close()
