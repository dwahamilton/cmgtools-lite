import sys
import ROOT
import os
import pdb
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker

import optparse
parser=optparse.OptionParser()
parser.add_option("-s","--signalType",dest="signalType",default='XWW',help="XWW or XWZ")
(options,args)=parser.parse_args()

lumi=137190

jets=['W','Z']
leptons=['e','mu']
purities=['HP','LP']
categories=['nob']
bkgs=['nonRes','resW']

bkg_norm={('e','HP','nonRes'):0.5*5.33963e-01,('e','LP','nonRes'):-0.5*2.18383e-05,('mu','HP','nonRes'):0.5*2.83171e-01,('mu','LP','nonRes'):-0.5*5.02642e-02,('lep','HP','nonRes'):0.5*4.14795e-01,('lep','LP','nonRes'):-0.5*1.18997e-02,('lep','allP','W','resW'):-0.5*2.79977e-02,('lep','allP','Z','resW'):-0.5*2.67983e-01}
bkg_normErr={('e','HP','nonRes'):0.5*2.25345e-01,('e','LP','nonRes'):0.5*1.83850e-01,('mu','HP','nonRes'):0.5*2.20691e-01,('mu','LP','nonRes'):0.5*1.73342e-01,('lep','HP','nonRes'):0.5*1.59389e-01,('lep','LP','nonRes'):0.5*1.29324e-01,('lep','allP','W','resW'):0.5*9.58976e-01,('lep','allP','Z','resW'):0.5*9.67829e-01}

HPunc=0.14
LPunc=0.33

inputDir='/scratch2/David/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/inputs/'
cardDir='/scratch2/David/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/datacards/'

for jet in jets:
  for lep in leptons:
    for pur in purities:
      for cat in categories:
        category=lep+'_'+pur+'_'+jet+'_'+cat
        sigCategory=lep+'_'+pur+'_combined_'+cat
        card=DataCardMaker('VBF_'+options.signalType+'_'+category,'','',lumi,'',cardDir)

        card.addMVVSignalParametricShape(options.signalType,"MLNuJ",inputDir+"LNuJJ_"+options.signalType+"_MVV_"+sigCategory+".json",{'CMS_scale_j':1,'CMS_scale_MET':1.0,'CMS_scale_lepton':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})
        card.addParametricYield(options.signalType,0,inputDir+"LNuJJ_"+options.signalType+"_"+sigCategory+"_yield.json",1,1.0)

        dataFile=inputDir+'LNuJJ_'+lep+'_'+pur+'_'+jet+'_'+cat+'.root'
        dataFileResW=inputDir+'LNuJJ_lep_allP_'+jet+'_'+cat+'.root'
        bkgCount=0
        for bkg in bkgs:
          bkgCount+=1
          rootFile=inputDir+'LNuJJ_'+bkg+'_MVV_'+lep+'_'+pur+'_'+jet+'_'+cat+'.root'
          rootFileResW=inputDir+'LNuJJ_resW_MVV_lep_allP_'+jet+'_'+cat+'.root'
          if bkg=='nonRes':
            card.addHistoShapeFromFile(bkg,["MLNuJ"],rootFile,"histo",['PT:CMS_LNuJ_'+bkg+'_'+lep+'_'+pur+'_'+jet+'_'+cat+'_PT'],False,0)
            card.addFixedYieldFromFile(bkg,bkgCount,dataFile,bkg,1+bkg_norm[lep,pur,bkg])
          elif bkg=='resW' and jet!='control':
            card.addHistoShapeFromFile(bkg,["MLNuJ"],rootFileResW,"histo",['PT:CMS_LNuJ_'+bkg+'_lep_allP_'+jet+'_'+cat+'_PT'],False,0)
            card.addFixedYieldFromFile(bkg,bkgCount,dataFile,bkg,1+bkg_norm['lep','allP',jet,bkg])
          elif bkg=='resW' and jet=='control':
            card.addHistoShapeFromFile(bkg,["MLNuJ"],rootFileResW,"histo",['PT:CMS_LNuJ_'+bkg+'_lep_allP_'+jet+'_'+cat+'_PT'],False,0)
            card.addFixedYieldFromFile(bkg,bkgCount,dataFile,bkg,1)

        #fix:
        card.importBinnedData(dataFile,"data",["MLNuJ"])

        #Scale and resolution uncertainties
        card.addSystematic("CMS_lumi","lnN",{'XWW':1.018,'XWZ':1.018,'XWH':1.018})
        card.addSystematic("CMS_lumi","lnN",{'nonRes':1.99,'resW':1.99})

        card.addSystematic("CMS_scale_j","param",[0.0,0.02])
        card.addSystematic("CMS_res_j","param",[0.0,0.05])
        card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
        card.addSystematic("CMS_res_MET","param",[0.0,0.01])

        # Scale uncertainties for backgrounds
        for bkg in bkgs:
          if bkg=='nonRes':
            card.addSystematic("CMS_LNuJ_"+bkg+"_"+lep+"_"+pur+"_"+jet+'_'+cat+"_PT","param",[0.0,0.333])
            card.addSystematic("CMS_LNuJ_"+bkg+"_"+lep+"_"+pur+'_'+cat+"_norm","lnN",{bkg:1+bkg_normErr[lep,pur,bkg]})
            #card.addSystematic("CMS_LNuJ_"+bkg+"_"+lep+"_"+pur+"_norm","lnN",{bkg:1.5})
          elif bkg=='resW':
            card.addSystematic("CMS_LNuJ_"+bkg+"_lep_allP_"+jet+'_'+cat+"_PT","param",[0.0,0.333])
            card.addSystematic("CMS_LNuJ_"+bkg+"_lep_allP_"+jet+'_'+cat+"_norm","lnN",{bkg:1+bkg_normErr['lep','allP',jet,bkg]})
            #card.addSystematic("CMS_LNuJ_"+bkg+"_lep_allP_"+jet+"_norm","lnN",{bkg:1.5})

        # Scale uncertainty for nob category
        if jet!='control':
          card.addSystematic("CMS_LNuJ_resW_bToNob_norm","lnN",{"resW":1.1})
          card.addSystematic("CMS_LNuJ_resW_bToNob_norm","lnN",{"bkg":1.1})

        # Purity scale uncertainties
        if pur=='HP':
          card.addSystematic("CMS_VV_LNuJ_Vtag_eff","lnN",{'XWW':1+HPunc,'XWZ':1+HPunc,'XWH':1+HPunc})
        if pur=='LP':
          card.addSystematic("CMS_VV_LNuJ_Vtag_eff","lnN",{'XWW':1-LPunc,'XWZ':1-LPunc,'XWH':1-LPunc})

        # PDF scale uncertainty
        card.addSystematic("CMS_pdf","lnN",{'XWW':1.01,'XWZ':1.01,'XWH':1.01})

        # btag efficiency
        card.addSystematic("CMS_btag_fake","lnN",{'XWW':1+0.02,'XWZ':1+0.02,'XWH':1+0.02})

        card.makeCard()

        cmd='text2workspace.py {cardDir}datacard_{tag}.txt -o {cardDir}datacard_final_{tag}.root'.format(tag=card.tag,cardDir=cardDir)
        os.system(cmd)
