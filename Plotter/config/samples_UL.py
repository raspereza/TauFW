# Description: Common configuration file for creating pico sample set plotting scripts
import re
from TauFW.Plotter.sample.utils import LOG, STYLE, ensuredir, repkey, joincuts, joinweights, ensurelist,\
                                       setera, getyear, loadmacro, Sel, Var
from TauFW.Plotter.sample.utils import getsampleset as _getsampleset

def getsampleset(channel,era,**kwargs):
  verbosity = LOG.getverbosity(kwargs)
  year     = getyear(era) # get integer year
  fname    = kwargs.get('fname', "$PICODIR/$SAMPLE_$CHANNEL$TAG.root" ) # file name pattern of pico files
  split    = kwargs.get('split',    ['DY'] if 'tau' in channel else [ ] ) # split samples (e.g. DY) into genmatch components
  join     = kwargs.get('join',     ['VV','Top'] ) # join samples (e.g. VV, top)
  rmsfs    = ensurelist(kwargs.get('rmsf', [ ])) # remove the tau ID SF, e.g. rmsf=['idweight_2','ltfweight_2']
  addsfs   = ensurelist(kwargs.get('addsf', [ ])) # add extra weight to all samples
  weight   = kwargs.get('weight',   None         ) # weight for all MC samples
  dyweight = kwargs.get('dyweight', 'zptweight'  ) # weight for DY samples
  ttweight = kwargs.get('ttweight', 'ttptweight' ) # weight for ttbar samples
  filter   = kwargs.get('filter',   None         ) # only include these MC samples
  vetoes   = kwargs.get('vetoes',   None         ) # veto these MC samples
  #tag      = kwargs.get('tag',      ""           ) # extra tag for sample file names
  table    = kwargs.get('table',    True         ) # print sample set table
  setera(era) # set era for plot style and lumi-xsec normalization
  if 'TT' in split and 'Top' in join: # don't join TT & ST
    join.remove('Top')
    join += ['TT','ST']

  # SM BACKGROUND MC SAMPLES
  if '2018' in era: 
    expsamples = [ # table of MC samples to be converted to Sample objects
      # GROUP  NAME                     TITLE                   XSEC      EXTRA OPTIONS
      ( 'DY', "DYJetsToLL_M-50",       "Drell-Yan 50",          6075., {'extraweight': dyweight, "nevts":197553995.0} ), 
      ( 'WJ', "WJetsToLNu",            "W + jets",              61526, {"nevts" : 82442496} ),

      ( 'VV', "WWTo2L2Nu",             "WW",                    11.09,{"nevts" :  9956710.0} ),
      ( 'VV', "WZTo2Q2L",              "WZ",                    6.419,{"nevts" : 17820214.0} ),
      ( 'VV', "WZTo3LNu",              "WZ",                    5.213,{"nevts" : 6482815.0} ),
      ( 'VV', "ZZTo2L2Nu",             "ZZ",                   0.6008,{"nevts" : 56766176.0} ),
      ( 'VV', "ZZTo2Q2L",              "ZZ",                    3.676,{"nevts" : 19020772.0} ),
      ( 'VV', "ZZTo4L",                "ZZ",                    1.325,{"nevts" : 98187568.0} ),

      ( 'TT', "TTTo2L2Nu",             "ttbar 2l2#nu",          88.29, {'extraweight': ttweight, "nevts" : 144831008} ),
      ( 'TT', "TTToSemiLeptonic",      "ttbar semileptonic",   365.35, {'extraweight': ttweight, "nevts" : 475111154.0} ),
      
      ( 'ST', "ST_t-channel_top",      "ST t-channel t",       136.02, {"nevts" : 167505220} ),
      ( 'ST', "ST_t-channel_antitop",  "ST t-channel at",       80.95, {"nevts" : 90216506} ),
      ( 'ST', "ST_tW_top",             "ST tW",                 35.85, {"nevts" : 11269836} ),
      ( 'ST', "ST_tW_antitop",         "ST atW",                35.85, {"nevts" : 11015416} ),
    ]
  elif '2017' in era:
    expsamples = [ # table of MC samples to be converted to Sample objects
      # GROUP  NAME                     TITLE                   XSEC      EXTRA OPTIONS
      ( 'DY', "DYJetsToLL_M-50",       "Drell-Yan 50",          6075., {'extraweight': dyweight, "nevts":205238822.0} ), # apply k-factor in stitching
      ( 'WJ', "WJetsToLNu",            "W + jets",              61526, {"nevts" : 78981243.0 } ),
      
      ( 'VV', "WWTo2L2Nu",             "WW",                    11.09,{"nevts" :  7071358.0} ),
      ( 'VV', "WZTo2Q2L",              "WZ",                    6.419,{"nevts" : 18136498.0} ),
      ( 'VV', "WZTo3LNu",              "WZ",                    5.213,{"nevts" : 6826898.0 } ),
      ( 'VV', "ZZTo2L2Nu",             "ZZ",                   0.6008,{"nevts" : 40753260.0} ),
      ( 'VV', "ZZTo2Q2L",              "ZZ",                    3.676,{"nevts" : 19134840.0} ),
      ( 'VV', "ZZTo4L",                "ZZ",                    1.325,{"nevts" : 98323626.0} ),
        
      ( 'TT', "TTTo2L2Nu",             "ttbar 2l2#nu",          88.29, {'extraweight': ttweight, "nevts" : 105859990.0} ),
      ( 'TT', "TTToSemiLeptonic",      "ttbar semileptonic",   365.35, {'extraweight': ttweight, "nevts" : 352462632.0} ),
        
      ( 'ST', "ST_t-channel_top",      "ST t-channel t",       136.02, {"nevts" : 121728252.0} ),
      ( 'ST', "ST_t-channel_antitop",  "ST t-channel at",       80.95, {"nevts" : 65821722.0} ),
      ( 'ST', "ST_tW_top",             "ST tW",                 35.85, {"nevts" : 8506765.0} ),
      ( 'ST', "ST_tW_antitop",         "ST atW",                35.85, {"nevts" : 8433562.0} ),
    ]
  elif '2016' in era:
    if 'post' in era: 
      expsamples = [ # table of MC samples to be converted to Sample objects
        # GROUP  NAME                     TITLE                  XSEC      EXTRA OPTIONS
        ( 'DY', "DYJetsToLL_M-50",       "Drell-Yan 50",         6075.0, {'extraweight': dyweight, "nevts": 82448537.0} ),
        ( 'WJ', "WJetsToLNu",            "W + jets",            61526.0, {"nevts" : 82754918.0} ),
   
        ( 'VV', "WWTo2L2Nu",             "WW",                    11.09,{"nevts" :  2888924.0} ),
        ( 'VV', "WZTo2Q2L",              "WZ",                    6.419,{"nevts" :  8434516.0} ),
        ( 'VV', "WZTo3LNu",              "WZ",                    5.213,{"nevts" :  6890010.0} ),
        ( 'VV', "ZZTo2L2Nu",             "ZZ",                   0.6008,{"nevts" :  15894442.0} ),
        ( 'VV', "ZZTo2Q2L",              "ZZ",                    3.676,{"nevts" :  8901074.0} ),
        ( 'VV', "ZZTo4L",                "ZZ",                    1.325,{"nevts" :  51609810.0} ),
  
        ( 'TT', "TTTo2L2Nu",             "ttbar 2l2#nu",          88.29, {'extraweight': ttweight, "nevts" : 43275620.0} ),
        ( 'TT', "TTToSemiLeptonic",      "ttbar semileptonic",   365.35, {'extraweight': ttweight, "nevts" : 143804034.0} ),
        
        ( 'ST', "ST_t-channel_top",      "ST t-channel t",       136.02, {"nevts" : 59099222.0} ),
        ( 'ST', "ST_t-channel_antitop",  "ST t-channel at",       80.95, {"nevts" : 28814596.0} ),
        ( 'ST', "ST_tW_top",             "ST tW",                 35.85, {"nevts" : 3368237.0} ),
        ( 'ST', "ST_tW_antitop",         "ST atW",                35.85, {"nevts" : 3654330.0} ),
      ] 
    elif 'pre'  in era:
      expsamples = [ # table of MC samples to be converted to Sample objects
        # GROUP  NAME                     TITLE                  XSEC      EXTRA OPTIONS
        ( 'DY', "DYJetsToLL_M-50",       "Drell-Yan 50",         6075.0, {'extraweight': dyweight, "nevts": 95170542.0} ),
        ( 'WJ', "WJetsToLNu",            "W + jets",            61526.0, {"nevts" : 74676454.0 } ),
  
        ( 'VV', "WWTo2L2Nu",             "WW",                    11.09,{"nevts" : 3006596.0} ),
        ( 'VV', "WZTo2Q2L",              "WZ",                    6.419,{"nevts" : 9780392.0} ),
        ( 'VV', "WZTo3LNu",              "WZ",                    5.213,{"nevts" : 6363896.0} ),
        ( 'VV', "ZZTo2L2Nu",             "ZZ",                   0.6008,{"nevts" : 16826232.0} ),
        ( 'VV', "ZZTo2Q2L",              "ZZ",                    3.676,{"nevts" : 10406942.0} ),
        ( 'VV', "ZZTo4L",                "ZZ",                    1.325,{"nevts" : 49189654.0} ),

        ( 'TT', "TTTo2L2Nu",             "ttbar 2l2#nu",          88.29, {'extraweight': ttweight, "nevts" : 37202074.0} ),
        ( 'TT', "TTToSemiLeptonic",      "ttbar semileptonic",   365.35, {'extraweight': ttweight, "nevts" : 131106830.0} ),
        
        ( 'ST', "ST_t-channel_top",      "ST t-channel t",       136.02, {"nevts" : 52437432.0} ),
        ( 'ST', "ST_t-channel_antitop",  "ST t-channel at",       80.95, {"nevts" : 29205918.0} ),
        ( 'ST', "ST_tW_top",             "ST tW",                 35.85, {"nevts" : 3294485.0} ),
        ( 'ST', "ST_tW_antitop",         "ST atW",                35.85, {"nevts" : 3176335.0} ),
      ]   
  else:
    LOG.throw(IOError,"Did not recognize era %r!"%(era))
  
  # OBSERVED DATA SAMPLES
  if   'tautau' in channel: dataset = "Tau_Run%d?"%year
  elif 'mutau'  in channel: dataset = "SingleMuon_Run%d?"%year
  elif 'etau'   in channel: dataset = "EGamma_Run%d?"%year if year==2018 else "SingleElectron_Run%d?"%year
  elif 'mumu'   in channel: dataset = "SingleMuon_Run%d?"%year
  elif 'emu'    in channel: dataset = "SingleMuon_Run%d?"%year
  elif 'ee'     in channel: dataset = "EGamma_Run%d?"%year if year==2018 else "SingleElectron_Run%d?"%year
  else:
    LOG.throw(IOError,"Did not recognize channel %r!"%(channel))
  datasample = ('Data',dataset) # GROUP, NAME
  
  # FILTER
  if filter:
    expsamples = [s for s in expsamples if any(f in s[0] for f in filter)]
  if vetoes:
    expsamples = [s for s in expsamples if not any(v in s[0] for v in vetoes)]
  
  # SAMPLE SET
  if weight=="":
    weight = ""
  #elif channel in ['mutau','etau']:
  if 'mutau' in channel or 'etau' in channel:
    weight = "sign(genweight)*trigweight*puweight*idisoweight_1*idweight_2*ltfweight_2"
  elif channel in ['tautau','ditau']:
    weight = "genweight/fabs(genweight)*trigweight*puweight*idweight_1*idweight_2*ltfweight_1*ltfweight_2"
  else: # mumu, emu, ...
    weight = "sign(genweight)*trigweight*puweight*idisoweight_1*idisoweight_2"
  for sf in rmsfs: # remove (old) SFs, e.g. for SF measurement
    weight = weight.replace(sf,"").replace("**","*").strip('*')
  for sf in addsfs:  # add extra SFs, e.g. for SF measurement
    weight = joinweights(weight,sf)
  kwargs.setdefault('weight',weight) # common weight for MC
  kwargs.setdefault('fname', fname)  # default filename pattern
  sampleset = _getsampleset(datasample,expsamples,channel=channel,era=era,**kwargs)
  LOG.verb("weight = %r"%(weight),verbosity,1)
  
  # STITCH
  # Note: titles are set via STYLE.sample_titles
  #  sampleset.stitch("W*Jets",    incl='WJ',  name='WJ'     ) # W + jets
  #  sampleset.stitch("DY*J*M-50", incl='DYJ', name="DY_M50" ) # Drell-Yan, M > 50 GeV
  #sampleset.stitch("DY*J*M-10to50", incl='DYJ', name="DY_M10to50" )
  
  # JOIN
  sampleset.join('DY', name='DY' ) # Drell-Yan, M < 50 GeV + M > 50 GeV
  if 'VV' in join:
    sampleset.join('VV','WZ','WW','ZZ', name='VV' ) # Diboson
  if 'TT' in join and era!='year':
    sampleset.join('TT', name='TT' ) # ttbar
  if 'ST' in join:
    sampleset.join('ST', name='ST' ) # single top
  if 'Top' in join:
    sampleset.join('TT','ST', name='Top' ) # ttbar + single top
  
  # SPLIT
  # Note: titles are set via STYLE.sample_titles
  if split and channel.count('tau')==1:
    ZTT = STYLE.sample_titles.get('ZTT',"Z -> %s"%channel) # title
    if channel.count('tau')==1:
      ZTT = ZTT.replace("{l}","{mu}" if "mu" in channel else "{e}")
      GMR = "genmatch_2==5"
      GML = "genmatch_2>0 && genmatch_2<5"
      GMJ = "genmatch_2==0"
      GMF = "genmatch_2<5"
    elif channel.count('tau')==2:
      ZTT = ZTT.replace("{l}","{h}")
      GMR = "genmatch_1==5 && genmatch_2==5"
      GML = "(genmatch_1<5 || genmatch_2<5) && genmatch_1>0 && genmatch_2>0"
      GMJ = "(genmatch_1==0 || genmatch_2==0)"
      GMF = "(genmatch_1<5 || genmatch_2<5)"
    else:
      LOG.throw(IOError,"Did not recognize channel %r!"%(channel))
    if 'DM' in split: # split DY by decay modes
      samples.split('DY', [('ZTTDM0', ZTT+", h^{#pm}",                   GMR+" && dm_2==0"),
                           ('ZTTDM1', ZTT+", h^{#pm}h^{0}",              GMR+" && dm_2==1"),
                           ('ZTTDM10',ZTT+", h^{#pm}h^{#mp}h^{#pm}",     GMR+" && dm_2==10"),
                           ('ZTTDM11',ZTT+", h^{#pm}h^{#mp}h^{#pm}h^{0}",GMR+" && dm_2==11"),
                           ('ZL',GML),('ZJ',GMJ),])
    elif 'DY' in split:
      sampleset.split('DY',[('ZTT',ZTT,GMR),('ZL',GML),('ZJ',GMJ),])
    if 'TT' in split:
      sampleset.split('TT',[('TTT',GMR),('TTJ',GMF),])
  
  if table:
    sampleset.printtable(merged=True,split=True)
  print(">>> common weight: %r"%(weight))
  return sampleset
  
