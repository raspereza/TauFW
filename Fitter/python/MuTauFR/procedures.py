import ROOT
import math
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
import TauFW.Fitter.MuTauFR.analysisMuTauFR as analysis
from TauFW.Plotter.plot.utils import ensuredir
from array import array
import os
from CombineHarvester.CombineTools import ch

###################################
####  Extracing scale factors #####
###################################
def ExtractScaleFactors(**kwargs):

    era = kwargs.get('era','2024')
    wpVsMu = kwargs.get('wpVsMu','VLoose')
    wpVsJet = kwargs.get('wpVsJet','Medium')
    wpVsE = kwargs.get('wpVsE','VVLoose')
    dm = kwargs.get('dm','1prong')
    coarse = kwargs.get('coarse',False)
    
    cmssw_base = os.getenv('CMSSW_BASE')
    name = f'{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE_{dm}'
    outname = name
    etaRange = utils.etaRanges1
    if coarse:
        etaRange = utils.etaRanges2
        outname += '_coarse'
        
    cardsfolder = f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/datacards/{name}'
    print(f'{cardsfolder}')
    histfolder = ensuredir(f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/ScaleFactors')
    if not os.path.isdir(cardsfolder):
        print('folder %s does not exist'%(cardsfolder))
        print('create datacards for respective WPs and run fit on them')
        print('quitting')
        exit()

    nbins = 0
    y = 0
    bins = []
    for etabin in etaRange:
        x = etaRange[etabin][0]
        y = etaRange[etabin][1]
        bins.append(x)
        nbins += 1
    bins.append(y)
    
    muTauFR = []
    jetTauFR = []
    qcdNorm = []
    tauID = []
    ib = 1
    for etabin in etaRange:

        inputFitFileName = '%s/%s_fit.root'%(cardsfolder,etabin)
        if not os.path.isfile(inputFitFileName):
            print('No fit results are found for bin %s'%(etabin))
            print('Make sure that datacards are created and run fit')
            print('Quitting')
            exit()
        inputFitFile = ROOT.TFile(inputFitFileName,'read')
        fitResult = inputFitFile.Get('fit_s')
        pars = fitResult.floatParsFinal()
        norm = 1
        normE = 0.1
        rpass = 1.
        rpassE = 0.1
        jfake_n = 1.0
        jfakeE_n = 0.1
        normZtt = 1.0
        normZttE = 0.1
        qcd_n = 1.0
        qcdE_n = 0.1
        for par in pars:
            if par.GetName()=='r': 
                norm = par.getVal()
                normE = par.getError()
            if par.GetName()=='r_pass':
                rpass = par.getVal()
                rpassE = par.getError()
            if par.GetName()=='jet_to_tauFR':
                jfake_n = par.getVal()
                jfakeE_n = par.getError()
            if par.GetName()=='tauID':
                normZtt = par.getVal()
                normZttE = par.getError()
            if par.GetName()=='normQCD':
                qcd_n = par.getVal()
                qcdE_n = par.getError()
        mutauFR = norm*rpass
        mutauFRE = math.sqrt(norm*norm*rpassE*rpassE+rpass*rpass*normE*normE)
        jtauFR = 1.0 + 0.2*jfake_n
        jtauFRE = 0.2*jfakeE_n
        normQCD = 1.0 + 0.2*qcd_n
        normQCDE = 0.2*qcdE_n
        print('%s -> muTauFR=%5.3f+/-%5.3f jetTauFR=%5.3f+/-%5.3f ZTTnorm=%5.3f+/-%5.3f QCDnorm=%5.3f+/-%5.3f'
              %(etabin,mutauFR,mutauFRE,jtauFR,jtauFRE,normZtt,normZttE,normQCD,normQCDE))
        muTauFR.append((mutauFR,mutauFRE))
        jetTauFR.append((jtauFR,jtauFRE))
        tauID.append((normZtt,normZttE))
        qcdNorm.append((normQCD,normQCDE))
        inputFitFile.Close()

    histMuTauFR = ROOT.TH1D('muTauFR','',nbins,array('d',list(bins)))
    histJetTauFR = ROOT.TH1D('jetTauFR','',nbins,array('d',list(bins)))
    histTauID = ROOT.TH1D('tauID','',nbins,array('d',list(bins)))
    histQCDNorm = ROOT.TH1D('qcdNorm','',nbins,array('d',list(bins)))
    for ib in range(nbins):
        histMuTauFR.SetBinContent(ib+1,muTauFR[ib][0])
        histMuTauFR.SetBinError(ib+1,muTauFR[ib][1])
        histJetTauFR.SetBinContent(ib+1,jetTauFR[ib][0])
        histJetTauFR.SetBinError(ib+1,jetTauFR[ib][1])
        histTauID.SetBinContent(ib+1,tauID[ib][0])
        histTauID.SetBinError(ib+1,tauID[ib][1])
        histQCDNorm.SetBinContent(ib+1,qcdNorm[ib][0])
        histQCDNorm.SetBinError(ib+1,qcdNorm[ib][1])
        
    outputfileName = f'{histfolder}/{outname}.root'
    outputFile = ROOT.TFile(outputfileName,'recreate')
    suffix = '%sVsJet_%sVsMu_%sVsE'%(wpVsJet,wpVsMu,wpVsE)
    outputFile.cd('')
    histMuTauFR.Write('muTauFR_%s'%(suffix))
    histJetTauFR.Write('jetTauFR_%s'%(suffix))
    histTauID.Write('tauID_%s'%(suffix))
    histQCDNorm.Write('qcdNorm_%s'%(suffix))
    outputFile.Close()

###############################
#### Running fits #############
###############################        
def RunFit(**kwargs):

    era = kwargs.get('era','2024')
    wpVsJet = kwargs.get('wpVsJet','Medium')
    wpVsMu = kwargs.get('wpVsMu','VLoose')
    wpVsE = kwargs.get('wpVsE','VVLoose')
    dm = kwargs.get('dm','1prong')

    cmssw_base = os.getenv('CMSSW_BASE') 

    basefolder = f'{cmssw_base}/src/TauFW/Fitter/MuTauFR'
    folder = f'{basefolder}/datacards/{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE_{dm}'
    if not os.path.isdir(folder):
        print('folder {folder} does not exist')
        print('quitting')
        exit()
        
    command = f'cd {folder} ; '
    for etabin in utils.etabins:
        command += f'combineTool.py -M T2W -o {etabin}_ws.root -i {etabin}.txt -m 90  ; ' 
        command += f'combineTool.py -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL -m 90 --robustHesse 1 -d {etabin}_ws.root --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 0 -v 2 ; '
        command += f'cp fitDiagnostics.Test.root {etabin}_fit.root ; '
    command += f'cd {basefolder}' 
    os.system(command)

    
def WriteDatacards(**kwargs): 

    iwp = kwargs.get('wpVsMu','VLoose')
    wp_vs_jet = kwargs.get('wpVsJet','Medium')
    wp_vs_e = kwargs.get('wpVsE','VVLoose')
    era = kwargs.get('era','2024')
    dm = kwargs.get('dm','1prong')
    cmssw_base = os.getenv('CMSSW_BASE')
    subfolder = f'{era}_{wp_vs_jet}VsJet_{iwp}VsMu_{wp_vs_e}VsE_{dm}'
    path2files = f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/datacards/{subfolder}'
    path2cards = ensuredir(f'{cmssw_base}/src/TauFW/Fitter/MuTauFR/datacards/{subfolder}')
    
    for etabin in utils.etabins:
        print('<<<<<<< eta range: ', etabin)
        #cb.SetFlag('workspaces-use-clone', True)
        cb = ch.CombineHarvester()
        mc_backgrounds = ['ZTT','ZJ','W','TTT','TTL','TTJ', 'VV']
        data_driven_backgrounds = ['QCD']
        backgrounds = mc_backgrounds + data_driven_backgrounds
        signals = ['ZL']
        categories = {
            'mutau_pass' : [( 1, 'pass' )],
            'mutau_fail' : [( 2, 'fail' )],
        }
        cb.AddObservations(['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'],              categories['mutau_pass']) # adding observed data
        cb.AddObservations(['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'],              categories['mutau_fail']) # adding observed data
        cb.AddProcesses(   ['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'], backgrounds, categories['mutau_pass'], False) # adding backgrounds
        cb.AddProcesses(   ['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'], backgrounds, categories['mutau_fail'], False) # adding backgrounds
        cb.AddProcesses(   ['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'], signals,     categories['mutau_pass'], True) # adding signals
        cb.AddProcesses(   ['*'], ['MuTauFR'], ['%s'%(era)], ['mutau'], signals,     categories['mutau_fail'], True) # adding signals

        cb.cp().process(mc_backgrounds+signals).AddSyst(cb, 'lumi_2024',   'lnN', ch.SystMap()(1.026))
        cb.cp().process(mc_backgrounds+signals).AddSyst(cb, 'CMS_eff_mu',  'lnN', ch.SystMap()(1.02))
        cb.cp().process(['TTT','ZTT'])         .AddSyst(cb, 'CMS_eff_t',   'lnN', ch.SystMap()(1.15))
        cb.cp().process(['ZJ','TTJ','W'])      .AddSyst(cb, 'jet_to_tauFR','lnN', ch.SystMap()(1.15))
        cb.cp().process(['TTT','TTL','TTJ'])   .AddSyst(cb, 'xsec_top',    'lnN', ch.SystMap()(1.06))
        cb.cp().process(['VV'])                .AddSyst(cb, 'xsec_vv',     'lnN', ch.SystMap()(1.06))
        cb.cp().process(['ZL','ZTT','ZJ'])     .AddSyst(cb, 'xsec_zjets',  'lnN', ch.SystMap()(1.03))
        cb.cp().process(['W'])                 .AddSyst(cb, 'xsec_wjets',  'lnN', ch.SystMap()(1.08))
        cb.cp().process(['QCD'])               .AddSyst(cb, 'normQCD',     'lnN', ch.SystMap()(1.15))
        #        cb.cp().process(['bkgd'])              .AddSyst(cb, 'normBKGD',    'lnN', ch.SystMap()(1.20))
        
        #        cb.cp().AddSyst(cb, 'norm_zmm', 'rateParam', ch.SystMap('process')(['ZL'],1.0)) #12.09.23 Stepan Zakharov    
        #        cb.cp().GetParameter('norm_zmm').set_range(0.5,6)
        
#        cb.cp().process(['ZTT','TTT']).AddSyst(cb, 'tauID', 'rateParam', ch.SystMap('bin_id')([1],1.00)) # unconstrained tauID
#        cb.cp().GetParameter('tauID').set_range(0.5,1.5)
        
        cb.cp().process(['ZTT','TTT'])              .AddSyst(cb, 'TES', 'shape', ch.SystMap()(1.0))
        cb.cp().process(['ZL','TTL'])               .AddSyst(cb, 'FES', 'shape', ch.SystMap()(1.0))
        #        cb.cp().process(['ZL'])                    .AddSyst(cb, 'shape_res', 'shape', ch.SystMap()(1.0))
        cb.cp().process(['ZL','TTL']).AddSyst(cb, 'r_pass', 'rateParam', ch.SystMap('bin_id')([1],1.0))
        #        cb.cp().process(['ZL']).AddSyst(cb, 'r_pass', 'rateParam', ch.SystMap('bin_id')([1],1.0))
        cb.cp().GetParameter('r_pass').set_range(0.5,3)

        filepath = os.path.join(path2files,"%s_inputs.root")%(etabin)
        print(filepath)
        processName = '$BIN/$PROCESS'
        systematicName = '%s$BIN/$PROCESS_$SYSTEMATIC'%(iwp)
        systematicName = '$BIN/$PROCESS_$SYSTEMATIC'
        cb.cp().backgrounds().ExtractShapes(filepath, processName, systematicName)
        cb.cp().signals().ExtractShapes(filepath, processName, systematicName)
        
        n_zmm_pass = cb.cp().bin_id([1]).process(['ZL']).GetRate()
        n_zmm_pass += cb.cp().bin_id([1]).process(['TTL']).GetRate()
        n_zmm_fail = cb.cp().bin_id([2]).process(['ZL']).GetRate()
        n_zmm_fail += cb.cp().bin_id([2]).process(['TTL']).GetRate()
        #       dn_zmm_pass = cb.cp().bin(['%s_pass'%(iwp)]).process(['ZL']).GetUncertainty()
        #       dn_zmm_fail = cb.cp().bin(['%s_fail'%(iwp)]).process(['ZL']).GetUncertainty()
        
        prefit_FR = n_zmm_pass / (n_zmm_pass + n_zmm_fail)
        #SF_zmm_fail_formula = "(@0-@1*{0})/(1-{0})".format(prefit_FR)
                
        #cb.cp().process(['ZL']).AddSyst(cb, 'SF_zmm_fail', 'rateParam', ch.SystMap('bin_id')([2],(SF_zmm_fail_formula, "norm_zmm,SF_zmm_pass")))
        
        ### Check of potential bug in the SF_fail region###
        SF_zmm_fail_formula = "(1-@0*{0})/(1-{0})".format(prefit_FR)
        cb.cp().process(['ZL','TTL']).AddSyst(cb, 'SF_zmm_fail', 'rateParam', ch.SystMap('bin_id')([2],(SF_zmm_fail_formula, "r_pass")))
        ###################################################
        
        #cb.AddDatacardLineAtEnd("* autoMCStats 0")
        ch.SetStandardBinNames(cb, '$BIN')
        bbb = ch.BinByBinFactory()
        bbb.SetAddThreshold(0.2).SetMergeThreshold(0.5).SetFixNorm(True)
        bbb.MergeBinErrors(cb.cp().backgrounds())
        bbb.AddBinByBin(cb.cp().backgrounds(), cb)

        datacardPath = '%s/%s.txt'%(path2cards,etabin)
        shapePath = '%s/%s.root'%(path2cards,etabin)
        writer = ch.CardWriter(datacardPath,shapePath)
        writer.SetWildcardMasses([])
        writer.WriteCards('cmb', cb) # writing all datacards into one folder for combination

##########################################
### Extracting histograms from RooT file #
##########################################
def ExtractHistos(f,bins,**kwargs):

    region = kwargs.get('region','pass')
    dm = kwargs.get('dm','1prong')
    etabin = kwargs.get('etabin','0p0to0p4')
    
    hists = {}
    procs = ['Data','ZTT','ZL','ZJ','TTT','TTL','TTJ','W','VV']
    for proc in procs:
        for sign in ['os','ss']:
            if etabin=='eta1p2to2p5':
                name1 = f'{proc}_m_vis_{sign}_{dm}_{region}_eta1p2to1p7'
                name2 = f'{proc}_m_vis_{sign}_{dm}_{region}_eta1p7to2p5'
                hist1 = utils.rebinHisto(f.Get(name1),bins,'rebinned')
                hist2 = utils.rebinHisto(f.Get(name2),bins,'rebinned')
                hist1.Add(hist1,hist2,1.,1.)
                outname = f'{proc}_{sign}'
                hists[outname] = hist1
            else:
                name = f'{proc}_m_vis_{sign}_{dm}_{region}_{etabin}'
                outname = f'{proc}_{sign}'
                hists[outname] = utils.rebinHisto(f.Get(name),bins,'rebinned')
            for sys in ['up','down']:
                if etabin=='eta1p2to2p5':
                    name1 = f'{proc}_m_vis_{sign}_{dm}_{region}_eta1p2to1p7_{sys}'
                    name2 = f'{proc}_m_vis_{sign}_{dm}_{region}_eta1p7to2p5_{sys}'
                    hist1 = utils.rebinHisto(f.Get(name1),bins,'rebinned')
                    hist2 = utils.rebinHisto(f.Get(name2),bins,'rebinned')
                    hist1.Add(hist1,hist2,1.,1.)
                    outname = f'{proc}_{sign}_{sys}'
                    hists[outname] = hist1
                else:
                    name = f'{proc}_m_vis_{sign}_{dm}_{region}_{etabin}_{sys}'
                    outname = f'{proc}_{sign}_{sys}'
                    hists[outname] = utils.rebinHisto(f.Get(name),bins,'rebinned')

    hists_out = {}
    # observed data 
    hists_out['data_obs'] = hists['Data_os']
    # VV
    hists_out['VV'] = hists['VV_os']
    # W 
    hists_out['W'] = hists['W_os']
    # TT 
    hists_out['TTL'] = hists['TTL_os']
    hists_out['TTL_FESUp'] = hists['TTL_os_up']
    hists_out['TTL_FESDown'] = hists['TTL_os_down']
    # TTT
    hists_out['TTT'] = hists['TTT_os']
    hists_out['TTT_TESUp'] = hists['TTT_os_up']
    hists_out['TTT_TESDown'] = hists['TTT_os_down']
    # TTJ
    hists_out['TTJ'] = hists['TTJ_os']
    # ZL
    hists_out['ZL'] = hists['ZL_os']
    hists_out['ZL_FESUp'] = hists['ZL_os_up']
    hists_out['ZL_FESDown'] = hists['ZL_os_down']
    # ZTT
    hists_out['ZTT'] = hists['ZTT_os']
    hists_out['ZTT_TESUp'] = hists['ZTT_os_up']
    hists_out['ZTT_TESDown'] = hists['ZTT_os_down']
    # ZJ
    hists_out['ZJ'] = hists['ZJ_os']
    # QCD
    hists_out['QCD'] = hists['Data_ss']
    procs = ['ZTT','ZL','ZJ','TTT','TTL','TTJ','W','VV']
    for proc in procs:
        hists_out['QCD'].Add(hists_out['QCD'],hists[f'{proc}_ss'],1.,-1.)

    return hists_out

