#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
import copy

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
parser.add_option("-f","--scaleFactors",dest="scaleFactors",help="Additional scale factors separated by comma",default='')
parser.add_option("-x","--xmin",dest="xmin",help="Minimum x value on histogram",default='0')
parser.add_option("-X","--xmax",dest="xmax",help="Maximum x value on histogram",default='5000')
parser.add_option("-b","--binsx",dest="binsx",help="Number of bins on x axis",default='100')
parser.add_option("-S","--scaleUnc",dest="scaleUnc",help="Scale uncertainty",default='0')
parser.add_option("-R","--resUnc",dest="resUnc",help="Resolution uncertainty",default='0')

(options,args) = parser.parse_args()
#define output dictionary

samples={}
graphs={'MEAN':ROOT.TGraphErrors(),'SIGMA':ROOT.TGraphErrors(),'ALPHA1':ROOT.TGraphErrors(),'N1':ROOT.TGraphErrors(),'ALPHA2':ROOT.TGraphErrors(),'N2':ROOT.TGraphErrors()}

for filename in os.listdir(args[0]):
    if not (filename.find(options.sample)!=-1):
        continue

#found sample. get the mass
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
        

    mass = float(fname.split('_')[-1])

        

    samples[mass] = fname

    print 'found',filename,'mass',str(mass) 



scaleFactors=options.scaleFactors.split(',')


hists=[]
histsScaleUp=[]
histsScaleDown=[]
histsResUp=[]
histsResDown=[]
bins=int(options.binsx)
xmin=float(options.xmin)
xmax=float(options.xmax)
scaleUnc=float(options.scaleUnc)
resUnc=float(options.resUnc)

#Now we have the samples: Sort the masses and run the fits
N=0
for mass in sorted(samples.keys()):

    print 'fitting',str(mass) 
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
    plotter.addCorrectionFactor('genWeight','tree')
    plotter.addCorrectionFactor('puWeight','tree')
    if options.scaleFactors!='':
        for s in scaleFactors:
            plotter.addCorrectionFactor(s,'tree')
       
    fitter=Fitter(['MVV'])
    fitter.signalResonance('model','MVV')
    fitter.w.var("MH").setVal(mass)
    histo = plotter.drawTH1(options.mvv,options.cut,"1",1000,0,8000)

    fitter.importBinnedData(histo,['MVV'],'data')
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])

    fitter.projection("model","data","MVV","debugVV_"+options.output+"_"+str(mass)+".root")
    fitter.projection("model","data","MVV","debugVV_"+options.output+"_"+str(mass)+".png")

    #for var,graph in graphs.iteritems():
        #value,error=fitter.fetch(var)
        #graph.SetPoint(N,mass,value)
        #graph.SetPointError(N,0.0,error)
    
    histoClone=copy.deepcopy(fitter.fetchHistogram("model","histo"+str(mass),"MVV",bins,xmin,xmax))
    histoClone.SetName(options.output.strip("combined_MVV.root")+"_"+str(int(mass)))
    hists.append(histoClone)

    # Get fit parameters
    mean=fitter.w.var("MEAN").getVal()
    meanUp=mean*(1+scaleUnc)
    meanDown=mean*(1-scaleUnc)
    sigma=fitter.w.var("SIGMA").getVal()
    sigmaUp=sigma*(1+resUnc)
    sigmaDown=sigma*(1-resUnc)
    
    # Make shape uncertainties
    fitterScaleUp=copy.deepcopy(fitter)
    fitterScaleUp.w.var("MEAN").setVal(meanUp)
    histoScaleUp=copy.deepcopy(fitterScaleUp.fetchHistogram("model","histo"+str(mass)+"_ScaleUp","MVV",bins,xmin,xmax))
    histoScaleUp.SetName(histoClone.GetName()+"_ScaleUp")
    histsScaleUp.append(histoScaleUp)

    fitterScaleDown=copy.deepcopy(fitter)
    fitterScaleDown.w.var("MEAN").setVal(meanDown)
    histoScaleDown=copy.deepcopy(fitterScaleDown.fetchHistogram("model","histo"+str(mass)+"_ScaleDown","MVV",bins,xmin,xmax))
    histoScaleDown.SetName(histoClone.GetName()+"_ScaleDown")
    histsScaleDown.append(histoScaleDown)
   
    fitterResUp=copy.deepcopy(fitter)
    fitterResUp.w.var("SIGMA").setVal(sigmaUp)
    histoResUp=copy.deepcopy(fitterResUp.fetchHistogram("model","histo"+str(mass)+"_ResUp","MVV",bins,xmin,xmax))
    histoResUp.SetName(histoClone.GetName()+"_ResUp")
    histsResUp.append(histoResUp)

    fitterResDown=copy.deepcopy(fitter)
    fitterResDown.w.var("SIGMA").setVal(sigmaDown)
    histoResDown=copy.deepcopy(fitterResDown.fetchHistogram("model","histo"+str(mass)+"_ResDown","MVV",bins,xmin,xmax))
    histoResDown.SetName(histoClone.GetName()+"_ResDown")
    histsResDown.append(histoResDown)

    N=N+1


F=ROOT.TFile(options.output,"RECREATE")
F.cd()
#for name,graph in graphs.iteritems():
    #graph.Write(name)
for hist in hists:
    hist.Write()
for hist in histsScaleUp:
    hist.Write()
for hist in histsScaleDown:
    hist.Write()
for hist in histsResUp:
    hist.Write()
for hist in histsResDown:
    hist.Write()

F.Close()
            
