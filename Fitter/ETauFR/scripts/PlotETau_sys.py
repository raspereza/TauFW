#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2026)
# Checking systematic variations in datacards
import ROOT
from array import array
import TauFW.Fitter.ETauFR.utils as utils
import TauFW.Fitter.ETauFR.styles as styles
import os
from TauFW.Plotter.plot.utils import ensuredir

def PlotSystematics(hists,**kwargs):

    era = kwargs.get('era','2526')
    sampleName = kwargs.get('sample','wtaunu')
    sysName = kwargs.get('sysName','JES')
    ratioLower = kwargs.get('ratioLower',0.5) 
    ratioUpper = kwargs.get('ratioUpper',1.5)
    logx = kwargs.get('logx',False)
    etabin = kwargs.get('etabin','eta0p0to1p48')
    dm     = kwargs.get('dm','DM0')

    h_central = hists['central']
    h_up = hists['up']
    h_down = hists['down']
    
    styles.InitData(h_central)
    styles.InitData(h_up)
    styles.InitData(h_down)

    h_up.SetMarkerSize(0)
    h_up.SetLineColor(2)
    h_up.SetMarkerColor(2)
    h_up.SetLineStyle(1)

    h_down.SetMarkerSize(0)
    h_down.SetLineColor(4)
    h_down.SetMarkerColor(4)
    h_down.SetLineStyle(1)

    h_ratio_up = utils.divideHistos(h_up,h_central,'ratio_up')
    h_ratio_down = utils.divideHistos(h_down,h_central,'ratio_down')
    h_ratio = utils.createUnitHisto(h_central,'ratio')
    styles.InitRatioHist(h_ratio)
    h_ratio.GetYaxis().SetRangeUser(ratioLower,ratioUpper)

    print('')
    print('Template %s  systematics %s'%(sampleName,sysName))
    print('')
    print('             down     nom     up')
    print('----------------------------------')
    #      [200, 300]  1091.8  1085.6  1079.4

    nbins = h_central.GetNbinsX()
    for ib in range(1,nbins+1):
        lower = h_central.GetBinLowEdge(ib)
        upper = h_central.GetBinLowEdge(ib+1)
        xcentral = h_central.GetBinContent(ib)
        xup = h_up.GetBinContent(ib)
        xdown = h_down.GetBinContent(ib)
        print('[%3i,%4i]  %6.1f  %6.1f  %6.1f'%(lower,upper,xdown,xcentral,xup))

    utils.zeroBinErrors(h_up)
    utils.zeroBinErrors(h_down)
    utils.zeroBinErrors(h_ratio_up)
    utils.zeroBinErrors(h_ratio_down)

    ymax = h_central.GetMaximum()
    if h_up.GetMaximum()>ymax: ymax = h_up.GetMaximum()
    if h_down.GetMaximum()>ymax: ymax = h_down.GetMaximum()
    h_central.GetYaxis().SetRangeUser(0.,1.2*ymax)
    h_central.GetXaxis().SetLabelSize(0)

    # canvas and pads
    canvas = styles.MakeCanvas("canv","",600,700)
    # upper pad
    upper = ROOT.TPad("upper", "pad",0,0.31,1,1)
    upper.Draw()
    upper.cd()
    styles.InitUpperPad(upper)    
    
    h_central.Draw('e1')
    h_down.Draw('hsame')
    h_up.Draw('hsame')
    h_central.Draw('e1same')
    
    leg = ROOT.TLegend(0.4,0.55,0.7,0.85)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.045)
    leg.SetHeader(sampleName+":"+sysName)
    leg.AddEntry(h_central,'central','lp')
    leg.AddEntry(h_up,'up','l')
    leg.AddEntry(h_down,'down','l')
    leg.Draw()

    upper.Draw("SAME")
    if logx: 
        upper.SetLogx(True)
    upper.RedrawAxis()
    upper.Modified()
    upper.Update()
    canvas.cd()

    # lower pad
    lower = ROOT.TPad("lower", "pad",0,0,1,0.30)
    lower.Draw()
    lower.cd()
    styles.InitLowerPad(lower)

    h_ratio.Draw('e1')
    h_ratio_up.Draw('hsame')
    h_ratio_down.Draw('hsame')
    h_ratio.Draw('e1same')
    nbins = h_ratio.GetNbinsX()
    xmin = h_ratio.GetXaxis().GetBinLowEdge(1)    
    xmax = h_ratio.GetXaxis().GetBinLowEdge(nbins+1)
    line = ROOT.TLine(xmin,1.,xmax,1.)
    line.Draw()
    if logx:
        lower.SetLogx(True)

    lower.Modified()
    lower.RedrawAxis()

    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()

    binname = '%s_%s'%(etabin,dm)
    Folder = utils.figuresFolder+'/Sys/'+'/'+era+'/'+binname
    filename = sampleName+'_'+sysName+'.png'
    ensuredir(Folder)
    canvas.Print(Folder+'/'+filename)

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

#####################################################################
#   Plotting shape Systematics :
#   default temlates : ZTT, TTT, TTL, ZL
#   default systematics : EES, TES, FES
#####################################################################
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era',dest='era',default='2526',choices=['2025','2026','2526'])
    parser.add_argument('-samples','--samples',dest='samples',nargs='+',default=['ZTT','TTT','TTL','ZL'])
    parser.add_argument('-wpVsJet','--WPvsJet',dest='wpVsJet',default='Medium')
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='VLoose')
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VVLoose')
    parser.add_argument('-sysnames','--sysnames',dest='sysnames', nargs='+', default=['EES','TES','FES'])
    parser
    parser.add_argument('-ymin','--ymin',dest='ymin',default=0.5)
    parser.add_argument('-ymax','--ymax',dest='ymax',default=1.5)
    parser.add_argument('-logx','--logx',dest='logx',action='store_true')
    args = parser.parse_args() 

    era = args.era
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE
    
    cmssw_base = os.getenv('CMSSW_BASE')
    path = f'{cmssw_base}/src/TauFW/Fitter/ETauFR/datacards/{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE'

    for etabin in utils.etabins:
        for dm in utils.dm_meas:
            filename = "%s_%s_inputs.root"%(etabin,dm)
            fullpath = path+'/'+filename
            
            if os.path.isfile(fullpath):
                print('Opening file %s'%(fullpath))
            else:
                print('File %s does not exist'%(fullpath))
                continue

            cardsFile = ROOT.TFile(fullpath)
            if cardsFile==None or cardsFile.IsZombie():
                print('File %s cannot be opened'%(fullpath))
                continue

            for sample in args.samples:
                for sysname in args.sysnames:
                    name_central='pass/'+sample
                    name_up='pass/'+sample+'_'+sysname+'Up'
                    name_down='pass/'+sample+"_"+sysname+'Down'
                    hist_central = cardsFile.Get(name_central)
                    hist_up = cardsFile.Get(name_up)
                    hist_down = cardsFile.Get(name_down)
                    if hist_central==None or hist_up==None or hist_down==None:
                        print('Histogram %s with %s is not found'%(sample,sysname))
                        continue

                    hists = {}
                    hists['central'] = hist_central
                    hists['up'] = hist_up
                    hists['down'] = hist_down

                    PlotSystematics(hists,
                                    era=args.era,
                                    sample=sample,
                                    sysName=sysname,
                                    ratioLower=args.ymin,
                                    ratioUpper=args.ymax,
                                    logx=args.logx,
                                    etabin=etabin,
                                    dm=dm)
