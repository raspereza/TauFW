#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# e->tau FR SF measurement
import ROOT
import math
import TauFW.Fitter.ETauFR.utils as utils
import TauFW.Fitter.ETauFR.styles as styles
import TauFW.Fitter.ETauFR.analysisETauFR as analysis
from TauFW.Plotter.plot.utils import ensuredir
from array import array
import os
from CombineHarvester.CombineTools import ch
from TauFW.Fitter.ETauFR.procedures import ExtractScaleFactors, RunFit, WriteDatacards, ExtractHistos 
        
############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2526', choices=['2025','2026','2526'])
    parser.add_argument('-wpVsJet','--wpVsJet', dest='wpVsJet', default='Medium', choices=['Loose','Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--wpVsMu', dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Loose','Medium','Tight'])
    parser.add_argument('-fes','--fes',dest='fes',action='store_true')
    parser.add_argument('-runFit','--runFit',dest='runFit',action='store_true')
    parser.add_argument('-extractSF','--extractSF',dest='extractSF',action='store_true')
    
    args = parser.parse_args()

    var = 'm_vis'
    era = args.era
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE
    chan = 'etau'
    runFit = args.runFit
    extractSF = args.extractSF
    nbins = 9
    xmin = 50
    xmax = 140
    fes = args.fes
    
    bins = {
        'pass': utils.createBins(nbins,xmin,xmax),
        'fail': utils.createBins(1,xmin,xmax)
    }

    cards_folder = 'datacards'
    if fes:
        cards_folder = 'datacards_fes'
    cmssw_base = os.getenv('CMSSW_BASE')
    suffix = utils.defineSuffix(chan,era,wpVsJet,wpVsMu,wpVsE,False)
    rootfolder = utils.outputFolder+'/'+suffix
    outfolder = ensuredir(f'{cmssw_base}/src/TauFW/Fitter/ETauFR/{cards_folder}/{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE')
    inputfileName = '%s/etau.root'%(rootfolder)
    if os.path.isfile(inputfileName):
        print(f'Opening file {inputfileName}')
    else:
        print(f'File {inputfileName} does not exist')
        exit()
    inputfile = ROOT.TFile(inputfileName,'read')
    for dm in utils.dm_meas:
        for etabin in utils.etabins:
            outputfileName = f'{outfolder}/{etabin}_{dm}_inputs.root'
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
                   fes=fes)

    if runFit:
        for etabin in utils.etabins:
            for dm in utils.dm_meas:
                RunFit(era=era,
                       wpVsMu=wpVsMu,
                       wpVsJet=wpVsJet,
                       wpVsE=wpVsE,
                       dm=dm,
                       etabin=etabin,
                       fes=fes)

    if extractSF:
        ExtractScaleFactors(era=era,
                            wpVsMu=wpVsMu,
                            wpVsJet=wpVsJet,
                            wpVsE=wpVsE)

