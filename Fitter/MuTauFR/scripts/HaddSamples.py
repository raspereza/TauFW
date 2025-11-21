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
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024'])
    parser.add_argument('-c','--channel',dest='channel',default='mutau',choices=['mutau','mumu'])
    parser.add_argument('-wpVsJet','--wpVsJet', dest='wpVsJet', default='Medium', choices=['Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--wpVsMu', dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Tight'])
    parser.add_argument('-prong','--prong', dest='prong',type=int,default=1,choices=[0,1,3])
    parser.add_argument('-applySF','--applySF',dest='applySF',action='store_true')
    args = parser.parse_args()

    era = args.era
    channel = args.channel
    
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE

    prong=args.prong
    applySF = args.applySF

    suffix = f'{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE'
    if prong==1:
        suffix += '_1pr'
    if prong==3:
        suffix += '_3pr'
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
        
