#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Datacard producer (Z->mumu control region)
import ROOT
import math
import TauPOG.MuTauFR.utils as utils
import TauPOG.MuTauFR.styles as styles
import TauPOG.MuTauFR.analysisMuTauFR as analysis
from array import array
import os
import CombineHarvester.CombineTools.ch as ch

#################################
#     definition of cuts        #
#################################

etabins = [
    'eta0p0to0p9',
    'eta0p9to1p2',
    'eta1p2to2p1',
    'eta2p1to2p5']

nbins = 4
bins = [[0,0.92,1.22,2.12,2.53],[0.,0.9,1.2,2.1,2.5]]
wps = [('Medium','VLoose','VVLoose'),
       ('Medium','Tight','VVLoose')]

def Plot(hists,**kwargs):

    era = kwargs.get('era','2024')
    tp = kwargs.get('tp',True)
    
    names = []
    for wp in wps:
        names.append('%sVsJet_%sVsMu_%sVsE'%(wp[0],wp[1],wp[2]))

    styles.InitData(hists[names[0]])
    styles.InitData(hists[names[1]])

    hists[names[0]].SetMarkerColor(ROOT.kRed)
    hists[names[0]].SetLineColor(ROOT.kRed)
    hists[names[0]].SetMarkerStyle(20)

    hists[names[1]].SetMarkerColor(ROOT.kBlue)
    hists[names[1]].SetLineColor(ROOT.kBlue)
    hists[names[1]].SetMarkerStyle(21)

    hists[names[0]].GetYaxis().SetTitle('SF')
    hists[names[0]].GetXaxis().SetTitle('|#eta|')
    hists[names[0]].GetYaxis().SetRangeUser(0.,2.4)
    
    # canvas and pads
    canvas = styles.MakeCanvas("canv","",600,600)
    
    hists[names[0]].Draw('e1')
    hists[names[1]].Draw('e1same')
    
    leg = ROOT.TLegend(0.25,0.2,0.5,0.4)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.045)
    leg.SetHeader('MediumVSjet  VVLooseVSe')
    leg.AddEntry(hists[names[0]],wps[0][1]+'VSmu','lp')
    leg.AddEntry(hists[names[1]],wps[1][1]+'VSmu','lp')
    leg.Draw()
    
    styles.CMS_label(canvas,era=era)

    canvas.Modified()
    canvas.RedrawAxis()
    canvas.Update()
    print('')
    print('Creating SF plot')

    suffix = ''
    if tp: suffix = '_tp'
    
    outfolder = '/eos/home-r/rasp/php-plots/plots/MuTauFR'
    canvas.Print('%s/SF_%s%s.png'%(outfolder,era,suffix))

############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024'])
    parser.add_argument('-tp','--tp',  dest='tp', action='store_true')
    args = parser.parse_args()
    
    era = args.era
    tp = args.tp
    print('')

    basefolder = '/afs/cern.ch/work/r/rasp/MuTauFR/datacards_backup'
    if tp: basefolder = '%s/src/TauFW/Fitter/MuTauFR/datacards'%(os.getenv('CMSSW_BASE'))
    
    mutau_contents = {}
    jtau_contents = {}
    tauid_contents = {}
    for wp in wps:
        name = '%sVsJet_%sVsMu_%sVsE'%(wp[0],wp[1],wp[2])
        nameWP = '%s_%s_%s'%(wp[0],wp[1],wp[2])
        if tp: nameWP = '%sVsJet_%sVsMu_%sVsE'%(wp[0],wp[1],wp[2])
        mutau_contents[name] = []
        jtau_contents[name] = []
        tauid_contents[name] = []
        for etabin in etabins:
            inputFitFileName = '%s/mutauFR_%s_%s_mtCut_1pr_%s_fit.root'%(basefolder,era,nameWP,etabin)
            if tp: inputFitFileName = '%s/%s/%s_%s_fit.root'%(basefolder,nameWP,era,etabin)
            inputFitFile = ROOT.TFile(inputFitFileName,'read')
            fitResult = inputFitFile.Get('fit_s')
            pars = fitResult.floatParsFinal()
            tauid = 1.0
            tauidE = 0.1
            mutauFR = 1.0
            mutauFRE = 0.1
            jtauFR = 1.0
            jtauFRE = 0.1
            if tp:
                norm = 1
                normE = 0.1
                rpass = 1.
                rpassE = 0.1
                jfake_n = 1.0
                jfakeE_n = 0.1
                for par in pars:
                    if par.GetName()=='r': 
                        norm = par.getVal()
                        normE = par.getError()
                    if par.GetName()=='SF_zmm_pass':
                        rpass = par.getVal()
                        rpassE = par.getError()
                    if par.GetName()=='jet_to_tauFR':
                        jfake_n = par.getVal()
                        jfakeE_n = par.getError()
                    if par.GetName()=='norm_ztt':
                        tauid = par.getVal()
                        tauidE = par.getError()
                mutauFR = norm*rpass
                mutauFRE = math.sqrt(norm*norm*rpassE*rpassE+rpass*rpass*normE*normE)
                jtauFR = 1.0 + 0.3*jfake_n
                jtauFRE = 0.3*jfakeE_n                
            else:
                for par in pars:
                    if par.GetName()=='r':
                        mutauFR = par.getVal()
                        mutauFRE = par.getError()
                    if par.GetName()=='jfake':
                        jtauFR = par.getVal()
                        jfakeE = par.getError()
                    if par.GetName()=='tauID':
                        tauid = par.getVal()
                        tauidE = par.getError()

            if mutauFR>2.0: mutauFR = 1.81
            mutau_contents[name].append((mutauFR,mutauFRE))
            jtau_contents[name].append((jtauFR,jtauFRE))
            tauid_contents[name].append((tauid,tauidE))
            inputFitFile.Close()
            
    # creating histograms
    N = 0
    hists = {}
    for wp in wps:
        name = '%sVsJet_%sVsMu_%sVsE'%(wp[0],wp[1],wp[2])
        hists[name] = ROOT.TH1D(name,'',nbins,array('d',list(bins[N])))
        N += 1
        print('%s'%(name))
        for ib in range(0,nbins):
            x_mutau = mutau_contents[name][ib][0]
            e_mutau = mutau_contents[name][ib][1]
            x_jtau = jtau_contents[name][ib][0]
            e_jtau = jtau_contents[name][ib][1]
            x_tauid = tauid_contents[name][ib][0]
            e_tauid = tauid_contents[name][ib][1]
            print('%s : mutau = %4.2f +/- %4.2f : jtau = %4.2f +/- %4.2f : tauid = %4.2f +/- %4.2f'%(etabins[ib],x_mutau,e_mutau,x_jtau,e_jtau,x_tauid,e_tauid))
            hists[name].SetBinContent(ib+1,x_mutau)
            hists[name].SetBinError(ib+1,e_mutau)
        print('')
    Plot(hists,era=era,tp=tp)
    for wp in wps:
        outputFolder = '/afs/cern.ch/work/r/rasp/MuTauFR/ScaleFactors'
        name = '%sVsJet_%sVsMu_%sVsE'%(wp[0],wp[1],wp[2])
        outputFileName = '%s/SF_%s_%s_mtCut_1pr.root'%(outputFolder,era,name)
        outputFile = ROOT.TFile(outputFileName,'recreate')
        outputFile.cd('')
        lfake = ROOT.TH1D('lfake','',nbins,array('d',list(bins[1])))
        jfake = ROOT.TH1D('jfake','',nbins,array('d',list(bins[1])))
        tauID = ROOT.TH1D('tauID','',nbins,array('d',list(bins[1])))
        for ib in range(0,nbins):
            lfake.SetBinContent(ib+1,mutau_contents[name][ib][0])
            lfake.SetBinError(ib+1,mutau_contents[name][ib][1])
            jfake.SetBinContent(ib+1,jtau_contents[name][ib][0])
            jfake.SetBinError(ib+1,jtau_contents[name][ib][1])
            tauID.SetBinContent(ib+1,tauid_contents[name][ib][0])
            tauID.SetBinError(ib+1,tauid_contents[name][ib][1])
        outputFile.cd('')
        lfake.Write('lfake')
        jfake.Write('jfake')
        tauID.Write('tauID')
        outputFile.Close()
