#!/bin/bash

indir2025=/eos/cms/store/group/phys_tau/rasp/HighPT/2025/Data
indir2026=/eos/cms/store/group/phys_tau/rasp/HighPT/2026/Data
outdir=/eos/cms/store/group/phys_tau/rasp/HighPT/2526/Data

for era in B C D E F G 
do
    ln -s ${indir2025}/Muon0_Run2025${era}_mutau.root ${outdir}/Muon0_Run2025${era}_mutau.root
    ln -s ${indir2025}/Muon1_Run2025${era}_mutau.root ${outdir}/Muon1_Run2025${era}_mutau.root
done

for era in B D 
do
    ln -s ${indir2026}/Muon0_Run2026${era}_mutau.root ${outdir}/Muon0_Run2026${era}_mutau.root
    ln -s ${indir2026}/Muon1_Run2026${era}_mutau.root ${outdir}/Muon1_Run2026${era}_mutau.root
    ln -s ${indir2026}/Muon2_Run2026${era}_mutau.root ${outdir}/Muon2_Run2026${era}_mutau.root
    ln -s ${indir2026}/Muon3_Run2026${era}_mutau.root ${outdir}/Muon3_Run2026${era}_mutau.root
done
