#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Computing impacts

import os
import TauFW.Fitter.MuTauFR.styles as styles
import TauFW.Fitter.MuTauFR.utils as utils

def RunImpacts(**kwargs):

    era = kwargs.get('era','2024')
    wpVsJet  = kwargs.get('wpVsJet','Medium')
    wpVsMu   = kwargs.get('wpVsMu','VLoose')
    wpVsE    = kwargs.get('wpVsE','VVLoose')
    dm = kwargs.get('dm','1prong')
    eta = kwargs.get('eta','eta0p0to0p4')

    cmssw_base = os.getenv('CMSSW_BASE')
    folder = f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/datacards/{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE_{dm}'
    if not os.path.isdir(folder):
        print(f'folder {folder} does not exist')
        print('quitting')
        exit()
    filename = f'{folder}/{eta}_ws.root'
    if not os.path.isfile(filename):
        print(f'file {folder}/{eta}_ws.root does not exist')
        print('quitting')
        exit()
    
    command = f'cd {folder} ; '
    command += f' combineTool.py -M Impacts -d {eta}_ws.root --redefineSignalPOIs r_pass --robustFit 1 --cminDefaultMinimizerTolerance 0.05 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 -m 90 --doInitialFit ; '
    command += f' combineTool.py -M Impacts -d {eta}_ws.root --redefineSignalPOIs r_pass --robustFit 1 --cminDefaultMinimizerTolerance 0.05 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 -m 90 --doFits ; '
    command += f' combineTool.py -M Impacts -d {eta}_ws.root --redefineSignalPOIs r_pass -m 90 -o impacts_{eta}.json ; '
    command += f' plotImpacts.py -i impacts_{eta}.json -o impacts_{eta} ; '
    command += ' cd - '
    os.system(command)

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024','2025','UL2017','UL2016_preVFP','UL2016_postVFP'])
    parser.add_argument('-wpVsJet','--wpVsJet', dest='wpVsJet', default='Medium', choices=['Loose','Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--wpVsMu', dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','VLoose','Loose','Medium','Tight'])
    parser.add_argument('-dm','--dm', dest='dm', default='1prong', choices=['1prong','DM0','DM1'])
    parser.add_argument('-eta','--eta', dest='eta', default='eta0p0to0p4', choices=utils.etabins)
    args = parser.parse_args()
    
    RunImpacts(era=args.era,
               wpVsJet=args.wpVsJet,
               wpVsMu=args.wpVsMu,
               wpVsE=args.wpVsE,
               dm=args.dm,
               eta=args.eta)
