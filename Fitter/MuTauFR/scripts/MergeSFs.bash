#!/bin/bash
n=$#
if [[ $n -ne 1 ]]; then
    echo usage MergeSFs.bash [era]
    echo era = [2022,2023,2024,2025,2026]
    exit
fi
era=$1
cd ${CMSSW_BASE}/src/TauFW/Fitter/MuTauFR/ScaleFactors
rm ${era}_ScaleFactors.root
hadd ${era}_ScaleFactors.root ${era}_*.root
cd -
