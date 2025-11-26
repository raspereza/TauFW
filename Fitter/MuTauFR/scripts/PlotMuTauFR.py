#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Plotting scale factors 
import ROOT
import math
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
import TauFW.Fitter.MuTauFR.analysisMuTauFR as analysis
from array import array
import os
from TauFW.Plotter.plot.utils import ensuredir

#################################
#     definition of cuts        #
#################################

etabins = [
    'eta0p0to0p9',
    'eta0p9to1p2',
    'eta1p2to2p1',
    'eta2p1to2p5']

colors = [ROOT.kBlack,ROOT.kRed,ROOT.kBlue,ROOT.kGreen]
markers = [20,21,22,23]

def Plot(hists,**kwargs):

    era = kwargs.get('era','2024')
    
    ymax = 0
    i = 0
    for hist in hists:
        hists[hist].GetYaxis().SetRangeUser(0.,2.5)
        styles.InitData(hists[hist])
        hists[hist].SetMarkerColor(colors[i])
        hists[hist].SetLineColor(colors[i])
        hists[hist].SetMarkerStyle(markers[i])
        i += 1
              
    # canvas and pads
    canvas = styles.MakeCanvas("canv","",600,600)

    isFirst = True
    for hist in hists:
        if isFirst:
            hists[hist].Draw('e1')
            isFirst = False
        else:
            hists[hist].Draw('e1same')
    
    leg = ROOT.TLegend(0.23,0.2,0.5,0.4)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.03)
    for hist in hists:
        leg.AddEntry(hists[hist],hist,'lp')
    leg.Draw()

    text = ROOT.TText(0.22,0.83,'%s'%(suffix))
    text.SetTextSize(0.045)
    text.SetNDC()
    text.Draw()
    
    styles.CMS_label(canvas,era=era)

    canvas.Modified()
    canvas.RedrawAxis()
    canvas.Update()
    print('')
    print('Creating SF plot')

    outfolder = ensuredir(utils.figuresFolder+'/ScaleFactors')
    canvas.Print('%s/SF_%s_%s.png'%(outfolder,era,suffix))

############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024'])
    parser.add_argument('-wpVsMu','--wpVsMu',dest='wpVsMu', nargs='+', default=['VLoose'], choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsJet','--wpVsJet',dest='wpVsJet', nargs='+', default=['Medium'], choices=['Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE',dest='wpVsE', nargs='+', default=['VVLoose'], choices=['VVLoose','Loose','Medium','Tight'])
    parser.add_argument('-discr','--discr',dest='discr',default='VsMu',choices=['VsMu','VsJet','VsE'])
    args = parser.parse_args()
    
    era = args.era
    wpVsJet = args.wpVsJet[0]
    wpVsE = args.wpVsE[0]
    wpVsMu = args.wpVsMu[0]
    suffix = ''
    if args.discr=='VsMu':
        wps = args.wpVsMu
        suffix = '%sVsJet_%sVsE'%(wpVsJet,wpVsE)
    elif args.discr=='VsJet':
        wps = args.wpVsJet
        suffix = '%sVsMu_%sVsE'%(wpVsMu,wpVsE)
    else:
        wps = args.wpVsE
        suffix = '%sVsJet_%sVsMu'%(wpVsJet,wpVsMu)
        
    print('')

    cmssw_base = os.getenv('CMSSW_BASE')
    filename = '%s/src/TauFW/Fitter/MuTauFR/ScaleFactors/%s_ScaleFactors.root'%(cmssw_base,era)
    if os.path.isfile(filename):
        print('opening file %s'%(filename))
    else:
        print('file %s is not found'%(filename))
        print('Extract and dump scale factors for all considered WPs to RooT files and merge all files for one era into one...')
        exit()

    inputFile = ROOT.TFile(filename,'READ')
    hists = {}
    for wp in wps:
        name = '%sVsJet_%sVsMu_%sVsE'%(wpVsJet,wp,wpVsE)
        if args.discr=='VsJet':
            name = '%sVsJet_%sVsMu_%sVsE'%(wp,wpVsMu,wpVsE)
        if args.discr=='VsE':
            name = '%sVsJet_%sVsMu_%sVsE'%(wpVsJet,wpVsMu,wp)
        namehist = wp+args.discr
        hists[namehist] = inputFile.Get('muTauFR_'+name)
        print(name,hists[namehist])

    Plot(hists,era=era,suffix=suffix)
