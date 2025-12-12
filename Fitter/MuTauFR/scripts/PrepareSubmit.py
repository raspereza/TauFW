#!/usr/bin/env python3

from TauFW.Plotter.plot.utils import ensuredir
import TauFW.Fitter.MuTauFR.utils as utils
import TauFW.Fitter.MuTauFR.styles as styles
import TauFW.Fitter.MuTauFR.analysisMuTauFR as analysis
import os

def SubmitJob(**kwargs):
    era = kwargs.get('era','2024')
    chan = kwargs.get('channel','mutau')
    sample = kwargs.get('sample','Muon0_2024B')
    start = kwargs.get('start',0)
    period = kwargs.get('period',10000000)
    wpVsMu = kwargs.get('wpVsMu','VLoose')
    wpVsE = kwargs.get('wpVsE','VVLoose')
    wpVsJet = kwargs.get('wpVsJet','Medium')
    applySF = kwargs.get('applySF',False)
    condor_folder = kwargs.get('condor_folder',utils.condorFolder)
    
    # executable
    cmssw_base = os.getenv('CMSSW_BASE')
    basefilename = f'{sample}_{start}'
    filename_exec = f'{condor_folder}/{basefilename}.sh'
    f = open(filename_exec,'w')
    f.write('#!/bin/tcsh\n')
    f.write(f'cd {cmssw_base}/src\n')
    f.write('setenv SCRAM_ARCH el9_amd64_gcc10\n')
    f.write('#export SCRAM_ARCH=el9_amd64_gcc10\n')
    f.write('cmsenv\n')
    f.write('cd TauFW/Fitter/MuTauFR\n')
    f.write('echo $PWD\n')
    commandline = f'./scripts/RunSelectionMuTau.py --era {era} --channel {chan} --sample {sample} --start {start} --period {period} --wpVsJet {wpVsJet} --wpVsMu {wpVsMu} --wpVsE {wpVsE}'
    if applySF:
        commandline += ' --applySF\n'
    else:
        commandline += '\n'
    f.write(commandline)
    os.system(f'chmod u+x {filename_exec}')
    
    # configuration 
    initialdir = os.getenv('CMSSW_BASE')+'/src/TauFW/Fitter/MuTauFR'
    filename_config = f'{condor_folder}/{basefilename}.submit'
    f = open(filename_config,'w')
    f.write('universe = vanilla\n')
    f.write(f'executable = {condor_folder}/{basefilename}.sh\n')
    f.write(f'output = {condor_folder}/{basefilename}.out\n')
    f.write(f'error = {condor_folder}/{basefilename}.err\n')
    f.write(f'log = {condor_folder}/{basefilename}.log\n')
    f.write('notification = Never\n')
    f.write(f'initialdir = {initialdir}\n')
    f.write('+MaxRuntime = 50000\n')
    f.write('+RequestRuntime = 50000\n')
    f.write('MY.WantOS = el9\n')
    f.write('queue')

    command = 'chmod u+x %s'%(filename_config)
    os.system(command)
    command = 'condor_submit %s'%(filename_config)
    return command

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['2024','2025','UL2017','UL2016_preVFP','UL2016_postVFP'])
    parser.add_argument('-wpVsJet','--wpVsJet', dest='wpVsJet', default='Medium', choices=['Loose','Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--wpVsMu', dest='wpVsMu', default='VLoose', choices=['VLoose','Loose','Medium','Tight'])
    parser.add_argument('-wpVsE','--wpVsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Loose','Medium','Tight'])
    parser.add_argument('-applySF','--applySF', dest='applySF',action='store_true')
    parser.add_argument('-period','--period',dest='period',type=int,default=10000000)
    args = parser.parse_args()

    era = args.era
    channel = 'mutau'
    wpVsJet = args.wpVsJet
    wpVsMu = args.wpVsMu
    wpVsE = args.wpVsE
    period = args.period
    applySF = args.applySF
    
    suffix = utils.defineSuffix(channel,era,wpVsJet,wpVsMu,wpVsE,applySF)
    foldername = utils.condorFolder + '/' + suffix
    condor_folder = ensuredir(foldername)
    command = f'rm {condor_folder}/*'
    os.system(command)
    
    submitfile = f'{condor_folder}/submit.bash'
    f = open(submitfile,'w')
    f.write('#!/bin/bash\n')
    
    for sample in utils.data_samples[era]:
        sampleToProcess = analysis.sampleMuTauFR(era,channel,sample)
        nentries = sampleToProcess.GetEntries()
        nperiods = int(nentries/period)
        print(f'{sample}  entries={nentries}  nperiods={nperiods}')
        for iperiod in range(0,nperiods+1):
            command = SubmitJob(era=era,
                                condor_folder=condor_folder,
                                channel=channel,
                                sample=sample,
                                wpVsJet=wpVsJet,
                                wpVsMu=wpVsMu,
                                wpVsE=wpVsE,
                                start=iperiod,
                                period=period,
                                applySF=applySF)
            f.write(command+'\n')
        
    for sample in utils.mc_samples[era]:
        sampleToProcess = analysis.sampleMuTauFR(era,channel,sample)
        nentries = sampleToProcess.GetEntries()
        nperiods = int(nentries/period)
        print(f'{sample}  entries={nentries}  nperiods={nperiods}')
        for iperiod in range(0,nperiods+1):
            command = SubmitJob(era=era,
                                channel=channel,
                                condor_folder=condor_folder,
                                sample=sample,
                                wpVsJet=wpVsJet,
                                wpVsMu=wpVsMu,
                                wpVsE=wpVsE,
                                start=iperiod,
                                period=period,
                                applySF=applySF)
            f.write(command+'\n')
    outputFolder = utils.outputFolder+'/'+suffix
    if os.path.isdir(outputFolder):
        f.write(f'rm {outputFolder}/*.root\n')
    command = f'chmod u+x {submitfile}'
    os.system(command)
    print(f'Submit jobs by executing file {submitfile}')
    if os.path.isdir(outputFolder):
        print('ATTENTION! CONTENT OF FOLDER')
        print(f'{outputFolder}')
        print('WILL BE ERASED!')
