import ROOT 
import math
from array import array
import numpy as np
import os

############################
## mu->tau FR measurement ##
##### General settings #####
############################

#########################
# folder for picotuples #
#########################
picoFolder= {
    '2526': '/eos/cms/store/group/phys_tau/rasp/ETau_FR',
    '2026': '/eos/cms/store/group/phys_tau/rasp/ETau_FR',
    '2025': '/eos/cms/store/group/phys_tau/rasp/ETau_FR',
    }
####################################################
# folders needs to be set by user                  #
# outputFolder - folder to store output RooT files #
#                with histograms after selection   #
# condorFolder - folder to store scripts           #
#                for submitting jobs to condor     #
####################################################
outputFolder = '/afs/cern.ch/work/r/rasp/ETauFR/selection' 
condorFolder = '/afs/cern.ch/work/r/rasp/ETauFR/condor' 
figuresFolder = '/eos/home-r/rasp/php-plots/plots/ETauFR'

###################
# Cross sections  #
###################

# k-factors for cross sections at 13.6 TeV
kfactor_dy_powheg = 6282.6/6731.99 # LO->NNLO+NLO_EW k-factor computed for 13.6 TeV
kfactor_dy=6282.6/5455.0 # LO->NNLO+NLO_EW k-factor computed for 13.6 TeV
kfactor_wj=0.93 # LO->NNLO+NLO_EW k-factor computed for 13.6 TeV
kfactor_ttbar=923.6/762.1 # NLO->NNLO k-factor computed for 13.6 TeV
kfactor_ww=1.524 # LO->NNLO+NLO_EW computed for 13.6 TeV
kfactor_zz=1.524 # LO->NNLO+NLO_EW computed for 13.6 TeV
kfactor_wz=1.414 # LO->NNLO+NLO_EW computed for 13.6 TeV 

mc_samples = {
    '2526': {
        #      Name  :  (xsec, nevts, group, split by genmatch_2)
        #    nevts = -1 implies that total number of events is
        #               taken from bin 16 of the cutflow histogram
        "DYto2E_Bin-MLL-10to50"   : (6744.0, -1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2E_Bin-MLL-50to120"  : (2219*kfactor_dy_powheg, -1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2E_Bin-MLL-120to200" : (21.65*kfactor_dy_powheg,-1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2Tau_Bin-MLL-50to120" : (2219*kfactor_dy_powheg, -1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2Tau_Bin-MLL-120to200" : (21.65*kfactor_dy_powheg, -1, "DY", ['ZTT','ZL','ZJ']),
        "WtoENu-2Jets" : (22666.*kfactor_wj, -1, "WJ", ['W']),
        "WtoTauNu-2Jets" : (22666.*kfactor_wj, -1, "WJ", ['W']),
        "TTto2L2Nu" : (80.9*kfactor_ttbar, -1, "TT", ['TTT','TTL','TTJ']),
        "TTtoLNu2Q" : (334.8*kfactor_ttbar, -1, "TT", ['TTT','TTL', 'TTJ']),
        "TWminustoLNu2Q" : (15.8, -1, "ST", ['VV']),
        "TWminusto2L2Nu" : (3.8, -1, "ST", ['VV']),
        "TbarWplustoLNu2Q" : (15.9, -1, "ST", ['VV']),
        "TbarWplusto2L2Nu" : (3.8, -1, "ST", ['VV']),
        "WZ" : (29.1*kfactor_wz, -1, "VV", ['VV']),
        "ZZ" : (12.75*kfactor_zz, -1, "VV", ['VV']),
        "WWto2L2Nu" : (11.79*kfactor_ww, -1, "VV", ['VV']),
        "WWtoLNu2Q" : (48.94*kfactor_ww, -1, "VV", ['VV']),
    },
    '2026': {
        #      Name  :  (xsec, nevts, group, split by genmatch_2)
        #    nevts = -1 implies that total number of events is
        #               taken from bin 16 of the cutflow histogram
        "DYto2E_Bin-MLL-10to50"   : (6744.0, -1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2E_Bin-MLL-50to120"  : (2219*kfactor_dy_powheg, -1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2E_Bin-MLL-120to200" : (21.65*kfactor_dy_powheg,-1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2Tau_Bin-MLL-50to120" : (2219*kfactor_dy_powheg, -1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2Tau_Bin-MLL-120to200" : (21.65*kfactor_dy_powheg, -1, "DY", ['ZTT','ZL','ZJ']),
        "WtoENu-2Jets" : (22666.*kfactor_wj, -1, "WJ", ['W']),
        "WtoTauNu-2Jets" : (22666.*kfactor_wj, -1, "WJ", ['W']),
        "TTto2L2Nu" : (80.9*kfactor_ttbar, -1, "TT", ['TTT','TTL','TTJ']),
        "TTtoLNu2Q" : (334.8*kfactor_ttbar, -1, "TT", ['TTT','TTL', 'TTJ']),
        "TWminustoLNu2Q" : (15.8, -1, "ST", ['VV']),
        "TWminusto2L2Nu" : (3.8, -1, "ST", ['VV']),
        "TbarWplustoLNu2Q" : (15.9, -1, "ST", ['VV']),
        "TbarWplusto2L2Nu" : (3.8, -1, "ST", ['VV']),
        "WZ" : (29.1*kfactor_wz, -1, "VV", ['VV']),
        "ZZ" : (12.75*kfactor_zz, -1, "VV", ['VV']),
        "WWto2L2Nu" : (11.79*kfactor_ww, -1, "VV", ['VV']),
        "WWtoLNu2Q" : (48.94*kfactor_ww, -1, "VV", ['VV']),
    },
    '2025': {
        #      Name  :  (xsec, nevts, group, split by genmatch_2)
        #    nevts = -1 implies that total number of events is
        #               taken from bin 16 of the cutflow histogram
        "DYto2E_Bin-MLL-10to50"   : (6744.0, -1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2E_Bin-MLL-50to120"  : (2219*kfactor_dy_powheg, -1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2E_Bin-MLL-120to200" : (21.65*kfactor_dy_powheg,-1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2Tau_Bin-MLL-50to120" : (2219*kfactor_dy_powheg, -1, "DY", ['ZTT','ZL','ZJ']),
        "DYto2Tau_Bin-MLL-120to200" : (21.65*kfactor_dy_powheg, -1, "DY", ['ZTT','ZL','ZJ']),
        "WtoENu-2Jets" : (22666.*kfactor_wj, -1, "WJ", ['W']),
        "WtoTauNu-2Jets" : (22666.*kfactor_wj, -1, "WJ", ['W']),
        "TTto2L2Nu" : (80.9*kfactor_ttbar, -1, "TT", ['TTT','TTL','TTJ']),
        "TTtoLNu2Q" : (334.8*kfactor_ttbar, -1, "TT", ['TTT','TTL', 'TTJ']),
        "TWminustoLNu2Q" : (15.8, -1, "ST", ['VV']),
        "TWminusto2L2Nu" : (3.8, -1, "ST", ['VV']),
        "TbarWplustoLNu2Q" : (15.9, -1, "ST", ['VV']),
        "TbarWplusto2L2Nu" : (3.8, -1, "ST", ['VV']),
        "WZ" : (29.1*kfactor_wz, -1, "VV", ['VV']),
        "ZZ" : (12.75*kfactor_zz, -1, "VV", ['VV']),
        "WWto2L2Nu" : (11.79*kfactor_ww, -1, "VV", ['VV']),
        "WWtoLNu2Q" : (48.94*kfactor_ww, -1, "VV", ['VV']),
    },
}

data_samples = {
    '2526': ['EGamma0_Run2026B','EGamma0_Run2026D',
             'EGamma1_Run2026B','EGamma1_Run2026D',
             'EGamma2_Run2026B','EGamma2_Run2026D',
             'EGamma3_Run2026B','EGamma3_Run2026D',
             'EGamma4_Run2026B','EGamma4_Run2026D',
             'EGamma5_Run2026B','EGamma5_Run2026D',
             'EGamma0_Run2025B','EGamma0_Run2025C','EGamma0_Run2025D','EGamma0_Run2025E','EGamma0_Run2025F','EGamma0_Run2025G',
             'EGamma1_Run2025B','EGamma1_Run2025C','EGamma1_Run2025D','EGamma1_Run2025E','EGamma1_Run2025F','EGamma1_Run2025G',
             'EGamma2_Run2025B','EGamma2_Run2025C','EGamma2_Run2025D','EGamma2_Run2025E','EGamma2_Run2025F','EGamma2_Run2025G',
             'EGamma3_Run2025B','EGamma3_Run2025C','EGamma3_Run2025D','EGamma3_Run2025E','EGamma3_Run2025F','EGamma3_Run2025G'],
    '2026': ['EGamma0_Run2026B','EGamma0_Run2026D',
             'EGamma1_Run2026B','EGamma1_Run2026D',
             'EGamma2_Run2026B','EGamma2_Run2026D',
             'EGamma3_Run2026B','EGamma3_Run2026D',
             'EGamma4_Run2026B','EGamma4_Run2026D',
             'EGamma5_Run2026B','EGamma5_Run2026D'],
    '2025': ['EGamma0_Run2025B','EGamma0_Run2025C','EGamma0_Run2025D','EGamma0_Run2025E','EGamma0_Run2025F','EGamma0_Run2025G',
             'EGamma1_Run2025B','EGamma1_Run2025C','EGamma1_Run2025D','EGamma1_Run2025E','EGamma1_Run2025F','EGamma1_Run2025G',
             'EGamma2_Run2025B','EGamma2_Run2025C','EGamma2_Run2025D','EGamma2_Run2025E','EGamma2_Run2025F','EGamma2_Run2025G',
             'EGamma3_Run2025B','EGamma3_Run2025C','EGamma3_Run2025D','EGamma3_Run2025E','EGamma3_Run2025F','EGamma3_Run2025G'], 
}

zptweightName = {
    '2526' : 'zptweight_nnlo',
    '2026' : 'zptweight_nnlo',
    '2025' : 'zptweight_nnlo',
}

eraLumi = {
    '2526'   : 136150.,
    '2026'   : 25300.,
    '2025'   : 110840.,
}

sys_TES = {
    'TES0.86': 0.86,
    'TES0.88': 0.88,
    'TES0.90': 0.90,
    'TES0.92': 0.92,
    'TES0.94': 0.94,
    'TES0.96': 0.96,
    'TES0.98': 0.98,
    'TES1.00': 1.00,
    'TES1.02': 1.02,
    'TES1.04': 1.04,
    'TES1.06': 1.06,
    'TES1.08': 1.08,
    'TES1.10': 1.10,
    'TES1.12': 1.12,
    'TES1.14': 1.14,
}
sys_EES = {
    'EES0.96': 0.96,
    'EES0.98': 0.98,
    'EES1.00': 1.00,
    'EES1.02': 1.02,
    'EES1.04': 1.04,
}

################
# Data samples #
################

procs = ['ZTT','ZL','ZJ','TTT','TTL','TTJ','W','VV']

tauVsEleWPs = {
    'VVVLoose': "1",
    'VVLoose' : "2",
    'VLoose'  : "3",
    'Loose'   : "4",
    'Medium'  : "5",
    'Tight'   : "6",
    'VTight'  : "7",
    'VVTight' : "8"
}

tauVsEleIntWPs = {
    'VVVLoose': 1,
    'VVLoose' : 2,
    'VLoose'  : 3,
    'Loose'   : 4,
    'Medium'  : 5,
    'Tight'   : 6,
    'VTight'  : 7,
    'VVTight' : 8
}

tauVsMuWPs = {
    'VLoose'  : "1",
    'Loose'   : "2",
    'Medium'  : "3",
    'Tight'   : "4"
}

tauVsMuIntWPs = {
    'VLoose'  : 1,
    'Loose'   : 2,
    'Medium'  : 3,
    'Tight'   : 4
}

tauVsJetWPs = {
    'Loose': "4",
    'Medium': "5",
    'Tight': "6",
    'VTight': "7",
    'VVTight': "8"
}

tauVsJetIntWPs = {
    'Loose': 4,
    'Medium': 5,
    'Tight': 6,
    'VTight': 7,
    'VVTight': 8    
}

# os labels 
os_labels = ['os','ss']
# sys labels
sys_labels = ['up','down']
# reg labels
reg_labels = ['pass','fail']
# dm labels
dm_labels = ['incl','DM0','DM1','DM10','DM11','1prong','3prong']
dm_meas = {'DM0':0.5,'DM1':1.5,'DM10':2.5,'DM11':3.5}

lib_histos = {
    'm_vis': [40,0,200],
    'pt_1' : [40,0,200],
    'pt_2' : [40,0,200],
    'eta_1': [25,-2.5,2.5],
    'eta_2': [25,-2.5,2.5],
    'met'  : [40,0,200],
    'mt_1' : [40,0,200],
    'dm_2' : [12,-0.5,11.5],
    'rawDeepTau2018v2p5VSe_2' : [50,0.,1.]
}

etabins = {
    'eta0p0to1p48' : [0.0,1.48, 1],
    'eta1p48to2p5' : [1.48,2.5, 2],
}

etaTitle = {
    'eta0p0to1p48' : 'Barrel',
    'eta1p48to2p5' : 'Endcap',
}

unc_jfake = 0.2
unc_qcd = 0.2
unc_tauID = 0.2
unc_fes = 0.06

def defineSuffix(channel,era,wpVsJet,wpVsMu,wpVsE,applySF):
    suffix = f'{channel}_{era}_{wpVsJet}VsJet_{wpVsMu}VsMu_{wpVsE}VsE'
    if applySF:
        suffix += '_SF'
    return suffix

def rebinHisto(hist,bins,suffix):
    nbins = hist.GetNbinsX()
    newbins = len(bins)-1
    name = hist.GetName()+"_"+suffix
    newhist = ROOT.TH1D(name,"",newbins,array('d',list(bins)))
    for ib in range(1,nbins+1):
        centre = hist.GetBinCenter(ib)
        bin_id = newhist.FindBin(centre)
        xbin = hist.GetBinContent(ib)
        ebin = hist.GetBinError(ib)
        xnew = newhist.GetBinContent(bin_id)
        enew = newhist.GetBinError(bin_id)
        x_update = xbin + xnew;
        e_update = math.sqrt(ebin*ebin + enew*enew);
        newhist.SetBinContent(bin_id,x_update)
        newhist.SetBinError(bin_id,e_update)
    return newhist

def createBins(nbins,xmin,xmax):
    binwidth = (xmax-xmin)/float(nbins)
    bins = []
    for i in range(0,nbins+1):
        xb = xmin + float(i)*binwidth
        bins.append(xb)
    return bins

def zeroBinErrors(hist):
    nbins = hist.GetNbinsX()
    for i in range(1,nbins+1):
        hist.SetBinError(i,0.)

def zeroBinContentErrors(hist):
    nbins = hist.GetNbinsX()
    for i in range(1,nbins+1):
        hist.SetBinError(i,0.)
        hist.SetBinContent(i,0.)

def removeNegativeBins(hist):
    nbins = hist.GetNbinsX()
    for i in range(1,nbins+1):
        x = hist.GetBinContent(i)
        if x<0.1:
            hist.SetBinContent(i,0.1)
        
        
def createUnitHisto(hist,histName):
    nbins = hist.GetNbinsX()
    unitHist = hist.Clone(histName)
    for i in range(1,nbins+1):
        x = hist.GetBinContent(i)
        e = hist.GetBinError(i)
        if x>0:
            rat = e/x
            unitHist.SetBinContent(i,1.)
            unitHist.SetBinError(i,rat)
    return unitHist

def dividePassProbe(passHist,failHist,histName):
    nbins = passHist.GetNbinsX()
    hist = passHist.Clone(histName)
    for i in range(1,nbins+1):
        xpass = passHist.GetBinContent(i)
        epass = passHist.GetBinError(i)
        xfail = failHist.GetBinContent(i)
        efail = failHist.GetBinError(i)
        xprobe = xpass+xfail
        ratio = 1
        eratio = 0
        if xprobe>1e-4:
            ratio = xpass/xprobe
            dpass = xfail*epass/(xprobe*xprobe)
            dfail = xpass*efail/(xprobe*xprobe)
            eratio = math.sqrt(dpass*dpass+dfail*dfail)
        hist.SetBinContent(i,ratio)
        hist.SetBinError(i,eratio)
    return hist

def divideHistos(numHist,denHist,histName):
    nbins = numHist.GetNbinsX()
    hist = numHist.Clone(histName)
    for i in range(1,nbins+1):
        xNum = numHist.GetBinContent(i)
        eNum = numHist.GetBinError(i)
        xDen = denHist.GetBinContent(i)
        eDen = denHist.GetBinError(i)
        ratio = 0
        eratio = 0
        if xDen>1e-5 and xNum>1e-5:
            ratio = xNum/xDen
            rNum = eNum/xNum
            rDen = eDen/xDen
            rratio = math.sqrt(rNum*rNum+rDen*rDen)
            eratio = rratio * ratio
#        else:
#            ratio = 0.5*eNum/xDen
#            eratio = ratio
            
        hist.SetBinContent(i,ratio)
        hist.SetBinError(i,eratio)
    return hist

def histoRatio(numHist,denHist,histName):
    nbins = numHist.GetNbinsX()
    hist = numHist.Clone(histName)
    for i in range(1,nbins+1):
        xNum = numHist.GetBinContent(i)
        eNum = numHist.GetBinError(i)
        xDen = denHist.GetBinContent(i)
        ratio = 0
        eratio = 0
        if xNum>1e-7 and xDen>1e-7:
            ratio = xNum/xDen
            eratio = eNum/xDen
        hist.SetBinContent(i,ratio)
        hist.SetBinError(i,eratio)
    return hist

#######################################
# Creating shape systematic templates #
#######################################
def ComputeSystematics(h_central, h_sys, name):
    h_up = h_central.Clone(name+"Up")
    h_down = h_central.Clone(name+"Down")
    nbins = h_central.GetNbinsX()
    for i in range(1,nbins+1):
        x_up = h_sys.GetBinContent(i)
        x_central = h_central.GetBinContent(i)
        x_down = max(0,2.0*x_central-x_up)
        h_up.SetBinContent(i,x_up)
        h_down.SetBinContent(i,x_down)
    return h_up, h_down

def unitBinContents2D(hist):
    nbinsX = hist.GetNbinsX()
    nbinsY = hist.GetNbinsY()
    for ix in range(nbinsX):
        for iy in range(nbinsY):
            hist.SetBinContent(ix,iy,1.0)
            hist.SetBinError(ix,iy,0.0)
