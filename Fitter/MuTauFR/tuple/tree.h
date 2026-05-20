//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed May 20 15:02:32 2026 by ROOT version 6.30/07
// from TTree tree/tree
// found on file: root://eoscms.cern.ch//eos/cms/store/group/phys_tau/TauFW/pico2024/TES_variations/2025/DY/DYto2Mu_Bin-MLL-50to120_mumu.root
//////////////////////////////////////////////////////////

#ifndef tree_h
#define tree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class tree {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           run;
   Int_t           lumi;
   ULong64_t       evt;
   Int_t           npv;
   Int_t           npv_good;
   Float_t         rho;
   Bool_t          metfilter;
   Int_t           npu;
   Int_t           npu_true;
   Int_t           NUP;
   Float_t         weight;
   Float_t         genweight;
   Float_t         trigweight;
   Float_t         trigweightUp;
   Float_t         trigweightDown;
   Float_t         puweight;
   Float_t         puweightUp;
   Float_t         puweightDown;
   Float_t         zptweight;
   Float_t         zptweight_lo;
   Float_t         zptweight_nlo;
   Float_t         zptweight_nnlo;
   Float_t         ttptweight;
   Float_t         btagweight;
   Float_t         prefireweight;
   Float_t         prefireweightUp;
   Float_t         prefireweightDown;
   Int_t           njets;
   Int_t           njets50;
   Int_t           ncjets;
   Int_t           ncjets50;
   Int_t           nfjets;
   Int_t           nbtag;
   Float_t         jpt_1;
   Float_t         jeta_1;
   Float_t         jphi_1;
   Float_t         jdeepjet_1;
   Float_t         jpt_2;
   Float_t         jeta_2;
   Float_t         jphi_2;
   Float_t         jdeepjet_2;
   Float_t         bpt_1;
   Float_t         beta_1;
   Float_t         bpt_2;
   Float_t         beta_2;
   Float_t         met;
   Float_t         metphi;
   Float_t         genmet;
   Float_t         genmetphi;
   Float_t         mt_1;
   Float_t         mt_2;
   Float_t         m_vis;
   Float_t         pt_ll;
   Float_t         dR_ll;
   Float_t         dphi_ll;
   Float_t         deta_ll;
   Float_t         pzetavis;
   Float_t         pzetamiss;
   Float_t         dzeta;
   Float_t         chi;
   Bool_t          dilepton_veto;
   Bool_t          extraelec_veto;
   Bool_t          extramuon_veto;
   Bool_t          lepton_vetoes;
   Bool_t          lepton_vetoes_notau;
   Float_t         m_moth;
   Float_t         pt_moth;
   Float_t         pt_1;
   Float_t         eta_1;
   Float_t         phi_1;
   Float_t         m_1;
   Float_t         y_1;
   Float_t         dxy_1;
   Float_t         dz_1;
   Int_t           q_1;
   Float_t         iso_1;
   Bool_t          idMedium_1;
   Bool_t          idTight_1;
   Int_t           idHighPt_1;
   Float_t         pt_2;
   Float_t         eta_2;
   Float_t         phi_2;
   Float_t         m_2;
   Float_t         y_2;
   Float_t         dxy_2;
   Float_t         dz_2;
   Int_t           q_2;
   Float_t         iso_2;
   Bool_t          idMedium_2;
   Bool_t          idTight_2;
   Int_t           idHighPt_2;
   Float_t         pt_3;
   Float_t         eta_3;
   Float_t         m_3;
   Float_t         q_3;
   Float_t         dm_3;
   Int_t           iso_3;
   Int_t           idiso_3;
   Int_t           idDeepTau2017v2p1VSe_3;
   Int_t           idDeepTau2017v2p1VSmu_3;
   Int_t           idDeepTau2017v2p1VSjet_3;
   Int_t           idDeepTau2018v2p5VSe_3;
   Int_t           idDeepTau2018v2p5VSmu_3;
   Int_t           idDeepTau2018v2p5VSjet_3;
   Float_t         rawDeepTau2018v2p5VSe_3;
   Float_t         rawDeepTau2018v2p5VSmu_3;
   Float_t         rawDeepTau2018v2p5VSjet_3;
   Float_t         rawPNetVSe_3;
   Float_t         rawPNetVSjet_3;
   Float_t         rawPNetVSmu_3;
   Int_t           decayModePNet_3;
   Float_t         probDM0PNet_3;
   Float_t         probDM1PNet_3;
   Float_t         probDM2PNet_3;
   Float_t         probDM10PNet_3;
   Float_t         probDM11PNet_3;
   Float_t         ptCorrPNet_3;
   Float_t         qConfPNet_3;
   Int_t           jpt_match_3;
   Int_t           decayModeUParT_3;
   Float_t         rawUParTVSe_3;
   Float_t         rawUParTVSmu_3;
   Float_t         rawUParTVSjet_3;
   Float_t         probDM0UParT_3;
   Float_t         probDM1UParT_3;
   Float_t         probDM2UParT_3;
   Float_t         probDM10UParT_3;
   Float_t         probDM11UParT_3;
   Float_t         ptCorrUParT_3;
   Float_t         qConfUParT_3;
   Int_t           genmatch_1;
   Int_t           genmatch_2;
   Int_t           genmatch_3;
   Int_t           jpt_genmatch_3;
   Int_t           genPartFlav_3;
   Float_t         idisoweight_1;
   Float_t         idisoweight_2;
   Float16_t       puweight_2025_80p0;
   Float16_t       puweight_2025_72p3832;
   Float16_t       puweight_2025_69p2;
   Float16_t       puweight_2025_66p0168;
   Float16_t       puweight_2025_80p0_v2;
   Float16_t       puweight_2025_72p3832_v2;
   Float16_t       puweight_2025_69p2_v2;
   Float16_t       puweight_2025_66p0168_v2;
   Float_t         idisoweight_1_2025;
   Float_t         trigweight_2025;
   Float_t         idisoweight_2_2025;
   Float16_t       puweight_2025_80p0_v3;
   Float16_t       puweight_2025_72p3832_v3;
   Float16_t       puweight_2025_69p2_v3;
   Float16_t       puweight_2025_66p0168_v3;

   // List of branches
   TBranch        *b_run;   //!
   TBranch        *b_lumi;   //!
   TBranch        *b_evt;   //!
   TBranch        *b_npv;   //!
   TBranch        *b_npv_good;   //!
   TBranch        *b_rho;   //!
   TBranch        *b_metfilter;   //!
   TBranch        *b_npu;   //!
   TBranch        *b_npu_true;   //!
   TBranch        *b_NUP;   //!
   TBranch        *b_weight;   //!
   TBranch        *b_genweight;   //!
   TBranch        *b_trigweight;   //!
   TBranch        *b_trigweightUp;   //!
   TBranch        *b_trigweightDown;   //!
   TBranch        *b_puweight;   //!
   TBranch        *b_puweightUp;   //!
   TBranch        *b_puweightDown;   //!
   TBranch        *b_zptweight;   //!
   TBranch        *b_zptweight_lo;   //!
   TBranch        *b_zptweight_nlo;   //!
   TBranch        *b_zptweight_nnlo;   //!
   TBranch        *b_ttptweight;   //!
   TBranch        *b_btagweight;   //!
   TBranch        *b_prefireweight;   //!
   TBranch        *b_prefireweightUp;   //!
   TBranch        *b_prefireweightDown;   //!
   TBranch        *b_njets;   //!
   TBranch        *b_njets50;   //!
   TBranch        *b_ncjets;   //!
   TBranch        *b_ncjets50;   //!
   TBranch        *b_nfjets;   //!
   TBranch        *b_nbtag;   //!
   TBranch        *b_jpt_1;   //!
   TBranch        *b_jeta_1;   //!
   TBranch        *b_jphi_1;   //!
   TBranch        *b_jdeepjet_1;   //!
   TBranch        *b_jpt_2;   //!
   TBranch        *b_jeta_2;   //!
   TBranch        *b_jphi_2;   //!
   TBranch        *b_jdeepjet_2;   //!
   TBranch        *b_bpt_1;   //!
   TBranch        *b_beta_1;   //!
   TBranch        *b_bpt_2;   //!
   TBranch        *b_beta_2;   //!
   TBranch        *b_met;   //!
   TBranch        *b_metphi;   //!
   TBranch        *b_genmet;   //!
   TBranch        *b_genmetphi;   //!
   TBranch        *b_mt_1;   //!
   TBranch        *b_mt_2;   //!
   TBranch        *b_m_vis;   //!
   TBranch        *b_pt_ll;   //!
   TBranch        *b_dR_ll;   //!
   TBranch        *b_dphi_ll;   //!
   TBranch        *b_deta_ll;   //!
   TBranch        *b_pzetavis;   //!
   TBranch        *b_pzetamiss;   //!
   TBranch        *b_dzeta;   //!
   TBranch        *b_chi;   //!
   TBranch        *b_dilepton_veto;   //!
   TBranch        *b_extraelec_veto;   //!
   TBranch        *b_extramuon_veto;   //!
   TBranch        *b_lepton_vetoes;   //!
   TBranch        *b_lepton_vetoes_notau;   //!
   TBranch        *b_m_moth;   //!
   TBranch        *b_pt_moth;   //!
   TBranch        *b_pt_1;   //!
   TBranch        *b_eta_1;   //!
   TBranch        *b_phi_1;   //!
   TBranch        *b_m_1;   //!
   TBranch        *b_y_1;   //!
   TBranch        *b_dxy_1;   //!
   TBranch        *b_dz_1;   //!
   TBranch        *b_q_1;   //!
   TBranch        *b_iso_1;   //!
   TBranch        *b_idMedium_1;   //!
   TBranch        *b_idTight_1;   //!
   TBranch        *b_idHighPt_1;   //!
   TBranch        *b_pt_2;   //!
   TBranch        *b_eta_2;   //!
   TBranch        *b_phi_2;   //!
   TBranch        *b_m_2;   //!
   TBranch        *b_y_2;   //!
   TBranch        *b_dxy_2;   //!
   TBranch        *b_dz_2;   //!
   TBranch        *b_q_2;   //!
   TBranch        *b_iso_2;   //!
   TBranch        *b_idMedium_2;   //!
   TBranch        *b_idTight_2;   //!
   TBranch        *b_idHighPt_2;   //!
   TBranch        *b_pt_3;   //!
   TBranch        *b_eta_3;   //!
   TBranch        *b_m_3;   //!
   TBranch        *b_q_3;   //!
   TBranch        *b_dm_3;   //!
   TBranch        *b_iso_3;   //!
   TBranch        *b_idiso_3;   //!
   TBranch        *b_idDeepTau2017v2p1VSe_3;   //!
   TBranch        *b_idDeepTau2017v2p1VSmu_3;   //!
   TBranch        *b_idDeepTau2017v2p1VSjet_3;   //!
   TBranch        *b_idDeepTau2018v2p5VSe_3;   //!
   TBranch        *b_idDeepTau2018v2p5VSmu_3;   //!
   TBranch        *b_idDeepTau2018v2p5VSjet_3;   //!
   TBranch        *b_rawDeepTau2018v2p5VSe_3;   //!
   TBranch        *b_rawDeepTau2018v2p5VSmu_3;   //!
   TBranch        *b_rawDeepTau2018v2p5VSjet_3;   //!
   TBranch        *b_rawPNetVSe_3;   //!
   TBranch        *b_rawPNetVSjet_3;   //!
   TBranch        *b_rawPNetVSmu_3;   //!
   TBranch        *b_decayModePNet_3;   //!
   TBranch        *b_probDM0PNet_3;   //!
   TBranch        *b_probDM1PNet_3;   //!
   TBranch        *b_probDM2PNet_3;   //!
   TBranch        *b_probDM10PNet_3;   //!
   TBranch        *b_probDM11PNet_3;   //!
   TBranch        *b_ptCorrPNet_3;   //!
   TBranch        *b_qConfPNet_3;   //!
   TBranch        *b_jpt_match_3;   //!
   TBranch        *b_decayModeUParT_3;   //!
   TBranch        *b_rawUParTVSe_3;   //!
   TBranch        *b_rawUParTVSmu_3;   //!
   TBranch        *b_rawUParTVSjet_3;   //!
   TBranch        *b_probDM0UParT_3;   //!
   TBranch        *b_probDM1UParT_3;   //!
   TBranch        *b_probDM2UParT_3;   //!
   TBranch        *b_probDM10UParT_3;   //!
   TBranch        *b_probDM11UParT_3;   //!
   TBranch        *b_ptCorrUParT_3;   //!
   TBranch        *b_qConfUParT_3;   //!
   TBranch        *b_genmatch_1;   //!
   TBranch        *b_genmatch_2;   //!
   TBranch        *b_genmatch_3;   //!
   TBranch        *b_jpt_genmatch_3;   //!
   TBranch        *b_genPartFlav_3;   //!
   TBranch        *b_idisoweight_1;   //!
   TBranch        *b_idisoweight_2;   //!
   TBranch        *b_f;   //!
   TBranch        *b_f;   //!
   TBranch        *b_f;   //!
   TBranch        *b_f;   //!
   TBranch        *b_f;   //!
   TBranch        *b_f;   //!
   TBranch        *b_f;   //!
   TBranch        *b_f;   //!
   TBranch        *b_idisoweight_1_2025;   //!
   TBranch        *b_trigweight_2025;   //!
   TBranch        *b_idisoweight_2_2025;   //!
   TBranch        *b_f;   //!
   TBranch        *b_f;   //!
   TBranch        *b_f;   //!
   TBranch        *b_f;   //!

   tree(TTree *tree=0);
   virtual ~tree();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef tree_cxx
tree::tree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("root://eoscms.cern.ch//eos/cms/store/group/phys_tau/TauFW/pico2024/TES_variations/2025/DY/DYto2Mu_Bin-MLL-50to120_mumu.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("root://eoscms.cern.ch//eos/cms/store/group/phys_tau/TauFW/pico2024/TES_variations/2025/DY/DYto2Mu_Bin-MLL-50to120_mumu.root");
      }
      f->GetObject("tree",tree);

   }
   Init(tree);
}

tree::~tree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t tree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t tree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void tree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("lumi", &lumi, &b_lumi);
   fChain->SetBranchAddress("evt", &evt, &b_evt);
   fChain->SetBranchAddress("npv", &npv, &b_npv);
   fChain->SetBranchAddress("npv_good", &npv_good, &b_npv_good);
   fChain->SetBranchAddress("rho", &rho, &b_rho);
   fChain->SetBranchAddress("metfilter", &metfilter, &b_metfilter);
   fChain->SetBranchAddress("npu", &npu, &b_npu);
   fChain->SetBranchAddress("npu_true", &npu_true, &b_npu_true);
   fChain->SetBranchAddress("NUP", &NUP, &b_NUP);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   fChain->SetBranchAddress("genweight", &genweight, &b_genweight);
   fChain->SetBranchAddress("trigweight", &trigweight, &b_trigweight);
   fChain->SetBranchAddress("trigweightUp", &trigweightUp, &b_trigweightUp);
   fChain->SetBranchAddress("trigweightDown", &trigweightDown, &b_trigweightDown);
   fChain->SetBranchAddress("puweight", &puweight, &b_puweight);
   fChain->SetBranchAddress("puweightUp", &puweightUp, &b_puweightUp);
   fChain->SetBranchAddress("puweightDown", &puweightDown, &b_puweightDown);
   fChain->SetBranchAddress("zptweight", &zptweight, &b_zptweight);
   fChain->SetBranchAddress("zptweight_lo", &zptweight_lo, &b_zptweight_lo);
   fChain->SetBranchAddress("zptweight_nlo", &zptweight_nlo, &b_zptweight_nlo);
   fChain->SetBranchAddress("zptweight_nnlo", &zptweight_nnlo, &b_zptweight_nnlo);
   fChain->SetBranchAddress("ttptweight", &ttptweight, &b_ttptweight);
   fChain->SetBranchAddress("btagweight", &btagweight, &b_btagweight);
   fChain->SetBranchAddress("prefireweight", &prefireweight, &b_prefireweight);
   fChain->SetBranchAddress("prefireweightUp", &prefireweightUp, &b_prefireweightUp);
   fChain->SetBranchAddress("prefireweightDown", &prefireweightDown, &b_prefireweightDown);
   fChain->SetBranchAddress("njets", &njets, &b_njets);
   fChain->SetBranchAddress("njets50", &njets50, &b_njets50);
   fChain->SetBranchAddress("ncjets", &ncjets, &b_ncjets);
   fChain->SetBranchAddress("ncjets50", &ncjets50, &b_ncjets50);
   fChain->SetBranchAddress("nfjets", &nfjets, &b_nfjets);
   fChain->SetBranchAddress("nbtag", &nbtag, &b_nbtag);
   fChain->SetBranchAddress("jpt_1", &jpt_1, &b_jpt_1);
   fChain->SetBranchAddress("jeta_1", &jeta_1, &b_jeta_1);
   fChain->SetBranchAddress("jphi_1", &jphi_1, &b_jphi_1);
   fChain->SetBranchAddress("jdeepjet_1", &jdeepjet_1, &b_jdeepjet_1);
   fChain->SetBranchAddress("jpt_2", &jpt_2, &b_jpt_2);
   fChain->SetBranchAddress("jeta_2", &jeta_2, &b_jeta_2);
   fChain->SetBranchAddress("jphi_2", &jphi_2, &b_jphi_2);
   fChain->SetBranchAddress("jdeepjet_2", &jdeepjet_2, &b_jdeepjet_2);
   fChain->SetBranchAddress("bpt_1", &bpt_1, &b_bpt_1);
   fChain->SetBranchAddress("beta_1", &beta_1, &b_beta_1);
   fChain->SetBranchAddress("bpt_2", &bpt_2, &b_bpt_2);
   fChain->SetBranchAddress("beta_2", &beta_2, &b_beta_2);
   fChain->SetBranchAddress("met", &met, &b_met);
   fChain->SetBranchAddress("metphi", &metphi, &b_metphi);
   fChain->SetBranchAddress("genmet", &genmet, &b_genmet);
   fChain->SetBranchAddress("genmetphi", &genmetphi, &b_genmetphi);
   fChain->SetBranchAddress("mt_1", &mt_1, &b_mt_1);
   fChain->SetBranchAddress("mt_2", &mt_2, &b_mt_2);
   fChain->SetBranchAddress("m_vis", &m_vis, &b_m_vis);
   fChain->SetBranchAddress("pt_ll", &pt_ll, &b_pt_ll);
   fChain->SetBranchAddress("dR_ll", &dR_ll, &b_dR_ll);
   fChain->SetBranchAddress("dphi_ll", &dphi_ll, &b_dphi_ll);
   fChain->SetBranchAddress("deta_ll", &deta_ll, &b_deta_ll);
   fChain->SetBranchAddress("pzetavis", &pzetavis, &b_pzetavis);
   fChain->SetBranchAddress("pzetamiss", &pzetamiss, &b_pzetamiss);
   fChain->SetBranchAddress("dzeta", &dzeta, &b_dzeta);
   fChain->SetBranchAddress("chi", &chi, &b_chi);
   fChain->SetBranchAddress("dilepton_veto", &dilepton_veto, &b_dilepton_veto);
   fChain->SetBranchAddress("extraelec_veto", &extraelec_veto, &b_extraelec_veto);
   fChain->SetBranchAddress("extramuon_veto", &extramuon_veto, &b_extramuon_veto);
   fChain->SetBranchAddress("lepton_vetoes", &lepton_vetoes, &b_lepton_vetoes);
   fChain->SetBranchAddress("lepton_vetoes_notau", &lepton_vetoes_notau, &b_lepton_vetoes_notau);
   fChain->SetBranchAddress("m_moth", &m_moth, &b_m_moth);
   fChain->SetBranchAddress("pt_moth", &pt_moth, &b_pt_moth);
   fChain->SetBranchAddress("pt_1", &pt_1, &b_pt_1);
   fChain->SetBranchAddress("eta_1", &eta_1, &b_eta_1);
   fChain->SetBranchAddress("phi_1", &phi_1, &b_phi_1);
   fChain->SetBranchAddress("m_1", &m_1, &b_m_1);
   fChain->SetBranchAddress("y_1", &y_1, &b_y_1);
   fChain->SetBranchAddress("dxy_1", &dxy_1, &b_dxy_1);
   fChain->SetBranchAddress("dz_1", &dz_1, &b_dz_1);
   fChain->SetBranchAddress("q_1", &q_1, &b_q_1);
   fChain->SetBranchAddress("iso_1", &iso_1, &b_iso_1);
   fChain->SetBranchAddress("idMedium_1", &idMedium_1, &b_idMedium_1);
   fChain->SetBranchAddress("idTight_1", &idTight_1, &b_idTight_1);
   fChain->SetBranchAddress("idHighPt_1", &idHighPt_1, &b_idHighPt_1);
   fChain->SetBranchAddress("pt_2", &pt_2, &b_pt_2);
   fChain->SetBranchAddress("eta_2", &eta_2, &b_eta_2);
   fChain->SetBranchAddress("phi_2", &phi_2, &b_phi_2);
   fChain->SetBranchAddress("m_2", &m_2, &b_m_2);
   fChain->SetBranchAddress("y_2", &y_2, &b_y_2);
   fChain->SetBranchAddress("dxy_2", &dxy_2, &b_dxy_2);
   fChain->SetBranchAddress("dz_2", &dz_2, &b_dz_2);
   fChain->SetBranchAddress("q_2", &q_2, &b_q_2);
   fChain->SetBranchAddress("iso_2", &iso_2, &b_iso_2);
   fChain->SetBranchAddress("idMedium_2", &idMedium_2, &b_idMedium_2);
   fChain->SetBranchAddress("idTight_2", &idTight_2, &b_idTight_2);
   fChain->SetBranchAddress("idHighPt_2", &idHighPt_2, &b_idHighPt_2);
   fChain->SetBranchAddress("pt_3", &pt_3, &b_pt_3);
   fChain->SetBranchAddress("eta_3", &eta_3, &b_eta_3);
   fChain->SetBranchAddress("m_3", &m_3, &b_m_3);
   fChain->SetBranchAddress("q_3", &q_3, &b_q_3);
   fChain->SetBranchAddress("dm_3", &dm_3, &b_dm_3);
   fChain->SetBranchAddress("iso_3", &iso_3, &b_iso_3);
   fChain->SetBranchAddress("idiso_3", &idiso_3, &b_idiso_3);
   fChain->SetBranchAddress("idDeepTau2017v2p1VSe_3", &idDeepTau2017v2p1VSe_3, &b_idDeepTau2017v2p1VSe_3);
   fChain->SetBranchAddress("idDeepTau2017v2p1VSmu_3", &idDeepTau2017v2p1VSmu_3, &b_idDeepTau2017v2p1VSmu_3);
   fChain->SetBranchAddress("idDeepTau2017v2p1VSjet_3", &idDeepTau2017v2p1VSjet_3, &b_idDeepTau2017v2p1VSjet_3);
   fChain->SetBranchAddress("idDeepTau2018v2p5VSe_3", &idDeepTau2018v2p5VSe_3, &b_idDeepTau2018v2p5VSe_3);
   fChain->SetBranchAddress("idDeepTau2018v2p5VSmu_3", &idDeepTau2018v2p5VSmu_3, &b_idDeepTau2018v2p5VSmu_3);
   fChain->SetBranchAddress("idDeepTau2018v2p5VSjet_3", &idDeepTau2018v2p5VSjet_3, &b_idDeepTau2018v2p5VSjet_3);
   fChain->SetBranchAddress("rawDeepTau2018v2p5VSe_3", &rawDeepTau2018v2p5VSe_3, &b_rawDeepTau2018v2p5VSe_3);
   fChain->SetBranchAddress("rawDeepTau2018v2p5VSmu_3", &rawDeepTau2018v2p5VSmu_3, &b_rawDeepTau2018v2p5VSmu_3);
   fChain->SetBranchAddress("rawDeepTau2018v2p5VSjet_3", &rawDeepTau2018v2p5VSjet_3, &b_rawDeepTau2018v2p5VSjet_3);
   fChain->SetBranchAddress("rawPNetVSe_3", &rawPNetVSe_3, &b_rawPNetVSe_3);
   fChain->SetBranchAddress("rawPNetVSjet_3", &rawPNetVSjet_3, &b_rawPNetVSjet_3);
   fChain->SetBranchAddress("rawPNetVSmu_3", &rawPNetVSmu_3, &b_rawPNetVSmu_3);
   fChain->SetBranchAddress("decayModePNet_3", &decayModePNet_3, &b_decayModePNet_3);
   fChain->SetBranchAddress("probDM0PNet_3", &probDM0PNet_3, &b_probDM0PNet_3);
   fChain->SetBranchAddress("probDM1PNet_3", &probDM1PNet_3, &b_probDM1PNet_3);
   fChain->SetBranchAddress("probDM2PNet_3", &probDM2PNet_3, &b_probDM2PNet_3);
   fChain->SetBranchAddress("probDM10PNet_3", &probDM10PNet_3, &b_probDM10PNet_3);
   fChain->SetBranchAddress("probDM11PNet_3", &probDM11PNet_3, &b_probDM11PNet_3);
   fChain->SetBranchAddress("ptCorrPNet_3", &ptCorrPNet_3, &b_ptCorrPNet_3);
   fChain->SetBranchAddress("qConfPNet_3", &qConfPNet_3, &b_qConfPNet_3);
   fChain->SetBranchAddress("jpt_match_3", &jpt_match_3, &b_jpt_match_3);
   fChain->SetBranchAddress("decayModeUParT_3", &decayModeUParT_3, &b_decayModeUParT_3);
   fChain->SetBranchAddress("rawUParTVSe_3", &rawUParTVSe_3, &b_rawUParTVSe_3);
   fChain->SetBranchAddress("rawUParTVSmu_3", &rawUParTVSmu_3, &b_rawUParTVSmu_3);
   fChain->SetBranchAddress("rawUParTVSjet_3", &rawUParTVSjet_3, &b_rawUParTVSjet_3);
   fChain->SetBranchAddress("probDM0UParT_3", &probDM0UParT_3, &b_probDM0UParT_3);
   fChain->SetBranchAddress("probDM1UParT_3", &probDM1UParT_3, &b_probDM1UParT_3);
   fChain->SetBranchAddress("probDM2UParT_3", &probDM2UParT_3, &b_probDM2UParT_3);
   fChain->SetBranchAddress("probDM10UParT_3", &probDM10UParT_3, &b_probDM10UParT_3);
   fChain->SetBranchAddress("probDM11UParT_3", &probDM11UParT_3, &b_probDM11UParT_3);
   fChain->SetBranchAddress("ptCorrUParT_3", &ptCorrUParT_3, &b_ptCorrUParT_3);
   fChain->SetBranchAddress("qConfUParT_3", &qConfUParT_3, &b_qConfUParT_3);
   fChain->SetBranchAddress("genmatch_1", &genmatch_1, &b_genmatch_1);
   fChain->SetBranchAddress("genmatch_2", &genmatch_2, &b_genmatch_2);
   fChain->SetBranchAddress("genmatch_3", &genmatch_3, &b_genmatch_3);
   fChain->SetBranchAddress("jpt_genmatch_3", &jpt_genmatch_3, &b_jpt_genmatch_3);
   fChain->SetBranchAddress("genPartFlav_3", &genPartFlav_3, &b_genPartFlav_3);
   fChain->SetBranchAddress("idisoweight_1", &idisoweight_1, &b_idisoweight_1);
   fChain->SetBranchAddress("idisoweight_2", &idisoweight_2, &b_idisoweight_2);
   fChain->SetBranchAddress("puweight_2025_80p0", &puweight_2025_80p0, &b_f);
   fChain->SetBranchAddress("puweight_2025_72p3832", &puweight_2025_72p3832, &b_f);
   fChain->SetBranchAddress("puweight_2025_69p2", &puweight_2025_69p2, &b_f);
   fChain->SetBranchAddress("puweight_2025_66p0168", &puweight_2025_66p0168, &b_f);
   fChain->SetBranchAddress("puweight_2025_80p0_v2", &puweight_2025_80p0_v2, &b_f);
   fChain->SetBranchAddress("puweight_2025_72p3832_v2", &puweight_2025_72p3832_v2, &b_f);
   fChain->SetBranchAddress("puweight_2025_69p2_v2", &puweight_2025_69p2_v2, &b_f);
   fChain->SetBranchAddress("puweight_2025_66p0168_v2", &puweight_2025_66p0168_v2, &b_f);
   fChain->SetBranchAddress("idisoweight_1_2025", &idisoweight_1_2025, &b_idisoweight_1_2025);
   fChain->SetBranchAddress("trigweight_2025", &trigweight_2025, &b_trigweight_2025);
   fChain->SetBranchAddress("idisoweight_2_2025", &idisoweight_2_2025, &b_idisoweight_2_2025);
   fChain->SetBranchAddress("puweight_2025_80p0_v3", &puweight_2025_80p0_v3, &b_f);
   fChain->SetBranchAddress("puweight_2025_72p3832_v3", &puweight_2025_72p3832_v3, &b_f);
   fChain->SetBranchAddress("puweight_2025_69p2_v3", &puweight_2025_69p2_v3, &b_f);
   fChain->SetBranchAddress("puweight_2025_66p0168_v3", &puweight_2025_66p0168_v3, &b_f);
   Notify();
}

Bool_t tree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void tree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t tree::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef tree_cxx
