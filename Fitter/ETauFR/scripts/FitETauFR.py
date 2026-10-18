#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Running fits
import ROOT
import math
from array import array
import os
import TauFW.Fitter.ETauFR.utils as utils
import TauFW.Fitter.ETauFR.styles as styles
from TauFW.Plotter.plot.utils import ensuredir
from TauFW.Fitter.ETauFR.procedures import RunFit
        
############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2526', choices=['2024','2025','2526','UL2017','UL2016_preVFP','UL2016_postVFP'])
    parser.add_argument('-wpVsJet','--wpVsJet', dest='wpVsJet', default='Medium', choices=['Loose','Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--wpVsMu', dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Tight'])
    parser.add_argument('-dm','--dm', dest='dm', default='DM0', choices=['DM0','DM1','DM10','DM11'])
    parser.add_argument('-etabin','--etabin', dest='etabin', default='eta0p0to1p48', choices=['eta0p0to1p48','eta1p48to2p5'])
    parser.add_argument('-fes','--fes', dest='fes',action='store_true')
    args = parser.parse_args()

    era = args.era
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE
    dm = args.dm    
    etabin = args.etabin
    fes = args.fes
                        
    RunFit(era=era,
           wpVsMu=wpVsMu,
           wpVsJet=wpVsJet,
           wpVsE=wpVsE,
           dm=dm,
           etabin=etabin,
           fes=fes)

