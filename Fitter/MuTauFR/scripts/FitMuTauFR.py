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
from TauFW.Plotter.plot.utils import ensuredir
from TauFW.Fitter.MuTauFR.procedures import RunFit
        
############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024','2025','UL2017','UL2016_preVFP','UL2016_postVFP'])
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

