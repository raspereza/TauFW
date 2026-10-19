# Measurement of e->tau fake rate scale factors

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

Measurement requires specialized picotuples produced for a cpecific era by dedicated pico producer [`TauFW/PicoProducer/python/analysis/Run3_DEV/ModuleETau_Inclusive.py`](https://github.com/raspereza/TauFW/blob/2024dev/PicoProducer/python/analysis/Run3_DEV/ModuleETau_Inclusive.py)

Picotuples for eras 2025, 2026 and 2025+2026 are located in
* `/eos/cms/store/group/phys_tau/rasp/ETau_FR/2025`
* `/eos/cms/store/group/phys_tau/rasp/ETau_FR/2026`
* `/eos/cms/store/group/phys_tau/rasp/ETau_FR/2526`


## Structure of the code
The software package includes two components. 
* Utilities and auxiliarly classes. They are located in the folder [`TauFW/Fitter/python/ETauFR`](https://github.com/raspereza/TauFW/tree/2024dev/Fitter/python/ETauFR).
* Scripts to run selection, plot control distributions, create datacards for measurement and store scale factors. They are located in the folder [`TauFW/FitterETauFR/scripts`](https://github.com/raspereza/TauFW/tree/2024dev/Fitter/ETauFR/scripts)

### Utilities and helper classes

File [`TauFW/Fitter/python/ETauFR/utils.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/python/ETauFR/utils.py) stores main configuration to run the measurements. The following variables have to be set/extended by the user
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

Python source file [`TauFW/Fitter/python/ETauFR/analysisETauFR.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/python/ETauFR/analysisETauFR.py) implements class facilitating processing of pico tuples of individual data and MC samples. The class is initialized for a given data or MC sample, performs selection of events and stores histograms used to produce control plots and perform measurements   

Python source file [`TauFW/Fitter/python/ETauFR/procedures.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/python/ETauFR/procedures.py) contains subroutines for creating datacards, fitting of mass distributions in the samples of passing and failing probes and extraction of e->tau fake rate scale factors. 

## Running selection on a given sample

The selection on a given sample is performed by the script [`TauFW/Fitter/ETauFR/scripts/RunSelectionETau.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/ETauFR/scripts/RunSelectionETau.py). The script requires the following input parameters:
* `--era` (string) : data-taking period (2025,2026,2526);
* `--wpVsJet` (string) : working point of DeepTau vs jet; 
* `--wpVsMu` (string) : working point of DeepTau vs muon;
* `--wpVsE` (string) : working point of DeepTau vs electron;
* `--sample` (string) : name of the sample from or dictionaries;
* `--start` (int) : first event in sample to process (if you would like to process chunk of the sample starting from the certain event);
* `--period` (int) : number of events to process.

If you measured scale factors and stored them as histogram in the RooT file you can apply them in the selection by setting flag `--applySF`.
Details will be discussed later.

You can run this script interactively in standalone mode for testing purpose. For practical purpose, it is more convenient to run selection
on all samples using batch system.

## Running selection using batch system

Script [`TauFW/Fitter/ETauFR/scripts/PrepareSubmit.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/ETauFR/scripts/PrepareSubmit.py) prepares condor config files and executable scripts to process all data and MC tuples for a given era. Each condor job executes `TauFW/Fitter/ETauFR/scripts/RunSelectionETau.py` script. Every data and MC sample is divided into chunks with the number of events specified by parameter `--period`. Last chunk for each sample contains remainder of events. All condor config files and script are put in the directory `{utils.condorFolder}/{subfolder}`, where `{utils.condorFolder}` is specified in the file `TauFW/Fitter/python/ETauFR/utils.h` (see above), and `{subfolder}` indicates channel (etau), era and specified working points of DeepTau discriminants, e.g.
* `etau_2526_MediumVsJet_LooseVsMu_VVLooseVsE`.

If jobs are run with option `--applySF`, suffix `SF` is added to subfolder name:
* `etau_2526_MediumVsJet_LooseVsMu_VVLooseVsE_SF`.

To submit all jobs to the batch system, user should manually execute bash script named `submit.bash` which is created in the same directory as condor configs and executables for individual jobs. The printout produced by the script reminds user to execute `submit.bash` script and indicates its location, as shown below:  
* `Submit jobs by executing file /afs/cern.ch/work/r/rasp/ETauFR/condor/etau_2526_MediumVsJet_LooseVsMu_VVLooseVsE/submit.bash`

The script `TauFW/Fitter/ETauFR/scripts/PrepareSubmit.py` takes the following arguments:  
* `--era` (string) : data-taking period (2024,2025,2526);
* `--wpVsJet` (string) : working point of DeepTau vs jet; 
* `--wpVsMu` (string) : working point of DeepTau vs muon;
* `--wpVsE` (string) : working point of DeepTau vs electron;
* `--applySF` : optional flag to apply already measured scale factors (should not be applied when output of the scripts is intended for measurements);
* `--period` (int) : number of events per chunk.

The output RooT files with histogram are saved in directory `{utils.outputFolder}/{subfolder}`, where `utils.{outputFolder}` is defined in the python config file `TauFW/Fitter/python/ETauFR/utils.h` and `{subfolder}` follows naming convention explained above.

Once jobs are finished, seperate RooT files with histograms should be merged with script [`TauFW/Fitter/ETauFR/scripts/HaddSamples.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/ETauFR/scripts/HaddSamples.py) passing as arguments era and working points of DeepTau tagger.

The output RooT file contain histograms of some kinematic variables produced by applying e+tau selection with taus passing specified. These histograms are intended for monitoring data-simulation agreement. There are also histograms of visible e+tau mass produced for two eta bins (0,1.48,2.5) and four individual decay HPS modes (0,1,10,11). These histograms are produced individually for samples of tau probes passing and failing anti-electron DeepTau discriminant.  

The control histograms have the following naming:
`{sample}_{var}_{sign}_{DM}`, where
* sample : Data, ZTT, ZJ, ZL, TTT, TTL, TTJ, W, VV;
* var : m_vis, pt_1, pt_2, eta_1, eta_2, met, mt_1 (name of kinematic variable)
* sign : os (opposite-sign), ss (same-sign) (same-sign selection is needed to estimate QCD background);
* DM : decay mode - incl (inclusive in decay modes), DM0, DM1, DM10, DM11.

Histograms used in fits has the following naming:
`{sample}_m_vis_{sign}_{DM}_{region}_{etabin}`
where 
* region : pass or fail
* etabin : eta0p0to1p48 and eta1p48to2p5

Also histograms with systematic templates are created for MC samples. They are obtained by varying energy scale of electron candidates from 0.96 to 1.04 with 0.02 step and energy scale of tau candidates from 0.86 to 1.14 with 0.02 step.
Corresponding templates has trailing suffix in the names
* EES{var} with {var} being variation of energy scale of electron candidates
* TES{var} with {var} being variation of energy scale of tau candidate (genuine and e->tau fakes)

These templates are then used to define shape systematics in datacards and implement morphing of ZL template with variation of the energy scale of the e->tau fake candidate.

The corresponding dictionaries are defined in the file `TauFW/Fitter/python/utils.py` 

## Plotting control distributions

Control plots are produced by script [`TauFW/Fitter/ETauFR/scripts/ControlPlotsETau.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/ETauFR/scripts/ControlPlotsETau.py). The following list of arguments should be provided
* `--era` (string) : data-taking period (2024,2025,2526);
* `--wpVsJet` (string) : working point of DeepTau vs jet; 
* `--wpVsMu` (string) : working point of DeepTau vs muon;
* `--wpVsE` (string) : working point of DeepTau vs electron;
Flag `--applySF` should be provided in the validation step of the workflow when plotting distributions after applying scale factors.

Plots are saved in the folder:
* `{utils.figuresFolder}/ControlPlots/{era}_{wpVsJet}_{wpVsMu}_{wpVsE}`.


## Measurement of e->tau fake rate

The measurement of e->tau fake rate is performed by executing script [`TauFW/Fitter/ETauFR/scripts/RunMeasurements.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/ETauFR/scripts/RunMeasurements.py). It calls subroutine accessing histograms in the RooT file and produces datacards. If flags `--runFit` and `--extractSF` are provided, fits are performed on datacards with `combine` tool and e->tau scale factors are extracted from output files produced by `combine`.

Fits are performed individually for each eta bin and decay mode. By default, e->tau fake energy scale is treated as gaussian constrained shape parameter with uncertainty of 0.06. If flag `--fes` is activated, e->tau fake energy scale is treated as unconstrained POI and `ZL` template is morphed when performing fit.

The script `TauFW/Fitter/ETauFR/RunMeasurements.py` takes the following arguments:
* `--era` (string) : data-taking period (2024,2025,2526);
* `--wpVsJet` (string) : working point of DeepTau vs jet; 
* `--wpVsMu` (string) : working point of DeepTau vs muon;
* `--wpVsE` (string) : working point of DeepTau vs electron;
Optional flags (see comment above):
* `--fes` : treat e->tau fake energy scale as POI
* `--runFit` : runs fit
* `--extractSF` : extract scale factors from and store them as 2D (eta - decay mode) histograms in RooT files (explained below).

Inputs, datacards and results of the fit are stored in the folder `TauFW/Fitter/ETau/datacards` if flag `--fes` is set, and in the folder `TauFW/Fitter/ETau/datacards_fes` if flag `--fes` is not set. Inside these folders, datacards for specific era and working points of DeepTau tagger are stored in individual subfolders with the name {era}_{wpVsJet}_{wpVsMu}_{wpVsE}, e.g.
* `2526_MediumVsJet_VLooseVsMu_VVLooseVsE`.

Fits can be performed separately for each eta bin and decay mode with the script [`TauFW/Fitter/ETauFR/scripts/FitETau.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/ETauFR/scripts/FitETau.py) with the following arguments:
* `--era`
* `--wpVsJet`
* `--wpVsMu`
* `--wpVsE`
* `--fes`
* `--dm` : decay mode (DM0, DM1, DM10, DM11)
* `--etabin` : eta bin (eta0p0to1p48, eta1p48to2p5)

This option is foreseen for diagnostics and debugging purpose. In this case make sure that corresponding datacards to perform fit have been created.

## Plotting results of the fit

Plotting prefit and postfit distributions for all eta bins and decay modes is performed by script (https://github.com/raspereza/TauFW/blob/2024dev/Fitter/ETauFR/scripts/PlotETau.py). Plots are stored in the folder
`{utils.figuresFolder}/Fits(_fes)/{era}_{wpVsJet}_{wpVsMu}_{wpVsE}`.
The standard set of arguments is required:
* `--era`
* `--wpVsJet`
* `--wpVsMu`
* `--wpVsE`
* `--fes` (if fit is done with e->tau fake energy scale as unconstrained POI)

## Storing SFs in RooT files

User can extract scale factors from RooT files produced by `combine` and dump to histograms files either in one go with creation of datacards and fitting with script `TauFW/Fitter/ETauFR/scripts/RunMeasurements` as described above or with the script [`TauFW/Fitter/ETauFR/scripts/ExtractScaleFactors.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/ETauFR/scripts/ExtractScaleFactors.py) with the following arguments
* `--era`
* `--wpVsJet`
* `--wpVsMu`
* `--wpVsE`
* `--fes`

RooT files with the results of the fit are located in the same folder as corresponding datacards, e.g. `TauFW/Fitter/ETauFR/datacards/{era}_{wpVsJet}_{wpVsMu}_{wpVsE}`, or if fit was run with option `--fes` - `TauFW/Fitter/ETauFR/datacards_fes/{era}_{wpVsJet}_{wpVsMu}_{wpVsE}`

The scale factors are dumped as histograms to the RooT file:
* `TauFW/Fitter/ETauFR/ScaleFactors(_fes)/{era}_{wpVsJet}_{wpVsMu}_{wpVsE}.root`.

It contains four 2D histograms named
1. `eTauFR_{wpVsJet}_{wpVsMu}_{wpVsE}` : e->tau fake rate SF;
2. `FES_{wpVsJet}_{wpVsMu}_{wpVsE}` : e->tau fake energy scale;
3. `jetTauFR_{wpVsJet}_{wpVsMu}_{wpVsE}` : j->tau fake rate SF;
4. `tauID_{wpVsJet}_{wpVsMu}_{wpVsE}` : tau ID SF.

Axis X of histograms corresponds to two eta bins:
* bin 1 : 0 < eta < 1.48 (barrel)
* bin 2 : 1.48 < eta < 2.5 (endcap)

Axis Y of histograms corresponds to four decay modes
* bin 1 : DM0
* bin 2 : DM1
* bin 3 : DM10
* bin 4 : DM11

All four histograms are used in the validation step (see next item) and can be used as inputs
for creation of JSON files.

## Validation of SFs

Before running validation step, merge all RooT files with scale factors produced for a given era using bash script `TauFW/Fitter/ETauFR/scripts/MergeSFs.bash`. It takes as a single argument era (2025, 2026 or 2526). The output file is created in the folder `TauFW/Fitter/ETauFR/ScaleFactors` and has the name:
* `{era}_ScaleFactor.root`

This step is necessiated by interface to scale factors implemented in python file [`TauFW/Fitter/python/ETauFR/TauScaleFactors.py.py`](https://github.com/raspereza/TauFW/blob/2024dev/Fitter/python/ETauFR/TauScaleFactors.py). Interface accesses file `{era}_ScaleFactor.root` and selects proper histograms by the name of working points of the DeepTau tagger.

Standard e+tau selection with taus passing nominal ID can be run once again but this time with scale factors applied. 

Run script `TauFW/Fitter/ETauFR/scripts/PrepareSubmit.py` with an argument `--applySF` following instruction given above. Don't forget to execute scripts submitting condor jobs. You will be reminded by the message issued by the script, e.g. 
* `Submit jobs by executing file /afs/cern.ch/work/r/rasp/ETauFR/condor/etau_2526_MediumVsJet_LooseVsMu_VVLooseVsE_SF/submit.bash`

Monitor jobs with condor_q. Once jobs are finnished collect them with script `TauFW/Fitter/ETauFR/scripts/HaddSamples.py`. The flag `--applySF` should be passed as argument. Afterwards you can produce control plots with scale factors applied using the script `TauFW/Fitter/ETauFR/scripts/ControlPlotsETau.py`. Once again flag `--applySF` should be passed as an argument. Plots are save in the folder:
* `{utils.figuresFolder}/ControlPlots/{era}_{wpVsJet}_{wpVsMu}_{wpVsE}_SF`.

