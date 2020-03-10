#!/usr/bin/env python

import ROOT
import optparse
import pdb
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *
parser = optparse.OptionParser()
#parser.add_option("-c","--compare",dest="compare",default='',help="Comparison File")

parser.add_option("-o","--output",dest="output",default='limitPlotRatio.root',help="Limit plot")

parser.add_option("-x","--minX",dest="minX",type=float,help="minimum x",default=1000.0)
parser.add_option("-X","--maxX",dest="maxX",type=float,help="maximum x",default=5000.0)
parser.add_option("-y","--minY",dest="minY",type=float,help="minimum y",default=0)
parser.add_option("-Y","--maxY",dest="maxY",type=float,help="maximum y",default=2)
parser.add_option("-b","--blind",dest="blind",type=int,help="Not do observed ",default=1)
parser.add_option("-l","--log",dest="log",type=int,help="Log plot",default=0)

parser.add_option("-t","--titleX",dest="titleX",default='M_{X} [GeV]',help="title of x axis")
parser.add_option("-T","--titleY",dest="titleY",default='#sigma_{1}BR_{1}/#sigma_{2}BR_{2} (X #rightarrow WW)',help="title of y axis")

parser.add_option("-p","--period",dest="period",default='2015',help="period")
parser.add_option("-f","--final",dest="final",type=int, default=1,help="Preliminary or not")



#    parser.add_option("-x","--minMVV",dest="minMVV",type=float,help="minimum MVV",default=1000.0)
#    parser.add_option("-X","--maxMVV",dest="maxMVV",type=float,help="maximum MVV",default=13000.0)






(options,args) = parser.parse_args()
#define output dictionary

setTDRStyle()

f1=ROOT.TFile(args[0])
f2=ROOT.TFile(args[1])
limit1=f1.Get("limit")
limit2=f2.Get("limit")
data1={}
data2={}
data={}


for event in limit1:
    if float(event.mh)<options.minX or float(event.mh)>options.maxX:
        continue

    if not (event.mh in data1.keys()):
        data1[event.mh]={}


    if event.quantileExpected<0:
        data1[event.mh]['obs']=event.limit
    if event.quantileExpected>0.02 and event.quantileExpected<0.03:
        data1[event.mh]['-2sigma']=event.limit
    if event.quantileExpected>0.15 and event.quantileExpected<0.17:
        data1[event.mh]['-1sigma']=event.limit
    if event.quantileExpected>0.49 and event.quantileExpected<0.51:
        data1[event.mh]['exp']=event.limit
    if event.quantileExpected>0.83 and event.quantileExpected<0.85:
        data1[event.mh]['+1sigma']=event.limit
    if event.quantileExpected>0.974 and event.quantileExpected<0.976:
        data1[event.mh]['+2sigma']=event.limit

for event in limit2:
    if float(event.mh)<options.minX or float(event.mh)>options.maxX:
        continue

    if not (event.mh in data2.keys()):
        data2[event.mh]={}


    if event.quantileExpected<0:
        data2[event.mh]['obs']=event.limit
    if event.quantileExpected>0.02 and event.quantileExpected<0.03:
        data2[event.mh]['-2sigma']=event.limit
    if event.quantileExpected>0.15 and event.quantileExpected<0.17:
        data2[event.mh]['-1sigma']=event.limit
    if event.quantileExpected>0.49 and event.quantileExpected<0.51:
        data2[event.mh]['exp']=event.limit
    if event.quantileExpected>0.83 and event.quantileExpected<0.85:
        data2[event.mh]['+1sigma']=event.limit
    if event.quantileExpected>0.974 and event.quantileExpected<0.976:
        data2[event.mh]['+2sigma']=event.limit

for mass,info in data1.iteritems():
    if not ('exp' in info.keys() and '+1sigma' in info.keys() and '+2sigma' in info.keys() and '-1sigma' in info.keys() and '-2sigma' in info.keys() and 'obs' in info.keys()):
        print 'Incomplete file'
        continue

    if not (mass in data.keys()):
        data[mass]={}

    data[mass]['obs']=data1[mass]['obs']/data2[mass]['obs']
    data[mass]['-2sigma']=data1[mass]['-2sigma']/data2[mass]['-2sigma']
    data[mass]['-1sigma']=data1[mass]['-1sigma']/data2[mass]['-1sigma']
    data[mass]['exp']=data1[mass]['exp']/data2[mass]['exp']
    data[mass]['+1sigma']=data1[mass]['+1sigma']/data2[mass]['+1sigma']
    data[mass]['+2sigma']=data1[mass]['+2sigma']/data2[mass]['+2sigma']

band68=ROOT.TGraphAsymmErrors()
band68.SetName("band68")
band95=ROOT.TGraphAsymmErrors()
band95.SetName("band95")
bandObs=ROOT.TGraph()
bandObs.SetName("bandObs")

line_plus1=ROOT.TGraph()
line_plus1.SetName("line_plus1")

line_plus2=ROOT.TGraph()
line_plus2.SetName("line_plus2")

line_minus1=ROOT.TGraph()
line_minus1.SetName("line_minus1")

line_minus2=ROOT.TGraph()
line_minus2.SetName("line_minus2")



N=0
for mass,info in data.iteritems():
    print 'Setting mass',mass,info

    if not ('exp' in info.keys() and '+1sigma' in info.keys() and '+2sigma' in info.keys() and '-1sigma' in info.keys() and '-2sigma' in info.keys() and 'obs' in info.keys()):
        print 'Incomplete file'
        continue


    band68.SetPoint(N,mass,info['exp'])
    band95.SetPoint(N,mass,info['exp'])
    line_plus1.SetPoint(N,mass,info['+1sigma'])
    line_plus2.SetPoint(N,mass,info['+2sigma'])
    line_minus1.SetPoint(N,mass,info['-1sigma'])
    line_minus2.SetPoint(N,mass,info['-2sigma'])

    bandObs.SetPoint(N,mass,info['obs'])
    band68.SetPointError(N,0.0,0.0,info['exp']-info['-1sigma'],info['+1sigma']-info['exp'])
    band95.SetPointError(N,0.0,0.0,info['exp']-info['-2sigma'],info['+2sigma']-info['exp'])
    N=N+1


band68.Sort()
band95.Sort()
bandObs.Sort()
line_plus1.Sort()
line_plus2.Sort()
line_minus1.Sort()
line_minus2.Sort()



#plotting information

c=ROOT.TCanvas("c","c")
frame=c.DrawFrame(options.minX,options.minY,options.maxX,options.maxY)
frame.GetXaxis().SetTitle(options.titleX)
frame.GetXaxis().SetTitleOffset(0.9)
frame.GetXaxis().SetTitleSize(0.05)

frame.GetYaxis().SetTitle(options.titleY)
frame.GetYaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleOffset(1.15)

band68.SetFillColor(ROOT.kGreen)
band68.SetLineWidth(3)
band68.SetLineColor(ROOT.kBlue)
band68.SetLineStyle(7)
band68.SetMarkerStyle(0)

band95.SetFillColor(ROOT.kYellow)

bandObs.SetLineWidth(3)
bandObs.SetLineColor(ROOT.kBlack)
bandObs.SetMarkerStyle(20)

line_plus1.SetLineWidth(1)
line_plus1.SetLineColor(ROOT.kGreen+1)

line_plus2.SetLineWidth(1)
line_plus2.SetLineColor(ROOT.kOrange-2)

line_minus1.SetLineWidth(1)
line_minus1.SetLineColor(ROOT.kGreen+1)

line_minus2.SetLineWidth(1)
line_minus2.SetLineColor(ROOT.kOrange-2)


c.cd()
frame.Draw()
#band95.Draw("3same")
#band68.Draw("3same")
band68.Draw("XLsame")
#line_plus1.Draw("Lsame")
#line_plus2.Draw("Lsame")
#line_minus1.Draw("Lsame")
#line_minus2.Draw("Lsame")
c.SetLogy(options.log)
c.Draw()


if options.final:
    cmslabel_final(c,options.period,11)
else:
    cmslabel_prelim(c,options.period,11)

c.Update()
c.RedrawAxis()

if options.blind==0:
    bandObs.Draw("PLsame")




c.SaveAs(options.output+".png")
c.SaveAs(options.output+".pdf")

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

fout.Close()
f1.Close()
f2.Close()
