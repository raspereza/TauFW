#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Extract scale factors from RooT files with fit results 
import ROOT
import math
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
import TauFW.Fitter.MuTauFR.analysisMuTauFR as analysis
from array import array
import os
from TauFW.Plotter.plot.utils import ensuredir
from TauFW.Fitter.MuTauFR.procedures import ExtractScaleFactors

############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024','2025','UL2017','UL2016_preVFP','UL2016_postVFP'])
    parser.add_argument('-wpVsMu','--wpVsMu',dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsJet','--wpVsJet',dest='wpVsJet', default='Medium', choices=['Loose','Medium','Tight','VTight'])
    parser.add_argument('-wpVsE','--wpVsE',dest='wpVsE', default='VVLoose', choices=['VVLoose','Loose','Medium','Tight'])
    parser.add_argument('-dm','--dm',dest='dm', default='1prong', choices=['1prong'])
    args = parser.parse_args()
    
    ExtractScaleFactors(era=args.era,
                        wpVsMu=args.wpVsMu,
                        wpVsJet=args.wpVsJet,
                        wpVsE=args.wpVsE,
                        dm=args.dm,
                        coarse=True)
    
    ExtractScaleFactors(era=args.era,
                        wpVsMu=args.wpVsMu,
                        wpVsJet=args.wpVsJet,
                        wpVsE=args.wpVsE,
                        dm=args.dm,
                        coarse=False)
    
