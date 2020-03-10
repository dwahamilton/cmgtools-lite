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

parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-m","--minMVV",dest="min",type=float,help="mVV variable",default=1)
parser.add_option("-M","--maxMVV",dest="max",type=float, help="mVV variable",default=1)
parser.add_option("-f","--function",dest="function",help="interpolating function",default='')
parser.add_option("-b","--BR",dest="BR",type=float, help="branching ratio",default=1)
parser.add_option("-x","--minMass",dest="minMass",type=float, help="minimumMass",default=0.0)

(options,args)=parser.parse_args()

yieldgraph=ROOT.TGraphErrors()

#define output dictionary
plotters={}

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
  histo=plotter.drawTH1(options.mvv,options.cut,"1",1000,0,8000)

  # Get the yield and its uncertainty
  err=ROOT.Double(0)
  integral=histo.IntegralAndError(1,histo.GetNbinsX(),err)
  print integral, err

  # Add them to the graph
  yieldgraph.SetPoint(N,mass,integral*options.BR)
  yieldgraph.SetPointError(N,0.0,err*options.BR)

  N=N+1

# Run the fit and store the parameterization
func=ROOT.TF1("func",options.function,0,13000)
yieldgraph.Fit(func)

parameterization={'yield':returnString(func)}
f=open(options.output+".json","w")
json.dump(parameterization,f)
f.close()

f=ROOT.TFile(options.output+".root","RECREATE")
f.cd()
yieldgraph.Write("yield")
f.Close()

c=ROOT.TCanvas("c")
c.cd()
yieldgraph.Draw("AP")
c.SaveAs("debug_"+options.output+".png")

#F=ROOT.TFile(options.output+".root",'RECREATE')
#F.cd()
#yieldgraph.Write("yield")
#F.Close()
