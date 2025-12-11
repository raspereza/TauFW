import ROOT 
import math
from array import array
import numpy as np
import os
import TauFW.Fitter.MuTauFR.utils as utils

def DeclareHistos(baseNames):

    hists = {}

    for baseName in baseNames:
        for var in utils.lib_histos:
            nbins = utils.lib_histos[var][0]
            xmin = utils.lib_histos[var][1]
            xmax = utils.lib_histos[var][2]        
            xbins = utils.createBins(nbins,xmin,xmax)
            for sign in utils.os_labels:
                for dm in utils.dm_labels:
                    histname = '%s_%s_%s_%s'%(baseName,var,sign,dm)
                    hists[histname] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
                    if var=='m_vis':
                        for reg in utils.reg_labels:
                            for etabin in utils.etabins:
                                histname = '%s_%s_%s_%s_%s_%s'%(baseName,var,sign,dm,reg,etabin)
                                hists[histname] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
                                for sys in utils.sys_labels:
                                    histname = '%s_%s_%s_%s_%s_%s_%s'%(baseName,var,sign,dm,reg,etabin,sys)
                                    hists[histname] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
    return hists

class sampleMuTauFR:

    def __init__(self,era,channel,sample):
        self.processName = ''
        self.xsec = -1
        self.nevts = -1
        self.baseNames = []
        self.applyZptWeight = False
        self.applyTopWeight = False
        if sample in utils.data_samples[era]:
            self.isdata = True
            self.ismc = False
            self.processName = 'Data'
            self.baseNames = ['Data']
        elif sample in utils.mc_samples[era]:
            self.ismc = True
            self.isdata = False
            self.xsec = utils.mc_samples[era][sample][0]
            self.nevts = utils.mc_samples[era][sample][1]
            self.processName = utils.mc_samples[era][sample][2]
            self.baseNames = utils.mc_samples[era][sample][3]
        else:
            print('Unknown sample is specified %s'%(sample))
            exit()
            
        filename = utils.picoFolder[era] + "/" + era + "/" + self.processName + "/" + sample + "_" + channel + ".root"
        if not os.path.isfile(filename):
            print("")
            print('File %s is not found '%(filename))
            print('for specified era : %s'%(era))
            print('check if variable "picoFolder" in file utils.py is correctly set')
            print('or check naming of samples')
            print("")
            exit()
        self.sampleName = sample
        self.sampleFile = ROOT.TFile(filename,"READ")
        self.sampleTree = self.sampleFile.Get("tree")
        self.ZPtweightName = ''
        if self.processName=='TT':
            self.applyTopWeight = True
        if self.processName=='DY':
            self.applyZptWeight = True
            self.ZPtweightName = utils.zptweightName[era]

        self.split = True
        if len(self.baseNames)!=3:
            self.split = False
            
        self.norm = 1.0
        if self.isdata:
            self.norm = 1.0
        else:
            sumw = self.nevts
            if self.nevts<0:
                sumw = self.sampleFile.Get('cutflow').GetBinContent(16)
            lumi = utils.eraLumi[era]
            self.norm = self.xsec*lumi/sumw
        print('')
        print('%s : %s : %s : norm = %10.8f'%(era,self.processName,self.sampleName,self.norm))
        print('baseNames : ',self.baseNames,'  split : ',self.split)
        print('')
        
    def GetSampleName(self):
        return self.sampleName


    def GetEntries(self):
        nentries = self.sampleTree.GetEntries()
        return nentries
    
    def SetMuTauConfig(self,scaleFactor,**kwargs):
        print('Setting config for sample %s ->'%(self.sampleName))
        self.scaleFactor = scaleFactor
        self.momScale = kwargs.get('momScale',0.03)
        self.muonPtCut = kwargs.get('muonPtCut',26.)
        self.tauPtCut  = kwargs.get('tauPtCut',22.)
        self.muonEtaCut = kwargs.get('muonEtaCut',2.4)
        self.tauEtaCut = kwargs.get('tauEtaCut',2.5)
        self.muonIsoCut = kwargs.get('muonIsoCut',0.15)
        self.mtCut = kwargs.get('mtCut',40.)
        self.drCut = kwargs.get('drCut',0.5)
        self.antiJet = kwargs.get('antiJet',5)
        self.antiMu = kwargs.get('antiMu',1)
        self.antiE  = kwargs.get('antiE',2)        
        print("Setting cuts for Z->tau(mu)tau(h) selection")
        print("muonPtCut",self.muonPtCut)
        print("muonEtaCut",self.muonEtaCut)
        print("muonIsoCut",self.muonIsoCut)
        print("tauPtCut",self.tauPtCut)
        print("tauEtaCut",self.tauEtaCut)
        print("mtCut",self.mtCut)
        print("drCut",self.drCut)
        print("antiJet",self.antiJet)
        print("antiMu",self.antiMu)
        print("antiE",self.antiE)
        print('momScale',self.momScale)
        
    def CreateHistosMuTau(self,start,period):

        # accessing tree
        tree = self.sampleFile.Get("tree")

        # initialization
        scaleFactor = self.scaleFactor
        applyZptWeight = self.applyZptWeight
        applyTopWeight = self.applyTopWeight
        momScale = self.momScale
        ismc = self.ismc 
        isdata = self.isdata
        processName = self.processName
        split = self.split
        baseNames = self.baseNames
        
        # creating histograms 
        hists = DeclareHistos(baseNames)
        
        # floats
        genweight   = np.zeros(1,dtype='f')
        puweight    = np.zeros(1,dtype='f')
        trigweight  = np.zeros(1,dtype='f')
        idisoweight_1 = np.zeros(1,dtype='f')
        
        pt_1        = np.zeros(1,dtype='f')
        eta_1       = np.zeros(1,dtype='f')
        pt_2        = np.zeros(1,dtype='f')
        eta_2       = np.zeros(1,dtype='f')
        met         = np.zeros(1,dtype='f')
        mt_1        = np.zeros(1,dtype='f')
        iso_1       = np.zeros(1,dtype='f')
        dR_ll       = np.zeros(1,dtype='f')
        mcweight    = np.zeros(1,dtype='f')
        m_vis       = np.zeros(1,dtype='f')
        rawDeepTau2018v2p5VSe_2 = np.zeros(1,dtype='f')
        rawDeepTau2018v2p5VSmu_2 = np.zeros(1,dtype='f')
        rawDeepTau2018v2p5VSjet_2 = np.zeros(1,dtype='f')
        
        # booleans
        metfilter      = np.zeros(1,dtype='?')
        lepton_vetoes_notau = np.zeros(1,dtype='?')
        idDecayModeNewDMs_2 = np.zeros(1,dtype='?')
        idMedium_1 = np.zeros(1,dtype='?')
        
        # integers
        idDeepTau2018v2p5VSe_2   = np.zeros(1,dtype='i')
        idDeepTau2018v2p5VSmu_2  = np.zeros(1,dtype='i')
        idDeepTau2018v2p5VSjet_2 = np.zeros(1,dtype='i')
        dm_2                     = np.zeros(1,dtype='i')
        q_1                      = np.zeros(1,dtype='i')
        q_2                      = np.zeros(1,dtype='i')
        genmatch_2               = np.zeros(1,dtype='i')
        
        # branches -> 
        # floats
        tree.SetBranchAddress('m_vis',m_vis)
        tree.SetBranchAddress('met',met)
        tree.SetBranchAddress('mt_1',mt_1)
        tree.SetBranchAddress('pt_1',pt_1)
        tree.SetBranchAddress('pt_2',pt_2)
        tree.SetBranchAddress('eta_1',eta_1)
        tree.SetBranchAddress('eta_2',eta_2)
        tree.SetBranchAddress('iso_1',iso_1)
        tree.SetBranchAddress('dR_ll',dR_ll)

        if ismc:
            tree.SetBranchAddress('genweight',genweight)
            tree.SetBranchAddress('puweight',puweight)
            tree.SetBranchAddress('idisoweight_1',idisoweight_1)
            tree.SetBranchAddress('genmatch_2',genmatch_2)
            if applyZptWeight:
                tree.SetBranchAddress(self.ZPtweightName,mcweight)
            if applyTopWeight:
                tree.SetBranchAddress('ttptweight',mcweight)

        
        tree.SetBranchAddress('rawDeepTau2018v2p5VSe_2',rawDeepTau2018v2p5VSe_2)
        tree.SetBranchAddress('rawDeepTau2018v2p5VSmu_2',rawDeepTau2018v2p5VSmu_2)
        tree.SetBranchAddress('rawDeepTau2018v2p5VSjet_2',rawDeepTau2018v2p5VSjet_2)
        
        # integers
        tree.SetBranchAddress('idDeepTau2018v2p5VSe_2',idDeepTau2018v2p5VSe_2)
        tree.SetBranchAddress('idDeepTau2018v2p5VSmu_2',idDeepTau2018v2p5VSmu_2)
        tree.SetBranchAddress('idDeepTau2018v2p5VSjet_2',idDeepTau2018v2p5VSjet_2)
        tree.SetBranchAddress('dm_2',dm_2)
        tree.SetBranchAddress('q_1',q_1)
        tree.SetBranchAddress('q_2',q_2)
        
        # booleans
        tree.SetBranchAddress('metfilter',metfilter)
        tree.SetBranchAddress('lepton_vetoes_notau',lepton_vetoes_notau)
        tree.SetBranchAddress('idMedium_1',idMedium_1)

        nentries = tree.GetEntries()

        ev_start = 0
        ev_end = nentries
        if period>0:
            ev_start = start*period
            ev_end = min(nentries,(start+1)*period)
            if ev_start>nentries:
                exit()

        print('')
        print('starting entry',ev_start)
        print('ending entry',ev_end)
        print('')
        
        # run over entries
        for entry in range(ev_start,ev_end):
            tree.GetEntry(entry)

            if entry%100000==0: print('processes %1i out of %1i events'%(entry,nentries))
            
            # met filters, vetos
            if not metfilter[0]: continue
            if lepton_vetoes_notau[0]: continue
            if dR_ll[0]<self.drCut: continue
            if mt_1[0]>self.mtCut: continue

            if pt_1[0]<self.muonPtCut: continue
            if not idMedium_1[0]: continue
            if iso_1[0]>self.muonIsoCut: continue
            if math.fabs(eta_1[0])>self.muonEtaCut: continue

            if math.fabs(eta_2[0])>self.tauEtaCut: continue
            # cut on tau pT will be applied later

            # tau discriminator against e and mu and jet
            if idDeepTau2018v2p5VSe_2[0]<self.antiE: continue
            if idDeepTau2018v2p5VSjet_2[0]<self.antiJet: continue

            dmcut = dm_2[0]==0 or dm_2[0]==1 or dm_2[0]==10 or dm_2[0]==11
            if not dmcut: continue
            dm_flags = {}
            for dm in utils.dm_labels:
                dm_flags[dm] = False

            dm_flags['incl'] = True
            if dm_2[0]==0: dm_flags['DM0'] = True
            if dm_2[0]==1: dm_flags['DM1'] = True
            if dm_2[0]==0 or dm_2[0]==1: dm_flags['1prong'] = True
            if dm_2[0]==10 or dm_2[0]==11: dm_flags['3prong'] = True

            baseName = self.baseNames[0]
            if split:
                baseName = self.baseNames[2]
                if genmatch_2[0]==5:
                    baseName = self.baseNames[0]
                if genmatch_2[0]>=1 and genmatch_2[0]<=4:
                    baseName = self.baseNames[1]

#            print(self.baseNames)           
#            print(genmatch_2[0],baseName)
                    
            Weight = 1.0
            if ismc:
                Weight = genweight[0]*puweight[0]*idisoweight_1[0]/abs(genweight[0])
#                print(genweight[0],puweight[0],idisoweight_1[0])
#                print(Weight)
                if applyZptWeight or applyTopWeight:
                    Weight *= mcweight[0]
#                    print(applyZptWeight,applyTopWeight)
#                    print('mcweight ',mcweight[0])
                if scaleFactor!=None:
                    sf = 1
                    if genmatch_2[0]==2 or genmatch_2[0]==4:
                        sf = scaleFactor.getSF(eta_2[0],'muTauFR')
#                        print('muon fake SF %5.3f'%(sf))
                    if genmatch_2[0]==0:
                        sf = scaleFactor.getSF(eta_2[0],'jetTauFR')
#                        print('jet fake SF %5.3f'%(sf))
                    if genmatch_2[0]==5:
                        sf = scaleFactor.getSF(eta_2[0],'tauID')
#                        print('tauID SF %5.3f'%(sf))
                    Weight *= sf

            sign_label = 'ss'
            if (q_1[0]*q_2[0])<0:
                sign_label = 'os'

            if sign_label == 'ss':
                if scaleFactor!=None:
                    sf = scaleFactor.getSF(eta_2[0],'qcdNorm')
#                    print('QCD factor %5.3f'%(sf))
                    Weight *= sf
                
            reg_label = 'pass'
            if idDeepTau2018v2p5VSmu_2[0]<self.antiMu:
                reg_label = 'fail'

            eta_label = 'eta0p0to0p4'
            for etabin in utils.etabins:
                etamin = utils.etabins[etabin][0]
                etamax = utils.etabins[etabin][1]
                etacut = math.fabs(eta_2[0])>etamin and math.fabs(eta_2[0])<etamax
                if etacut: eta_label=etabin

#            print(eta_2[0],eta_label)

            if pt_2[0]>self.tauPtCut:
                for dm in dm_flags:
                    if dm_flags[dm]:
                        name = '%s_m_vis_%s_%s_%s_%s'%(baseName,sign_label,dm,reg_label,eta_label)
                        hists[name].Fill(m_vis[0],Weight)
                
            for sys in utils.sys_labels:
                pt2 = pt_2[0]*(1.0+momScale)
                mvis = m_vis[0]*(1.0+0.5*momScale)
                if sys=='down':
                    pt2 = pt_2[0]*(1.0-momScale)
                    mvis = m_vis[0]*(1.0-0.5*momScale)
                if pt2>self.tauPtCut:
                    for dm in dm_flags:
                        if dm_flags[dm]:
                            name = '%s_m_vis_%s_%s_%s_%s_%s'%(baseName,sign_label,dm,reg_label,eta_label,sys)
                            hists[name].Fill(mvis,Weight)

            if pt_2[0]<self.tauPtCut:
                continue
            
            name = '%s_rawDeepTau2018v2p5VSmu_2_%s_1prong'%(baseName,sign_label)
            if dm_flags['1prong'] : hists[name].Fill(rawDeepTau2018v2p5VSmu_2[0],Weight)
            
            if idDeepTau2018v2p5VSmu_2[0]<self.antiMu:
                continue
            
            variables = {}
            variables['mt_1'] = mt_1[0]
            variables['m_vis'] = m_vis[0]
            variables['met'] = met[0]
            variables['pt_1'] = pt_1[0]
            variables['pt_2'] = pt_2[0]
            variables['eta_1'] = eta_1[0]
            variables['eta_2'] = eta_2[0]
            variables['dm_2'] = dm_2[0]

            if pt_2[0]>self.tauPtCut:
                for variable in variables:
                    for dm in dm_flags:
                        if dm_flags[dm]:
                            name = '%s_%s_%s_%s'%(baseName,variable,sign_label,dm)
                            hists[name].Fill(variables[variable],Weight)
            
        for hist in hists:
            hists[hist].Scale(self.norm)
        return hists
