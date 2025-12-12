#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
import ROOT
import math
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
import TauFW.Fitter.MuTauFR.analysisMuTauFR as analysis
from TauFW.Plotter.plot.utils import ensuredir
from array import array
import os
from CombineHarvester.CombineTools import ch
from TauFW.Fitter.MuTauFR.procedures import ExtractScaleFactors, RunFit, WriteDatacards, ExtractHistos 
        
############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024'])
    parser.add_argument('-wpVsJet','--wpVsJet', dest='wpVsJet', default='Medium', choices=['Loose','Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--wpVsMu', dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Loose','Medium','Tight'])
    parser.add_argument('-dm','--dm', dest='dm', default='1prong', choices=['1prong','DM0','DM1'])
    parser.add_argument('-runFit','--runFit',dest='runFit',action='store_true')
    parser.add_argument('-extractSF','--extractSF',dest='extractSF',action='store_true')
    
    args = parser.parse_args()

    var = 'm_vis'
    era = args.era
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE
    chan = 'mutau'
    dm = args.dm
    runFit = args.runFit
    extractSF = args.extractSF
    nbins = 9
    xmin = 50
    xmax = 140

    bins = {
        'pass': utils.createBins(nbins,xmin,xmax),
        'fail': utils.createBins(1,xmin,xmax)
    }

    cmssw_base = os.getenv('CMSSW_BASE')
    suffix = utils.defineSuffix(chan,era,wpVsJet,wpVsMu,wpVsE,False)
    rootfolder = utils.outputFolder+'/'+suffix
    outfolder = ensuredir(f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/datacards/{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE_{dm}')
    inputfileName = '%s/mutau.root'%(rootfolder)
    if os.path.isfile(inputfileName):
        print(f'Opening file {inputfileName}')
    else:
        print(f'File {inputfileName} does not exist')
        exit()
    inputfile = ROOT.TFile(inputfileName,'read')
    for etabin in utils.etabins:
        outputfileName = f'{outfolder}/{etabin}_inputs.root'
        outputfile = ROOT.TFile(outputfileName,'recreate')
        for region in ['pass','fail']:
            hists = ExtractHistos(inputfile,bins[region],dm=dm,etabin=etabin,region=region)
            outputfile.cd('')
            outputfile.mkdir(region)
            outputfile.cd(region)
            for hist in hists:
                utils.removeNegativeBins(hists[hist])
                hists[hist].Write(hist)
        outputfile.Close()
        print(f'Writing input file {outputfileName}')

    WriteDatacards(era=era,
                   wpVsMu=wpVsMu,
                   wpVsJet=wpVsJet,
                   wpVsE=wpVsE,
                   dm=dm)

    if runFit:
        RunFit(era=era,
               wpVsMu=wpVsMu,
               wpVsJet=wpVsJet,
               wpVsE=wpVsE,
               dm=dm)

    if extractSF:
        ExtractScaleFactors(era=era,
                            wpVsMu=wpVsMu,
                            wpVsJet=wpVsJet,
                            wpVsE=wpVsE,
                            dm=dm,
                            coarse=False)
        ExtractScaleFactors(era=era,
                            wpVsMu=wpVsMu,
                            wpVsJet=wpVsJet,
                            wpVsE=wpVsE,
                            dm=dm,
                            coarse=True)
