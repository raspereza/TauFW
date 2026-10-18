#!/bin/bash
n=$#
if [[ $n -ne 1 ]]; then
    echo usage MergeSFs.bash [era]
    echo era = [2022,2023,2024,2025,2026,2526]
    exit
fi
era=$1
cd ${CMSSW_BASE}/src/TauFW/Fitter/ETauFR/ScaleFactors
rm ${era}_ScaleFactors.root
hadd ${era}_ScaleFactors.root ${era}_*.root
cd ${CMSSW_BASE}/src/TauFW/Fitter/ETauFR/ScaleFactors_fes
rm ${era}_ScaleFactors.root
hadd ${era}_ScaleFactors.root ${era}_*.root
cd -
