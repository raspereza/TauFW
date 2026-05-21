#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Collecting samples
import ROOT
import math
from array import array
import os
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
import TauFW.Fitter.MuTauFR.analysisMuTauFR as analysis
import TauFW.Fitter.MuTauFR.TauScaleFactors as tauScaleFactor
from TauFW.Plotter.plot.utils import ensuredir

############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2025', choices=['2024','2025','UL2017','UL2016_preVFP','UL2016_postVFP'])
    parser.add_argument('-wpVsJet','--wpVsJet', dest='wpVsJet', default='Medium', choices=['Loose','Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--wpVsMu', dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Tight'])
    parser.add_argument('-applySF','--applySF',dest='applySF',action='store_true')
    args = parser.parse_args()

    era = args.era
    channel = 'mutau'
    
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE

    applySF = args.applySF

    suffix = f'{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE'
    if applySF:
        suffix += '_SF'

    subfolder = f'mutau_{era}_{suffix}'   
    outputfolder = utils.outputFolder+'/'+subfolder
    if os.path.isdir(outputfolder):
        mergefileName = outputfolder+'/mutau.root'
        if os.path.isfile(mergefileName):
            print('removing old file %s'%(mergefileName))
            command = f'rm {mergefileName}'
            os.system(command)
        command = f'hadd {mergefileName} {outputfolder}/*.root'
        os.system(command)
    else:
        print(f'folder {outputfolder} does not exist...')
        print('check if you run the respective selection...')
        
