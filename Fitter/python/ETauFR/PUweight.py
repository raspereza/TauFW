import ROOT
import os

class PUweight:

    def __init__(self,**kwargs):
        mcFileName = kwargs.get('FileMC','MC_PileUp_2025.root')
        dataFileName = kwargs.get('FileData','Data_PileUp_2025_69p2.root')
        cms_base = os.getenv('CMSSW_BASE')
        mcPath = '%s/src/TauFW/PicoProducer/data/pileup/%s'%(cms_base,mcFileName)
        dataPath = '%s/src/TauFW/PicoProducer/data/pileup/%s'%(cms_base,dataFileName)
        self.mcFile = None
        self.dataFile = None
        if os.path.isfile(mcPath):
            self.mcFile = ROOT.TFile(mcPath)
        else:
            print('%s does not exist'%(mcPath))
            exit()
        if os.path.isfile(dataPath):
            self.dataFile = ROOT.TFile(dataPath)

        self.dataHist = self.dataFile.Get('pileup')
        self.mcHist = self.mcFile.Get('pileup')
        dataYield = self.dataHist.GetSumOfWeights()
        mcYield = self.mcHist.GetSumOfWeights()
        self.dataHist.Scale(1./dataYield)
        self.mcHist.Scale(1./mcYield)
        print('')
        print('Class PUweight')
        print(self.dataHist,'  integral = %5.3f'%(self.mcHist.GetSumOfWeights()))
        print(self.mcHist,'  integral = %5.3f'%(self.mcHist.GetSumOfWeights()))
        print('')

    def getWeight(self,npu):
        x = float(npu)
        if x>100.: x = 99
        x_mc = self.mcHist.GetBinContent(self.mcHist.FindBin(x))
        x_data = self.dataHist.GetBinContent(self.dataHist.FindBin(x))
        # some protection
        if x_mc<1e-8: x_mc = 1e-8
        weight = x_data/x_mc
        if weight>50.: weight = 50.
        return weight
