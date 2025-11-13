#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# plotting prefit and postfit distributions
import ROOT
import math
import TauPOG.MuTauFR.utils as utils
import TauPOG.MuTauFR.styles as styles
import TauPOG.MuTauFR.analysisMuTauFR as analysis
from array import array
import os
import CombineHarvester.CombineTools.ch as ch
from TauFW.common.tools.file import ensuredir
#################################
#     definition of cuts        #
#################################

etabins = ['eta0p0to0p9','eta0p9to1p2','eta1p2to2p1','eta2p1to2p5']
samplesToMerge = ['TTT','TTJ','VV','ST']

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024'])
    parser.add_argument('-wp_vs_jet','--wp_vs_jet', dest='wpVsJet', default='Medium', choices=['Medium','Tight','VTight'])
    parser.add_argument('-wp_vs_mu','--wp_vs_mu', dest='wpVsMu', default='VLoose', choices=['VLoose','Tight'])
    parser.add_argument('-wp_vs_e','--wp_vs_e', dest='wpVsEle', default='VVLoose', choices=['VVLoose','Tight'])
    args = parser.parse_args()

    era = args.era
    wp_vs_jet = args.wpVsJet
    wp_vs_mu  = args.wpVsMu
    wp_vs_e   = args.wpVsEle

    cmssw_base = os.getenv('CMSSW_BASE')
    basedir = '%s/src/TauFW/Fitter/MuTauFR'%(cmssw_base)
    olddir  = '%s/input/%sVsJet_%sVsMu_%sVsE'%(basedir,wp_vs_jet,wp_vs_mu,wp_vs_e)
    ensuredir('%s/input_update'%(basedir))
    newdir = ensuredir('%s/input_update/%sVsJet_%sVsMu_%sVsE'%(basedir,wp_vs_jet,wp_vs_mu,wp_vs_e))
    command = 'cp %s/*.root %s/'%(olddir,newdir)
    os.system(command)

    for etabin in etabins:
        filename = 'MuTauFR_m_vis_%s_mt-%s.inputs.root'%(etabin,era)
        inputCardsFileName = '%s/%s'%(newdir,filename)
        inputCardsFile = ROOT.TFile(inputCardsFileName,'update')
        folder = '%s_fail'%(wp_vs_mu)
        inputCardsFile.cd(folder)
        W = inputCardsFile.Get(folder+'/W')
        xW = W.GetBinContent(1)
        eW = W.GetBinError(1)
        xW += 1.0
        eW = math.sqrt(eW*eW+1.0)
        W.SetBinContent(1,xW)
        W.SetBinError(1,eW)
        bkgd = W.Clone('bkgd')
        bkgd.SetBinContent(1,0.)
        bkgd.SetBinError(1,0.)
        for sample in samplesToMerge:
            hist = inputCardsFile.Get(folder+'/'+sample)
            bkgd.Add(bkgd,hist)
        inputCardsFile.cd(folder)
        inputCardsFile.Write('W')
        inputCardsFile.Write('bkgd')
#        ROOT.gROOT.pwd()
#        inputCardsFile.Write('bkgd')
#        inputCardsFile.Write('W')

        inputCardsFile.Close()

