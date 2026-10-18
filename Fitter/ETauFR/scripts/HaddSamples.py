#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# e->tau FR SF measurement
# Collecting samples
import ROOT
import math
from array import array
import os
import TauFW.Fitter.ETauFR.utils as utils
import TauFW.Fitter.ETauFR.styles as styles
import TauFW.Fitter.ETauFR.analysisETauFR as analysis
import TauFW.Fitter.ETauFR.TauScaleFactors as tauScaleFactor
from TauFW.Plotter.plot.utils import ensuredir

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
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Tight'])
    parser.add_argument('-applySF','--applySF',dest='applySF',action='store_true')
    args = parser.parse_args()

    era = args.era
    channel = 'etau'
    
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE

    applySF = args.applySF

    suffix = f'{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE'
    if applySF:
        suffix += '_SF'

    subfolder = f'etau_{era}_{suffix}'   
    outputfolder = utils.outputFolder+'/'+subfolder
    if os.path.isdir(outputfolder):
        mergefileName = outputfolder+'/etau.root'
        if os.path.isfile(mergefileName):
            print('removing old file %s'%(mergefileName))
            command = f'rm {mergefileName}'
            os.system(command)
        command = f'hadd {mergefileName} {outputfolder}/*.root'
        os.system(command)
    else:
        print(f'folder {outputfolder} does not exist...')
        print('check if you run the respective selection...')
        
