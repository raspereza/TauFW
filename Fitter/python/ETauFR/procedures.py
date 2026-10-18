import ROOT
import math
import TauFW.Fitter.ETauFR.utils as utils
import TauFW.Fitter.ETauFR.styles as styles
import TauFW.Fitter.ETauFR.analysisETauFR as analysis
from TauFW.Plotter.plot.utils import ensuredir

from array import array
import os
from CombineHarvester.CombineTools import ch
from CombineHarvester.CombineTools.ch import CombineHarvester, MassesFromRange, SystMap, BinByBinFactory, CardWriter, SetStandardBinNames, AutoRebin
import CombineHarvester.CombinePdfs.morphing as morphing
from CombineHarvester.CombinePdfs.morphing import BuildRooMorphing
from CombineHarvester.CombinePdfs.morphing import BuildCMSHistFuncFactory

import ROOT
from ROOT import RooWorkspace, TFile, RooRealVar

###################################
####  Extracing scale factors #####
###################################
def ExtractScaleFactors(**kwargs):

    era = kwargs.get('era','2526')
    wpVsMu = kwargs.get('wpVsMu','VLoose')
    wpVsJet = kwargs.get('wpVsJet','Medium')
    wpVsE = kwargs.get('wpVsE','VVLoose')
    fes = kwargs.get('fes',False)
    
    cmssw_base = os.getenv('CMSSW_BASE')
    name = f'{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE'
    wp_name = '%sVsJet_%sVsMu_%sVsE'%(wpVsJet,wpVsMu,wpVsE)

    cardsfolder = f'{cmssw_base}/src/TauFW/Fitter/ETauFR/datacards/{name}'
    if fes:
        cardsfolder = f'{cmssw_base}/src/TauFW/Fitter/ETauFR/datacards_fes/{name}'
    print(f'{cardsfolder}')
    outfolder = f'{cmssw_base}/src/TauFW/Fitter/ETauFR/ScaleFactors'
    if fes:
        outfolder = ensuredir(f'{cmssw_base}/src/TauFW/Fitter/ETauFR/ScaleFactors_fes')
    histfolder = ensuredir(outfolder)
    
    if not os.path.isdir(cardsfolder):
        print('folder %s does not exist'%(cardsfolder))
        print('create datacards for respective WPs and run fit on them')
        print('quitting')
        exit()

    nbinsDM = 4
    binsDM = []
    xmin = 0.
    for ib in range(nbinsDM+1):
        xbin = xmin + float(ib)
        binsDM.append(xbin)

    nbinsEta = 0
    binsEta = []
    final_bin = 0
    for etabin in utils.etabins:
        nbinsEta += 1
        binsEta.append(utils.etabins[etabin][0])
        final_bin = utils.etabins[etabin][1]        
    binsEta.append(final_bin)

    tuple_eTauFR = []
    tuple_jetTauFR = []
    tuple_FES = []
    tuple_tauID = []

    print(' eta - DM     |  e->tau FR  |  j->tau FR  |    tauID    |     FES    ')
    print('--------------+-------------+-------------+-------------+------------')
#    print('Barrel -  DM0 | 1.27+/-0.06 | 0.69+/-0.12 | 1.27+/-0.07 | 0.80+/-0.17')

    for etabin in utils.etabins:
        for dm in utils.dm_meas:
            decayMode = utils.dm_meas[dm]
            etaIndx = 0.5*(utils.etabins[etabin][0]+utils.etabins[etabin][1])
            inputFitFileName = '%s/%s_%s_fit.root'%(cardsfolder,etabin,dm)
            if not os.path.isfile(inputFitFileName):
                print('No file with fit results is found for %s and %s'%(etabin,dm))
                print('Setting scale factors to 1.')
                tuple_eTauFR.append((etaIndx,decayMode,1.0,0.0))
                tuple_jetTauFR.append((etaIndx,decayMode,1.0,0.0))
                tuple_tauID.append((etaIndx,decayMode,1.0,0.0))
                tuple_FES.append((etaIndx,decayMode,1.0,0.0))
                continue
                
            inputFitFile = ROOT.TFile(inputFitFileName,'read')
            fitResult = inputFitFile.Get('fit_s')
            if fitResult==None:
                print('No fit results is found for %s and %s'%(etabin,dm))
                print('setting scale factors to 1.0')
                tuple_eTauFR.append((etaIndx,decayMode,1.0,0.0))
                tuple_jetTauFR.append((etaIndx,decayMode,1.0,0.0))
                tuple_tauID.append((etaIndx,decayMode,1.0,0.0))
                tuple_FES.append((etaIndx,decayMode,1.0,0.0))
                continue
            
            pars = fitResult.floatParsFinal()
            if pars==None:
                print('No fit results is found for %s and %s'%(etabin,dm))
                print('setting scale factors to 1.0')
                tuple_eTauFR.append((etaIndx,decayMode,1.0,0.0))
                tuple_jetTauFR.append((etaIndx,decayMode,1.0,0.0))
                tuple_tauID.append((etaIndx,decayMode,1.0,0.0))
                tuple_FES.append((etaIndx,decayMode,1.0,0.0))
                continue
            
            r_par = pars.find('r')
            rpass_par = pars.find('r_pass')
            jtau_par = pars.find('jet_to_tauFR')
            tauID_par = pars.find('tauID')
            fes_par = pars.find('FES')

            norm = r_par.getVal()
            sf = rpass_par.getVal()
            etauFR_formula = ROOT.RooFormulaVar('etau_FR', 'x[0]*x[1]',ROOT.RooArgList(r_par,rpass_par)) 
            etauFR = norm*sf
            etauFRE = etauFR_formula.getPropagatedError(fitResult)
            
            jtauFR  = 1.0 + utils.unc_jfake * jtau_par.getVal()
            jtauFRE = utils.unc_jfake * jtau_par.getError()

            tauID  = 1.0 + utils.unc_tauID * tauID_par.getVal()
            tauIDE = utils.unc_tauID * tauID_par.getError()

            FES = fes_par.getVal()
            FESE = fes_par.getError()
            if not fes:
                FES = 1.0 + utils.unc_fes * FES
                FESE = utils.unc_fes * FESE
            
            print('%6s - %4s | %4.2f+/-%4.2f | %4.2f+/-%4.2f | %4.2f+/-%4.2f | %4.2f+/-%4.2f'%(utils.etaTitle[etabin],dm,etauFR,etauFRE,jtauFR,jtauFRE,tauID,tauIDE,FES,FESE))
            
            inputFitFile.Close()
            
            tuple_eTauFR.append((etaIndx,decayMode,etauFR,etauFRE))
            tuple_jetTauFR.append((etaIndx,decayMode,jtauFR,jtauFRE))
            tuple_tauID.append((etaIndx,decayMode,tauID,tauIDE))
            tuple_FES.append((etaIndx,decayMode,FES,FESE))

    outputfileName = f'{histfolder}/{name}.root'
    outputFile = ROOT.TFile(outputfileName,'recreate')
    suffix = '%sVsJet_%sVsMu_%sVsE'%(wpVsJet,wpVsMu,wpVsE)
    outputFile.cd('')

    histnames = ['eTauFR','jetTauFR','tauID','FES']
    hists = {}
    tuples = {
        'eTauFR':   tuple_eTauFR,
        'jetTauFR': tuple_jetTauFR,
        'tauID':    tuple_tauID,
        'FES':  tuple_FES,
    }
    
    for histname in histnames:
        hists[histname] = ROOT.TH2D(histname,'',nbinsEta,array('d',list(binsEta)),nbinsDM,array('d',list(binsDM)))
        utils.unitBinContents2D(hists[histname])
        for tupl in tuples[histname]:
            indx = hists[histname].FindBin(tupl[0],tupl[1])
            content = tupl[2]
            error = tupl[3]
            hists[histname].SetBinContent(indx,content)
            hists[histname].SetBinError(indx,error)
        outputname = histname+'_'+wp_name
        hists[histname].Write(outputname)
    outputFile.Close()

###############################
#### Running fits #############
###############################
def RunFit(**kwargs):

    era = kwargs.get('era','2526')
    wpVsJet = kwargs.get('wpVsJet','Medium')
    wpVsMu = kwargs.get('wpVsMu','VLoose')
    wpVsE = kwargs.get('wpVsE','VVLoose')
    etabin = kwargs.get('etabin','eta0p0to1p48')
    dm = kwargs.get('dm','DM0')
    fes = kwargs.get('fes',False)
    
    cmssw_base = os.getenv('CMSSW_BASE') 
    basefolder = f'{cmssw_base}/src/TauFW/Fitter/ETauFR'
    folder = f'{basefolder}/datacards/{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE'
    if fes:
        folder = f'{basefolder}/datacards_fes/{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE'
    if not os.path.isdir(folder):
        print('folder %s does not exist'%s(folder))
        print('quitting')
        exit()
        
    command = f'cd {folder} ; '
    command += f'combineTool.py -M T2W -o {etabin}_{dm}_ws.root -i {etabin}_{dm}.txt -m 90  ; '
    if fes:
        command += f'combineTool.py -M FitDiagnostics --redefineSignalPOIs r,FES --setParameters r=1,FES=1 --setParameterRanges r=0.5,2.5:fes=0.5,1.5:r_pass=0.5:3. --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL -m 90 --robustHesse 1 -d {etabin}_{dm}_ws.root --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --skipBOnlyFit --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1 -v 1 ; '
    else:
        command += f'combineTool.py -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL -m 90 --robustHesse 1 -d {etabin}_{dm}_ws.root --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --skipBOnlyFit --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1 -v 1 ; '
        
    command += f'cp fitDiagnostics.Test.root {etabin}_{dm}_fit.root ; '
    command += f'cd {basefolder}' 
    os.system(command)
    
def WriteDatacards(**kwargs): 

    iwp = kwargs.get('wpVsMu','VLoose')
    wp_vs_jet = kwargs.get('wpVsJet','Medium')
    wp_vs_e = kwargs.get('wpVsE','VVLoose')
    era = kwargs.get('era','2526')
    fes = kwargs.get('fes',False)

    cmssw_base = os.getenv('CMSSW_BASE')    
    subfolder = f'{era}_{wp_vs_jet}VsJet_{iwp}VsMu_{wp_vs_e}VsE'
    path2files = f'{cmssw_base}/src/TauFW/Fitter/ETauFR/datacards/{subfolder}'
    if fes:
        path2files = f'{cmssw_base}/src/TauFW/Fitter/ETauFR/datacards_fes/{subfolder}'
    path2cards = ensuredir(path2files)

    unc_jfake = 1.0+utils.unc_jfake
    unc_qcd = 1.0+utils.unc_qcd
    unc_tauID = 1.0+utils.unc_tauID
    
    tes_char = []
    tes_vars = []
    tes_min = 2.0
    tes_max = 0.0
    for tes in utils.sys_TES:
        value = utils.sys_TES[tes]
        tes_vars.append(value)
        tes_char.append('%4.2f'%value)

    for etabin in utils.etabins:
        for dm in utils.dm_meas:
            print('<<<<<<< eta range: ', etabin,'  dm: ',dm)
            #cb.SetFlag('workspaces-use-clone', True)
            cb = ch.CombineHarvester()
            mc_backgrounds = ['ZTT','ZJ','W','TTT','TTL','TTJ', 'VV']
            data_driven_backgrounds = ['QCD']
            backgrounds = mc_backgrounds + data_driven_backgrounds
            signals = ['ZL']
            mc_samples = signals + mc_backgrounds
            categories = {
                'etau_pass' : [( 1, 'pass' )],
                'etau_fail' : [( 2, 'fail' )],
            }
            
            cb.AddObservations(['*'],['ETauFR'],['%s'%(era)],['etau'],categories['etau_pass'])
            cb.AddObservations(['*'],['ETauFR'],['%s'%(era)],['etau'],categories['etau_fail'])
            cb.AddProcesses(['*'],['ETauFR'],['%s'%(era)],['etau'],backgrounds,categories['etau_pass'],False)
            cb.AddProcesses(['*'],['ETauFR'],['%s'%(era)],['etau'],backgrounds,categories['etau_fail'],False)
            if fes:
                cb.AddProcesses(tes_char,['ETauFR'],['%s'%(era)],['etau'],signals,categories['etau_pass'],True)
                cb.AddProcesses(tes_char,['ETauFR'],['%s'%(era)],['etau'],signals,categories['etau_fail'],True)
            else:
                cb.AddProcesses(['*'],['ETauFR'],['%s'%(era)],['etau'],signals,categories['etau_pass'],True)
                cb.AddProcesses(['*'],['ETauFR'],['%s'%(era)],['etau'],signals,categories['etau_fail'],True)
                
            cb.cp().process(mc_backgrounds+signals).AddSyst(cb, 'lumi',        'lnN', ch.SystMap()(1.026))
            cb.cp().process(mc_backgrounds+signals).AddSyst(cb, 'CMS_eff_e',   'lnN', ch.SystMap()(1.02))

            cb.cp().process(['ZJ','TTJ','W'])   .AddSyst(cb, 'jet_to_tauFR','lnN', ch.SystMap()(unc_jfake))
            cb.cp().process(['TTT','TTL','TTJ']).AddSyst(cb, 'xsec_top',    'lnN', ch.SystMap()(1.06))
            cb.cp().process(['VV'])             .AddSyst(cb, 'xsec_vv',     'lnN', ch.SystMap()(1.06))
            cb.cp().process(['ZL','ZTT','ZJ'])  .AddSyst(cb, 'xsec_zjets',  'lnN', ch.SystMap()(1.03))
            cb.cp().process(['W'])              .AddSyst(cb, 'xsec_wjets',  'lnN', ch.SystMap()(1.08))
            cb.cp().process(['QCD'])            .AddSyst(cb, 'normQCD',     'lnN', ch.SystMap()(unc_qcd))
            cb.cp().process(['ZTT'])      .AddSyst(cb, 'tauID', 'lnN', ch.SystMap('bin_id')([1],unc_tauID))

            
            cb.cp().process(['ZTT','TTT'])             .AddSyst(cb, 'TES', 'shape', ch.SystMap()(1.0))
            cb.cp().process(['ZTT','TTT','TTL','VV','W','ZL']).AddSyst(cb, 'EES', 'shape', ch.SystMap()(1.0))

            
            cb.cp().process(['ZL']).AddSyst(cb, 'r_pass', 'rateParam', ch.SystMap('bin_id')([1],1.0))
            cb.cp().GetParameter('r_pass').set_range(0.1,4.0)
            if not fes:
                cb.cp().process(['ZL']).AddSyst(cb, 'FES', 'shape', ch.SystMap()(1.0))
            
            filepath = os.path.join(path2files,"%s_%s_inputs.root")%(etabin,dm)
            processName = '$BIN/$PROCESS'
            systematicName = '$BIN/$PROCESS_$SYSTEMATIC'
            cb.cp().backgrounds().ExtractShapes(filepath, processName, systematicName)
            if fes:
                processNameMorph = "$BIN/$PROCESS_FES$MASS"
                cb.cp().process(['ZL']).ExtractShapes(filepath,processNameMorph,systematicName)
            else:
                cb.cp().process(['ZL']).ExtractShapes(filepath, processName, systematicName)
                                 
            n_zee_pass = cb.cp().bin_id([1]).process(['ZL']).GetRate()
            n_zee_fail = cb.cp().bin_id([2]).process(['ZL']).GetRate()
            #dn_zee_pass = cb.cp().bin(['%s_pass'%(iwp)]).process(['ZL']).GetUncertainty()
            #dn_zee_fail = cb.cp().bin(['%s_fail'%(iwp)]).process(['ZL']).GetUncertainty()
        
            prefit_FR = n_zee_pass / (n_zee_pass + n_zee_fail)        

            SF_zee_fail_formula = "(1-@0*{0})/(1-{0})".format(prefit_FR)
            cb.cp().process(['ZL']).AddSyst(cb, 'SF_zee_fail', 'rateParam', ch.SystMap('bin_id')([2],(SF_zee_fail_formula, "r_pass")))



            ch.SetStandardBinNames(cb, '$BIN')
            
            ###################################################

            if fes:
                workspace = RooWorkspace('ETauFR','ETauFR')
                fes = RooRealVar('FES','FES',min(tes_vars),max(tes_vars))
                fes.setConstant(True)
                BuildCMSHistFuncFactory(workspace, cb, fes, 'ZL')
                cb.AddWorkspace(workspace,False)
                cb.ExtractPdfs(cb, "ETauFR", "$BIN_$PROCESS_morph", "")
                cb.ExtractData("ETauFR", "$BIN_data_obs")
                cb.SetAutoMCStats(cb, 0, 1, 1)
            else:
                #cb.AddDatacardLineAtEnd("* autoMCStats 0")
                bbb = ch.BinByBinFactory()
                bbb.SetAddThreshold(0.2).SetMergeThreshold(0.5).SetFixNorm(True)
                bbb.MergeBinErrors(cb.cp().backgrounds())
                bbb.AddBinByBin(cb.cp().backgrounds(), cb)

            datacardPath = '%s/%s_%s.txt'%(path2cards,etabin,dm)
            shapePath = '%s/%s_%s.root'%(path2cards,etabin,dm)
            writer = ch.CardWriter(datacardPath,shapePath)
            writer.SetWildcardMasses([])
            writer.WriteCards('cmb', cb) # writing all datacards into one folder for combination

##########################################
### Extracting histograms from RooT file #
##########################################
def ExtractHistos(f,bins,**kwargs):

    region = kwargs.get('region','pass')
    dm = kwargs.get('dm','DM0')
    etabin = kwargs.get('etabin','0p0to1p48')
    
    hists = {}
    procs = ['Data','ZTT','ZL','ZJ','TTT','TTL','TTJ','W','VV']
    for proc in procs:
        for sign in ['os','ss']:
            name = f'{proc}_m_vis_{sign}_{dm}_{region}_{etabin}'
            outname = f'{proc}_{sign}'
            hists[outname] = utils.rebinHisto(f.Get(name),bins,'rebinned')
            for sys in utils.sys_TES:
                name = f'{proc}_m_vis_{sign}_{dm}_{region}_{etabin}_{sys}'
                outname = f'{proc}_{sign}_{sys}'
                hists[outname] = utils.rebinHisto(f.Get(name),bins,'rebinned')
            for sys in utils.sys_EES:
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
    # TTL 
    hists_out['TTL'] = hists['TTL_os']
    # TTT
    hists_out['TTT'] = hists['TTT_os']
    hists_out['TTT_TESUp'] = hists['TTT_os_TES1.04']
    hists_out['TTT_TESDown'] = hists['TTT_os_TES0.96']
    # TTJ
    hists_out['TTJ'] = hists['TTJ_os']
    # ZL
    hists_out['ZL'] = hists['ZL_os']
    hists_out['ZL_FESUp'] = hists['ZL_os_TES1.06']
    hists_out['ZL_FESDown'] = hists['ZL_os_TES0.94']
    # ZTT
    hists_out['ZTT'] = hists['ZTT_os']
    hists_out['ZTT_TESUp'] = hists['ZTT_os_TES1.02']
    hists_out['ZTT_TESDown'] = hists['ZTT_os_TES0.98']
    # ZJ
    hists_out['ZJ'] = hists['ZJ_os']
    for s in ['ZTT','ZL','ZJ','TTT','TTJ','TTL','W','VV']:
        hists_out['%s_EESUp'%(s)]=hists['%s_os_EES1.02'%(s)]
        hists_out['%s_EESDown'%(s)]=hists['%s_os_EES0.98'%(s)]
    for sys in utils.sys_TES:
        shift = utils.sys_TES[sys]
        hists_out['ZL_FES%.2f'%(shift)]=hists['ZL_os_%s'%(sys)]
    
    # QCD
    hists_out['QCD'] = hists['Data_ss']
    procs = ['ZTT','ZL','ZJ','TTT','TTL','TTJ','W','VV']
    for proc in procs:
        hists_out['QCD'].Add(hists_out['QCD'],hists[f'{proc}_ss'],1.,-1.)

    return hists_out

