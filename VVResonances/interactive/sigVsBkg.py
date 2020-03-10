import ROOT,math
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *
import os
import pdb
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


    return canvas,h1,h2#,legend,pt

def sigVsBkg1D(sig,bkg,var,name,cut,bins,direc,titlex):
    # Get histograms
    sigh=sig.drawTH1(var,cut,"1",bins[0],bins[1],bins[2],'','')
    bkgh=bkg.drawTH1(var,cut,"1",bins[0],bins[1],bins[2],'','')

    # Get SvB values
    SvBVec=[]
    if direc=='<':
	for i in xrange(1,bins[0]+1):
	    S=sigh.Integral(0,i)
	    B=bkgh.Integral(0,i)
	    if B==0 and S==0:
		SvB=0
	    elif B==0 and S!=0:
	        SvB=S
	    else:
	        SvB=S/math.sqrt(B)
	    SvBVec.append([i,SvB])
    elif direc=='>':
        for i in xrange(0,bins[0]):
	    S=sigh.Integral(i,bins[0]+1)
	    B=bkgh.Integral(i,bins[0]+1)
	    if B==0 and S==0:
		SvB=0
	    elif B==0 and S!=0:
	        SvB=S
	    else:
	        SvB=S/math.sqrt(B)
	    SvBVec.append([i,SvB])

    # Make histogram
    sigVsBkgHist=ROOT.TH1D('','',bins[0],bins[1],bins[2])
    for i in xrange(0,len(SvBVec)):
	histBin=sigVsBkgHist.GetBin(SvBVec[i][0])
	sigVsBkgHist.SetBinContent(histBin,SvBVec[i][1])
    
    canv=ROOT.TCanvas(name)
    canv.cd()
    sigVsBkgHist.Draw()
    sigVsBkgHist.GetXaxis().SetTitle(titlex)
    sigVsBkgHist.GetYaxis().SetTitle('S/#sqrt{B}')
    sigVsBkgHist.GetYaxis().SetTitleOffset(1.75)
    sigVsBkgHist.SetTitle('')
    sigVsBkgHist.SetStats(0)
    canv.Write()
    imgname='/scratch2/David/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/Fig/SVB/'+name+'.pdf'
    canv.Print(imgname)

def sigVsBkg2D(sig,bkg,var,name,cut,bins1,bins2,direc1,direc2,titlex,titley):
    # Get histograms
    sigh=sig.drawTH2(var,cut,"1",bins1[0],bins1[1],bins1[2],bins2[0],bins2[1],bins2[2],'','','','')
    bkgh=bkg.drawTH2(var,cut,"1",bins1[0],bins1[1],bins1[2],bins2[0],bins2[1],bins2[2],'','','','')

    # Get SvB values
    SvBVec=[]
    if direc1=='<' and direc2=='<':
	for i in xrange(1,bins1[0]+1):
	    for j in xrange(1,bins2[0]+1):
		S=sigh.Integral(0,i,0,j)
		B=bkgh.Integral(0,i,0,j)
		if B==0 and S==0:
		    SvB=0
		elif B==0 and S!=0:
		    SvB=S
		else:
		    SvB=S/math.sqrt(B)
		SvBVec.append([i,j,SvB])
    elif direc1=='>' and direc2=='<':
	for i in xrange(0,bins1[0]):
	    for j in xrange(1,bins2[0]+1):
		S=sigh.Integral(i,bins1[0]+1,0,j)
		B=bkgh.Integral(i,bins1[0]+1,0,j)
		if B==0 and S==0:
		    SvB=0
		elif B==0 and S!=0:
		    SvB=S
		else:
		    SvB=S/math.sqrt(B)
		SvBVec.append([i,j,SvB])
    elif direc1=='<' and direc2=='>':
	for i in xrange(1,bins1[0]+1):
	    for j in xrange(0,bins2[0]):
		S=sigh.Integral(0,i,j,bins2[0]+1)
		B=bkgh.Integral(0,i,j,bins2[0]+1)
		if B==0 and S==0:
		    SvB=0
		elif B==0 and S!=0:
		    SvB=S
		else:
		    SvB=S/math.sqrt(B)
		SvBVec.append([i,j,SvB])
    elif direc1=='>' and direc2=='>':
	for i in xrange(0,bins1[0]):
	    for j in xrange(0,bins2[0]):
		S=sigh.Integral(i,bins1[0]+1,j,bins2[0]+1)
		B=bkgh.Integral(i,bins1[0]+1,j,bins2[0]+1)
		if B==0 and S==0:
		    SvB=0
		elif B==0 and S!=0:
		    SvB=S
		else:
		    SvB=S/math.sqrt(B)
		SvBVec.append([i,j,SvB])

    # Make histogram
    sigVsBkgHist=ROOT.TH2D('','',bins1[0],bins1[1],bins1[2],bins2[0],bins2[1],bins2[2])
    for i in xrange(0,len(SvBVec)):
	histBin=sigVsBkgHist.GetBin(SvBVec[i][0],SvBVec[i][1])
	sigVsBkgHist.SetBinContent(histBin,SvBVec[i][2])

    ROOT.gStyle.SetPadLeftMargin(0.125)
    ROOT.gStyle.SetPadRightMargin(0.175)
    canv=ROOT.TCanvas(name,name,650,500)
    canv.cd()
    sigVsBkgHist.Draw("COLZ")
    sigVsBkgHist.GetXaxis().SetTitle(titlex)
    sigVsBkgHist.GetYaxis().SetTitle(titley)
    sigVsBkgHist.GetYaxis().SetTitleOffset(1.5)
    sigVsBkgHist.GetZaxis().SetTitle('S/#sqrt{B}')
    sigVsBkgHist.GetZaxis().SetTitleOffset(1.4)
    sigVsBkgHist.SetStats(0)
    sigVsBkgHist.SetTitle('')
    ROOT.gStyle.SetPalette(1)
    canv.Update()
    palette=sigVsBkgHist.GetListOfFunctions().FindObject("palette")
    palette.SetX1NDC(0.84)
    palette.SetX2NDC(0.865)
    canv.Write()
    imgname='/scratch2/David/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/Fig/SVB/'+name+'.pdf'
    canv.Print(imgname)
    ROOT.gStyle.SetPadRightMargin(0.019999999552965164)
    ROOT.gStyle.SetPadLeftMargin(0.1599999964237213)

def sigEff1D(sig,var,name,cut,bins,direc,titlex):
    # Get histograms
    sigh=sig.drawTH1(var,cut,"1",bins[0],bins[1],bins[2],'','')

    # Get SvB values
    STot=sigh.Integral()
    SvTVec=[]
    if direc=='<':
	for i in xrange(1,bins[0]+1):
	    S=sigh.Integral(0,i)
	    SvT=S/STot
	    SvTVec.append([i,SvT])
    elif direc=='>':
        for i in xrange(0,bins[0]):
	    S=sigh.Integral(i,bins[0]+1)
	    SvT=S/STot
	    SvTVec.append([i,SvT])

    # Make histogram
    sigEffHist=ROOT.TH1D('','',bins[0],bins[1],bins[2])
    for i in xrange(0,len(SvTVec)):
	histBin=sigEffHist.GetBin(SvTVec[i][0])
	sigEffHist.SetBinContent(histBin,SvTVec[i][1])
    
    canv=ROOT.TCanvas(name)
    canv.cd()
    sigEffHist.Draw()
    sigEffHist.GetXaxis().SetTitle(titlex)
    sigEffHist.GetYaxis().SetTitle('S/S_{tot}')
    sigEffHist.GetYaxis().SetTitleOffset(1.6)
    sigEffHist.SetTitle('')
    sigEffHist.SetStats(0)
    canv.Write()
    imgname='/scratch2/David/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/Fig/SVB/'+name+'.pdf'
    canv.Print(imgname)

def sigEff2D(sig,var,name,cut,bins1,bins2,direc1,direc2,titlex,titley):
    # Get histograms
    sigh=sig.drawTH2(var,cut,"1",bins1[0],bins1[1],bins1[2],bins2[0],bins2[1],bins2[2],'','','','')

    # Get SvB values
    STot=sigh.Integral()
    SvTVec=[]
    if direc1=='<' and direc2=='<':
	for i in xrange(1,bins1[0]+1):
	    for j in xrange(1,bins2[0]+1):
		S=sigh.Integral(0,i,0,j)
		SvT=S/STot
		SvTVec.append([i,j,SvT])
    elif direc1=='>' and direc2=='<':
	for i in xrange(0,bins1[0]):
	    for j in xrange(1,bins2[0]+1):
		S=sigh.Integral(i,bins1[0]+1,0,j)
		SvT=S/STot
		SvTVec.append([i,j,SvT])
    elif direc1=='<' and direc2=='>':
	for i in xrange(1,bins1[0]+1):
	    for j in xrange(0,bins2[0]):
		S=sigh.Integral(0,i,j,bins2[0]+1)
		SvT=S/STot
		SvTVec.append([i,j,SvT])
    elif direc1=='>' and direc2=='>':
	for i in xrange(0,bins1[0]):
	    for j in xrange(0,bins2[0]):
		S=sigh.Integral(i,bins1[0]+1,j,bins2[0]+1)
		SvT=S/STot
		SvTVec.append([i,j,SvT])

    # Make histogram
    sigEffHist=ROOT.TH2D('','',bins1[0],bins1[1],bins1[2],bins2[0],bins2[1],bins2[2])
    for i in xrange(0,len(SvTVec)):
	histBin=sigEffHist.GetBin(SvTVec[i][0],SvTVec[i][1])
	sigEffHist.SetBinContent(histBin,SvTVec[i][2])
    
    ROOT.gStyle.SetPadLeftMargin(0.125)
    ROOT.gStyle.SetPadRightMargin(0.175)
    canv=ROOT.TCanvas(name,name,650,500)
    canv.cd()
    sigEffHist.Draw("COLZ")
    sigEffHist.GetXaxis().SetTitle(titlex)
    sigEffHist.GetYaxis().SetTitle(titley)
    sigEffHist.GetYaxis().SetTitleOffset(1.5)
    sigEffHist.GetZaxis().SetTitle('S/S_{tot}')
    sigEffHist.GetZaxis().SetTitleOffset(1.4)
    sigEffHist.SetStats(0)
    sigEffHist.SetTitle('')
    ROOT.gStyle.SetPalette(1)
    canv.Update()
    palette=sigEffHist.GetListOfFunctions().FindObject("palette")
    palette.SetX1NDC(0.84)
    palette.SetX2NDC(0.865)
    canv.Write()
    imgname='/scratch2/David/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/Fig/SVB/'+name+'.pdf'
    canv.Print(imgname)
    ROOT.gStyle.SetPadRightMargin(0.019999999552965164)
    ROOT.gStyle.SetPadLeftMargin(0.1599999964237213)

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
cuts['resMass']='(lnujj_LV_mass>1500&&lnujj_LV_mass<2500)'
cuts['pTm']='(lnujj_l1_pt/lnujj_LV_mass>0.4)'
cuts['dijet1']='(lnujj_vbf_j1_pt>0)'
cuts['dijet2']='(lnujj_vbf_j2_pt>0)'
cuts['dijet']='(lnujj_vbf_j1_pt>0&&lnujj_vbf_j2_pt>0)'

#change the CMS_lumi variables (see CMS_lumi.py)
lumi_13TeV = "35.9 fb^{-1}"
lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod=4
iPos = 11

BKGPlotters = getPlotters('QCD_HT,WWToLNuQQ,WZTolL1Nu2Q,ZZTo2L2Q,DYJetsToLL_M50_HT,WJetsToLNu_HT,TT_pow,T_tWch,TBar_tWch',False)
BKG = MergedPlotter(BKGPlotters)

sigPlotters = getPlotters('VBF_RadionToWW_narrow_2000',False,1)
sig = MergedPlotter(sigPlotters)

bins={'pt':[100,0,1000],'mass':[100,0,1000],'sigMass':[100,0,4000],'eta':[100,-5,5],'abseta':[100,0,5],'deta':[100,0,10],'phi':[100,-3.2,3.2],'tau':[100,0,1],'eta12':[100,-25,25]}
plots={'SD_mass':('lnujj_l2_softDrop_mass',bins['mass']),'Tot_mass':('lnujj_LV_mass',bins['sigMass']),'Jet1_pt':('lnujj_vbf_j1_pt',bins['pt']),'Jet2_pt':('lnujj_vbf_j2_pt',bins['pt']),'Jet1_mass':('lnujj_vbf_j1_mass',bins['mass']),'Jet2_mass':('lnujj_vbf_j2_mass',bins['mass']),'Jet1_eta':('lnujj_vbf_j1_eta',bins['eta']),'Jet2_eta':('lnujj_vbf_j2_eta',bins['eta']),'Jet_deta':('lnujj_vbfDEta',bins['deta']),'Jet_mass':('lnujj_vbfMass',bins['mass'])}
cut=cuts['common']+'*'+cuts['dijet1']+'*'+cuts['dijet2']+'*'+cuts['nob']+'*'+cuts['tau']+'*'+cuts['resMass']+'*'+cuts['SDWindow']
lumi='35900'

#detaMjjSB=sigEff2D(sig,'lnujj_vbfMass:lnujj_vbfDEta','detaMjjSB',cut,bins['deta'],bins['sigMass'],'>','>','#Delta#eta','m_{jj} (GeV)')

f=ROOT.TFile("SVB.root","RECREATE")
f.cd()

sigVsBkg1D(sig,BKG,'abs(lnujj_vbf_j1_eta)','eta1SB',cut,bins['abseta'],'>','#eta_{1} Cut Threshold')
#sigVsBkg1D(sig,BKG,'abs(lnujj_vbf_j2_eta)','eta2SB',cut,bins['abseta'],'>','#eta_{2}')
#sigVsBkg1D(sig,BKG,'lnujj_vbf_j1_eta*lnujj_vbf_j2_eta','eta12SB',cut,bins['eta12'],'<','#eta_{1}#eta_{2}')
#sigVsBkg1D(sig,BKG,'lnujj_vbfDEta','detaSB',cut,bins['deta'],'>','#Delta#eta')
#sigVsBkg1D(sig,BKG,'lnujj_vbfMass','mjjSB',cut,bins['sigMass'],'>','m_{jj} (GeV)')

#sigEff1D(sig,'abs(lnujj_vbf_j1_eta)','eta1Eff',cut,bins['abseta'],'>','#eta_{1}')
#sigEff1D(sig,'abs(lnujj_vbf_j2_eta)','eta2Eff',cut,bins['abseta'],'>','#eta_{2}')
#sigEff1D(sig,'lnujj_vbf_j1_eta*lnujj_vbf_j2_eta','eta12Eff',cut,bins['eta12'],'<','#eta_{1}#eta_{2}')
#sigEff1D(sig,'lnujj_vbfDEta','detaEff',cut,bins['deta'],'>','#Delta#eta')
#sigEff1D(sig,'lnujj_vbfMass','mjjEff',cut,bins['sigMass'],'>','m_{jj} (GeV)')

#sigVsBkg2D(sig,BKG,'abs(lnujj_vbf_j2_eta):abs(lnujj_vbf_j1_eta)','eta1Eta2SB',cut,bins['abseta'],bins['abseta'],'>','>','#eta_{1}','#eta_{2}')
#sigVsBkg2D(sig,BKG,'lnujj_vbfMass:abs(lnujj_vbf_j1_eta)','eta1MjjSB',cut,bins['abseta'],bins['sigMass'],'>','>','#eta_{1}','m_{jj} (GeV)')
#sigVsBkg2D(sig,BKG,'lnujj_vbfMass:abs(lnujj_vbf_j2_eta)','eta2MjjSB',cut,bins['abseta'],bins['sigMass'],'>','>','#eta_{2}','m_{jj} (GeV)')
#sigVsBkg2D(sig,BKG,'lnujj_vbfMass:lnujj_vbf_j1_eta*lnujj_vbf_j2_eta','eta12MjjSB',cut,bins['eta12'],bins['sigMass'],'<','>','#eta_{1}#eta_{2}','m_{jj} (GeV)')
#sigVsBkg2D(sig,BKG,'lnujj_vbfMass:lnujj_vbfDEta','detaMjjSB',cut,bins['deta'],bins['sigMass'],'>','>','#Delta#eta','m_{jj} (GeV)')

#sigEff2D(sig,'abs(lnujj_vbf_j2_eta):abs(lnujj_vbf_j1_eta)','eta1Eta2Eff',cut,bins['abseta'],bins['abseta'],'>','>','#eta_{1}','#eta_{2}')
#sigEff2D(sig,'lnujj_vbfMass:abs(lnujj_vbf_j1_eta)','eta1MjjEff',cut,bins['abseta'],bins['sigMass'],'>','>','#eta_{1}','m_{jj} (GeV)')
#sigEff2D(sig,'lnujj_vbfMass:abs(lnujj_vbf_j2_eta)','eta2MjjEff',cut,bins['abseta'],bins['sigMass'],'>','>','#eta_{2}','m_{jj} (GeV)')
#sigEff2D(sig,'lnujj_vbfMass:lnujj_vbf_j1_eta*lnujj_vbf_j2_eta','eta12MjjEff',cut,bins['eta12'],bins['sigMass'],'<','>','#eta_{1}#eta_{2}','m_{jj} (GeV)')
#sigEff2D(sig,'lnujj_vbfMass:lnujj_vbfDEta','detaMjjEff',cut,bins['deta'],bins['sigMass'],'>','>','#Delta#eta','m_{jj} (GeV)')

#for plotname,plot in plots.iteritems():
    #comp=compare(sig,BKG,plot[0],cut,cut,plot[1][0],plot[1][1],plot[1][2],'','','sig','bkg')
    #comp.SetName(plotname)
    #comp.Write()

f.Close()

