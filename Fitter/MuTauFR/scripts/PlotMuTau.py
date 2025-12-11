#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# plotting prefit and postfit distributions
import ROOT
import math
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
from TauFW.Plotter.plot.utils import ensuredir
from array import array
import os
import CombineHarvester.CombineTools.ch as ch

#################################
#     definition of cuts        #
#################################

def createEmptyHisto(hist,name):
    nbins = hist.GetNbinsX()
    bins = []
    for ib in range(1,nbins+2):
        x = hist.GetBinLowEdge(ib)
        bins.append(x)
    newhist = ROOT.TH1D(name,'',nbins,array('d',list(bins)))
    return newhist

def copyHisto(histo1,histo2):
    if histo1!=None:
        nbins = histo1.GetNbinsX()
        for ib in range(1,nbins+1):
            x = histo1.GetBinContent(ib)
            e = histo1.GetBinError(ib)
            histo2.SetBinContent(ib,x)
            histo2.SetBinError(ib,e)


regions = ['pass','fail']
samples = ['data_obs','ZTT','ZJ','ZL','TTT','TTL','TTJ','VV','W','QCD']
mc_samples = ['ZTT','ZJ','ZL','TTT','TTL','TTJ','VV','W','QCD']
options = ['shapes_prefit','shapes_fit_s'] 

#################################
###### plotting subroutine ######
#################################
def Plot(hists,**kwargs):

    era = kwargs.get('era','2024')
    etabin = kwargs.get('etabin','eta0p0to0p9')
    wpVsJet = kwargs.get('wpVsJet','Medium')
    wpVsMu = kwargs.get('wpVsMu','VLoose')
    wpVsEle = kwargs.get('wpVsEle','Tight')
    plotLegend = kwargs.get('plotLegend',True)
    option = kwargs.get('option','shapes_fit_s')
    region = kwargs.get('region','pass')
    dm = kwargs.get('dm','1prong')

    FIT = 'prefit'
    if option=='shapes_fit_s': FIT = 'postfit'
    
    
    postFit = True
    if option=='shapes_prefit': postFit = False
    
    preFit = not postFit

    h_data = hists['data_obs']

    h_zll = hists['ZL']
    h_ztt = hists['ZTT']
    
    h_tt = hists['TTT']
    h_tt.Add(h_tt,hists['TTL'])

    h_ewk = hists['VV']

    h_jfakes = hists['ZJ']
    h_jfakes.Add(h_jfakes,hists['TTJ'])
    h_jfakes.Add(h_jfakes,hists['W'])

    h_qcd = hists['QCD']
    
    styles.InitData(h_data)
    styles.InitHist(h_zll,   "","",ROOT.TColor.GetColor(100,192,232),1001)
    styles.InitHist(h_ztt,   "","",ROOT.TColor.GetColor("#FFCC66"),1001)
    styles.InitHist(h_ewk,   "","",ROOT.TColor.GetColor("#DE5A6A"),1001)
    styles.InitHist(h_tt,    "","",ROOT.TColor.GetColor("#9999CC"),1001)
    styles.InitHist(h_qcd,   "","",ROOT.TColor.GetColor("#FFCCFF"),1001)
    styles.InitHist(h_jfakes,"","",ROOT.kGreen+6,1001)
    
    h_tot = hists['total']
    styles.InitTotalHist(h_tot)
    
    x_zll = h_zll.GetSumOfWeights()
    x_ztt = h_ztt.GetSumOfWeights()
    x_qcd = h_qcd.GetSumOfWeights()
    x_ewk = h_ewk.GetSumOfWeights()
    x_tt = h_tt.GetSumOfWeights()
    x_jfakes = h_jfakes.GetSumOfWeights()
    x_data = h_data.GetSumOfWeights()
    x_tot = x_zll+x_ztt+x_qcd+x_ewk+x_tt+x_jfakes
    x_checksum = h_tot.GetSumOfWeights()
    
    print('ZTT   : %7.0f'%(x_ztt))
    print('ZL    : %7.0f'%(x_zll))
    print('QCD   : %7.0f'%(x_qcd)) 
    print('JFakes: %7.0f'%(x_jfakes))
    print('EWK   : %7.0f'%(x_ewk))
    print('TT    : %7.0f'%(x_tt))
    print('Total : %7.0f'%(x_tot))
#    print('Check : %7.0f'%(x_checksum))
    print('Data  : %7.0f'%(x_data))
    
    h_ewk.Add(h_ewk,h_tt,1.,1.)
    h_jfakes.Add(h_jfakes,h_ewk,1.,1.)
    h_qcd.Add(h_qcd,h_jfakes,1.,1.)
    h_ztt.Add(h_ztt,h_qcd,1.,1.)
    h_zll.Add(h_zll,h_ztt,1.,1.)

    h_ratio = utils.histoRatio(h_data,h_tot,'ratio')
    h_tot_ratio = utils.createUnitHisto(h_tot,'tot_ratio')

    styles.InitRatioHist(h_ratio)
    h_ratio.GetYaxis().SetRangeUser(0.501,1.499)
    
    utils.zeroBinErrors(h_zll)
    utils.zeroBinErrors(h_ztt)
    utils.zeroBinErrors(h_qcd)
    utils.zeroBinErrors(h_ewk)
    utils.zeroBinErrors(h_jfakes)
    utils.zeroBinErrors(h_tt)

    ymax = h_data.GetMaximum()
    if h_tot.GetMaximum()>ymax: ymax = h_tot.GetMaximum()

    h_data.GetYaxis().SetRangeUser(0.,1.5*ymax)
    if region=='fail': h_data.GetYaxis().SetRangeUser(0.,2.5*ymax)
    h_data.GetXaxis().SetLabelSize(0)
    h_data.GetYaxis().SetTitle("Events")
    h_ratio.GetYaxis().SetTitle("obs/exp")
    h_ratio.GetXaxis().SetTitle('m_vis')

    # canvas and pads
    canvas = styles.MakeCanvas("canv","",600,700)
    # upper pad
    upper = ROOT.TPad("upper", "pad",0,0.31,1,1)
    upper.Draw()
    upper.cd()
    styles.InitUpperPad(upper)    
    
    h_data.Draw('e1')
    h_zll.Draw('hsame')
    h_ztt.Draw('hsame')
    if region=='pass':
        h_qcd.Draw('hsame')
#        h_jfakes.Draw('hsame')
        h_ewk.Draw('hsame')
#        h_tt.Draw('hsame')
    h_data.Draw('e1same')
    h_tot.Draw('e2same')

    leg = None
    if region=='pass':
        leg = ROOT.TLegend(0.70,0.40,0.90,0.75)
    else:
        leg = ROOT.TLegend(0.25,0.57,0.5,0.78)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.043)
    leg.SetHeader(utils.etaTitle[etabin])
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_zll,'Z#rightarrow#mu#mu','f')
    if region=='pass':
        leg.AddEntry(h_ztt,'Z#rightarrow#tau#tau','f')
        leg.AddEntry(h_qcd,'j#rightarrow#tau misID','f')
#        leg.AddEntry(h_jfakes,'non-QCD j#rightarrow#tau','f')
        leg.AddEntry(h_ewk,'other','f')
#        leg.AddEntry(h_tt,'t#bar{t}','f')
    else:
        leg.AddEntry(h_ztt,'bkg','f')
        
    if plotLegend: leg.Draw()

    text = ROOT.TText(0.25,0.83,'%s %s'%(FIT,region))
    text.SetTextSize(0.07)
    text.SetNDC()
    text.Draw()
    
    styles.CMS_label(upper,era=era)

    upper.Draw("SAME")
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
    h_tot_ratio.Draw('e2same')
    h_ratio.Draw('e1same')
    nbins = h_ratio.GetNbinsX()
    xmin = h_ratio.GetXaxis().GetBinLowEdge(1)    
    xmax = h_ratio.GetXaxis().GetBinLowEdge(nbins+1)
    line = ROOT.TLine(xmin,1.,xmax,1.)
    line.SetLineStyle(1)
    line.SetLineWidth(2)
    line.SetLineColor(4)
    line.Draw()
    lower.Modified()
    lower.RedrawAxis()

    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()
    print('')

    subfolder = '%s_%sVsJet_%sVsMu_%sVsE'%(era,wpVsJet,wpVsMu,wpVsEle)
    outputFolderName = utils.figuresFolder+'/Fits/'+subfolder
    outputFolder = ensuredir(outputFolderName)
    canvas.Print("%s/%s_%s_%s_%s.png"%(outputFolder,etabin,region,dm,FIT))
    print('')
    
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
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Loose','Medium','Tight'])
    parser.add_argument('-dm','--dm',dest='dm',default='1prong')
    args = parser.parse_args()

    era = args.era
    wp_vs_jet = args.wpVsJet
    wp_vs_mu  = args.wpVsMu
    wp_vs_e   = args.wpVsE
    dm = args.dm
    
    cmssw_base = os.getenv('CMSSW_BASE')
    basedir = '%s/src/TauFW/Fitter/MuTauFR/datacards/%s_%sVsJet_%sVsMu_%sVsE_%s'%(cmssw_base,era,wp_vs_jet,wp_vs_mu,wp_vs_e,dm)
    if os.path.isdir(basedir):
        print('folder %s')
    else:
        print('folder %s does not exist'%(basedir))
        print('You have to produced datacards for era=%s, WP: %sVsJet %sVsMu %sVsE and dm=%s'%(era,wp_vs_jet,wp_vs_mu,wp_vs_e,dm))
    for etabin in utils.etabins:

        inputCardsFileName = '%s/%s.root'%(basedir,etabin)
        if os.path.isfile(inputCardsFileName):
            print('datacards file %s'%(inputCardsFileName))
        else:
            print('file %s does not exist. quitting'%(inputCardsFileName))
            exit()
        inputCardsFile = ROOT.TFile(inputCardsFileName,'read')
        inputFitFileName = '%s/%s_fit.root'%(basedir,etabin)
        if os.path.isfile(inputFitFileName):
            print('file with the fit results : %s '%(inputFitFileName))
        else:
            print('file with fit results %s does not exist. quitting'%(inputCardsFileName))
            exit()
        
        inputFitFile = ROOT.TFile(inputFitFileName,'read')

        for option in options:
            for region in regions:
                print('%s  %s  %s'%(etabin,option,region))
                hists = {}
                folder = '%s'%(region)
                name = '%s_%s_%s'%(etabin,option,region)                
                hist_ref = inputCardsFile.Get(folder+'/data_obs')
                hists['data_obs'] = createEmptyHisto(hist_ref,'data_'+name)
                copyHisto(hist_ref,hists['data_obs'])
                folder_fit = '%s/%s'%(option,folder)
                for sample in mc_samples:
                    histname_input = folder+'/'+sample
                    histname_input_fit = folder_fit+'/'+sample
                    hists[sample] = inputCardsFile.Get(histname_input).Clone(sample+'_'+name)
                    hist = inputFitFile.Get(folder_fit+'/'+sample)
                    copyHisto(hist,hists[sample])
                hists['total'] = createEmptyHisto(hist_ref,'total_'+name)
                hist = inputFitFile.Get(folder_fit+'/total')
                copyHisto(hist,hists['total'])
                Plot(hists,
                     era=era,
                     etabin=etabin,
                     wpVsJet=wp_vs_jet,
                     wpVsEle=wp_vs_e,
                     wpVsMu=wp_vs_mu,
                     option=option,
                     plotLegend=True,
                     region=region)


