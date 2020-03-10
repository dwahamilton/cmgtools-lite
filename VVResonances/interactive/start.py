import ROOT,math
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *
import os
from array import array

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


def makeEff():
    f=ROOT.TFile("trigger.root","RECREATE")
    f.cd()
    g=efficiency1D(VJets,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['e'],'HLT_ELE']),'HLT_MET120')
    g.Write("MET_ELE_MC")
    g=efficiency1D(data,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['e'],'HLT_ELE']),'HLT_MET120')
    g.Write("MET_ELE_DATA")
    g=efficiency1D(VJets,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['mu'],'HLT_MU']),'HLT_MET120')
    g.Write("MET_MU_MC")
    g=efficiency1D(data,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['mu'],'HLT_MU']),'HLT_MET120')
    g.Write("MET_MU_DATA")


    g=efficiency2D(VJets,"lnujj_l1_l_eta:lnujj_l1_l_pt",[30,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['e'],'HLT_MET120']),'HLT_ELE')
    g.Write("ELE_MC")
    g=efficiency2D(data,"lnujj_l1_l_eta:lnujj_l1_l_pt",[30,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['e'],'HLT_MET120']),'HLT_ELE')
    g.Write("ELE_DATA")

    g=efficiency2D(VJets,"lnujj_l1_l_eta:lnujj_l1_l_pt",[30,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['mu'],'HLT_MET120']),'HLT_MU')
    g.Write("MU_MC")
    g=efficiency2D(data,"lnujj_l1_l_eta:lnujj_l1_l_pt",[50,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['mu'],'HLT_MET120']),'HLT_MU')
    g.Write("MU_DATA")
    
    f.Close()





def getPlotters(samples,isData=False,corr="1"):
    sampleTypes=samples.split(',')
    plotters=[]
    for filename in os.listdir('samples'):
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1:
                    continue
                print 'Adding file',fname
                plotters.append(TreePlotter('samples/'+fname+'.root','tree'))
                if not isData:
                    plotters[-1].setupFromFile('samples/'+fname+'.pck')
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

#def sigOverBkg(name,sig,bkg,xmin,xmax): 
    #binNum=sig.GetNbinsX()
    #sigBkg=ROOT.TH2D(name+'_sigOverBkg','',binNum,xmin,xmax,binNum,0,10)
    #for i in xrange(0,binNum):
	#xval=sig.GetBinCenter(i)
	#sigVal=sig.GetBinContent(i)
	#bkgVal=bkg.GetBinContent(i)
	#sigBkgVal=sigVal/math.sqrt(bkgVal+1)
	#sigBkg.Fill(xval,sigBkgVal)

    #return sigBkg

cuts={}

cuts['common'] = '(((HLT_MU)&&(abs(lnujj_l1_l_pdgId)==13))||((HLT_ELE)&&abs(lnujj_l1_l_pdgId)==11)||HLT_MET120)*(Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>600&&Flag_badChargedHadronFilter&&Flag_badMuonFilter&&Flag_globalTightHalo2016Filter)'
cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['HP'] = '(lnujj_l2_tau2/lnujj_l2_tau1<0.55)'
cuts['LP'] = '(lnujj_l2_tau2/lnujj_l2_tau1>0.55&&lnujj_l2_tau2/lnujj_l2_tau1<0.75)'
cuts['tau'] = '(lnujj_l2_tau2/lnujj_l2_tau1<0.365)'
cuts['nob'] = '(lnujj_nMediumBTags==0)*lnujj_btagWeight'
cuts['b'] = '(lnujj_nMediumBTags>0)*lnujj_btagWeight'
cuts['resW']='(lnujj_l2_mergedVTruth==1)'
cuts['nonres']='(lnujj_l2_mergedVTruth==0)'
cuts['SDSideBand']='((lnujj_l2_softDrop_mass>30&&lnujj_l2_softDrop_mass<65)||(lnujj_l2_softDrop_mass>135&&lnujj_l2_softDrop_mass<250))'
cuts['SDWindow']='(lnujj_l2_softDrop_mass>30&&lnujj_l2_softDrop_mass<210)'
#cuts['resMass']='(lnujj_LV_mass>3000&&lnujj_LV_mass<4000)'
cuts['pTm']='(lnujj_l1_pt/lnujj_LV_mass>0.4)'
cuts['dijet1']='(lnujj_vbf_j1_pt>0)'
cuts['dijet2']='(lnujj_vbf_j2_pt>0)'
cuts['dijet']='(lnujj_vbf_j1_pt>0&&lnujj_vbf_j2_pt>0)'
cuts['dijetEta']='(lnujj_vbf_j1_eta*lnujj_vbf_j2_eta<0)'

#change the CMS_lumi variables (see CMS_lumi.py)
lumi_13TeV = "35.9 fb^{-1}"
lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod=4
iPos = 11

#zjPlotters=[]
VJetsPlotters = getPlotters('DYJetsToLL_M50_HT,WJetsToLNu_HT',False)
VJets = MergedPlotter(VJetsPlotters)

TTVVPlotters = getPlotters('TT_pow,T_tWch,TBar_tWch,WWTo1L1Nu2Q,WZTo1L1Nu2Q',False)
ttVV=MergedPlotter(TTVVPlotters)

#BKGPlotters = getPlotters('DYJetsToLL_M50_HT,WJetsToLNu_HT,TT_pow,T_tWch,TBar_tWch,WWTo1L1Nu2Q,WZTo1L1Nu2Q',False,cuts['nonres'])
#BKG = MergedPlotter(BKGPlotters)

BKGPlotters = getPlotters('QCD_HT,WWToLNuQQ,WZTolL1Nu2Q,ZZTo2L2Q,DYJetsToLL_M50_HT,WJetsToLNu_HT,TT_pow,T_tWch,TBar_tWch',False)
BKG = MergedPlotter(BKGPlotters)

WPlotters = getPlotters('TT_pow,T_tWch,TBar_tWch,WWTo1L1Nu2Q,WZTo1L1Nu2Q',False,cuts['resW'])
W = MergedPlotter(WPlotters)

TOPPlotters = getPlotters('TT_pow,T_tWch,TBar_tWch',False)
top = MergedPlotter(TOPPlotters)

dibosonPlotters = getPlotters('WWToLNuQQ,WZTo1L1Nu2Q,ZZTo2L2Q',False)
diboson = MergedPlotter(dibosonPlotters)

QCDPlotters = getPlotters('QCD_HT',False)
QCD = MergedPlotter(QCDPlotters)

mc = MergedPlotter(QCDPlotters+WPlotters+BKGPlotters)

DATAPlotters = getPlotters('SingleMuon_,SingleElectron_,MET_',True)
data=MergedPlotter(DATAPlotters)

#sigPlotters = getPlotters('BulkGravToWWToWlepWhad_narrow_2000',False,0.01)
#sigPlotters = getPlotters('VBF_RadionToWW_narrow_3000',False,1)
#sig = MergedPlotter(sigPlotters)

#Fill properties
#VJets.setFillProperties(1001,ROOT.kAzure-9)
#BKG.setFillProperties(1001,ROOT.kAzure-9)
#ttVV.setFillProperties(1001,ROOT.kSpring-5)
#top.setFillProperties(1001,ROOT.kSpring-5)
#W.setFillProperties(1001,ROOT.kSpring-5)
#QCD.setFillProperties(1001,ROOT.kGray)
#diboson.setFillProperties(1001,ROOT.kOrange)

#Stack for lnu+J
#lnujjStack = StackPlotter()
#lnujjStack.addPlotter(QCD,"QCD","QCD multijet","background")
#lnujjStack.addPlotter(diboson,"diboson","Diboson","background")
#lnujjStack.addPlotter(VJets,"WJets","V+Jets","background")
#lnujjStack.addPlotter(top,"top","Top","background")
#lnujjStack.addPlotter(sig,"sig","Signal","signal")

bins={'pt':[100,0,1000],'mass':[100,0,1000],'sigMass':[100,0,4000],'eta':[100,-5,5],'deta':[100,0,10],'phi':[100,-3.2,3.2],'tau':[100,0,1],'eta12':[100,-25,25]}
plots={'l1_pt':('lnujj_l1_pt',bins['pt']),'l1_mass':('lnujj_l1_mass',bins['mass']),'l1_eta':('lnujj_l1_eta',bins['eta']),'l1_l_pt':('lnujj_l1_l_pt',bins['pt']),'l1_l_mass':('lnujj_l1_l_mass',bins['mass']),'l2_softDrop_mass':('lnujj_l2_softDrop_mass',bins['mass']),'l2_softDrop_eta':('lnujj_l2_softDrop_eta',bins['eta']),'l2_tau21':('lnujj_l2_tau2/lnujj_l2_tau1',bins['tau'])}
#plots={'SD_mass':('lnujj_l2_softDrop_mass',bins['mass']),'Tot_mass':('lnujj_LV_mass',bins['sigMass']),'Jet1_pt':('lnujj_vbf_j1_pt',bins['pt']),'Jet2_pt':('lnujj_vbf_j2_pt',bins['pt']),'Jet1_mass':('lnujj_vbf_j1_mass',bins['mass']),'Jet2_mass':('lnujj_vbf_j2_mass',bins['mass']),'Jet1_eta':('lnujj_vbf_j1_eta',bins['eta']),'Jet2_eta':('lnujj_vbf_j2_eta',bins['eta']),'Jet_deta':('lnujj_vbfDEta',bins['deta']),'Jet_mass':('lnujj_vbfMass',bins['mass']),'Jet_eta12':('lnujj_vbf_j1_eta*lnujj_vbf_j2_eta',bins['eta12'])}
#plots={'Tot_mass':('lnujj_LV_mass',bins['sigMass']),'l2_tau21':('lnujj_l2_tau2/lnujj_l2_tau1',bins['tau'])}
#cut=cuts['common']+'*'+cuts['dijet1']+'*'+cuts['dijet2']+'*'+cuts['nob']+'*'+cuts['tau']+'*'+cuts['resMass']+'*'+cuts['SDWindow']
lumi='35900'

masses=[1000,1200,1400,1600,1800,2000,2500,3000,3500,3000,4500]

for mass in masses:
  sigPlotters = getPlotters('VBF_RadionToWW_narrow_'+str(mass),False,1)
  sig = MergedPlotter(sigPlotters)

  cuts['resMass']='(lnujj_LV_mass>'+str(mass-500)+'&&lnujj_LV_mass<'+str(mass+500)+')'
  cut=cuts['common']+'*'+cuts['dijet1']+'*'+cuts['dijet2']+'*'+cuts['nob']+'*'+cuts['tau']+'*'+cuts['resMass']+'*'+cuts['SDWindow']
#SDSigHist=sig.drawTH1('lnujj_l2_softDrop_mass',cut,lumi,bins['mass'][0],bins['mass'][1],bins['mass'][2])
#SDBkgHist=BKG.drawTH1('lnujj_l2_softDrop_mass',cut,lumi,bins['mass'][0],bins['mass'][1],bins['mass'][2])
#massSigHist=sig.drawTH1('lnujj_LV_mass',cut,lumi,bins['sigMass'][0],bins['sigMass'][1],bins['sigMass'][2])
#massBkgHist=BKG.drawTH1('lnujj_LV_mass',cut,lumi,bins['sigMass'][0],bins['sigMass'][1],bins['sigMass'][2])
#SDSigBkg=sigOverBkg('softDrop_mass',SDSigHist,SDBkgHist,bins['mass'][1],bins['mass'][2])
#massSigBkg=sigOverBkg('LV_mass',massSigHist,massBkgHist,bins['sigMass'][1],bins['sigMass'][2])

  f=ROOT.TFile("fig/VBF"+str(mass)+".root","RECREATE")
  f.cd()

  for plotname,plot in plots.iteritems():
      comp=compare(sig,BKG,plot[0],cut,cut,plot[1][0],plot[1][1],plot[1][2],'','','sig','bkg')
      comp.SetName(plotname)
      comp.Write()
      #stack=lnujjStack.drawStack(plot[0],cut,lumi,plot[1][0],plot[1][1],plot[1][2])
      #stack['canvas'].SetName(plotname)
      #stack['canvas'].Write()

  f.Close()

