#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Producer
import ROOT
import math
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
import TauFW.Fitter.MuTauFR.analysisMuTauFR as analysis
from TauFW.Plotter.plot.utils import ensuredir
from array import array
import os

def ExtractHistos(f,bins,**kwargs):

    region = kwargs.get('region','pass')
    etabin = kwargs.get('etabin','0p0to0p9')
    
    hists = {}
    procs = ['Data','ZTT','ZL','ZJ','TTT','TTL','TTJ','W','VV']
    for proc in procs:
        for sign in ['os','ss']:
            name = f'{proc}_m_vis_{sign}_{region}_{etabin}'
            outname = f'{proc}_{sign}'
            hists[outname] = utils.rebinHisto(f.Get(name),bins,'rebinned')
            for sys in ['up','down']:
                name = f'{proc}_m_vis_{sign}_{region}_{etabin}_{sys}'
                outname = f'{proc}_{sign}_{sys}'
                hists[outname] = utils.rebinHisto(f.Get(name),bins,'rebinned')

    hists_out = {}
    # observed data 
    hists_out['data_obs'] = hists['Data_os']
    # VV
    hists_out['VV'] = hists['VV_os']
    # W 
    hists_out['W'] = hists['W_os']
    # TT 
    hists_out['TTL'] = hists['TTL_os']
    hists_out['TTL_FESUp'] = hists['TTL_os_up']
    hists_out['TTL_FESDown'] = hists['TTL_os_down']
    # TTT
    hists_out['TTT'] = hists['TTT_os']
    hists_out['TTT_TESUp'] = hists['TTT_os_up']
    hists_out['TTT_TESDown'] = hists['TTT_os_down']
    # TTJ
    hists_out['TTJ'] = hists['TTJ_os']
    # ZL
    hists_out['ZL'] = hists['ZL_os']
    hists_out['ZL_FESUp'] = hists['ZL_os_up']
    hists_out['ZL_FESDown'] = hists['ZL_os_down']
    # ZTT
    hists_out['ZTT'] = hists['ZTT_os']
    hists_out['ZTT_TESUp'] = hists['ZTT_os_up']
    hists_out['ZTT_TESDown'] = hists['ZTT_os_down']
    # ZJ
    hists_out['ZJ'] = hists['ZJ_os']
    # QCD
    hists_out['QCD'] = hists['Data_ss']
    procs = ['ZTT','ZL','ZJ','TTT','TTL','TTJ','W','VV']
    for proc in procs:
        hists_out['QCD'].Add(hists_out['QCD'],hists[f'{proc}_ss'],1.,-1.)

    return hists_out
        
############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024'])
    parser.add_argument('-c', '--channel', dest='channel', default='mutau')
    parser.add_argument('-wpVsJet','--wpVsJet', dest='wpVsJet', default='Medium', choices=['Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--wpVsMu', dest='wpVsMu', default='VLoose', choices=['VLoose','Tight'])
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Tight'])
    parser.add_argument('-prong','--prong', dest='prong', type=int, default=1, choices=[0,1,3])
    
    args = parser.parse_args()

    var = 'm_vis'
    era = args.era
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE
    chan = args.channel
    prong = args.prong
    
    nbins = 9
    xmin = 50
    xmax = 140

    bins = {
        'pass': utils.createBins(nbins,xmin,xmax),
        'fail': utils.createBins(1,xmin,xmax)
    }

    cmssw_base = os.getenv('CMSSW_BASE')
    suffix = utils.defineSuffix(chan,era,wpVsJet,wpVsMu,wpVsE,prong,False)
    rootfolder = utils.outputFolder+'/'+suffix
    outfolder = ensuredir(f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/input/{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE')
    inputfileName = '%s/mutau.root'%(rootfolder)
    if os.path.isfile(inputfileName):
        print(f'Opening file {inputfileName}')
    else:
        print(f'File {inputfileName} does not exist')
        exit()
    inputfile = ROOT.TFile(inputfileName,'read')
    for etabin in utils.etabins:
        outputfileName = f'{outfolder}/mutauFR_{etabin}_inputs.root'
        outputfile = ROOT.TFile(outputfileName,'recreate')
        for region in ['pass','fail']:
            hists = ExtractHistos(inputfile,bins[region],etabin=etabin,region=region)
            outputfile.cd('')
            outputfile.mkdir(region)
            outputfile.cd(region)
            for hist in hists:
                if hists[hist].GetSumOfWeights()<1.0:
                    hists[hist].SetBinContent(2,1.0)
                    hists[hist].SetBinError(2,1.0)
                hists[hist].Write(hist)
        outputfile.Close()
        print(f'Writing file {outputfileName}')
