import ROOT,math,copy
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *
import os
from array import array
from numpy import arange
import pdb
ROOT.gROOT.SetBatch(True)

def efficiency1D(plotter,var,bins,denom,num):
    h1 = plotter.drawTH1Binned(var,denom,"1",bins)
    h2 = plotter.drawTH1Binned(var,denom+"*"+num,"1",bins)

#    graph=ROOT.TGraphAsymmErrors()
#    graph.Divide(h2,h1)
    h2.Divide(h1)
    return h2

def efficiency2D(plotter,var,binsx,binsy,denom,num):
    h1 = plotter.drawTH2Binned(var,denom,"1",binsx,binsy)
    h2 = plotter.drawTH2Binned(var,denom+"*"+num,"1",binsx,binsy)
    h2.Divide(h1)
    return h2

def getPlotters(samples,folder,isData=False,corr="1"):
    sampleTypes=samples.split(',')
    plotters=[]
    for filename in os.listdir('samples/'+folder):
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1:
                    continue
                print 'Adding file',fname
                plotters.append(TreePlotter('samples/'+folder+'/'+fname+'.root','tree'))
                if not isData:
                    plotters[-1].setupFromFile('samples/'+folder+'/'+fname+'.pck')
                    plotters[-1].addCorrectionFactor('xsec','tree')
                    plotters[-1].addCorrectionFactor('genWeight','tree')
                    plotters[-1].addCorrectionFactor('puWeight','tree')
                    plotters[-1].addCorrectionFactor('lnujj_sf','tree')
                    plotters[-1].addCorrectionFactor('truth_genTop_weight','tree')
                    plotters[-1].addCorrectionFactor(corr,'flat')

    return plotters

def compare(p1,p2,var,cut1,cut2,bins,mini,maxi,title,unit,leg1,leg2):
    canvas = ROOT.TCanvas("canvas","")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    canvas.cd()
    legend = ROOT.TLegend(0.62,0.2,0.92,0.4,"","brNDC")
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)


    h1=p1.drawTH1(var,cut1,"1",bins,mini,maxi,title,unit)
    h2=p2.drawTH1(var,cut2,"1",bins,mini,maxi,title,unit)
    h1.DrawNormalized("HIST")
    h2.DrawNormalized("SAME")
    legend.AddEntry(h1,leg1,"LF")
    legend.AddEntry(h2,leg2,"P")
    legend.Draw()

    pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)
#    text = pt.AddText(0.01,0.3,"CMS Preliminary 2016")
#    text = pt.AddText(0.25,0.3,"#sqrt{s} = 13 TeV")
    pt.Draw()


    return canvas#,h1,h2,legend,pt

def hist1D(plot,name,title,var,cut,lumi,bins,minx,maxx,titlex,unitsx,style='HIST'):
  hist=plot.drawTH1(var,cut,lumi,bins,minx,maxx,titlex,unitsx,style)
  hist.SetName(name)
  hist.GetYaxis().SetTitle('Count')
  hist.SetStats(0)
  hist.SetTitle(title)

  #canv=ROOT.TCanvas(name,name,650,500)
  #canv.cd()
  hist.Draw(style)

  #titleText=ROOT.TPaveText(0.1,0.95,0.9,1,"NDC")
  #titleText.AddText(title)
  #titleText.SetBorderSize(0)
  #titleText.SetFillStyle(0)
  #titleText.SetTextFont(42)
  #titleText.Draw()

  #hist.Write()
  return hist

  #canv.Write()
  #imgname='/scratch2/David/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/Fig/1DJetResonance/'+name+'.pdf'
  #canv.Print(imgname)

def hist2DBinned(plot,name,title,var,cut,lumi,binsx,binsy,titlex,unitsx,titley,unitsy,style="COLZ"):
  hist=plot.drawTH2Binned(var,cut,lumi,binsx,binsy,titlex,unitsx,titley,unitsy,style)
  hist.SetName(name)
  #hist.SetTitle(title)
  #hist.SetTitleOffset(5)
  hist.SetStats(0)
  ROOT.gStyle.SetPadLeftMargin(0.125)
  ROOT.gStyle.SetPadRightMargin(0.175)

  canv=ROOT.TCanvas(name,name,650,500)
  canv.cd()
  hist.Draw(style)
  ROOT.gStyle.SetPalette(1)
  canv.Update()
  palette=hist.GetListOfFunctions().FindObject("palette")
  palette.SetX1NDC(0.84)
  palette.SetX2NDC(0.865)

  titleText=ROOT.TPaveText(0.1,0.95,0.9,1,"NDC")
  titleText.AddText(title)
  titleText.SetBorderSize(0)
  titleText.SetFillStyle(0)
  titleText.SetTextFont(42)
  titleText.Draw()

  canv.Write()
  imgname='/scratch2/David/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/Fig/2DEvent/'+name+'.pdf'
  canv.Print(imgname)

cuts={}

cuts['common'] = '(((HLT_MU)&&(abs(lnujj_l1_l_pdgId)==13))||((HLT_ELE)&&abs(lnujj_l1_l_pdgId)==11)||HLT_MET120)*(Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>600&&Flag_badChargedHadronFilter&&Flag_badMuonFilter&&Flag_globalTightHalo2016Filter)'

cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['lep']='(abs(lnujj_l1_l_pdgId)==13||abs(lnujj_l1_l_pdgId)==11)'

Vtagger='(lnujj_l2_tau2/lnujj_l2_tau1-(-0.08)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt))'
thrHP='0.65'
thrLP='0.96'
cuts['HP']='('+Vtagger+'<'+thrHP+')'
cuts['LP']='('+thrHP+'<='+Vtagger+'&&'+Vtagger+'<'+thrLP+')'
cuts['allP']='('+cuts['HP']+'||'+cuts['LP']+')'
#cuts['HP'] = '(lnujj_l2_tau2/lnujj_l2_tau1<0.55)'
#cuts['LP'] = '(lnujj_l2_tau2/lnujj_l2_tau1>0.55&&lnujj_l2_tau2/lnujj_l2_tau1<0.75)'
#cuts['tau'] = '(lnujj_l2_tau2/lnujj_l2_tau1<0.75)'

cuts['nob'] = '(lnujj_nMediumBTags==0)*lnujj_btagWeight'
cuts['b'] = '(lnujj_nMediumBTags>0)*lnujj_btagWeight'

cuts['resW']='(lnujj_l2_mergedVTruth==1)'
cuts['nonres']='(lnujj_l2_mergedVTruth==0)'

cuts['SDSideBand']='((lnujj_l2_softDrop_mass>30&&lnujj_l2_softDrop_mass<65)||(lnujj_l2_softDrop_mass>135&&lnujj_l2_softDrop_mass<250))'
cuts['SDWindow']='(lnujj_l2_softDrop_mass>65&&lnujj_l2_softDrop_mass<135)'
cuts['SDMass']='(lnujj_l2_softDrop_mass>30)'
#cuts['resMass']='(lnujj_LV_mass>1500&&lnujj_LV_mass<2500)'
cuts['resMass']='(lnujj_LV_mass>600)'
cuts['pTm']='(lnujj_l1_pt/lnujj_LV_mass>0.4)'

cuts['dijet1']='(lnujj_vbf_j1_pt>0)'
cuts['dijet2']='(lnujj_vbf_j2_pt>0)'
cuts['dijet']='(lnujj_vbf_j1_pt>0&&lnujj_vbf_j2_pt>0)'
cuts['dijetEta']='(lnujj_vbf_j1_eta*lnujj_vbf_j2_eta<0)'

cuts['eta']='(abs(lnujj_vbf_j1_eta)>2&&abs(lnujj_vbf_j2_eta)>2)'
cuts['deta']='(lnujj_vbfDEta>4)'
cuts['mjj']='(lnujj_vbfMass>500)'

cuts['control']='(lnujj_l2_softDrop_mass>=30&&lnujj_l2_softDrop_mass<=55)'
cuts['W']='(lnujj_l2_softDrop_mass>55&&lnujj_l2_softDrop_mass<85)'
cuts['Z']='(lnujj_l2_softDrop_mass>=85&&lnujj_l2_softDrop_mass<=105)'
cuts['H']='(lnujj_l2_softDrop_mass>105&&lnujj_l2_softDrop_mass<140)'
cuts['combined']='(lnujj_l2_softDrop_mass>55&&lnujj_l2_softDrop_mass<=105)'

jets=['control','W','Z','H','combined']
leptons=['lep','e','mu']
purities=['HP','LP','allP']
#purities=['HP','LP']
#categories=['nob']

#change the CMS_lumi variables (see CMS_lumi.py)
lumi_13TeV="35.9 fb^{-1}"
lumi_sqrtS="13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod=4
iPos=11

masses={
'2016':['600','800','1000','1200','1400','1600','1800','2000','2500','3000','3500','4000','4500'],
'2017':['1200','1400','1600','1800','2000','2500','3000','3500','4000','4500'],
'2018':['1200','1400','1600','1800','2000','2500','3000','3500','4000','4500','5000','5500','6000','6500','7000','7500','8000']
}
masses['all']=set(list(set(masses['2016'])&set(masses['2017']))+list(set(masses['2017'])&set(masses['2018']))+list(set(masses['2016'])&set(masses['2018'])))

# data
dataPlotters2016=getPlotters('SingleMuon,SingleElectron,MET','ntuples2016',True)
data2016=MergedPlotter(dataPlotters2016)
dataPlotters2017=getPlotters('SingleMuon,SingleElectron,MET','ntuples2017',True)
data2017=MergedPlotter(dataPlotters2017)
dataPlotters2018=getPlotters('SingleMuon,EGamma,MET','ntuples2018',True)
data2018=MergedPlotter(dataPlotters2018)

dataPlotters=[]
dataPlotters.extend(dataPlotters2016)
dataPlotters.extend(dataPlotters2017)
dataPlotters.extend(dataPlotters2018)
data=MergedPlotter(dataPlotters)

# 2016 background
VJets2016Plotters=getPlotters('DYJetsToLL_M50_HT,WJetsToLNu_HT','ntuples2016',False)
VJets2016=MergedPlotter(VJets2016Plotters)
#WVT2016Plotters=getPlotters('TT_pow,T_tWch,TBar_tWch,WWToLNuQQ,WZTo1L1Nu2Q,ZZTo2L2Q','ntuples2016',False)
WVT2016Plotters=getPlotters('TT_pow,T_tWch,TBar_tWch,WWToLNuQQ','ntuples2016',False)
WVT2016=MergedPlotter(WVT2016Plotters)
BKG2016Plotters=getPlotters('TT_pow,T_tWch,TBar_tWch,WWToLNuQQ,DYJetsToLL_M50_HT,WJetsToLNu_HT','ntuples2016',False)
BKG2016=MergedPlotter(BKG2016Plotters)

'''
# 2016 signal
VBFRadionWW2016Plotters=getPlotters('VBF_RadionToWW_narrow','ntuples2016',False,0.001)
VBFRadionWW2016=MergedPlotter(VBFRadionWW2016Plotters)
'''
VBFRadionWW2016Plotters={}
VBFRadionWW2016={}
for mass in masses['2016']:
  VBFRadionWW2016Plotters[mass]=getPlotters('VBF_RadionToWW_narrow_'+mass,'ntuples2016',False,0.001)
  VBFRadionWW2016[mass]=MergedPlotter(VBFRadionWW2016Plotters[mass])

# 2017 background
VJets2017Plotters=getPlotters('DYJetsToLL_M50_HT,WJetsToLNu_HT','ntuples2017',False)
VJets2017=MergedPlotter(VJets2017Plotters)
#WVT2017Plotters=getPlotters('T_tch,T_tW,TBar_tch,TBar_tW,TTHad_pow,TTLep_pow,TTSemi_pow,WWToLNuQQ,WZTo1L1Nu2Q','ntuples2017',False)
WVT2017Plotters=getPlotters('T_tch,T_tW,TBar_tch,TBar_tW,TTHad_pow,TTLep_pow,TTSemi_pow,WWToLNuQQ','ntuples2017',False)
WVT2017=MergedPlotter(WVT2017Plotters)
BKG2017Plotters=getPlotters('T_tch,T_tW,TBar_tch,TBar_tW,TTHad_pow,TTLep_pow,TTSemi_pow,WWToLNuQQ,DYJetsToLL_M50_HT,WJetsToLNu_HT','ntuples2017',False)
BKG2017=MergedPlotter(BKG2017Plotters)

'''
# 2017 signal
VBFRadionWW2017Plotters=getPlotters('VBF_RadionToWW_narrow','ntuples2017',False,0.001)
VBFRadionWW2017=MergedPlotter(VBFRadionWW2017Plotters)
VBFWprimeWZ2017Plotters=getPlotters('VBF_WprimeToWZ_narrow','ntuples2017',False,0.001)
VBFWprimeWZ2017=MergedPlotter(VBFWprimeWZ2017Plotters)
#VBFZprimeWW2017Plotters=getPlotters('VBF_ZprimeToWW_narrow','ntuples2017',False,0.001)
#VBFZprimeWW2017=MergedPlotter(VBFZprimeWW2017Plotters)
VBFBulkGravWW2017Plotters=getPlotters('VBF_BulkGravToWW_narrow','ntuples2017',False,0.001)
VBFBulkGravWW2017=MergedPlotter(VBFBulkGravWW2017Plotters)
'''
VBFRadionWW2017Plotters={}
VBFRadionWW2017={}
for mass in masses['2017']:
  VBFRadionWW2017Plotters[mass]=getPlotters('VBF_RadionToWW_narrow_'+mass,'ntuples2017',False,0.001)
  VBFRadionWW2017[mass]=MergedPlotter(VBFRadionWW2017Plotters[mass])

# 2018 background
VJets2018Plotters=getPlotters('DYJetsToLL_M50_HT,WJetsToLNu_HT','ntuples2018',False)
VJets2018=MergedPlotter(VJets2018Plotters)
WVT2018Plotters=getPlotters('T_tch,T_tWch,TBar_tch,TBar_tWch,TTLep_pow,TTSemi_pow,WWToLNuQQ','ntuples2018',False)
WVT2018=MergedPlotter(WVT2018Plotters)
BKG2018Plotters=getPlotters('T_tch,T_tWch,TBar_tch,TBar_tWch,TTLep_pow,TTSemi_pow,WWToLNuQQ,DYJetsToLL_M50_HT,WJetsToLNu_HT','ntuples2018',False)
BKG2018=MergedPlotter(BKG2018Plotters)

'''
# 2018 signal
VBFRadionWW2018Plotters=getPlotters('VBF_RadionToWW_narrow','ntuples2018',False,0.001)
VBFRadionWW2018=MergedPlotter(VBFRadionWW2018Plotters)
VBFWprimeWZ2018Plotters=getPlotters('VBF_WprimeToWZ_narrow','ntuples2018',False,0.001)
VBFWprimeWZ2018=MergedPlotter(VBFWprimeWZ2018Plotters)
VBFZprimeWW2018Plotters=getPlotters('VBF_ZprimeToWW_narrow','ntuples2018',False,0.001)
VBFZprimeWW2018=MergedPlotter(VBFZprimeWW2018Plotters)
VBFBulkGravWW2018Plotters=getPlotters('VBF_BulkGravToWW_narrow','ntuples2018',False,0.001)
VBFBulkGravWW2018=MergedPlotter(VBFBulkGravWW2018Plotters)
'''
VBFRadionWW2018Plotters={}
VBFRadionWW2018={}
for mass in masses['2018']:
  VBFRadionWW2018Plotters[mass]=getPlotters('VBF_RadionToWW_narrow_'+mass,'ntuples2018',False,0.001)
  VBFRadionWW2018[mass]=MergedPlotter(VBFRadionWW2018Plotters[mass])

# Background plotters
VJetsPlotters=[]
VJetsPlotters.extend(VJets2016Plotters)
VJetsPlotters.extend(VJets2017Plotters)
VJetsPlotters.extend(VJets2018Plotters)
VJets=MergedPlotter(VJetsPlotters)
WVTPlotters=[]
WVTPlotters.extend(WVT2016Plotters)
WVTPlotters.extend(WVT2017Plotters)
WVTPlotters.extend(WVT2018Plotters)
WVT=MergedPlotter(WVTPlotters)
BKGPlotters=[]
BKGPlotters.extend(BKG2016Plotters)
BKGPlotters.extend(BKG2017Plotters)
BKGPlotters.extend(BKG2018Plotters)
BKG=MergedPlotter(BKGPlotters)

# Signal plotters
VBFRadionWWPlotters={}
VBFRadionWW={}
for mass in masses['all']:
  VBFRadionWWPlotters[mass]=[]
  VBFRadionWWPlotters[mass].extend(VBFRadionWW2016Plotters[mass])
  VBFRadionWWPlotters[mass].extend(VBFRadionWW2017Plotters[mass])
  VBFRadionWWPlotters[mass].extend(VBFRadionWW2018Plotters[mass])
  VBFRadionWW[mass]=MergedPlotter(VBFRadionWWPlotters[mass])

# Fill properties
VJets2016.setFillProperties(1001,ROOT.kAzure-9)
WVT2016.setFillProperties(1001,ROOT.kSpring-5)
BKG2016.setFillProperties(1001,ROOT.kAzure-9)
VJets2017.setFillProperties(1001,ROOT.kAzure-9)
WVT2017.setFillProperties(1001,ROOT.kSpring-5)
BKG2017.setFillProperties(1001,ROOT.kAzure-9)
VJets2018.setFillProperties(1001,ROOT.kAzure-9)
WVT2018.setFillProperties(1001,ROOT.kSpring-5)
BKG2018.setFillProperties(1001,ROOT.kAzure-9)

VJets.setFillProperties(1001,ROOT.kAzure-9)
WVT.setFillProperties(1001,ROOT.kSpring-5)
BKG.setFillProperties(1001,ROOT.kAzure-9)

# Stacks for background and data
BKGDataStack2016={}
BKGDataStack2017={}
BKGDataStack2018={}
BKGDataStack={}
for jet in jets:
  BKGDataStack2016[jet]=StackPlotter()
  BKGDataStack2016[jet].addPlotter(VJets2016,'WJets','W+Jets','background')
  BKGDataStack2016[jet].addPlotter(WVT2016,'WVT','W+V/t','background')

  BKGDataStack2017[jet]=StackPlotter()
  BKGDataStack2017[jet].addPlotter(VJets2017,'WJets','W+Jets','background')
  BKGDataStack2017[jet].addPlotter(WVT2017,'WVT','W+V/t','background')

  BKGDataStack2018[jet]=StackPlotter()
  BKGDataStack2018[jet].addPlotter(VJets2018,'WJets','W+Jets','background')
  BKGDataStack2018[jet].addPlotter(WVT2018,'WVT','W+V/t','background')

  BKGDataStack[jet]=StackPlotter()
  BKGDataStack[jet].addPlotter(VJets,'WJets','W+Jets','background')
  BKGDataStack[jet].addPlotter(WVT,'WVT','W+V/t','background')

  #if jet=='control':
  BKGDataStack2016[jet].addPlotter(data2016,'data','data','data')
  BKGDataStack2017[jet].addPlotter(data2017,'data','data','data')
  BKGDataStack2018[jet].addPlotter(data2018,'data','data','data')
  BKGDataStack[jet].addPlotter(data,'data','data','data')

# Make background and signal dictionaries
VJetsDict={('nonRes','W+Jets','2016'):VJets2016,('nonRes','W+Jets','2017'):VJets2017,('nonRes','W+Jets','2018'):VJets2018,('nonRes','W+Jets','all'):VJets}
WVTDict={('resW','W+V/t','2016'):WVT2016,('resW','W+V/t','2017'):WVT2017,('resW','W+V/t','2018'):WVT2018,('resW','W+V/t','all'):WVT}
BKGDict={('bkg','Background','2016'):BKG2016,('bkg','Background','2017'):BKG2017,('bkg','Background','2018'):BKG2018,('bkg','Background','all'):BKG}
BKGStackDict={('bkgDataStack','Background','2016'):BKGDataStack2016,('bkgDataStack','Background','2017'):BKGDataStack2017,('bkgDataStack','Background','2018'):BKGDataStack2018,('bkgDataStack','Background','all'):BKGDataStack}
#VBFDict={('radion','VBF Radion','2016'):VBFRadionWW2016,('radion','VBF Radion','2017'):VBFRadionWW2017,('Wprime','VBF W#prime','2017'):VBFWprimeWZ2017,('bulkGrav','VBF G_{bulk}','2017'):VBFBulkGravWW2017,('radion','VBF Radion','2018'):VBFRadionWW2018,('Wprime','VBF W#prime','2018'):VBFWprimeWZ2018,('Zprime','VBF Z#prime','2018'):VBFZprimeWW2018,('bulkGrav','VBF G_{bulk}','2018'):VBFBulkGravWW2018}
VBFDict={('radion','VBF Radion','2016'):VBFRadionWW2016,('radion','VBF Radion','2017'):VBFRadionWW2017,('radion','VBF Radion','2018'):VBFRadionWW2018,('radion','VBF Radion','all'):VBFRadionWW}

#bins={'pt':[100,0,1000],'mass':[100,0,300],'jetMass':[18,30,210],'sigMass':[30,600,4350],'eta':[100,-5,5],'deta':[100,0,10],'phi':[100,-3.2,3.2],'tau':[100,0,1],'eta12':[100,-25,25]}
#bins={'pt':[100,0,1000],'mass':[100,0,300],'jetMass':[18,30,210],'sigMass':[168,800,7000],'eta':[100,-5,5],'deta':[100,0,10],'phi':[100,-3.2,3.2],'tau':[100,0,1],'eta12':[100,-25,25]}
bins={'pt':[100,0,1000],'mass':[100,0,300],'jetMass':[18,30,210],'sigMass':[50,800,7000],'eta':[100,-5,5],'deta':[100,0,10],'phi':[100,-3.2,3.2],'tau':[100,0,1],'eta12':[100,-25,25]}
#lumi={'2016':'35920','2017':'41530','2018':'59740'}
#lumi['all']=str(int(lumi['2016'])+int(lumi['2017'])+int(lumi['2018']))
lumi2016='35920'
lumi2017='41530'
lumi2018='59740'
lumi='((year==2016)*'+lumi2016+'+(year==2017)*'+lumi2017+'+(year==2018)*'+lumi2018+')'

# Make cut dictionaries
#cut='*'.join([cuts['common'],cuts['lep'],cuts['tau'],cuts['nob'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])
#lepCuts={}
#for lep in ['e','mu']:
  #for pur in ['LP','HP']:
    #lepCuts[lep,pur]='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts['nob'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])

f=ROOT.TFile("Fig/1DHistCoarse_b.root","RECREATE")
f.cd()

#for sample in ['nonRes','resW','bkg','bkgStack','radion','Wprime','Zprime','bulkGrav']:
for year in ['2016','2017','2018','all']:
  for sample in ['bkgDataStack','bkg','resW','nonRes','radion']:
    for lep in leptons:
      for pur in purities:
        for jet in jets:
          f.mkdir('/'.join([year,sample,lep+pur+jet]))
          if sample=='radion':
            for mass in masses[year]:
              f.mkdir('/'.join([year,sample,lep+pur+jet,mass]))

for key,sample in BKGStackDict.items():
  folder=key[0]
  name=key[1]
  year=key[2]
  for lep in leptons:
    for pur in purities:
      for jet in jets:
        f.cd('/'.join([year,folder,lep+pur+jet]))
        lepCut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['b'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])
        stack=sample[jet].drawStack('lnujj_LV_mass',lepCut,lumi,bins['sigMass'][0],bins['sigMass'][1],bins['sigMass'][2],'m_{WV}','GeV')
        stack['canvas'].SetName(name+'_stack')
        stack['canvas'].Write()

for key,sample in VJetsDict.items():
  folder=key[0]
  name=key[1]
  year=key[2]
  for lep in leptons:
    for pur in purities:
      for jet in jets:
        f.cd('/'.join([year,folder,lep+pur+jet]))
        lepCut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['b'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])
        hist=hist1D(sample,folder,name,'lnujj_LV_mass',lepCut,lumi,bins['sigMass'][0],bins['sigMass'][1],bins['sigMass'][2],'m_{WV}','GeV')
        hist.Write()

for key,sample in WVTDict.items():
  folder=key[0]
  name=key[1]
  year=key[2]
  for lep in leptons:
    for pur in purities:
      for jet in jets:
        f.cd('/'.join([year,folder,lep+pur+jet]))
        lepCut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['b'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])
        hist=hist1D(sample,folder,name,'lnujj_LV_mass',lepCut,lumi,bins['sigMass'][0],bins['sigMass'][1],bins['sigMass'][2],'m_{WV}','GeV')
        hist.Write()

for key,sample in BKGDict.items():
  folder=key[0]
  name=key[1]
  year=key[2]
  for lep in leptons:
    for pur in purities:
      for jet in jets:
        f.cd('/'.join([year,folder,lep+pur+jet]))
        lepCut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['b'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])
        hist=hist1D(sample,folder,name,'lnujj_LV_mass',lepCut,lumi,bins['sigMass'][0],bins['sigMass'][1],bins['sigMass'][2],'m_{WV}','GeV')
        hist.Write()

for key,sample in VBFDict.items():
  folder=key[0]
  name=key[1]
  year=key[2]
  for lep in leptons:
    for pur in purities:
      for jet in jets:
        for mass in sample:
          f.cd('/'.join([year,folder,lep+pur+jet,mass]))
          lepCut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['b'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])
          hist=hist1D(sample[mass],folder,name,'lnujj_LV_mass',lepCut,lumi,bins['sigMass'][0],bins['sigMass'][1],bins['sigMass'][2],'m_{WV}','GeV')
          hist.Write()

f.Close()
