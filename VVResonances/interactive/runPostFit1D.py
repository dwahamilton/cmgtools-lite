import os
import ROOT
import pdb
from ROOT import gStyle,gROOT,gPad
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *
from CMGTools.VVResonances.plotting.RooPlotter import *
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import optparse
parser = optparse.OptionParser()
#parser.add_option("-i","--input",dest="inputFile",default='combined.root',help="input root datacard")
parser.add_option("-r","--fixR",dest="fixR",type=float,help="fix r in the fit")
parser.add_option("-s","--signalType",dest="signalType",default='',help="XWW or XWZ")
parser.add_option("-u","--doUncBand",dest="doUncBand",type=int,default=0,help="do uncertainty band")
(options,args) = parser.parse_args()

def massPlot(mass,channel):
  plotter.w.var("MH").setVal(mass)
  massFrame=plotter.w.var("MLNuJ").frame()
  #plotter.w.pdf("shapeSig_XWW_nob_VBF_Radion_mu_HP_2016_NP_13TeV").plotOn(frame)
  plotter.w.pdf("shapeSig_XWW_nob_VBF_Radion_"+channel+"_NP_13TeV").plotOn(massFrame)
  #plotter.w.pdf("shapeSig_XWW_nob_VBF_Radion_"+channel+"_NP_13TeV").plotOn(massFrame)
  canv=ROOT.TCanvas(channel,channel)
  canv.cd()
  massFrame.Draw()
  canv.SaveAs("PlotsPostFit_/massPlot_"+channel+"_"+str(mass)+".pdf")

def yieldPlot(channel):
  yieldFrame=plotter.w.var("MH").frame(ROOT.RooFit.Bins(100),ROOT.RooFit.Range(1000,4500))
  plotter.w.function("shapeSig_XWW_nob_VBF_Radion_"+channel+"_NP_13TeV__norm").plotOn(yieldFrame)
  #plotter.w.function("shapeSig_XWW_nob_VBF_Radion_"+channel+"_NP_13TeV__norm").plotOn(yieldFrame)
  canv=ROOT.TCanvas(channel,channel)
  canv.cd()
  yieldFrame.Draw()
  canv.SaveAs("PlotsPostFit_/yieldPlot_"+channel+".pdf")

def makeSignalParam(channel,mxpoints,var,xaxistitle):
  color=["#8B4D00","#A15900","#B16200","#C36B01","#D97700","#ED8200","#FF8D00","#FF9410","#FF9B1F","#FFA22F","#FFAA40"]
  #F=ROOT.TFile(filename)
  #w=F.Get('w')
  #pdb.set_trace()
  #frame=w.var(var).frame()
  #plotter.w.var("MH").setVal(mass)
  frame=plotter.w.var("MLNuJ").frame()
  masses=mxpoints.split(",")
  for m in range(len(masses)):
    plotter.w.var("MH").setVal(int(masses[m]))
    plotter.w.pdf("shapeSig_XWW__VBF_XWW_"+channel+"__").plotOn(frame,ROOT.RooFit.LineColor(ROOT.TColor.GetColor(color[m])))
  frame.GetXaxis().SetTitle(xaxistitle)
  frame.GetYaxis().SetTitle("a.u.")
  frame.GetYaxis().SetTitleOffset(1.35)
  frame.SetTitle('')
  c1=ROOT.TCanvas("c")
  c1.cd()
  frame.Draw()
  c1.Update()
  c1.SaveAs("PlotsPostFit_/masses_"+channel+".pdf")

def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  canvas.SaveAs(name+".C")
  canvas.SaveAs(name+".pdf")
  #canvas.SaveAs(name+".png")
  canvas.SaveAs(name+".eps")
  os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
  #os.system("rm "+name+".eps") ## don't uncomment this for jobs

def cmsLabel(canvas):
  #cmslabel_not(canvas,'2016',11)
  #cmslabel_prelim(canvas,'2016',11)
  cmslabel_final(canvas,'2016',11)


#jets=['W','Z','H']
jets=['W','Z']
#jets=['control']
#jets=['combined']
#leptons=['e','mu','lep']
#leptons=['e','mu']
leptons=['lep']
#purities=['HP','LP']
purities=['allP']
bkgs=['nonRes','resW']
#bkgs=['nonRes']
#years=['2016','2017_5','2018_2']
#years=['2017_5','2018_2']
labels={'nonRes':'W+Jets','resW':'W+V/t'}
colors={'bkg':('#0041AA','#A5D2FF'),'nonRes':('#0041AA','#A5D2FF'),'resW':('#0F5500','#60B037')}
#years=['2016']

directory='PlotsPostFit_'+options.signalType
os.system("mkdir -p "+directory)

s = options.signalType

for jet in jets:
  for lep in leptons:
    for pur in purities:
      channel='_'.join([lep,pur,jet])
      filename='datacard_final__VBF_XWW_resWCombined_'+channel+'_b_.root'

      plotter=RooPlotter(filename)

      if options.fixR is not None:
        plotter.fix("r",options.fixR)


      if s=='XWW':
        plotter.addContribution("XWW",True,"X #rightarrow WW",3,1,ROOT.kOrange+10,0,ROOT.kWhite)
      elif s=='XWZ':
        plotter.addContribution("XWZ",True,"X #rightarrow WZ",3,1,ROOT.kMagenta,0,ROOT.kWhite)
      for bkg in bkgs:
        plotter.addContribution(bkg,False,labels[bkg],1,1,ROOT.TColor.GetColor(colors[bkg][0]),1001,ROOT.TColor.GetColor(colors[bkg][1])) #4CB319"))

      #makeSignalParam(channel,"1000,1500,2000,2500,3000,3500,4000,4500",'MH','M_{X}')

      plotter.prefit()
      plotter.drawBinned("MLNuJ","m_{WV} (GeV)","","_VBF_XWW_resWCombined_"+channel+"_b_",[0,0],options.doUncBand,1,"")
      saveCanvas(plotter.canvas,directory+"/postFitMVV_XWW_resWCombined_"+s+"_"+channel+"_b")
      #plotter.drawBinned("MLNuJ","m_{WV} (GeV)","","_VBF_XWW_resWCombined_"+channel+"_b_",[0,0],options.doUncBand) # Linear
      #saveCanvas(plotter.canvas,directory+"/postFitMVV_XWW_resWCombined_"+s+"_"+channel+"_lin_b")
      cmsLabel(plotter.canvas)
      pdb.set_trace()
