#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Extract scale factors from RooT files with fit results 
import ROOT
import math
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
import TauFW.Fitter.MuTauFR.analysisMuTauFR as analysis
from array import array
import os
from TauFW.Plotter.plot.utils import ensuredir

def ExtractScaleFactors(**kwargs):

    era = kwargs.get('era','2024')
    wpVsMu = kwargs.get('wpVsMu','VLoose')
    wpVsJet = kwargs.get('wpVsJet','Medium')
    wpVsE = kwargs.get('wpVsE','VVLoose')
    dm = kwargs.get('dm','1prong')
    
    cmssw_base = os.getenv('CMSSW_BASE')
    name = f'{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE_{dm}'
    cardsfolder = f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/datacards/{name}'
    print(f'{cardsfolder}')
    histfolder = ensuredir(f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/ScaleFactors')
    if not os.path.isdir(cardsfolder):
        print('folder %s does not exist'%(cardsfolder))
        print('create datacards for respective WPs and run fit on them')
        print('quitting')
        exit()

    nbins = 0
    y = 0
    bins = []
    for etabin in utils.etabins:
        x = utils.etabins[etabin][0]
        y = utils.etabins[etabin][1]
        bins.append(x)
        nbins += 1
    bins.append(y)
    
    muTauFR = []
    jetTauFR = []
    qcdNorm = []
    tauID = []
    ib = 1
    for etabin in utils.etabins:
        inputFitFileName = '%s/%s_fit.root'%(cardsfolder,etabin)
        if not os.path.isfile(inputFitFileName):
            print('No fit results are found for bin %s'%(etabin))
            print('Make sure that datacards are created and run fit')
            print('Quitting')
            exit()
        inputFitFile = ROOT.TFile(inputFitFileName,'read')
        fitResult = inputFitFile.Get('fit_s')
        pars = fitResult.floatParsFinal()
        norm = 1
        normE = 0.1
        rpass = 1.
        rpassE = 0.1
        jfake_n = 1.0
        jfakeE_n = 0.1
        normZtt = 1.0
        normZttE = 0.1
        qcd_n = 1.0
        qcdE_n = 0.1
        for par in pars:
            if par.GetName()=='r': 
                norm = par.getVal()
                normE = par.getError()
            if par.GetName()=='r_pass':
                rpass = par.getVal()
                rpassE = par.getError()
            if par.GetName()=='jet_to_tauFR':
                jfake_n = par.getVal()
                jfakeE_n = par.getError()
            if par.GetName()=='tauID':
                normZtt = par.getVal()
                normZttE = par.getError()
            if par.GetName()=='normQCD':
                qcd_n = par.getVal()
                qcdE_n = par.getError()
        mutauFR = norm*rpass
        mutauFRE = math.sqrt(norm*norm*rpassE*rpassE+rpass*rpass*normE*normE)
        jtauFR = 1.0 + 0.3*jfake_n
        jtauFRE = 0.3*jfakeE_n
        normQCD = 1.0 + 0.3*qcd_n
        normQCDE = 0.2*qcdE_n
        print('%s -> muTauFR=%5.3f+/-%5.3f jetTauFR=%5.3f+/-%5.3f ZTTnorm=%5.3f+/-%5.3f QCDnorm=%5.3f+/-%5.3f'
              %(etabin,mutauFR,mutauFRE,jtauFR,jtauFRE,normZtt,normZttE,normQCD,normQCDE))
        muTauFR.append((mutauFR,mutauFRE))
        jetTauFR.append((jtauFR,jtauFRE))
        tauID.append((normZtt,normZttE))
        qcdNorm.append((normQCD,normQCDE))
        inputFitFile.Close()

    histMuTauFR = ROOT.TH1D('muTauFR','',nbins,array('d',list(bins)))
    histJetTauFR = ROOT.TH1D('jetTauFR','',nbins,array('d',list(bins)))
    histTauID = ROOT.TH1D('tauID','',nbins,array('d',list(bins)))
    histQCDNorm = ROOT.TH1D('qcdNorm','',nbins,array('d',list(bins)))
    for ib in range(nbins):
        histMuTauFR.SetBinContent(ib+1,muTauFR[ib][0])
        histMuTauFR.SetBinError(ib+1,muTauFR[ib][1])
        histJetTauFR.SetBinContent(ib+1,jetTauFR[ib][0])
        histJetTauFR.SetBinError(ib+1,jetTauFR[ib][1])
        histTauID.SetBinContent(ib+1,tauID[ib][0])
        histTauID.SetBinError(ib+1,tauID[ib][1])
        histQCDNorm.SetBinContent(ib+1,qcdNorm[ib][0])
        histQCDNorm.SetBinError(ib+1,qcdNorm[ib][1])
        
    outputfileName = f'{histfolder}/{name}.root'
    outputFile = ROOT.TFile(outputfileName,'recreate')
    suffix = '%sVsJet_%sVsMu_%sVsE'%(wpVsJet,wpVsMu,wpVsE)
    outputFile.cd('')
    histMuTauFR.Write('muTauFR_%s'%(suffix))
    histJetTauFR.Write('jetTauFR_%s'%(suffix))
    histTauID.Write('tauID_%s'%(suffix))
    histQCDNorm.Write('qcdNorm_%s'%(suffix))
    outputFile.Close()



############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024'])
    parser.add_argument('-wpVsMu','--wpVsMu',dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsJet','--wpVsJet',dest='wpVsJet', default='Medium', choices=['Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE',dest='wpVsE', default='VVLoose', choices=['VVLoose','Loose','Medium','Tight'])
    parser.add_argument('-dm','--dm',dest='dm', default='1prong', choices=['1prong'])
    args = parser.parse_args()
    
#    ExtractScaleFactors(era=args.era,
#                        wpVsMu=args.wpVsMu,
#                        wpVsJet=args.wpVsJet,
#                        wpVsE=args.wpVsE,
#                        dm=args.dm)
    
