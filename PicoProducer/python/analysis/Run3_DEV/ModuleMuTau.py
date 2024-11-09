# Author: Andrea Cardini (Oct 2023)
# Description: Simple module to pre-select mutau events
import sys
import numpy as np
from TauFW.PicoProducer.analysis.TreeProducerMuTau import *
from TauFW.PicoProducer.analysis.ModuleTauPair import *
from TauFW.PicoProducer.analysis.utils import LeptonTauPair, loosestIso, idIso, matchgenvistau, matchtaujet, filtermutau
from TauFW.PicoProducer.corrections.MuonSFs import *
#from TauFW.PicoProducer.corrections.TrigObjMatcher import loadTriggerDataFromJSON, TrigObjMatcher
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool, TauESTool


class ModuleMuTau(ModuleTauPair):
  
  def __init__(self, fname, **kwargs):
    kwargs['channel'] = 'mutau'
    super(ModuleMuTau,self).__init__(fname,**kwargs)
    self.out = TreeProducerMuTau(fname,self)
    print("=====> ERA: ", self.era)
    print("=====> YEAR: ", self.year) 
    # TRIGGERS
    if self.year==2016:
      self.trigger    = lambda e: e.HLT_IsoMu22 or e.HLT_IsoMu22_eta2p1 or e.HLT_IsoTkMu22 or e.HLT_IsoTkMu22_eta2p1 #or e.HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1
      self.muonCutPt  = lambda e: 23
      self.muonCutEta = lambda e: 2.4 if e.HLT_IsoMu22 or e.HLT_IsoTkMu22 else 2.1
    elif self.year==2017:
      self.trigger    = lambda e: e.HLT_IsoMu24 or e.HLT_IsoMu27 #or e.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1
      self.muonCutPt  = lambda e: 25 if e.HLT_IsoMu24 else 28
      self.muonCutEta = lambda e: 2.4
    elif self.year==2018:
      self.trigger    = lambda e: e.HLT_IsoMu24 or e.HLT_IsoMu27#e.HLT_IsoMu27 #or e.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1
      self.muonCutPt  = lambda e: 25
      self.muonCutEta = lambda e: 2.4
    elif self.year==2022 or self.year==2023:
      self.trigger    = lambda e: e.HLT_IsoMu24 or e.HLT_IsoMu27#e.HLT_IsoMu27 #or e.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1
      self.muonCutPt  = lambda e: 26
      self.muonCutEta = lambda e: 2.4
    self.tauCutPt     = 20
    self.tauCutEta    = 2.5 # 2.3 DeepTau2p1 and 2.5 for DeepTau2p5
    
    # CORRECTIONS
    if self.ismc:
      self.muSFs   = MuonSFs(era=self.era,verb=self.verbosity) # muon id/iso/trigger SFs
    
    # CUTFLOW
    self.out.cutflow.addcut('none',         "no cut"                     )
    self.out.cutflow.addcut('trig',         "trigger"                    )
    self.out.cutflow.addcut('muon',         "muon"                       )
    self.out.cutflow.addcut('tau',          "tau"                        )
    self.out.cutflow.addcut('pair',         "pair"                       )
    #self.out.cutflow.addcut('muonveto',     "muon veto"                  )
    #self.out.cutflow.addcut('elecveto',     "electron veto"              )
    self.out.cutflow.addcut('lepvetoes',     "lep vetoes"              )
    self.out.cutflow.addcut('jetvetoes',     "jet vetoes"              )
    self.out.cutflow.addcut('weight',       "no cut, weighted", 15       )
    self.out.cutflow.addcut('weight_no0PU', "no cut, weighted, PU>0", 16 ) # use for normalization
    ## Important cutflow entries to make stitching with exclusive mutauh sample
    self.out.cutflow.addcut('weight_mutaufilter', "no cut, mutaufilter", 17 )    
    self.out.cutflow.addcut('weight_mutaufilter_NUP0orp4', "no cut, weighted, mutau, 0 or >4 jets", 18 )
    self.out.cutflow.addcut('weight_mutaufilter_NUP1', "no cut, weighted, mutau, 1 jet", 19 )
    self.out.cutflow.addcut('weight_mutaufilter_NUP2', "no cut, weighted, mutau, 2 jets", 20 )
    self.out.cutflow.addcut('weight_mutaufilter_NUP3', "no cut, weighted, mutau, 3 jets", 21 )
    self.out.cutflow.addcut('weight_mutaufilter_NUP4', "no cut, weighted, mutau, 4 jets", 22 )

  
  def beginJob(self):
    """Before processing any events or files."""
    super(ModuleMuTau,self).beginJob()
    print(">>> %-12s = %s"%('tauwp',      self.tauwp))
    print(">>> %-12s = %s"%('muonCutPt',  self.muonCutPt))
    print(">>> %-12s = %s"%('muonCutEta', self.muonCutEta))
    print(">>> %-12s = %s"%('tauCutPt',   self.tauCutPt))
    print(">>> %-12s = %s"%('tauCutEta',  self.tauCutEta))
    pass
    
  
  def analyze(self, event):
    """Process and pre-select events; fill branches and return True if the events passes,
    return False otherwise."""
    sys.stdout.flush()
    
    
    ##### NO CUT #####################################
    if not self.fillhists(event):
      return False
    
    
    ##### TRIGGER ####################################
    if not self.trigger(event):
      return False
    self.out.cutflow.fill('trig')
    
    
    ##### MUON #######################################
    muons = [ ]
    for muon in Collection(event,'Muon'):
      if muon.pt<self.muonCutPt(event): continue
      if abs(muon.eta)>self.muonCutEta(event): continue
      if abs(muon.dz)>0.2: continue
      if abs(muon.dxy)>0.045: continue
      if not muon.mediumId: continue
      if muon.pfRelIso04_all>0.50: continue
      muons.append(muon)
    if len(muons)==0:
      return False
    self.out.cutflow.fill('muon')
    
    
    ##### TAU ########################################
    taus = [ ]
    for tau in Collection(event,'Tau'):
      if abs(tau.eta)>self.tauCutEta: continue
      if abs(tau.dz)>0.2: continue
      if tau.decayMode not in [0,1,10,11]: continue
      if abs(tau.charge)!=1: continue
      #id cuts v2p5
      if tau.idDeepTau2018v2p5VSe<1: continue # VVVLoose
      if tau.idDeepTau2018v2p5VSmu<1: continue # VLoose
      if tau.idDeepTau2018v2p5VSjet<1: continue # VVVLoose
      if self.ismc:
        tau.es   = 1 # store energy scale for propagating to MET
        genmatch = tau.genPartFlav
        if genmatch==5: # real tau
          if self.tes!=None: # user-defined energy scale (for TES studies)
            tes = self.tes
          else: # (apply by default)
            tes = 1 #self.tesTool.getTES(tau.pt,tau.decayMode,unc=self.tessys)
          if tes!=1:
            tau.pt   *= tes
            tau.mass *= tes
            tau.es    = tes
        elif self.ltf and 0<genmatch<5: # lepton -> tau fake
          tau.pt   *= self.ltf
          tau.mass *= self.ltf
          tau.es    = self.ltf
        elif self.jtf!=1.0 and genmatch==0: # jet -> tau fake
          tau.pt   *= self.jtf
          tau.mass *= self.jtf
          tau.es    = self.jtf
      if tau.pt<self.tauCutPt: continue
      taus.append(tau)
    if len(taus)==0:
      return False
    self.out.cutflow.fill('tau')
    
    
    ##### MUTAU PAIR #################################
    ltaus = [ ]
    for muon in muons:
      for tau in taus:
        if tau.DeltaR(muon)<0.5: continue
        ltau = LeptonTauPair(muon,muon.pfRelIso04_all,tau,tau.rawDeepTau2018v2p5VSjet)
        ltaus.append(ltau)
    if len(ltaus)==0:
      return False
    muon, tau = max(ltaus).pair
    muon.tlv  = muon.p4()
    tau.tlv   = tau.p4()
    self.out.cutflow.fill('pair')
    
    
    # VETOS
    extramuon_veto, extraelec_veto, dilepton_veto = getlepvetoes(event,[ ],[muon],[tau],self.channel,era=self.era)
    self.out.extramuon_veto[0], self.out.extraelec_veto[0], self.out.dilepton_veto[0] = getlepvetoes(event,[ ],[muon],[ ],self.channel,era=self.era)
    self.out.lepton_vetoes[0]       = self.out.extramuon_veto[0] or self.out.extraelec_veto[0] or self.out.dilepton_veto[0]
    self.out.lepton_vetoes_notau[0] = extramuon_veto or extraelec_veto or dilepton_veto
    

    #cutflow on veto
    if self.out.lepton_vetoes[0] and self.out.lepton_vetoes_notau[0]: return False
    self.out.cutflow.fill('lepvetoes')

    if self.jetveto(event): return False
    self.out.cutflow.fill('jetvetoes')
   
 
    # EVENT
    self.fillEventBranches(event)
    
    
    # MUON
    self.out.pt_1[0]                       = muon.pt
    self.out.eta_1[0]                      = muon.eta
    self.out.phi_1[0]                      = muon.phi
    self.out.m_1[0]                        = muon.mass
    self.out.y_1[0]                        = muon.tlv.Rapidity()
    self.out.dxy_1[0]                      = muon.dxy
    self.out.dz_1[0]                       = muon.dz
    self.out.q_1[0]                        = muon.charge
    self.out.iso_1[0]                      = muon.pfRelIso04_all
    #self.out.tkRelIso_1[0]                 = muon.tkRelIso
    self.out.idMedium_1[0]                 = muon.mediumId
    self.out.idTight_1[0]                  = muon.tightId
    self.out.idHighPt_1[0]                 = muon.highPtId
    
    # TAU
    self.out.pt_2[0]                       = tau.pt
    self.out.eta_2[0]                      = tau.eta
    self.out.phi_2[0]                      = tau.phi
    self.out.m_2[0]                        = tau.mass
    self.out.y_2[0]                        = tau.tlv.Rapidity()
    self.out.dxy_2[0]                      = tau.dxy
    self.out.dz_2[0]                       = tau.dz
    self.out.q_2[0]                        = tau.charge
    self.out.dm_2[0]                       = tau.decayMode
    self.out.iso_2[0]                      = tau.rawIso
    self.out.rawDeepTau2017v2p1VSe_2[0]    = tau.rawDeepTau2017v2p1VSe
    self.out.rawDeepTau2017v2p1VSmu_2[0]   = tau.rawDeepTau2017v2p1VSmu
    self.out.rawDeepTau2017v2p1VSjet_2[0]  = tau.rawDeepTau2017v2p1VSjet
    
    self.out.rawDeepTau2018v2p5VSe_2[0]    = tau.rawDeepTau2018v2p5VSe
    self.out.rawDeepTau2018v2p5VSmu_2[0]   = tau.rawDeepTau2018v2p5VSmu
    self.out.rawDeepTau2018v2p5VSjet_2[0]  = tau.rawDeepTau2018v2p5VSjet

    self.out.idDecayMode_2[0]              = tau.idDecayMode
    self.out.idDecayModeNewDMs_2[0]        = tau.idDecayModeNewDMs
    self.out.idDeepTau2017v2p1VSe_2[0]     = tau.idDeepTau2017v2p1VSe
    self.out.idDeepTau2017v2p1VSmu_2[0]    = tau.idDeepTau2017v2p1VSmu
    self.out.idDeepTau2017v2p1VSjet_2[0]   = tau.idDeepTau2017v2p1VSjet

    self.out.idDeepTau2018v2p5VSe_2[0]     = tau.idDeepTau2018v2p5VSe
    self.out.idDeepTau2018v2p5VSmu_2[0]    = tau.idDeepTau2018v2p5VSmu
    self.out.idDeepTau2018v2p5VSjet_2[0]   = tau.idDeepTau2018v2p5VSjet

    
    # GENERATOR
    if self.ismc:
      self.out.genmatch_1[0]     = muon.genPartFlav
      self.out.genmatch_2[0]     = tau.genPartFlav
      pt, eta, phi, status       = matchgenvistau(event,tau)
      self.out.genvistaupt_2[0]  = pt
      self.out.genvistaueta_2[0] = eta
      self.out.genvistauphi_2[0] = phi
      self.out.gendm_2[0]        = status
      if self.dozpt:
        self.out.mutaufilter[0]  = filtermutau(event)
    
    # JETS
    jets, met, njets_vars, met_vars = self.fillJetBranches(event,muon,tau)

    if self.ismc:
      self.out.jpt_match_2[0], self.out.jpt_genmatch_2[0] = matchtaujet(event,tau,self.ismc)
    else:
      self.out.jpt_match_2[0] = matchtaujet(event,tau,self.ismc)[0]
    
    # WEIGHTS
    if self.ismc:
      self.fillCommonCorrBranches(event,jets,met,njets_vars,met_vars)
      if muon.pfRelIso04_all<0.50 and tau.idDeepTau2018v2p5VSjet>=2:
         self.btagTool.fillEffMaps(jets,usejec=self.dojec)
      
      # MUON WEIGHTS
      self.out.trigweight[0]          = self.muSFs.getTriggerSF(muon.pt,muon.eta) # assume leading muon was triggered on
      self.out.idisoweight_1[0]       = self.muSFs.getIdIsoSF(muon.pt,muon.eta)
      
      #print("eta: ", muon.eta)
      #print("pt: ",  muon.pt)
      ##print("idiso sf: ", self.out.idisoweight_1[0])
      ##print("trig sf: ", self.out.trigweight[0])
      #print("===>>> ID&ISO SF")
      #print("sf wo abs: ", self.muSFs.getIdIsoSF(muon.pt,muon.eta))
      #print("sf w abs: ", self.muSFs.getIdIsoSF(muon.pt,abs(muon.eta)))
      #print("===>>> TRIG SF")
      #print("sf wo abs: ", self.muSFs.getTriggerSF(muon.pt,muon.eta))
      #print("sf w abs: ", self.muSFs.getTriggerSF(muon.pt,abs(muon.eta)))

      # DEFAULTS
      self.out.idweight_2[0]          = 1.
      self.out.idweight_dm_2[0]       = 1.
      self.out.idweight_medium_2[0]   = 1.
      
      self.out.ltfweight_2[0]         = 1.
      if self.dosys:
        self.out.idweightUp_2[0]      = 1.
        self.out.idweightDown_2[0]    = 1.
        self.out.idweightUp_dm_2[0]   = 1.
        self.out.idweightDown_dm_2[0] = 1.
        self.out.ltfweightUp_2[0]     = 1.
        self.out.ltfweightDown_2[0]   = 1.
      
      # WEIGHTS

      self.out.weight[0]              = self.out.genweight[0]*self.out.puweight[0]*self.out.trigweight[0]*self.out.idisoweight_1[0] #*self.out.idisoweight_2[0]
    elif self.isembed:
      ###self.applyCommonEmbdedCorrections(event,jets,jetIds50,met,njets_vars,met_vars)
      self.out.genweight[0]           = event.genWeight
      self.out.trackweight[0]         = 0.975 if tau.decayMode==0 else 1.0247 if tau.decayMode==1 else 0.927 if tau.decayMode==10 else 0.974 if tau.decayMode==11 else 1.0
     
        
    # MET & DILEPTON VARIABLES
    self.fillMETAndDiLeptonBranches(event,muon,tau,met,met_vars)
    
    
    self.out.fill()
    return True
    
