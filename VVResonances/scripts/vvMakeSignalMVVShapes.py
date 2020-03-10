#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json

def returnString(func):
  st='0'
  for i in range(0,func.GetNpar()):
    st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
  return st

parser=optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-f","--scaleFactors",dest="scaleFactors",help="Additional scale factors separated by comma",default='')

(options,args)=parser.parse_args()

# Define output dictionary
plotters={}
graphs={
'MEAN':ROOT.TGraphErrors(),
'SIGMA':ROOT.TGraphErrors(),
'ALPHA1':ROOT.TGraphErrors(),
'N1':ROOT.TGraphErrors(),
'ALPHA2':ROOT.TGraphErrors(),
'N2':ROOT.TGraphErrors()
}

scaleFactors=options.scaleFactors.split(',')

sampleTypes=options.sample.split(',')

filelist=[]
if args[0]=='ntuples':
  filelist=[g for flist in [[(path+'/'+f) for f in os.listdir(args[0]+'/'+path)] for path in os.listdir(args[0])] for g in flist]
else:
  filelist=os.listdir(args[0])


for filename in filelist:
  for sampleType in sampleTypes:
    if not (filename.find(sampleType)!=-1):
      continue

    #pdb.set_trace()
    # Get masses from samples
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
      continue

    mass=float(fname.split('_')[-1])
    if not mass in plotters.keys():
      plotters[mass]=[]

    plotters[mass].append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
    plotters[mass][-1].setupFromFile(args[0]+'/'+fname+'.pck')
    plotters[mass][-1].addCorrectionFactor('xsec','tree')
    plotters[mass][-1].addCorrectionFactor('genWeight','tree')
    plotters[mass][-1].addCorrectionFactor('puWeight','tree')
    plotters[mass][-1].filename=fname
    if options.scaleFactors!='':
      for s in scaleFactors:
        plotter[mass][-1].addCorrectionFactor(s,'tree')

    print 'found',filename,'mass',str(mass)

# Sort the masses and run the fits
N=0
for mass in sorted(plotters.keys()):
  print 'fitting',str(mass)

  # Check if plotter contains samples for all Run 2 years
  if len(plotters[mass])!=(1,3)[args[0]=='ntuples'] and len(plotters[mass])!=(1,2)[args[0]=='ntuples']:
    continue

  # Get the histo from MC
  plotter=MergedPlotter(plotters[mass])
  histo=plotter.drawTH1(options.mvv,options.cut,"10000",1000,0,8000)

  # Set up the fitter
  fitter=Fitter(['MVV'])
  fitter.signalResonance('model','MVV')
  fitter.w.var("MH").setVal(mass)
  fitter.importBinnedData(histo,['MVV'],'data')

  # Perform the fit
  fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
  fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])

  # Control plots
  fitter.projection("model","data","MVV","debugVV_"+options.output+"_"+str(mass)+".root")
  fitter.projection("model","data","MVV","debugVV_"+options.output+"_"+str(mass)+".png")

  for var,graph in graphs.iteritems():
    value,error=fitter.fetch(var)
    graph.SetPoint(N,mass,value)
    graph.SetPointError(N,0.0,error)

  N=N+1

# Store all graphs
F=ROOT.TFile(options.output,"RECREATE")
F.cd()
for name,graph in graphs.iteritems():
    graph.Write(name)
F.Close()
