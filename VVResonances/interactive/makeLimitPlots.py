#!/usr/bin/env python

import ROOT
import optparse
import pdb
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *

# Plot settings
minX=1000
maxX=4500
minY=0.00001
maxY=1000
blind=1
output='asymptotic_channels_XWZ'

# Categories
leptons=['e','mu']
purities=['HP','LP']
jets=['W','Z']
colors=[2,3,4,5,6,7,8,9]

setTDRStyle()

# Get limits and data
files={}
limits={}
data={}
band68={}
band95={}
bandObs={}
line_plus1={}
line_plus2={}
line_minus1={}
line_minus2={}
NColor=-1
for lep in leptons:
  for pur in purities:
    for jet in jets:
      channel='_'.join([lep,pur,jet])
      filename='/scratch2/David/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/outputs/VBF2016_2018_dijet500_sep_all/Asymptotic_XWZ_'+channel+'/VBF_asymptotic_XWZ_'+channel+'_nob.root'
      files[lep,pur,jet]=ROOT.TFile(filename,"OPEN")
      limits[lep,pur,jet]=files[lep,pur,jet].Get("limit")

      # Get data from events
      data[lep,pur,jet]={}
      for event in limits[lep,pur,jet]:
        if float(event.mh)<minX or float(event.mh)>maxX:
          continue

        if not (event.mh in data[lep,pur,jet].keys()):
          data[lep,pur,jet][event.mh]={}

        if event.quantileExpected<0:
          data[lep,pur,jet][event.mh]['obs']=event.limit
        if event.quantileExpected>0.02 and event.quantileExpected<0.03:
          data[lep,pur,jet][event.mh]['-2sigma']=event.limit
        if event.quantileExpected>0.15 and event.quantileExpected<0.17:
          data[lep,pur,jet][event.mh]['-1sigma']=event.limit
        if event.quantileExpected>0.49 and event.quantileExpected<0.51:
          data[lep,pur,jet][event.mh]['exp']=event.limit
        if event.quantileExpected>0.83 and event.quantileExpected<0.85:
          data[lep,pur,jet][event.mh]['+1sigma']=event.limit
        if event.quantileExpected>0.974 and event.quantileExpected<0.976:
          data[lep,pur,jet][event.mh]['+2sigma']=event.limit

      band68[lep,pur,jet]=ROOT.TGraphAsymmErrors()
      band68[lep,pur,jet].SetName("band68")
      band95[lep,pur,jet]=ROOT.TGraphAsymmErrors()
      band95[lep,pur,jet].SetName("band95")
      bandObs[lep,pur,jet]=ROOT.TGraphAsymmErrors()
      bandObs[lep,pur,jet].SetName("bandObs")

      line_plus1[lep,pur,jet]=ROOT.TGraph()
      line_plus1[lep,pur,jet].SetName("line_plus1")

      line_plus2[lep,pur,jet]=ROOT.TGraph()
      line_plus2[lep,pur,jet].SetName("line_plus2")

      line_minus1[lep,pur,jet]=ROOT.TGraph()
      line_minus1[lep,pur,jet].SetName("line_minus1")

      line_minus2[lep,pur,jet]=ROOT.TGraph()
      line_minus2[lep,pur,jet].SetName("line_minus2")

      N=0
      for mass,info in data[lep,pur,jet].iteritems():
        print 'Setting mass',mass,info

        if not ('exp' in info.keys() and '+1sigma' in info.keys() and '+2sigma' in info.keys() and '-1sigma' in info.keys() and '-2sigma' in info.keys() and 'obs' in info.keys()):
          print 'Incomplete file'
          continue

        band68[lep,pur,jet].SetPoint(N,mass,info['exp'])
        band95[lep,pur,jet].SetPoint(N,mass,info['exp'])
        line_plus1[lep,pur,jet].SetPoint(N,mass,info['+1sigma'])
        line_plus2[lep,pur,jet].SetPoint(N,mass,info['+2sigma'])
        line_minus1[lep,pur,jet].SetPoint(N,mass,info['-1sigma'])
        line_minus2[lep,pur,jet].SetPoint(N,mass,info['-2sigma'])

        bandObs[lep,pur,jet].SetPoint(N,mass,info['obs'])
        band68[lep,pur,jet].SetPointError(N,0.0,0.0,info['exp']-info['-1sigma'],info['+1sigma']-info['exp'])
        band95[lep,pur,jet].SetPointError(N,0.0,0.0,info['exp']-info['-2sigma'],info['+2sigma']-info['exp'])
        N=N+1

      band68[lep,pur,jet].Sort()
      band95[lep,pur,jet].Sort()
      bandObs[lep,pur,jet].Sort()
      line_plus1[lep,pur,jet].Sort()
      line_plus2[lep,pur,jet].Sort()
      line_minus1[lep,pur,jet].Sort()
      line_minus2[lep,pur,jet].Sort()

      NColor+=1

      band68[lep,pur,jet].SetFillColor(ROOT.kGreen)
      band68[lep,pur,jet].SetLineWidth(3)
      band68[lep,pur,jet].SetLineColor(colors[NColor])
      band68[lep,pur,jet].SetLineStyle(7)
      band68[lep,pur,jet].SetMarkerStyle(0)

      band95[lep,pur,jet].SetFillColor(ROOT.kYellow)

      bandObs[lep,pur,jet].SetLineWidth(3)
      bandObs[lep,pur,jet].SetLineColor(ROOT.kBlack)
      bandObs[lep,pur,jet].SetMarkerStyle(20)

      line_plus1[lep,pur,jet].SetLineWidth(1)
      line_plus1[lep,pur,jet].SetLineColor(ROOT.kGreen+1)

      line_plus2[lep,pur,jet].SetLineWidth(1)
      line_plus2[lep,pur,jet].SetLineColor(ROOT.kOrange-2)

      line_minus1[lep,pur,jet].SetLineWidth(1)
      line_minus1[lep,pur,jet].SetLineColor(ROOT.kGreen+1)

      line_minus2[lep,pur,jet].SetLineWidth(1)
      line_minus2[lep,pur,jet].SetLineColor(ROOT.kOrange-2)

#plotting information

c=ROOT.TCanvas("c","c")
frame=c.DrawFrame(minX,minY,maxX,maxY)
frame.GetXaxis().SetTitle('M_{X} [GeV]')
frame.GetXaxis().SetTitleOffset(0.9)
frame.GetXaxis().SetTitleSize(0.05)

frame.GetYaxis().SetTitle('#sigma x BR(X #rightarrow WW) [pb]')
frame.GetYaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleOffset(1.15)

leg=ROOT.TLegend(0.7,0.55,0.9,0.9)

c.cd()
frame.Draw()
for lep in leptons:
  for pur in purities:
    for jet in jets:
      #band95.Draw("3same")
      #band68.Draw("3same")
      band68[lep,pur,jet].Draw("XLsame")
      legLabel=' '.join([lep,pur,jet])
      leg.AddEntry(band68[lep,pur,jet],legLabel,"lp")
      #line_plus1.Draw("Lsame")
      #line_plus2.Draw("Lsame")
      #line_minus1.Draw("Lsame")
      #line_minus2.Draw("Lsame")
c.SetLogy(1)
c.Draw()

leg.Draw()
cmslabel_prelim(c,'2015',11)

c.Update()
c.RedrawAxis()

if blind==0:
    bandObs.Draw("PLsame")

c.SaveAs(output+".png")
c.SaveAs(output+".pdf")

'''
fout=ROOT.TFile(options.output+".root","RECREATE")
fout.cd()
c.Write()
band68.Write()
band95.Write()
bandObs.Write()
line_plus1.Write()
line_plus2.Write()
line_minus1.Write()
line_minus2.Write()
'''

#fout.Close()
for lep in leptons:
  for pur in purities:
    for jet in jets:
      files[lep,pur,jet].Close()
