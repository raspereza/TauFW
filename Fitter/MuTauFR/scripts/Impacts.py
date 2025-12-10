#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Computing impacts

import os

def RunImpacts(**kwargs):

    era = kwargs.get('era','2024')
    wpVsJet  = kwargs.get('wpVsJet','Medium')
    wpVsMuon = kwargs.get('wpVsJet','VLoose')
    wpVsE    = kwargs.get('wpVsJet','VVLoose')
    dm = kwargs.get('dm','1prong')
    eta = kwargs.get('eta','0p0to0p4')

    cmssw_base = os.getenv('CMSSW_BASE')
    folder = f'{cmssw_base}/src/Fitter/MuTauFR/datacards/{era}_{wpVsJet}_{wpVsMu}_{wpVsE}_{dm}'
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
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024'])
    parser.add_argument('-wpVsJet','--wpVsJet', dest='wpVsJet', default='Medium', choices=['Loose','Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--wpVsMu', dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Loose','Medium','Tight'])
    parser.add_argument('-dm','--dm', dest='dm', default='1prong', choices=['1prong','DM0','DM1'])
    parser.add_argument('-eta','--eta', dest='eta', default='0p0to0p4', choices=utils.etabins)

    RunImpacts(era=args.era,
               wpVsJet=args.wpVsJet,
               wpVsMu=args.wpVsMu,
               wpVsE=args.wpVsE,
               dm=args.dm,
               eta=args.eta)
