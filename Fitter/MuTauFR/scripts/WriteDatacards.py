#! /usr/bin/env python3
# Based on createinputs.py created by Izaak N.
# Stepan Zakharov 2023
# adapted by Alexei Raspereza for 2024
# Description: Create datacards for combine
import sys
from CombineHarvester.CombineTools import ch
from TauFW.Plotter.plot.utils import LOG#, STYLE, ensuredir, repkey, Var, Sel
import os
import math
from TauFW.common.tools.file import ensuredir
import TauFW.Fitter.MuTauFR.utils as utils
eta = ['0p0to0p9','0p9to1p2','1p2to2p1','2p1to2p5']

if __name__ == "__main__":
    from argparse import ArgumentParser
    argv = sys.argv
    description = """Create datacards for stat. inference"""
    parser = ArgumentParser(prog="createInputs",description=description,epilog="Good luck!")
    parser.add_argument('-e', '--era',dest='era',default='2024', help="set era")
    parser.add_argument('-wpVsE','--wpVsE',dest='wpVsE',default='VVLoose',choices=['VVLoose','Tight'])
    parser.add_argument('-wpVsMu','--wpVsMu',dest='wpVsMu',default='VLoose',choices=['VLoose','Tight'])
    parser.add_argument('-wpVsJet','--wpVsJet',dest='wpVsJet',default='Medium',choices=['Medium','Tight'])
    args = parser.parse_args()

    iwp = args.wpVsMu
    wp_vs_jet = args.wpVsJet
    wp_vs_e = args.wpVsE
    era = args.era
    print ('<<<<<<<<<<<<<< working point: ', iwp)
    cmssw_base = os.getenv('CMSSW_BASE')
    subfolder = f'{era}_{wp_vs_jet}VsJet_{iwp}VsMu_{wp_vs_e}VsE'
    path2files = f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/input/{subfolder}'
    path2cards = ensuredir(f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/datacards/{subfolder}'
    
    for ieta in eta:
        print('<<<<<<< eta range: ', ieta)
        #cb.SetFlag('workspaces-use-clone', True)
        cb = ch.CombineHarvester()
        mc_backgrounds = ['ZTT','ZJ','W','TTT','TTL','TTJ', 'VV']
        data_driven_backgrounds = ['QCD']
        backgrounds = mc_backgrounds + data_driven_backgrounds
        signals = ['ZL']
        categories = {
            'mutau_pass' : [( 1, 'pass' )],
            'mutau_fail' : [( 2, 'fail' )],
        }
        cb.AddObservations(['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'],              categories['mutau_pass']) # adding observed data
        cb.AddObservations(['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'],              categories['mutau_fail']) # adding observed data
        cb.AddProcesses(   ['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'], backgrounds, categories['mutau_pass'], False) # adding backgrounds
        cb.AddProcesses(   ['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'], backgrounds, categories['mutau_fail'], False) # adding backgrounds
        cb.AddProcesses(   ['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'], signals,     categories['mutau_pass'], True) # adding signals
        cb.AddProcesses(   ['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'], signals,     categories['mutau_fail'], True) # adding signals

        cb.cp().process(mc_backgrounds+signals).AddSyst(cb, 'lumi_2024',   'lnN', ch.SystMap()(1.026))
        cb.cp().process(mc_backgrounds+signals).AddSyst(cb, 'CMS_eff_mu',  'lnN', ch.SystMap()(1.02))
        cb.cp().process(['TTT','ZTT'])         .AddSyst(cb, 'CMS_eff_t',   'lnN', ch.SystMap()(1.10))
        cb.cp().process(['ZJ','TTJ','W'])      .AddSyst(cb, 'jet_to_tauFR','lnN', ch.SystMap()(1.30))
        cb.cp().process(['TTT','TTL','TTJ'])   .AddSyst(cb, 'xsec_top',    'lnN', ch.SystMap()(1.06))
        cb.cp().process(['VV'])                .AddSyst(cb, 'xsec_vv',     'lnN', ch.SystMap()(1.06))
        cb.cp().process(['ZL','ZTT','ZJ'])     .AddSyst(cb, 'xsec_zjets',  'lnN', ch.SystMap()(1.03))
        cb.cp().process(['W'])                 .AddSyst(cb, 'xsec_wjets',  'lnN', ch.SystMap()(1.08))
        cb.cp().process(['QCD'])               .AddSyst(cb, 'normQCD',     'lnN', ch.SystMap()(1.20))
#        cb.cp().process(['bkgd'])              .AddSyst(cb, 'normBKGD',    'lnN', ch.SystMap()(1.20))
        
        #        cb.cp().AddSyst(cb, 'norm_zmm', 'rateParam', ch.SystMap('process')(['ZL'],1.0)) #12.09.23 Stepan Zakharov    
        #        cb.cp().GetParameter('norm_zmm').set_range(0.5,6)
        
        cb.cp().AddSyst(cb, 'norm_ztt', 'rateParam', ch.SystMap('process')(['ZTT'],0.95)) #12.09.23 Stepan Zakharov This parameter was used to solve the problem with normalisation   
        cb.cp().GetParameter('norm_ztt').set_range(0.5,2.5)
        
        cb.cp().process(['ZTT','TTT'])              .AddSyst(cb, 'TES', 'shape', ch.SystMap()(1.0))
        cb.cp().process(['ZL','TTL'])               .AddSyst(cb, 'FES', 'shape', ch.SystMap()(1.0))
        #        cb.cp().process(['ZL'])                    .AddSyst(cb, 'shape_res', 'shape', ch.SystMap()(1.0))
        cb.cp().process(['ZL','TTL']).AddSyst(cb, 'SF_zmm_pass', 'rateParam', ch.SystMap('bin_id')([1],1.0))
        cb.cp().GetParameter('SF_zmm_pass').set_range(0.01,6)

        filepath = os.path.join(path2files,"mutauFR_%s_eta%s_inputs.root")%(era,ieta)
        print(filepath)
        processName = '$BIN/$PROCESS'
        systematicName = '%s$BIN/$PROCESS_$SYSTEMATIC'%(iwp)
        systematicName = '$BIN/$PROCESS_$SYSTEMATIC'
        cb.cp().backgrounds().ExtractShapes(filepath, processName, systematicName)
        cb.cp().signals().ExtractShapes(filepath, processName, systematicName)
        
        n_zmm_pass = cb.cp().bin_id([1]).process(['ZL']).GetRate()
        n_zmm_pass += cb.cp().bin_id([1]).process(['TTL']).GetRate()
        n_zmm_fail = cb.cp().bin_id([2]).process(['ZL']).GetRate()
        n_zmm_fail += cb.cp().bin_id([2]).process(['TTL']).GetRate()
        #       dn_zmm_pass = cb.cp().bin(['%s_pass'%(iwp)]).process(['ZL']).GetUncertainty()
        #       dn_zmm_fail = cb.cp().bin(['%s_fail'%(iwp)]).process(['ZL']).GetUncertainty()
        
        prefit_FR = n_zmm_pass / (n_zmm_pass + n_zmm_fail)
        #SF_zmm_fail_formula = "(@0-@1*{0})/(1-{0})".format(prefit_FR)
                
        #cb.cp().process(['ZL']).AddSyst(cb, 'SF_zmm_fail', 'rateParam', ch.SystMap('bin_id')([2],(SF_zmm_fail_formula, "norm_zmm,SF_zmm_pass")))
        
        ### Check of potential bug in the SF_fail region###
        SF_zmm_fail_formula = "(1-@0*{0})/(1-{0})".format(prefit_FR)
        cb.cp().process(['ZL','TTL']).AddSyst(cb, 'SF_zmm_fail', 'rateParam', ch.SystMap('bin_id')([2],(SF_zmm_fail_formula, "SF_zmm_pass")))
        ###################################################
        
        #cb.AddDatacardLineAtEnd("* autoMCStats 0")
        ch.SetStandardBinNames(cb, '$BIN')
        bbb = ch.BinByBinFactory()
        bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(True)
        bbb.MergeBinErrors(cb.cp().backgrounds())
        bbb.AddBinByBin(cb.cp().backgrounds(), cb)

        datacardPath = '%s/%s_eta%s.txt'%(path2cards,era,ieta)
        shapePath = '%s/%s_eta%s.root'%(path2cards,era,ieta)
        writer = ch.CardWriter(datacardPath,shapePath)
        writer.SetWildcardMasses([])
        writer.WriteCards('cmb', cb) # writing all datacards into one folder for combination
