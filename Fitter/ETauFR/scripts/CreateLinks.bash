#!/bin/bash
folder=/eos/cms/store/group/phys_tau/rasp/ETau_FR

#for s in DY ST TT VV WJ
#do
#    ln -s ${folder}/2025/${s} ${folder}/2026/${s}
#    ln -s ${folder}/2025/${s} ${folder}/2526/${s}
#done

#for era in B C D E F G
#do
#    for indx in 0 1 2 3
#    do
#	name=EGamma${indx}_Run2025${era}_etau.root
#	ln -s ${folder}/2025/Data/${name} ${folder}/2526/Data/${name}
#    done
#done

for era in B D
do
    for indx in 0 1 2 3 4 5
    do
	name=EGamma${indx}_Run2026${era}_etau.root
	ln -s ${folder}/2026/Data/${name} ${folder}/2526/Data/${name}	
    done
done
