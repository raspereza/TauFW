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
        self.types = ['muTauFR','jetTauFR','tauID','qcdNorm']
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

    def getSF(self,eta,typ):
        absEta = math.fabs(eta)
        sf = 1.0
        sf = self.SF[typ].GetBinContent(self.SF[typ].FindBin(absEta))
        return sf
