#!/bin/bash

./scripts/ControlPlotsMuTau.py --var m_vis --nbins 32 --xmin 0 --xmax 160 
./scripts/ControlPlotsMuTau.py --var met --nbins 20 --xmin 0 --xmax 200
./scripts/ControlPlotsMuTau.py --var pt_1 --nbins 20 --xmin 25 --xmax 125 
./scripts/ControlPlotsMuTau.py --var pt_2 --nbins 21 --xmin 20 --xmax 125
./scripts/ControlPlotsMuTau.py --var eta_1 --nbins 24 --xmin -2.4 --xmax 2.4 
./scripts/ControlPlotsMuTau.py --var eta_2 --nbins 24 --xmin -2.4 --xmax 2.4
./scripts/ControlPlotsMuTau.py --var rawDeepTau2018v2p5VSmu_2 --nbins 25 --xmin 0 --xmax 1


