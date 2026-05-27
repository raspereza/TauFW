#!/bin/bash
indir=/eos/cms/store/group/phys_tau/TauFW/pico2024/mutau_FR/2024/
outdir=/eos/cms/store/group/phys_tau/rasp/HighPT/2025
for s in DY ST TT VV WJ
do
    ln -s ${indir}/${s} ${outdir}/${s}
done
