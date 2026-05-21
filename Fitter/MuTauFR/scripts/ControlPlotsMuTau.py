#! /usr/bin/env python3
# Author: Alexei Raspereza (October 2025)
# mu->tau FR SF measurement
# Control plots
import ROOT
import math
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
from TauFW.Plotter.plot.utils import ensuredir
from array import array
import os

#################################
#     definition of cuts        #
#################################

Vars = {
#    VAR        TITLE                          BINNING       Legend   Logy   
    'pt_1'  : ("muon p_{T} (GeV)",           20,  25., 125.,  True,  False),
    'eta_1' : ("muon #eta",                  24, -2.4,  2.4, False,  False),
    'pt_2'  : ("tau p_{T} (GeV)",            20,  20., 120.,  True,  False),
    'eta_2' : ("tau #eta",                   25, -2.5,  2.5, False,  False),
    'm_vis' : ("m_{vis} (GeV)",              32,   0., 160.,  True,  False), 
    'met'   : ("E_{T}^{mis} (GeV)",          20,   0., 200.,  True,  False),
    'dm_2'  : ("decay mode",                 12, -0.5, 11.5,  True,  False),
    'mt_1'  : ("m_{T}(#mu,MET) (GeV)",        8,   0.,  40.,  True,  False),
    'rawDeepTau2018v2p5VSmu_2' : ('D_{#mu}', 10,   0.,   1.,  True,  True),
}

def ExtractHistos(f,var,dm,bins):
    hists = {}
    
    hists['Data_os'] = utils.rebinHisto(f.Get(f'Data_{var}_os_{dm}'),bins,'rebinned')
    hists['Data_ss'] = utils.rebinHisto(f.Get(f'Data_{var}_ss_{dm}'),bins,'rebinned')
    for s in utils.procs:
        for sign in ['os','ss']:
            name_reduced = f'{s}_{sign}'
            name = f'{s}_{var}_{sign}_{dm}'
            hists[name_reduced] = utils.rebinHisto(f.Get(name),bins,'rebinned')
    return hists

def PlotZtoMuTau(hists,**kwargs):

    era = kwargs.get('era','2024')
    chan = kwargs.get('chan','mutau')
    var = kwargs.get('var','m_vis')
    wpVsJet = kwargs.get('wpVsJet','Medium')
    wpVsMu = kwargs.get('wpVsMu','VLoose')
    wpVsE = kwargs.get('wpVsE','VVLoose')
    plotLegend = kwargs.get('plotLegend',True)
    setLogy = kwargs.get('setLogy',False)
    dm = kwargs.get('dm','1prong')
    applySF = kwargs.get('applySF',False)
    
    h_data = hists['Data_os'].Clone('h_data')
    
    h_ewk = hists['VV_os'].Clone('h_ewk')
    
    h_tt = hists['TTT_os'].Clone('h_tt')
    h_tt.Add(h_tt,hists['TTL_os'],1.,1.)

    h_zll = hists['ZL_os'].Clone('h_zll')
    h_ztt = hists['ZTT_os'].Clone('h_ztt')

    h_fakes = hists['W_os'].Clone('h_fakes')
    h_fakes.Add(h_fakes,hists['ZJ_os'],1.,1.)
    h_fakes.Add(h_fakes,hists['TTJ_os'],1.,1.)
    
    h_qcd = hists['Data_ss'].Clone('h_qcd')
    for s in utils.procs:
        h_qcd.Add(h_qcd,hists[f'{s}_ss'],1.,-1.) 

    styles.InitData(h_data)
    styles.InitHist(h_zll,"","",ROOT.TColor.GetColor(100,192,232),1001)
    styles.InitHist(h_ztt,"","",ROOT.TColor.GetColor("#FFCC66"),1001)
    styles.InitHist(h_ewk,"","",ROOT.TColor.GetColor("#DE5A6A"),1001)
    styles.InitHist(h_fakes,"","",ROOT.kCyan,1001)
    styles.InitHist(h_tt,"","",ROOT.TColor.GetColor("#9999CC"),1001)
    styles.InitHist(h_qcd,"","",ROOT.TColor.GetColor("#FFCCFF"),1001)

    x_zll = h_zll.GetSumOfWeights()
    x_ztt = h_ztt.GetSumOfWeights()
    x_qcd = h_qcd.GetSumOfWeights()
    x_ewk = h_ewk.GetSumOfWeights()
    x_tt = h_tt.GetSumOfWeights()
    x_fakes = h_fakes.GetSumOfWeights()
    x_data = h_data.GetSumOfWeights()
    x_tot = x_zll+x_ztt+x_qcd+x_ewk+x_tt+x_fakes

    
    print('')
    print('Yields ->')
    print('ZTT  : %7.0f'%(x_ztt))
    print('TT   : %7.0f'%(x_tt))
    print('QCD  : %7.0f'%(x_qcd))
    print('EWK  : %7.0f'%(x_ewk))
    print('Fakes: %7.0f'%(x_fakes))
    print('ZL   : %7.0f'%(x_zll))
    print('Tot  : %7.0f'%(x_tot))
    print('Data : %7.0f'%(x_data))


    h_ewk.Add(h_ewk,h_tt,1.,1.)
    h_fakes.Add(h_fakes,h_ewk,1.,1.)
    h_qcd.Add(h_qcd,h_fakes,1.,1.)
    h_ztt.Add(h_ztt,h_qcd,1.,1.)
    h_zll.Add(h_zll,h_ztt,1.,1.)
    
    h_tot = h_zll.Clone("total")
    styles.InitTotalHist(h_tot)


    # applying ad-hoc uncertainties
    # 20% -> jet->tau fake rate
    # 10% -> tauID
    # 70% -> mu->tau fake rate
    
    sf_jfake = 0.20
    sf_tauID = 0.10
    sf_lfake = 0.70
    sf_qcd = 0.15
    if applySF:
        sf_jfake = 0.10
        sf_tauID = 0.05
        sf_lfake = 0.20
        sf_qcd = 0.10
    
    nbins = h_data.GetNbinsX()        
    for ib in range(1,nbins+1):
        e_jfake = sf_jfake*h_fakes.GetBinContent(ib)
        e_lfake = sf_lfake*(hists['ZL_os'].GetBinContent(ib)+hists['TTL_os'].GetBinContent(ib))
        e_tauID = sf_tauID*(hists['ZTT_os'].GetBinContent(ib)+hists['TTT_os'].GetBinContent(ib))
        e_QCD = sf_qcd*h_qcd.GetBinContent(ib)
        e_tot = h_tot.GetBinError(ib)
        err = math.sqrt(e_jfake*e_jfake+e_lfake*e_lfake+e_tauID*e_tauID+e_QCD*e_QCD+e_tot*e_tot)
        h_tot.SetBinError(ib,err)

    
    h_ratio = utils.histoRatio(h_data,h_tot,'ratio')
    h_tot_ratio = utils.createUnitHisto(h_tot,'tot_ratio')

    styles.InitRatioHist(h_ratio)
    if setLogy:
        h_ratio.GetYaxis().SetRangeUser(0.601,1.399)
    else:
        h_ratio.GetYaxis().SetRangeUser(0.601,1.399)
    
    utils.zeroBinErrors(h_zll)
    utils.zeroBinErrors(h_ztt)
    utils.zeroBinErrors(h_qcd)
    utils.zeroBinErrors(h_ewk)
    utils.zeroBinErrors(h_tt)

    ymax = h_data.GetMaximum()
    if h_tot.GetMaximum()>ymax: ymax = h_tot.GetMaximum()

    h_data.GetYaxis().SetRangeUser(0.,1.2*ymax)
    if setLogy:
        h_data.GetYaxis().SetRangeUser(10.,20.*ymax)
    else:
        h_data.GetYaxis().SetRangeUser(0.,1.2*ymax)
    h_data.GetXaxis().SetLabelSize(0)
    h_data.GetYaxis().SetTitle("Events")
    h_ratio.GetYaxis().SetTitle("obs/exp")
    h_ratio.GetXaxis().SetTitle(Vars[var][0])

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
    h_qcd.Draw('hsame')
#    h_fakes.Draw('hsame')
    h_ewk.Draw('hsame')
#    h_tt.Draw('hsame')
    h_data.Draw('e1same')
    h_tot.Draw('e2same')

    leg = ROOT.TLegend(0.7,0.4,0.9,0.7)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.043)
    leg.SetHeader(dm)
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_zll,'Z#rightarrow#mu#mu','f')
    leg.AddEntry(h_ztt,'Z#rightarrow#tau#tau','f')
    leg.AddEntry(h_qcd,'jet#rightarrow#tau fakes','f')
#    leg.AddEntry(h_fakes,'non-QCD j#rightarrow#tau','f')
    leg.AddEntry(h_ewk,'other','f')
#    leg.AddEntry(h_tt,'t#bar{t}','f')
    if plotLegend: leg.Draw()

    styles.CMS_label(upper,era=era)

    upper.Draw("SAME")
    upper.RedrawAxis()
    if setLogy: upper.SetLogy(True)
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
    print('Creating control plot')

    suffix = utils.defineSuffix(chan,era,wpVsJet,wpVsMu,wpVsE,applySF)
    
    subfolder = ensuredir('%s/ControlPlots'%(utils.figuresFolder))
    outputfolder = ensuredir('%s/%s'%(subfolder,suffix))
    canvas.Print(outputfolder+"/"+var+"_"+dm+".png")
    
############
#   MAIN   #
############

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2025', choices=['2024','2025','UL2017','UL2016_preVFP','UL2016_postVFP'])
    parser.add_argument('-var', '--var', dest='var', default=['m_vis','pt_1','pt_2','eta_1','eta_2'], nargs='+', choices=['m_vis','pt_1', 'pt_2', 'eta_1','eta_2', 'mt_1', 'dm_2', 'met', 'rawDeepTau2018v2p5VSmu_2'])
    parser.add_argument('-wpVsJet','--wpVsJet', dest='wpVsJet', default='Medium', choices=['Loose','Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--wpVsMu', dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Medium','Tight'])
    parser.add_argument('-dm','--dm', dest='dm',default='1prong',choices=['1prong','DM0','DM1','3prong','incl'])
    parser.add_argument('-applySF','--applySF',dest='applySF',action='store_true')
    
    args = parser.parse_args()
    
    variables = args.var
    era = args.era
    chan = 'mutau'
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE
    dm = args.dm
    applySF = args.applySF
#    nbins = args.nbins
#    xmin = args.xmin
#    xmax = args.xmax


    suffix = utils.defineSuffix(chan,era,wpVsJet,wpVsMu,wpVsE,applySF)
    inputfolder = '%s/%s'%(utils.outputFolder,suffix)
    inputfileName = '%s/mutau.root'%(inputfolder)
    if os.path.isfile(inputfileName):
        print('Opening file %s'%(inputfileName))
    else:
        print('file %s does not exist.'%(inputfileName))
        print('check existence and content of folder %s'%(inputfolder))
        print('if such folder does not exist, you have not run respective selection')
        print('quit')
        exit()
    inputfile = ROOT.TFile(inputfileName,'read')

    for var in variables:
        nbins = Vars[var][1]
        xmin  = Vars[var][2]
        xmax  = Vars[var][3]
        plotLegend = Vars[var][4]
        setLogy = Vars[var][5]
        bins  = utils.createBins(nbins,xmin,xmax)
        hists = ExtractHistos(inputfile,var,dm,bins)
        
        PlotZtoMuTau(hists,
                     era=era,
                     chan=chan,
                     var=var,
                     wpVsJet=wpVsJet,
                     wpVsE=wpVsE,
                     wpVsMu=wpVsMu,
                     applySF=applySF,
                     dm=dm,
                     plotLegend=plotLegend,
                     setLogy=setLogy)
