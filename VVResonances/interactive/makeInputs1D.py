import ROOT
import os
import pdb
ROOT.gROOT.SetBatch(True)

cuts={}

cuts['common']='((HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)*(run>500) + (run<500)*lnujj_sf)*(Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>0&&Flag_badChargedHadronFilter&&Flag_badMuonFilter)'

lumi16=35920
lumi17=41530
lumi18=59740
lumiTotal=lumi16+lumi17+lumi18
lumiWeight2016="("+str(lumi16)+"/"+str(lumiTotal)+")"
lumiWeight2017="("+str(lumi17)+"/"+str(lumiTotal)+")"
lumiWeight2018="("+str(lumi18)+"/"+str(lumiTotal)+")"

cuts['common']=cuts['common']+'*((run>500) +(run<500)*((year==2016)*'+lumiWeight2016+'+(year==2017)*'+lumiWeight2017+'+(year==2018)*'+lumiWeight2018+'))'

cuts['mu']='(abs(lnujj_l1_l_pdgId)==13)'
cuts['e']='(abs(lnujj_l1_l_pdgId)==11)'
cuts['lep']='(abs(lnujj_l1_l_pdgId)==13||abs(lnujj_l1_l_pdgId)==11)'

Vtagger='(lnujj_l2_tau2/lnujj_l2_tau1-(-0.08)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt))'
thrHP='0.65'
thrLP='0.96'
cuts['HP']='('+Vtagger+'<'+thrHP+')'
cuts['LP']='('+thrHP+'<='+Vtagger+'&&'+Vtagger+'<'+thrLP+')'
cuts['allP']='('+cuts['HP']+'||'+cuts['LP']+')'
#cuts['HP']='(lnujj_l2_tau2/lnujj_l2_tau1<0.55)'
#cuts['LP']='(lnujj_l2_tau2/lnujj_l2_tau1>0.55&&lnujj_l2_tau2/lnujj_l2_tau1<0.75)'
#cuts['tau']='(lnujj_l2_tau2/lnujj_l2_tau1<0.75)'

cuts['nob']='(lnujj_nMediumBTags==0)*lnujj_btagWeight'
cuts['b']='(lnujj_nMediumBTags>0)*lnujj_btagWeight'

#cuts['SDWindow']='(lnujj_l2_softDrop_mass>65&&lnujj_l2_softDrop_mass<135)'
cuts['SDWindow']='(lnujj_l2_softDrop_mass>55&&lnujj_l2_softDrop_mass<140)'

cuts['SDMass']='(lnujj_l2_softDrop_mass>30)'
cuts['resMass']='(lnujj_LV_mass>600)'

cuts['dijet']='(lnujj_vbf_j1_pt>0&&lnujj_vbf_j2_pt>0)'

cuts['resW']='(lnujj_l2_mergedVTruth==1)'
cuts['nonRes']='(lnujj_l2_mergedVTruth==0)'

cuts['eta']='(abs(lnujj_vbf_j1_eta)>2&&abs(lnujj_vbf_j2_eta)>2)'
#cuts['eta']='((lnujj_vbf_j1_eta)*(lnujj_vbf_j2_eta)<0)' # Jordan's cut
cuts['deta']='(lnujj_vbfDEta>4)'
#cuts['mjj']='(lnujj_vbfMass>450)'
cuts['mjj']='(lnujj_vbfMass>500)'
#cuts['mjj']='(lnujj_vbfMass>550)'
#cuts['mjj']='(lnujj_vbfMass>600)'

cuts['control']='(lnujj_l2_softDrop_mass>=30&&lnujj_l2_softDrop_mass<=55)'
cuts['W']='(lnujj_l2_softDrop_mass>55&&lnujj_l2_softDrop_mass<85)'
cuts['Z']='(lnujj_l2_softDrop_mass>=85&&lnujj_l2_softDrop_mass<=105)'
cuts['H']='(lnujj_l2_softDrop_mass>105&&lnujj_l2_softDrop_mass<140)'
cuts['combined']='(lnujj_l2_softDrop_mass>55&&lnujj_l2_softDrop_mass<=105)'
#cuts['combined']='(lnujj_l2_softDrop_mass>55&&lnujj_l2_softDrop_mass<140)'

#jets=['control','W','Z','H','combined']
#jets=['W','Z','H','combined']
#jets=['control','W','Z','H']
#jets=['control']
#jets=['control','W','Z']
#jets=['control','combined']
#jets=['W','Z','H']
jets=['combined']
leptons=['e','mu','lep']
#leptons=['e','mu']
#leptons=['e']
#leptons=['lep']
#purities=['HP','LP','allP']
purities=['HP','LP']
#purities=['allP']
#purities=['HP']
#categories=['nob']
categories=['b']

WWTemplate="BulkGravToWWToWlepWhad_narrow"
BRWW=2.*0.327*0.6760

VBFWWMasses=['1000','1200','1400','1600','1800','2000','2500','3000','3500','4000','4500']
VBFWWMassesTemplate={}
for mass in VBFWWMasses:
  VBFWWMassesTemplate[mass]="VBF_RadionToWW_narrow_"+mass

VBFWWTemplate="VBF_RadionToWW_narrow"
BRVBFWW=1.0

BRVBFWZ=1.0

WZTemplate="WprimeToWZToWlepZhad_narrow"
BRWZ=0.327*0.6991

WHTemplate="WprimeToWhToWlephbb"
#BRWH=0.59*0.327
BRWH=0.327

dataTemplate='ntuples2016/SingleElectron,ntuples2017/SingleElectron,ntuples2018/EGamma,ntuples2016/SingleMuon,ntuples2017/SingleMuon,ntuples2018/SingleMuon,ntuples2016/MET,ntuples2017/MET,ntuples2018/MET'
#dataTemplate='SingleMuon,SingleElectron,MET'
#resWTemplate="TT_pow,WWTo1L1Nu2Q"
#resWMJJTemplate="TT_pow,WWTo1L1Nu2Q"
#resZTemplate="WZTo1L1Nu2Q"

nonResTemplate='ntuples2016/TT_pow,ntuples2017/TTHad_pow,ntuples2017/TTLep_pow,ntuples2017/TTSemi_pow,ntuples2018/TTHad_pow,ntuples2018/TTLep_pow,ntuples2018/TTSemi_pow,ntuples2016/WJetsToLNu_HT,ntuples2017/WJetsToLNu_HT,ntuples2018/WJetsToLNu_HT,ntuples2016/DYJetsToLL_M50_HT,ntuples2017/DYJetsToLL_M50_HT,ntuples2018/DYJetsToLL_M50_HT'
#nonResTemplate='WJetsToLNu_HT,TT_pow,DYJetsToLL_M50_HT'
#nonResTemplate='WJetsToLNu_HT,DYJetsToLL_M50_HT'
resWTemplate='ntuples2016/TT_pow,ntuples2017/TTHad_pow,ntuples2017/TTLep_pow,ntuples2017/TTSemi_pow,ntuples2018/TTHad_pow,ntuples2018/TTLep_pow,ntuples2018/TTSemi_pow,ntuples2016/WWToLNuQQ,ntuples2016/WZTo1L1Nu2Q,ntuples2017/WWToLNuQQ,ntuples2017/WZTo1L1Nu2Q,ntuples2018/WWToLNuQQ,ntuples2017/T_tW,ntuples2017/TBar_tW'
#resWTemplate2016='TT_pow,T_tWch,TBar_tWch,TBar_tWch,WWToLNuQQ,WZTo1L1Nu2Q'
#resWTemplate2017='T_tch,T_tW,TBar_tch,TBar_tW,TTHad_pow,TTLep_pow,TTSemi_pow,WWToLNuQQ,WZTo1L1Nu2Q'
#resWTemplate2018='T_tch,T_tWch,TBar_tch,TBar_tWch,TTLep_pow,TTSemi_pow,WWToLNuQQ'
#resWTemplate2016='TT_pow,T_tWch,TBar_tWch,TBar_tWch,WWToLNuQQ'
#resWTemplate2017='T_tch,T_tW,TBar_tch,TBar_tW,TTHad_pow,TTLep_pow,TTSemi_pow,WWToLNuQQ'
#resWTemplate2018='T_tch,T_tWch,TBar_tch,TBar_tWch,TTLep_pow,TTSemi_pow,WWToLNuQQ'

#bkgTemplate2016='TT_pow,T-tWch,TBar_tWch,TBar_tWch,WWToLNuQQ,WZTo1L1Nu2Q,WJetsToLNu_HT,DYJetsToLL_M50_HT'
#bkgTemplate2016='TT_pow,WWTo1L1Nu2Q,WJetsToLNu_HT,DYJetsToLL_M50_HT'
#bkgTemplate2017='T_tch,T_tW,TBar_tch,TBar_tW,TTHad_pow,TTLep_pow,TTSemi_pow,WWToLNuQQ,WZTo1L1Nu2Q,WJetsToLNu_HT,TT_pow,DYJetsToLL_M50_HT'
#bkgTemplate2018='T_tch,T_tWch,TBar_tch,TBar_tWch,TTLep_pow,TTSemi_pow,WWToLNuQQ,WJetsToLNu_HT,TT_pow,DYJetsToLL_M50_HT'

#radionTemplate='ntuples2016/VBF_RadionToWW_narrow,ntuples2017/VBF_RadionToWW_narrow,ntuples2018/VBF_RadionToWW_narrow'
WprimeTemplate='ntuples2017/VBF_WprimeToWZ_narrow,ntuples2018/VBF_WprimeToWZ_narrow'
#ZprimeTemplate='VBF_ZprimeToWW_narrow'
#bulkGravTemplate='VBF_BulkGravToWW_narrow'

minMJJ=30.0
maxMJJ=210.0

minMVV=800.0
#maxMVV=5000.0
#minMVV=600
#minMVV=400
maxMVV=7000

minMX=700
maxMX=8100

binsMJJ=90
#binsMVV=672
#binsMVV=168
binsMVV=200
#binsMVV=50
#binsMVV=8
#binsMVV=40

lumi=137190

cuts['acceptance']="(lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV}&&lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
cuts['acceptanceGEN']="(lnujj_l2_gen_softDrop_mass>{minMJJ}&&lnujj_l2_gen_softDrop_mass<{maxMJJ}&&lnujj_gen_partialMass>{minMVV}&&lnujj_gen_partialMass<{maxMVV})".format(minMJJ=25,maxMJJ=300,minMVV=700,maxMVV=10000)
#cuts['acceptanceGEN']="(lnujj_l2_gen_softDrop_mass>0&&lnujj_gen_partialMass>0)"

cuts['acceptanceGENMVV']="(lnujj_gen_partialMass>{minMVV}&&lnujj_gen_partialMass<{maxMVV})".format(minMVV=700,maxMVV=5000)
cuts['acceptanceGENMJJ']="(lnujj_l2_gen_softDrop_mass>{minMJJ}&&lnujj_l2_gen_softDrop_mass<{maxMJJ}&&lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV})".format(minMJJ=minMJJ-5,maxMJJ=maxMJJ+5,minMVV=minMVV,maxMVV=maxMVV)
cuts['acceptanceMJJ']="(lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMJJ=minMJJ,maxMJJ=maxMJJ)

def makeSignalShapesMVV(filename,template):
  for jet in jets:
    for lep in leptons:
      for pur in purities:
        cut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['nob'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])
        #cut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['nob'],cuts['dijet'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])
        rootFile=filename+'_MVV_'+lep+'_'+pur+'_'+jet+'.root'
        cmd='vvMakeSignalMVVShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "lnujj_LV_mass" ntuples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ)
        os.system(cmd)
        jsonFile=filename+'_MVV_'+lep+'_'+pur+'_'+jet+'.json'
        print 'Making JSON'
        cmd='vvMakeJSON.py  -o "{jsonFile}" -g "MEAN:pol1,SIGMA:pol1,ALPHA1:pol2,N1:pol0,ALPHA2:pol2,N2:pol0" -m 800 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
        os.system(cmd)

def makeSignalShapesMVVHist(filename,template):
    #cut='*'.join([cuts['common'],cuts['lep'],cuts['acceptanceMJJ']])
    cut='*'.join([cuts['common'],cuts['lep'],cuts['tau'],cuts['nob'],cuts['dijet'],cuts['SDWindow'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['acceptanceMJJ']])
    rootFile=filename+"_combined_MVV.root"
    cmd='vvMakeSignalMVVShapesHist.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -x {minMVV} -X {maxMVV} -b "{bins}" -S "0.03" -R "0.03" ntuples'.format(template=template,cut=cut,rootFile=rootFile,bins=binsMVV,minMVV=minMVV,maxMVV=maxMVV)
    os.system(cmd)

def makeSignalShapesMJJ(filename,template):
    for p in purities:
        cut='*'.join([cuts['common'],cuts[p]])
        rootFile=filename+"_MJJ_"+p+".root"
        doExp=1
        if p=='HP' or p=='NP':
            doExp=0
        cmd='vvMakeSignalMJJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -m {minMJJ} -M {maxMJJ} -e {doExp} -f "alpha:1.347" ntuples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ,doExp=doExp)
        os.system(cmd)
        jsonFile=filename+"_MJJ_"+p+".json"

        if p=='HP' or p=='NP':
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol4,sigma:pol4,alpha:pol3,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol0" -m 601 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
        else:
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol3,sigma:pol1,alpha:pol0,n:pol0,slope:pol1,f:laur4,alpha2:pol0,n2:pol0" -m 601 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)

        os.system(cmd)

def makeHiggsShapesMJJ(filename,template):
    for p in purities:
        cut='*'.join([cuts['common'],cuts[p]])
        rootFile=filename+"_MJJ_"+p+".root"
        doExp=1
        if p=='HP' or p=='NP':
            doExp=0
        cmd='vvMakeSignalMJJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -m {minMJJ} -M {maxMJJ} -e {doExp} -f "" ntuples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ,doExp=doExp)
        os.system(cmd)
        jsonFile=filename+"_MJJ_"+p+".json"

        if p=='HP' or p=='NP':
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol4,sigma:pol4,alpha:pol3,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol0" -m 601 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
        else:
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol3,sigma:pol1,alpha:pol0,n:pol0,slope:pol1,f:laur4,alpha2:pol0,n2:pol0" -m 601 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)

        os.system(cmd)

def makeSignalShapeParam(file,var):
  n=1

  for jet in jets:
    for lep in leptons:
      for pur in purities:
        rootFile=file+'_'+var+'_'+lep+'_'+pur+'_'+jet+'.json.root'

        if not os.path.isfile(rootFile):
          print 'Error in makeSignalShapeParam: file '+rootFile+' does not exist.'
          return

        '''
        if not os.path.isfile(fileW):
          print "Error in makeSignalShapeParam: file "+fileW+" does not exist."
          return
        if not os.path.isfile(fileZ):
          print "Error in makeSignalShapeParam: file "+fileZ+" does not exist."
          return
        if not os.path.isfile(fileH):
          print "Warning in makeSignalShapeParam: file "+fileH+" does not exist."
          n=2
        '''

        contribs=[
          (rootFile, ROOT.kOrange+2, 20, "X #rightarrow WW",)
          #(fileW, colorSignal['XWW'], 20, "X #rightarrow WW",),
          #(fileZ, colorSignal['XWZ'], 21, "X #rightarrow WZ",),
          #(fileH, colorSignal['XWH'], 22, "X #rightarrow WH",),
          ]

        f=[None]*n
        g=[None]*n
        func=[None]*n
        for j in range(n):
          f[j]=ROOT.TFile(contribs[j][0])

        paramsMJJ=[
          ("mean",  "#mu (GeV)",    70,  130, ),
          ("sigma", "#sigma (GeV)", 0,   18,  ),
          ("alpha", "#alpha",       0,   3,   ),
          ("alpha2","#alpha2",      0,   12,   ),
          ("slope", "slope",        -0.1,0.05,),
          ("f",     "f",            0,   1.5, ),
        ]
        paramsMVV=[
          ("MEAN",  "#mu (GeV)",    1000, 8000,),
          ("SIGMA", "#sigma (GeV)", 0,   400, ),
          ("ALPHA1","#alpha",       0,   8,   ),
          ("ALPHA2","#alpha2",      0,   8,   ),
          ("MEAN_0",  "#mu_{0} (GeV)",    700, 4500,),#
          ("MEAN_1",  "#mu_{1} (GeV)",    -1,  1,   ),#
          ("SIGMA_0", "#sigma_{0} (GeV)", 0,   400, ),#
          ("SIGMA_1", "#sigma_{1} (GeV)", -1,  1,   ),#
          #("N1", "n_{1}", 0, 10),#
          #("N2", "n_{2}", 0, 10),#
        ]

        params=[]
        if var=='MJJ':
          params=paramsMJJ
        elif var=='MVV':
          params=paramsMVV

        for i in range(len(params)):
          name=params[i][0]
          if not f[0].GetListOfKeys().Contains(name):
            continue

          c=ROOT.TCanvas("c_"+name)
          c.cd()
          frame=c.DrawFrame(minMX,params[i][2],maxMX,params[i][3])
          frame.GetXaxis().SetTitle("m_{X} (GeV)")
          frame.GetYaxis().SetTitle(params[i][1])
          l=ROOT.TLegend(0.6,0.8,0.9,0.95)
          l.SetBorderSize(0)
          l.SetFillStyle(0)

          notfound=False
          for j in range(n):
            g[j]=f[j].Get(name)
            g[j].SetName(name+str(j))
            g[j].SetMarkerColor(contribs[j][1])
            g[j].SetMarkerStyle(contribs[j][2])
            g[j].SetMarkerSize(0.8)
            g[j].SetLineColor(contribs[j][1])
            g[j].Draw("Psame")
            func[j]=f[j].Get(name)
            func[j].SetLineColor(contribs[j][1])
            func[j].Draw("lsame")
            l.AddEntry(g[j],contribs[j][3],"p")

          l.Draw()
          c.SaveAs("params/paramSignalShape_"+jet+"_"+lep+"_"+pur+"_"+year+"_"+name+".pdf")

def makeSignalYields(filename,template,branchingFraction,sfP={'HP':1.0,'LP':1.0}):
  for jet in jets:
    for lep in leptons:
      for pur in purities:
        cut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['nob'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])
        #cut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['nob'],cuts['dijet'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass']])
        yieldFile=filename+"_"+lep+"_"+pur+"_"+jet+"_yield"
        cmd='vvMakeSignalYields.py -s {template} -c "{cut}" -o {output} -V "lnujj_LV_mass" -m {minMVV} -M {maxMVV} -f "pol5" -b {BR} -x 950 ntuples'.format(template=template, cut=cut, output=yieldFile,minMVV=minMVV,maxMVV=maxMVV,BR=branchingFraction)
        os.system(cmd)

def makeBackgroundShapesMVVConditional(name,filename,template,addCut=""):
    #first parameterize detector response
    cut='*'.join([cuts['common'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
    resFile=filename+"_"+name+"_detectorResponse.root"
    cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_LV_mass,lnujj_l2_softDrop_mass"  -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt"  -b "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000"   ntuples'.format(rootFile=resFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name)
    os.system(cmd)


    for c in categories:
        if c=='vbf':
            pur=['NP']
            catcut=cuts['dijet']
        else:
            pur=['HP','LP']
            catcut=cuts[c]

        for p in pur:
            for l in leptons:
                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[p],catcut,cuts[l],cuts['acceptanceGEN']])
                else:
                    cut='*'.join([cuts['common'],cuts[p],catcut,cuts[l],addCut,cuts['acceptanceGEN']])
                rootFile=filename+"_"+name+"_COND2D_"+l+"_"+p+"_"+c+".root"
                cmd='vvMake2DTemplateWithKernels.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass"  -b {binsMVV} -B {binsMJJ} -x {minMVV} -X {maxMVV} -y {minMJJ} -Y {maxMJJ}  -r {res} ntuples'.format(rootFile=rootFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ)
                os.system(cmd)



def makeBackgroundShapesMJJKernel(name,filename,template,addCut=""):
    #first parameterize detector response
    cut='*'.join([cuts['common'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
    resFile=filename+"_"+name+"_detectorResponse.root"
    cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_LV_mass,lnujj_l2_softDrop_mass"  -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt"  -b "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000"   ntuples'.format(rootFile=resFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name)
    os.system(cmd)

    for c in categories:
        if c=='vbf':
            pur=['NP']
#            c='dijet'
        else:
            pur=['HP','LP']
        for p in pur:
            for l in leptons:
                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[p],cuts[c],cuts[l],cuts['acceptanceGENMJJ']])
                else:
                    cut='*'.join([cuts['common'],cuts[p],cuts[c],addCut,cuts[l],cuts['acceptanceGENMJJ']])
                rootFile=filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"
                cmd='vvMake1DTemplateWithKernels.py -H "y" -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_l2_gen_softDrop_mass"  -b {binsMJJ}  -x {minMJJ} -X {maxMJJ} -r {res} ntuples'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ)
                os.system(cmd)


def makeBackgroundShapesMJJSpline(name,filename,template,addCut=""):
    for c in categories:
        if c=='vbf':
            pur=['NP']
#            c='dijet'
        else:
            pur=['HP','LP']
        for p in pur:
            for l in leptons:
                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[p],cuts[c],cuts[l],cuts['acceptance']])
                else:
                    cut='*'.join([cuts['common'],cuts[p],cuts[c],addCut,cuts[l],cuts['acceptance']])
                rootFile=filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"
                cmd='vvMake1DTemplateSpline.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_l2_softDrop_mass"  -b {binsMJJ}  -x {minMJJ} -X {maxMJJ} -f 6 ntuples'.format(rootFile=rootFile,samples=template,cut=cut,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ)
                os.system(cmd)


def mergeBackgroundShapes(name,filename):
    #first parameterize detector response
    for c in categories:
        if c=='vbf':
            pur=['NP']
        else:
            pur=['HP','LP']
        for p in pur:
            for l in leptons:
                inputy=filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"
                inputx=filename+"_"+name+"_COND2D_"+l+"_"+p+"_"+c+".root"
                rootFile=filename+"_"+name+"_2D_"+l+"_"+p+"_"+c+".root"
                cmd='vvMergeHistosToPDF2D.py -i "{inputx}" -I "{inputy}" -o "{rootFile}" -s "Scale:ScaleX,PT:PTX,OPT:OPTX,PT2:PTX2,Res:ResX,TOP:TOPX" -S "PT:PTY,OPT:OPTY" -C "PT:PTBoth" '.format(rootFile=rootFile,inputx=inputx,inputy=inputy)
                os.system(cmd)

                os.system(cmd)


def makeBackgroundShapesMVV(name,filename,template,addCut='1'):
  #first parameterize detector response
  cut='*'.join([cuts['common'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
  resFile=filename+"_"+name+"_detectorResponse.root"
  cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_LV_mass,lnujj_l2_softDrop_mass"  -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt"  -b "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000"   ntuples'.format(rootFile=resFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name)
  os.system(cmd)

  for jet in jets:
    for lep in leptons:
      for pur in purities:
        cut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts['b'],cuts['dijet'],cuts[jet],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['acceptanceGENMVV'],addCut])
        rootFile=filename+"_"+name+"_MVV_"+lep+"_"+pur+"_"+jet+"_b.root"
        cmd='vvMake1DTemplateWithKernels.py -H "x" -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_gen_partialMass"  -b {binsMVV}  -x {minMVV} -X {maxMVV} -r {res} ntuples'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV)
        os.system(cmd)

def makeResWMJJShapes(name,filename,template,addCut=""):
    for p in purities:
        if p=='HP' or p=='NP':
            doExp=0
        else:
            doExp=1

        if addCut=='':
            cut='*'.join([cuts['common'],cuts[p],cuts['inc']])
        else:
            cut='*'.join([cuts['common'],cuts[p],cuts['inc'],addCut])

        mjjFile=filename+"_MJJ_"+name+"_"+p
        jsonFile=filename+"_XWW_MJJ_"+p+".json"
        cmd='vvMakeTopMJJConditionalShapesFromTruth.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -v "lnujj_LV_mass"  -b 20  -x {minMJJ} -X {maxMJJ} -e {doExp} -j {jsonFile} ntuples'.format(template=template,cut=cut,rootFile=mjjFile,minMJJ=minMJJ,maxMJJ=maxMJJ,doExp=doExp,jsonFile=jsonFile)
        os.system(cmd)
#        print 'NOT RUNNING FIT'
        jsonFile=filename+"_MJJ_"+name+"_"+p+".json"
        if doExp==0:
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol1,sigma:llog,alpha:pol3,n:pol0,alpha2:pol0,n2:pol0" -m 500 -M 2500  {rootFile}  '.format(jsonFile=jsonFile,rootFile=mjjFile+'.root')
        else:
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol1,sigma:llog,alpha:pol3,n:pol0,alpha2:pol0,n2:pol0,slope:pol0,f:pol0" -m 500 -M 2500  {rootFile}  '.format(jsonFile=jsonFile,rootFile=mjjFile+'.root')

        os.system(cmd)




def makeResTopMJJShapes(name,filename,template,addCut=""):
    for p in purities:
        if addCut=='':
            cut='*'.join([cuts['common'],cuts[p]])
        else:
            cut='*'.join([cuts['common'],cuts[p],addCut])

        mjjFile=filename+"_MJJ_"+name+"_"+p
        jsonFile=filename+"_MJJ_"+name+"_"+p+".json"

        if p in ['HP','NP']:
            cmd='vvMakeTopMJJMergedConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -v "lnujj_LV_mass"  -b 60  -x {minMJJ} -X {maxMJJ} -f "meanW:81.9752,sigmaW:9.10,sigmaTop:15.075,alphaW:1.3,alphaW2:1.17,alphaTop:0.622,alphaTop2:1.58" ntuples'.format(template=template,cut=cut,rootFile=mjjFile,minMJJ=minMJJ,maxMJJ=230)
            os.system(cmd)
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "meanW:pol0,sigmaW:pol0,meanTop:laur3,sigmaTop:pol0,alphaW:pol0,alphaTop:pol0,alphaW2:pol2,alphaTop2:pol0,n:pol0,f:laur5,f2:pol0,slope:pol0" -m 500 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=mjjFile+'.root')
            os.system(cmd)

        else:
            cmd='vvMakeTopMJJMergedConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -v "lnujj_LV_mass"  -b 60  -x {minMJJ} -X {maxMJJ} -f "meanW:77.045,sigmaW:8.6,sigmaTop:18.49,alphaTop2:1.069,alphaW2:0.768,alphaTop:0.524,slope:-0.0196,f2:0.952" -e 1 ntuples'.format(template=template,cut=cut,rootFile=mjjFile,minMJJ=minMJJ,maxMJJ=230)
            os.system(cmd)
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "meanW:pol0,sigmaW:pol0,meanTop:laur3,sigmaTop:pol0,alphaW:laur2,alphaTop:pol0,alphaW2:pol2,alphaTop2:pol0,n:pol0,f:laur5,f2:pol0,slope:pol0" -m 500 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=mjjFile+'.root')
            os.system(cmd)




def makeNormalizations(name,filename,template,data=0,addCut='1',factor=1):
  for jet in jets:
    for lep in leptons:
      for pur in purities:
        cut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['b'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass'],addCut])
        #cut='*'.join([cuts['common'],cuts[lep],cuts[pur],cuts[jet],cuts['nob'],cuts['dijet'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass'],addCut])
        rootFile=filename+"_"+lep+"_"+pur+"_"+jet+"_b.root"
        cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -b "{BINS},{bins}" -m "{MINI},{mini}" -M "{MAXI},{maxi}" -f {factor} -n "{name}"  ntuples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,bins=binsMJJ,MINI=minMVV,MAXI=maxMVV,mini=minMJJ,maxi=maxMJJ,factor=factor,name=name,data=data)
        os.system(cmd)

def makeNormalizationsCombined(name,filename,template,data=0,addCut='1',factor=1,smooth=0):
  for jet in jets:
    cut='*'.join([cuts['common'],cuts['lep'],cuts['tau'],cuts[jet],cuts['nob'],cuts['dijet'],cuts['eta'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass'],addCut])
    #cut='*'.join([cuts['common'],cuts['lep'],cuts['tau'],cuts[jet],cuts['nob'],cuts['dijet'],cuts['deta'],cuts['mjj'],cuts['SDMass'],cuts['resMass'],addCut])
    rootFile=filename+"_"+jet+".root"
    cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -b "{BINS},{bins}" -m "{MINI},{mini}" -M "{MAXI},{maxi}" -f {factor} -n "{name}" -S {smooth}  ntuples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,bins=binsMJJ,MINI=minMVV,MAXI=maxMVV,mini=minMJJ,maxi=maxMJJ,factor=factor,name=name,data=data,smooth=smooth)
    os.system(cmd)

def makeToyModels(fileName,histName,numToy,fileOut,scale=1):
  rootFile=ROOT.TFile(fileName,"OPEN")
  rndm=ROOT.TRandom3(68432)
  data=rootFile.Get(histName)
  dataBins=data.GetNbinsX()
  dataMin=data.GetXaxis().GetXmin()
  dataMax=data.GetXaxis().GetXmax()

  toys=[]
  for toyNum in xrange(0,numToy):
    toyName="toy"+str(toyNum)
    toy=ROOT.TH1D(toyName,toyName,dataBins,dataMin,dataMax)
    toy.FillRandom(data,rndm.Poisson(scale*data.Integral()))
    toys.append(toy)

  rootOut=ROOT.TFile(fileOut,"RECREATE")
  rootOut.cd()
  for toy in toys:
    toy.Write()
  rootOut.Close()

'''
makeSignalShapesMVV('LNuJJ_Radion',radionTemplate)
'''

makeSignalShapesMVV('LNuJJ_Wprime',WprimeTemplate)

'''
makeSignalYields("LNuJJ_Radion",radionTemplate,BRVBFWW,{'HP':1.03,'LP':0.95})
'''

makeSignalYields("LNuJJ_Wprime",WprimeTemplate,BRVBFWZ,{'HP':1.03,'LP':0.95})

'''
makeSignalShapeParam('debug/debug_LNuJJ_Radion','MVV')
'''

'''
makeBackgroundShapesMVV("resW","LNuJJ",resWTemplate,cuts['resW'])
makeBackgroundShapesMVV("nonRes","LNuJJ",nonResTemplate,cuts['nonRes'])

makeNormalizations("nonRes","LNuJJ",nonResTemplate,0,cuts['nonRes'],1.0)
makeNormalizations("resW","LNuJJ",resWTemplate,0,cuts['resW'],1.0)

makeNormalizations("data","LNuJJ",dataTemplate,1)
'''

###makeToyModels("LNuJJ_combined_2016.root","data",100,"LNuJJ_combined_toys.root")
