#!/bin/bash
# $1 - era
# $2 - WPvsJet
# $3 - WPvsMu
# $4 - WPvsE
# $5 - eta
n=$#
if [[ $n -ne 5 ]]; then
    echo usage : FitMuTauFR.bash [ERA] [CHANNEL]
    echo ERA = [2024]
    echo WPvsJet = [Medium]
    echo WPvsMu = [VLoose]
    echo WPvsE = [VVLoose]
    echo Eta = [0p0to0p9]
    exit
fi

era=${1}
wp_jet=${2}
wp_mu=${3}
wp_e=${4}
eta=${5}
folder=${CMSSW_BASE}/src/TauFW/Fitter/MuTauFR/datacards/${wp_jet}VsJet_${wp_mu}VsMu_${wp_e}VsE
cd ${folder}
name=${era}_eta${eta}
combineTool.py -M T2W -o ${name}_ws.root -i ${name}.txt -m 90
combineTool.py -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL -m 90 --robustHesse 1 -d ${name}_ws.root --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1 -v 2
mv fitDiagnostics.Test.root ${name}_fit.root
cd -
