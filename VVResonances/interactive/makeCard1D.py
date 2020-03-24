import sys
import ROOT
import os
import pdb
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '

import optparse
parser = optparse.OptionParser()
parser.add_option("-s","--signalType",dest="signalType",default='XWW',help="XWW or XWZ")
(options,args) = parser.parse_args()

#lumi={'2016':35920,'2017_5':41530,'2018_2':59740}
#lumi={'2016':137190,'2017_5':137190,'2018_2':137190}
lumi=137190

#bkg={'2016':188.05705,'2017_5':634.75313,'2018_2':892.09947}
bkg={('control','e','HP','2016'):13.499780,('W','e','HP','2016'):42.043208,('Z','e','HP','2016'):26.088060,('H','e','HP','2016'):24.195823,('control','e','LP','2016'):28.944053,('W','e','LP','2016'):14.273380,('Z','e','LP','2016'):6.2752002,('H','e','LP','2016'):4.7739073,('control','mu','HP','2016'):27.528856,('W','mu','HP','2016'):68.266606,('Z','mu','HP','2016'):38.074321,('H','mu','HP','2016'):31.111195,('control','mu','LP','2016'):31.613563,('W','mu','LP','2016'):23.083277,('Z','mu','LP','2016'):9.9887858,('H','mu','LP','2016'):6.1966259,('control','e','HP','2017_5'):76.731385,('W','e','HP','2017_5'):148.06195,('Z','e','HP','2017_5'):93.391460,('H','e','HP','2017_5'):86.650240,('control','e','LP','2017_5'):83.888047,('W','e','LP','2017_5'):52.942047,('Z','e','LP','2017_5'):25.714571,('H','e','LP','2017_5'):12.544047,('control','mu','HP','2017_5'):111.03278,('W','mu','HP','2017_5'):194.74530,('Z','mu','HP','2017_5'):131.19518,('H','mu','HP','2017_5'):119.44255,('control','mu','LP','2017_5'):113.14269,('W','mu','LP','2017_5'):75.698488,('Z','mu','LP','2017_5'):23.232694,('H','mu','LP','2017_5'):17.527820,('control','e','HP','2018_2'):113.18840,('W','e','HP','2018_2'):207.29984,('Z','e','HP','2018_2'):133.18523,('H','e','HP','2018_2'):133.80610,('control','e','LP','2018_2'):127.88123,('W','e','LP','2018_2'):79.339567,('Z','e','LP','2018_2'):26.275242,('H','e','LP','2018_2'):20.568970,('control','mu','HP','2018_2'):158.59926,('W','mu','HP','2018_2'):260.44882,('Z','mu','HP','2018_2'):185.16028,('H','mu','HP','2018_2'):168.60683,('control','mu','LP','2018_2'):183.55298,('W','mu','LP','2018_2'):121.37156,('Z','mu','LP','2018_2'):43.955580,('H','mu','LP','2018_2'):30.734954}

#jets=['W','Z','H','combined']
#jets=['control']
jets=['W','Z']
#jets=['combined']
#leptons=['lep','e','mu']
leptons=['e','mu']
#leptons=['e']
#purities=['HP','LP','allP']
purities=['HP','LP']
#purities=['allP']
#purities=['HP']
bkgs=['nonRes','resW']
#bkgs=['resW']
#years=['2016','2017_5','2018_2']
#years=['2016']

#signalYear={'2016':'2017_5','2017_5':'2017_5','2018_2':'2018_2'}
#bkgYear={'2016':'2016','2017_5':'2017_5','2018_2':'2018_2'}

#numToys=100

bkg_norm={('e','HP','nonRes'):0.5*5.33963e-01,('e','LP','nonRes'):-0.5*2.18383e-05,('mu','HP','nonRes'):0.5*2.83171e-01,('mu','LP','nonRes'):-0.5*5.02642e-02,('lep','HP','nonRes'):0.5*4.14795e-01,('lep','LP','nonRes'):-0.5*1.18997e-02,('e','HP','W','resW'):-0.5*5.36930e-02,('e','HP','Z','resW'):-0.5*4.97050e-01,('e','LP','W','resW'):0.5*8.93484e-01,('e','LP','Z','resW'):0.5*2.30752e-01,('mu','HP','W','resW'):0.5*3.19151e-02,('mu','HP','Z','resW'):-0.5*1.76774e-01,('mu','LP','W','resW'):-0.5*1.74678e-02,('mu','LP','Z','resW'):-0.5*2.39168e-01,('lep','HP','W','resW'):0.5*1.01419e-02,('lep','HP','Z','resW'):-0.5*4.82527e-01,('lep','LP','W','resW'):0.5*6.23588e-01,('lep','LP','Z','resW'):-0.5*2.02816e-02}
bkg_normErr={('e','HP','nonRes'):0.5*2.25345e-01,('e','LP','nonRes'):0.5*1.83850e-01,('mu','HP','nonRes'):0.5*2.20691e-01,('mu','LP','nonRes'):0.5*1.73342e-01,('lep','HP','nonRes'):0.5*1.59389e-01,('lep','LP','nonRes'):0.5*1.29324e-01,('e','HP','W','resW'):0.5*7.04856e-01,('e','HP','Z','resW'):0.5*7.46460e-01,('e','LP','W','resW'):0.5*7.73198e-01,('e','LP','Z','resW'):0.5*8.96634e-01,('mu','HP','W','resW'):0.5*5.98715e-01,('mu','HP','Z','resW'):0.5*6.98166e-01,('mu','LP','W','resW'):0.5*8.92260e-01,('mu','LP','Z','resW'):0.5*8.86146e-01,('lep','HP','W','resW'):0.5*5.17115e-01,('lep','HP','Z','resW'):0.5*6.12463e-01,('lep','LP','W','resW'):0.5*7.08912e-01,('lep','LP','Z','resW'):0.5*8.32015e-01}

HPunc=0.14
LPunc=0.33

for jet in jets:
  for lep in leptons:
    for pur in purities:
      category=lep+'_'+pur+'_'+jet
      sigCategory=lep+'_'+pur+'_combined'
      card=DataCardMaker('VBF_'+options.signalType+'_'+category,'nob','',lumi,'')
      #category='combined_'+year
      #category='combined_'+signalYear[year]
      #card=DataCardMaker('VBF_Radion_'+lep+'_'+pur+'_'+jet+'_'+year,'NP','13TeV',lumi[year],'nob')

      card.addMVVSignalParametricShape("XWW","MLNuJ","LNuJJ_Radion_MVV_"+sigCategory+".json",{'CMS_scale_j':1,'CMS_scale_MET':1.0,'CMS_scale_lepton':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})

      card.addMVVSignalParametricShape("XWZ","MLNuJ","LNuJJ_Radion_MVV_"+sigCategory+".json",{'CMS_scale_j':1,'CMS_scale_MET':1.0,'CMS_scale_lepton':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})
      card.addParametricYield("XWZ",0,"LNuJJ_Radion_"+sigCategory+"_yield.json",1,1.0)

      #Background
      #card.addMVVBackgroundShapeQCD("bkg","MLNuJ",False,"",{})
      #card.addFloatingYield("bkg","1",bkg[jet,lep,pur,year])
      #card.addConstrainedYield("bkg","MLNuJ",)

      dataFile='LNuJJ_'+lep+'_'+pur+'_'+jet+'.root'
      bkgCount=0
      for bkg in bkgs:
        bkgCount+=1
        rootFile='LNuJJ_'+bkg+'_MVV_'+lep+'_'+pur+'_'+jet+'.root'
        card.addHistoShapeFromFile(bkg,["MLNuJ"],rootFile,"histo",['PT:CMS_LNuJ_'+bkg+'_'+lep+'_'+pur+'_'+jet+'_PT'],False,0)
        if bkg=='nonRes':
          card.addFixedYieldFromFile(bkg,bkgCount,dataFile,bkg,1+bkg_norm[lep,pur,bkg])
        elif bkg=='resW' and jet!='control':
          card.addFixedYieldFromFile(bkg,bkgCount,dataFile,bkg,1+bkg_norm[lep,pur,jet,bkg])
        elif bkg=='resW' and jet=='control':
          card.addFixedYieldFromFile(bkg,bkgCount,dataFile,bkg,1)
      #fix:
      card.importBinnedData(dataFile,"data",["MLNuJ"])
      #card.importBinnedData("LNuJJ_control_combined.root","data",["MLNuJ"])

      #Scale and resolution uncertainties
      card.addSystematic("CMS_lumi","lnN",{'XWW':1.018,'XWZ':1.018,'XWH':1.018})
      card.addSystematic("CMS_lumi","lnN",{'nonRes':1.99,'resW':1.99})

      card.addSystematic("CMS_scale_j","param",[0.0,0.02])
      card.addSystematic("CMS_res_j","param",[0.0,0.05])
      card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
      card.addSystematic("CMS_res_MET","param",[0.0,0.01])

      # Scale uncertainties for backgrounds
      for bkg in bkgs:
        card.addSystematic("CMS_LNuJ_"+bkg+"_"+lep+"_"+pur+"_"+jet+"_PT","param",[0.0,0.333])
        if bkg=='nonRes':
          card.addSystematic("CMS_LNuJ_"+bkg+"_"+lep+"_"+pur+"_norm","lnN",{bkg:1+bkg_normErr[lep,pur,bkg]})
        elif bkg=='resW' and jet!='control':
          card.addSystematic("CMS_LNuJ_"+bkg+"_"+lep+"_"+pur+"_"+jet+"_norm","lnN",{bkg:1+bkg_normErr[lep,pur,jet,bkg]})
        elif bkg=='resW' and jet=='control':
          card.addSystematic("CMS_LNuJ_"+bkg+"_"+lep+"_"+pur+"_"+jet+"_norm","lnN",{bkg:1.5})

      # Scale uncertainty for nob category
      if jet!='control':
        card.addSystematic("CMS_LNuJ_resW_bToNob_norm","lnN",{"resW":1.1})

      # Purity scale uncertainties
      if pur=='HP':
        card.addSystematic("CMS_VV_LNuJ_Vtag_eff","lnN",{'XWW':1+HPunc,'XWZ':1+HPunc,'XWH':1+HPunc})
      if pur=='LP':
        card.addSystematic("CMS_VV_LNuJ_Vtag_eff","lnN",{'XWW':1-LPunc,'XWZ':1-LPunc,'XWH':1-LPunc})

      # Lepton efficiency
      #card.addSystematic("CMS_eff_"+lep+,"lnN",{'XWW':1.05,'XWZ':1.05,'XWH':1.05})

      # PDF scale uncertainty
      card.addSystematic("CMS_pdf","lnN",{'XWW':1.01,'XWZ':1.01,'XWH':1.01})

      # btag efficiency
      card.addSystematic("CMS_btag_fake","lnN",{'XWW':1+0.02,'XWZ':1+0.02,'XWH':1+0.02})

      card.makeCard()

      cmd='text2workspace.py datacard_{tag}.txt -o datacard_final_{tag}.root'.format(tag=card.tag)
      os.system(cmd)

'''
for jet in jets:
  for lep in leptons:
    for pur in purities:
      for year in years:
        category=lep+'_'+pur+'_'+jet+'_'+year
        signalCategory=lep+'_'+pur+'_'+jet+'_'+signalYear[year]
        card=DataCardMaker('VBF_Radion_'+category,'NP','13TeV',lumi[year],'nob')
        #category='combined_'+year
        #signalCategory='combined_'+signalYear[year]
        #card=DataCardMaker('VBF_Radion_'+lep+'_'+pur+'_'+jet+'_'+year,'NP','13TeV',lumi[year],'nob')

        card.addMVVSignalParametricShape("XWW","MLNuJ","LNuJJ_Radion_MVV_"+signalCategory+".json",{'CMS_scale_j_'+year:1,'CMS_scale_MET_'+year:1.0,'CMS_scale_lepton_'+year:1.0},{'CMS_res_j_'+year:1.0,'CMS_res_MET_'+year:1.0})

        card.addMVVSignalParametricShape("XWW","MLNuJ","LNuJJ_Radion_MVV_"+signalCategory+".json",{'CMS_scale_j_'+year:1,'CMS_scale_MET_'+year:1.0,'CMS_scale_lepton_'+year:1.0},{'CMS_res_j_'+year:1.0,'CMS_res_MET_'+year:1.0})
        card.addParametricYield("XWW",0,"LNuJJ_Radion_"+signalCategory+"_yield.json",1,1.0)

        #Background
        #card.addMVVBackgroundShapeQCD("bkg","MLNuJ",False,"",{})
        #card.addFloatingYield("bkg","1",bkg[jet,lep,pur,year])
        #card.addConstrainedYield("bkg","MLNuJ",)

        dataFile='LNuJJ_'+lep+'_'+pur+'_'+jet+'_'+year+'.root'
        bkgCount=0
        for bkg in bkgs:
          bkgCount+=1
          rootFile='LNuJJ_'+bkg+'_MVV_'+lep+'_'+pur+'_'+jet+'_'+year+'.root'
          card.addHistoShapeFromFile(bkg,["MLNuJ"],rootFile,"histo",['PT:CMS_LNuJ_'+bkg+'_PT_'+lep+'_'+pur+'_'+jet+'_'+year],False,0)
          card.addFixedYieldFromFile(bkg,bkgCount,dataFile,bkg)

        #fix:
        card.importBinnedData(dataFile,"data",["MLNuJ"])
        #card.importBinnedData("LNuJJ_control_combined.root","data",["MLNuJ"])

        #Scale and resolution uncertainties
        card.addSystematic("CMS_lumi_"+year,"lnN",{'XWW':1.026})
        card.addSystematic("CMS_lumi_"+year,"lnN",{'bkg':1.99})

        card.addSystematic("CMS_scale_j_"+year,"param",[0.0,0.02])
        card.addSystematic("CMS_res_j_"+year,"param",[0.0,0.05])
        card.addSystematic("CMS_scale_MET_"+year,"param",[0.0,0.02])
        card.addSystematic("CMS_res_MET_"+year,"param",[0.0,0.01])

        for bkg in bkgs:
          card.addSystematic("CMS_LNuJ_"+bkg+"_PT_"+lep+"_"+pur+"_"+jet+"_"+year,"param",[0.0,0.333])

        #pruned mass scale
        #card.addSystematic("CMS_scale_j","param",[0.0,0.02])
        #card.addSystematic("CMS_res_j","param",[0.0,0.05])

        #card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
        #card.addSystematic("CMS_res_MET","param",[0.0,0.01])

        card.addSystematic("CMS_scale_lepton_"+year,"param",[0.0,0.004])

        card.makeCard()

        cmd='text2workspace.py datacard_{tag}.txt -o datacard_final_{tag}.root'.format(tag=card.tag)
        os.system(cmd)
'''

'''
for year in years:
  for jet in jets:
    category=jet+'_'+year
    signalCategory=jet+'_'+signalYear[year]
    card=DataCardMaker('VBF_Radion_'+category,'NP','13TeV',lumi[year],'nob')

    card.addMVVSignalParametricShape("XWW","MLNuJ","LNuJJ_Radion_MVV_"+signalCategory+".json",{'CMS_scale_j_'+year:1,'CMS_scale_MET_'+year:1.0,'CMS_scale_lepton_'+year:1.0},{'CMS_res_j_'+year:1.0,'CMS_res_MET_'+year:1.0})

    card.addMVVSignalParametricShape("XWW","MLNuJ","LNuJJ_Radion_MVV_"+signalCategory+".json",{'CMS_scale_j_'+year:1,'CMS_scale_MET_'+year:1.0,'CMS_scale_lepton_'+year:1.0},{'CMS_res_j_'+year:1.0,'CMS_res_MET_'+year:1.0})
    card.addParametricYield("XWW",0,"LNuJJ_Radion_"+signalCategory+"_yield.json",1,1.0)

    #Background
    card.addMVVBackgroundShapeQCD("bkg","MLNuJ",False,"",{})
    #card.addFloatingYield("bkg","1",bkg[jet,lep,pur,year])
    card.addFloatingYield("bkg","1",500)
    #card.addConstrainedYield("bkg","MLNuJ",)

    rootFile='LNuJJ_bkg_MVV_'+jet+'_'+year+'.root'
    card.addHistoShapeFromFile("bkg",["MLNuJ"],rootFile,"histo",['Res:CMS_LNuJ_bkg_res_'+year,'Scale:CMS_LNuJ_bkg_scale_'+year],False,0)
    #card.addFixedYieldFromFile("bkg",1,rootFile,"histo")
    card.addFixedYieldFromFile("bkg",1,"LNuJJ_"+jet+"_"+year+".root","bkg")

    #fix:
    card.importBinnedData("LNuJJ_"+category+".root","data",["MLNuJ"])
    #card.importBinnedData("LNuJJ_control_combined.root","data",["MLNuJ"])

    #Scale and resolution uncertainties
    card.addSystematic("CMS_lumi_"+year,"lnN",{'XWW':1.026})
    #card.addSystematic("CMS_lumi_"+year,"lnN",{'bkg':1.99})

    card.addSystematic("CMS_scale_j_"+year,"param",[0.0,0.02])
    card.addSystematic("CMS_res_j_"+year,"param",[0.0,0.05])
    card.addSystematic("CMS_scale_MET_"+year,"param",[0.0,0.02])
    card.addSystematic("CMS_res_MET_"+year,"param",[0.0,0.01])

    card.addSystematic("CMS_LNuJ_bkg_res_"+year,"param",[0.0,0.333])
    card.addSystematic("CMS_LNuJ_bkg_scale_"+year,"param",[0.0,0.333])

    #pruned mass scale
    #card.addSystematic("CMS_scale_j","param",[0.0,0.02])
    #card.addSystematic("CMS_res_j","param",[0.0,0.05])

    #card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
    #card.addSystematic("CMS_res_MET","param",[0.0,0.01])

    card.addSystematic("CMS_scale_lepton_"+year,"param",[0.0,0.004])

    card.makeCard()

    cmd='text2workspace.py datacard_{tag}.txt -o datacard_final_{tag}.root'.format(tag=card.tag)
    os.system(cmd)
'''

'''
for toyNum in xrange(0,numToys):
  for year in years:
    for jet in jets:
      category=jet+'_'+year+'_toy'+str(toyNum)
      signalCategory=jet+'_'+signalYear[year]
      card=DataCardMaker('VBF_Radion_'+category,'','',lumi[year],'nob')

      card.addMVVSignalParametricShape("XWW","MLNuJ","LNuJJ_Radion_MVV_"+signalCategory+".json",{'CMS_scale_j_'+year:1,'CMS_scale_MET_'+year:1.0,'CMS_scale_lepton_'+year:1.0},{'CMS_res_j_'+year:1.0,'CMS_res_MET_'+year:1.0})

      card.addMVVSignalParametricShape("XWW","MLNuJ","LNuJJ_Radion_MVV_"+signalCategory+".json",{'CMS_scale_j_'+year:1,'CMS_scale_MET_'+year:1.0,'CMS_scale_lepton_'+year:1.0},{'CMS_res_j_'+year:1.0,'CMS_res_MET_'+year:1.0})
      card.addParametricYield("XWW",0,"LNuJJ_Radion_"+signalCategory+"_yield.json",1,1.0)

      ''''''
      #Background
      card.addMVVBackgroundShapeQCD("bkg","MLNuJ",False,"",{})
      #card.addFloatingYield("bkg","1",bkg[jet,lep,pur,year])
      card.addFloatingYield("bkg","1",500)
      #card.addConstrainedYield("bkg","MLNuJ",)
      ''''''

      #Background
      rootFile='LNuJJ_bkg_MVV_'+jet+'_'+year+'.root'
      card.addHistoShapeFromFile("bkg",["MLNuJ"],rootFile,"histo",['Res:CMS_LNuJ_bkg_res_'+year,'Scale:CMS_LNuJ_bkg_scale_'+year],False,0)
      #card.addFixedYieldFromFile("bkg",1,rootFile,"histo")
      card.addFixedYieldFromFile("bkg",1,"LNuJJ_"+jet+"_"+year+".root","bkg")

      #fix:
      card.importBinnedData("LNuJJ_combined_toys.root","toy"+str(toyNum),["MLNuJ"])
      #card.importBinnedData("LNuJJ_control_combined.root","data",["MLNuJ"])

      #Scale and resolution uncertainties
      card.addSystematic("CMS_lumi_"+year,"lnN",{'XWW':1.026})
      #card.addSystematic("CMS_lumi_"+year,"lnN",{'bkg':1.99})

      card.addSystematic("CMS_scale_j_"+year,"param",[0.0,0.02])
      card.addSystematic("CMS_res_j_"+year,"param",[0.0,0.05])
      card.addSystematic("CMS_scale_MET_"+year,"param",[0.0,0.02])
      card.addSystematic("CMS_res_MET_"+year,"param",[0.0,0.01])

      card.addSystematic("CMS_LNuJ_bkg_res_"+year,"param",[0.0,0.333])
      card.addSystematic("CMS_LNuJ_bkg_scale_"+year,"param",[0.0,0.333])

      #pruned mass scale
      #card.addSystematic("CMS_scale_j","param",[0.0,0.02])
      #card.addSystematic("CMS_res_j","param",[0.0,0.05])

      #card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
      #card.addSystematic("CMS_res_MET","param",[0.0,0.01])

      card.addSystematic("CMS_scale_lepton_"+year,"param",[0.0,0.004])

      card.makeCard()

      cmd='text2workspace.py datacard_{tag}.txt -o datacard_final_{tag}.root'.format(tag=card.tag)
      os.system(cmd)
'''

#card=DataCardMaker('VBF_Radion_mu_HP_2016','NP','13TeV',35900,'nob')
#Signal
#sig="XWW_"+mass
#card.addHistoShapeFromFile(sig,["MLNuJ"],"LNuJJ_combined.root",sig,[],False,0)
#card.addFixedYieldFromFile(sig,0,"LNuJJ_combined.root",sig)

#card.addMVVSignalParametricShape("XWW","MLNuJ","LNuJJ_Radion_MVV_mu_HP_2016.json",{'CMS_scale_j':1,'CMS_scale_MET':1.0,'CMS_scale_lepton':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})
#card.addParametricYield("XWW",0,"LNuJJ_Radion_mu_HP_2016_yield.json",1,1.0)

#Background
#card.addMVVBackgroundShapeQCD("bkg","MLNuJ",False,"",{})
#card.addFloatingYield("bkg","1",188.05705)
#card.addConstrainedYield("bkg","MLNuJ",)

#fix:
#card.importBinnedData("LNuJJ_mu_HP_2016.root","data",["MLNuJ"])

#Scale and resolution uncertainties
#card.addSystematic("CMS_lumi","lnN",{'XWW':1.026})

#card.addSystematic("CMS_scale_j","param",[0.0,0.02])
#card.addSystematic("CMS_res_j","param",[0.0,0.05])
#card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
#card.addSystematic("CMS_res_MET","param",[0.0,0.01])

#pruned mass scale
#card.addSystematic("CMS_scale_j","param",[0.0,0.02])
#card.addSystematic("CMS_res_j","param",[0.0,0.05])

#card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
#card.addSystematic("CMS_res_MET","param",[0.0,0.01])

#card.addSystematic("CMS_scale_lepton","param",[0.0,0.004])

#card.makeCard()
