import ROOT
import math
import os

class TauScaleFactor:
    
    def __init__(self,**kwargs):
        self.filename = kwargs.get('filename','None')
        if os.path.isfile(self.filename):
            print('Loading file with tau scale factors : %s'%(self.filename))
        else:
            print('No file %s is found'%(self.filename))
            print('Quitting')
            exit()
        self.sfFile = ROOT.TFile(self.filename,'read')
        self.sf = {}
        self.sf['tauID'] = self.sfFile.Get('tauID')
        self.sf['jfake'] = self.sfFile.Get('jfake')
        self.sf['lfake'] = self.sfFile.Get('lfake')
        self.nbinsEta = self.sf['tauID'].GetNbinsX()
        self.maxEta = self.sf['tauID'].GetBinLowEdge(self.nbinsEta+1)

    def getSF(self,eta,typ):
        absEta = math.fabs(eta)
        sf = self.sf[typ].GetBinContent(self.sf[typ].FindBin(absEta))
        return sf
