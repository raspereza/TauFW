# Measurement of mu->tau fake rate scale factors

## Installation

```
export CMSSW=CMSSW_14_1_0_pre4
export SCRAM_ARCH el9_amd64_gcc10
cmsrel $CMSSW
cd $CMSSW/src
cmsenv
git clone https://github.com/raspereza/TauFW.git
git checkout 2024dev

# Installation of combine utility
git -c advice.detachedHead=false clone --depth 1 --branch v10.4.1 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
scramv1 b clean; scramv1 b -j$(nproc --ignore=2)

# Installation of Combine Harvester
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
# IMPORTANT: Checkout the recommended tag on the link above
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
git checkout v3.0.0-pre1
scram b

```

Measurement requires specialized picotuples produced for a cpecific era by dedicated pico producer [`TauFW/PicoProducer/python/analysis/Run3_DEV/ModuleMuTau_Inclusive.py`](https://github.com/raspereza/TauFW/blob/2024dev/PicoProducer/python/analysis/Run3_DEV/ModuleMuTau_Inclusive.py)

## Structure of the code
The software package includes two components. 
* Utilities and auxiliarly classes. They are located in the folder (`TauFW/Fitter/python/MuTauFR`)[https://github.com/raspereza/TauFW/tree/2024dev/Fitter/python/MuTauFR].
* Scripts to run selection, plot control distributions, create datacards for measurement and store scale factors. They are located in the folder (`TauFW/FitterMuTauFR/scripts`)[https://github.com/raspereza/TauFW/tree/2024dev/Fitter/MuTauFR/scripts]

### Utilities and helper classes

File [`TauFW/Fitter/python/MuTauFR/utils.h`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/python/MuTauFR/utils.py) stores main configuration to run the measurements. The following variables have to be set/extended by the user
* dictionary `picoFolder` - for a given era specifies path to picotuples to be processes
* `outputFolder` - folder which will contain output of selection: RooT files with histograms for plotting and creaton of datacards  
* `condorFolder` - folder with batch configuration scripts
* `figuresFolder` - folder where plots are stored

There are also two dictionaries: 
* `mc_samples` 
* `data_samples`
They contain important information on datasets and MC samples to be processes for a given era. Before running measurements make sure that data and MC samples, corresponding to the era considered in the measurement, are added to the respective dictionaries. Each MC sample is assigned a number of attributes
* cross section,
* number of generated events,
* name of the group of MC processes; this is also the name of subfolder where picotuples for a give MC sample are located
* scheme of splitting. For example if MC is assigned three strings, like ZJ, ZL and ZTT, it will be split according to genmatch_2 variable:
  * ZJ -> hadronic tau has genmatch_2==0: hadronic jet fakes tau;
  * ZL -> hadronic tau has genmatch_2>=1 and genmatch_2<=4: light lepton (e/mu) fakes tau;
  * ZTT -> hadronic tau has genmatch_2==5: genuine tau lepton decaying hadronically
Currently, only TT and DY processes are split according to this scheme.

Other configuration settings define eta binning scheme, luminosity per era, deepTau working points, etc.

Python source file [`TauFW/Fitter/python/MuTauFR/analysisMuTauFR.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/python/MuTauFR/analysisMuTauFR.py) implements class facilitating processing of pico tuples of individual data and MC samples. The class is initialized for a given data or MC sample, performs selection of events and stores histograms used to produce control plots and perform measurements   

Python source file [`TauFW/Fitter/python/MuTauFR/procedures.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/python/MuTauFR/procedures.py) contains subroutines for creating datacards and fitting of mass distributions in the samples of passing and failing probes and extraction of mu->tau fake rate scale factors. 

## Running selection on a give sample

The selection on a given sample is performed by the script [`TauFW/Fitter/MuTauFR/scripts/RunSelectionMuTau.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/MuTauFR/scripts/RunSelectionMuTau.py). The script requires the following input parameters:
* `--era` (string) : data-taking period (2024,2025,UL2017,UL2016_preVFP,UL2016_postVFP);
* `--wpVsJet` (string) : working point of DeepTau vs jet; 
* `--wpVsMu` (string) : working point of DeepTau vs muon;
* `--wpVsE` (string) : working point of DeepTau vs electron;
* `--sample` (string) : name of the sample from or dictionaries;
* `--start` (int) : first event in sample to process (if you would like to process chunk of the sample starting from the certain event);
* `--period` (int) : number of events to process.

If you measured scale factors and stored them as histogram in the RooT file you can apply them in the selection by setting flag `--applySF`.
Details will be discussed later.

You can run this script interactively in standalone mode for testing purpose. For practical purpouse, it is more convenient to run selection
on all samples using batch system.

## Running selection using batch system

Script [`TauFW/Fitter/MuTauFR/scripts/PrepareSubmit.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/MuTauFR/scripts/PrepareSubmit.py) prepares condor config files and executable scripts to process all data and MC tuples for a given era. Each condor job executes `TauFW/Fitter/MuTauFR/scripts/RunSelectionMuTau.py` script. Every data and MC sample is divided into chunks with the number of events specified by parameter `--period`. Last chunk for each sample contains remainder of events. All condor config files and script are put in the directory `$condorFolder/$subfolder`, where `$condorFolder` specified in the file `TauFW/Fitter/python/MuTauFR/utils.h` (see above), and `$subfolder` indicates channel, era and specified working points of DeepTau discriminants, e.g. `mutau_UL2017_MediumVsJet_LooseVsMu_VVLooseVsE`. If jobs are run with option `--applySF`, suffix `SF` is added `$subfolder`: `mutau_UL2017_MediumVsJet_LooseVsMu_VVLooseVsE_SF`.

To submit all jobs to the batch system, user should manually execute bash script named `submit.bash` and placed in the same directory as condor config and executables. The printout produced by the script invites user to execute `submit.bash` script and indicates its location, as exemplified below:  

* `Submit jobs by executing file /afs/cern.ch/work/r/rasp/MuTauFR/condor/mutau_UL2017_MediumVsJet_LooseVsMu_VVLooseVsE/submit.bash`

The script `TauFW/Fitter/MuTauFR/scripts/PrepareSubmit.py` takes the following arguments:  
* `--era` (string) : data-taking period (2024,2025,UL2017,UL2016_preVFP,UL2016_postVFP);
* `--wpVsJet` (string) : working point of DeepTau vs jet; 
* `--wpVsMu` (string) : working point of DeepTau vs muon;
* `--wpVsE` (string) : working point of DeepTau vs electron;
* `--applySF` : optional flag to apply already measured scale factors;
* `--period` (int) : number of events per chunk.

The output RooT files with histogram are saved in directory `$outputFolder/$subfolder`, where `$outputFolder` is defined in the python file
`TauFW/Fitter/python/MuTauFR/utils.h` and `$subfolder` follows naming convention explained above.
Once jobs are finished, seperate RooT files with histograms can be merged with script [`TauFW/Fitter/MuTauFR/scripts/HaddSamples.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/MuTauFR/scripts/HaddSamples.py) passing as arguments era and working points of DeepTau tagger.

## Plotting control distributions

Control plots are produced by script [`TauFW/Fitter/MuTauFR/scripts/ControlPlotsMuTau.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/MuTauFR/scripts/ControlPlotsMuTau.py)

## Measurement of mu->tau fake rate

The measurement of mu->tau fake rate is performed by executing script [`TauFW/Fitter/MuTauFR/scripts/RunMeasurements.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/MuTauFR/scripts/RunMeasurements.py). It calls subroutine accessing histograms
in the merged RooT file and produces datacards. If flags `--runFit` and `--extractSF` are activated, fits are performed on datacards with `combine tool and mu->tau scale factors are extracted from output files produced by `combine`.
