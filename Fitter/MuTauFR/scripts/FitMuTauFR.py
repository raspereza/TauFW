#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Running fits
import ROOT
import math
from array import array
import os
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
import TauFW.Fitter.MuTauFR.analysisMuTauFR as analysis
import TauFW.Fitter.MuTauFR.TauScaleFactors as tauScaleFactor
from TauFW.Plotter.plot.utils import ensuredir

def RunFit(**kwargs):

    era = kwargs.get('era','2024')
    wpVsJet = kwargs.get('wpVsJet','Medium')
    wpVsMu = kwargs.get('wpVsMu','VLoose')
    wpVsE = kwargs.get('wpVsE','VVLoose')
    dm = kwargs.get('dm','1prong')

    cmssw_base = os.getenv('CMSSW_BASE') 

    basefolder = f'{cmssw_base}/src/TauFW/Fitter/MuTauFR'
    folder = f'{basefolder}/datacards/{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE_{dm}'
    if not os.path.isdir(folder):
        print('folder {folder} does not exist')
        print('quitting')
        exit()
        
    command = f'cd {folder} ; '
    for etabin in utils.etabins:
        command += f'combineTool.py -M T2W -o {etabin}_ws.root -i {etabin}.txt -m 90  ; ' 
        command += f'combineTool.py -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL -m 90 --robustHesse 1 -d {etabin}_ws.root --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 0 -v 2 ; '
        command += f'cp fitDiagnostics.Test.root {etabin}_fit.root ; '
    command += f'cd {basefolder}' 
    os.system(command)

        
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
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Tight'])
    parser.add_argument('-dm','--dm', dest='dm', choices=['1prong','DM0','DM1','3prong'])
    args = parser.parse_args()

    era = args.era    
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE
    dm = args.dm
    etabins
                        
    RunFit(era=era,
           wpVsMu=wpVsMu,
           wpVsJet=wpVsJet,
           wpVsE=wpVsE,
           dm=dm)

