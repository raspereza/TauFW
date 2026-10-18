import ROOT
import math
import os

class TauScaleFactor:
    
    def __init__(self,**kwargs):
        self.filename = kwargs.get('filename','None')
        wpVsJet = kwargs.get('wpVsJet','Medium')
        wpVsMu = kwargs.get('wpVsMu','VLoose')
        wpVsE = kwargs.get('wpVsE','VVLoose')
        if os.path.isfile(self.filename):
            print('Loading file with tau fake scale factors : %s'%(self.filename))
        else:
            print('No file %s is found'%(self.filename))
            print('Quitting')
            exit()
        self.sfFile = ROOT.TFile(self.filename,'read')
        self.types = ['eTauFR','jetTauFR','tauID','FES']
        self.SF = {}
        for typ in self.types:
            name = '%s_%sVsJet_%sVsMu_%sVsE'%(typ,wpVsJet,wpVsMu,wpVsE)
            self.SF[typ] = self.sfFile.Get(name)
#            print(typ,self.SF[typ])
            if self.SF[typ]==None:
                print('%s for %sVsJet %sVsMu %sVsE do not exist in file %s'%(name,
                                                                             wpVsJet,
                                                                             wpVsMu,
                                                                             wpVsE,
                                                                             self.filename))
                print('quitting')
                exit()

    def getSF(self,eta,dm,typ):
        absEta = math.fabs(eta)
        sf = 1.0
        dm_input = 0.5
        if dm==0: dm_input = 0.5
        elif dm==1: dm_input = 1.5
        elif dm==10: dm_input = 2.5
        elif dm==11: dm_input = 3.5
        sf = self.SF[typ].GetBinContent(self.SF[typ].FindBin(absEta,dm_input))
        return sf
