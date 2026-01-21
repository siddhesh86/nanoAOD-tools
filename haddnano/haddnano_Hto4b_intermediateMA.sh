#!/bin/bash

### USERS settings ------------------------------------------------------------------------------------

## Higgs production mode
prodmodes=("SUSY_GluGluH_01J_HToAATo4B"
           "SUSY_VBFH_HToAATo4B"
           "SUSY_WH_WToAll_HToAATo4B"
           "SUSY_ZH_ZToAll_HToAATo4B"
           "SUSY_TTH_TTToAll_HToAATo4B")
#prodmodes=("SUSY_TTH_TTToAll_HToAATo4B")
#prodmodes=("SUSY_GluGluH_01J_HToAATo4B")

#HiggsPtMinList=(150 250 350 450)
HiggsPtMinList=(150)

## "a" boson mass points
#mApoints=(12 15 20 25 30 35 40 45 50 55 60)
#mApoints=(8.5 9.0 9.5 10.0 10.5 11.0 11.5 12.5 13.0 13.5 14.0 16.0 17.0 18.5 21.5 23.0 27.5 32.5 37.5 42.5 47.5 52.5 57.5 62.5)
mApoints=(11.0 11.5 12.5 13.0 13.5 14.0 16.0 17.0 18.5 21.5 23.0 27.5 32.5 37.5 42.5 47.5 52.5 57.5 62.5)
#mApoints=(11.0)

# Decay width of a-boson
wA=0 # 0 for narrow A width sample. 10 or 70 for broader A width samples. 

## Dataset ERA
#ERA="RunIISummer20UL17" # Options: "RunIISummer20UL18", "RunIISummer20UL17", "RunIISummer20UL16", "RunIISummer20UL16APV"
#Eras=("RunIISummer20UL18"
#	  "RunIISummer20UL17"
#	  "RunIISummer20UL16"
#	  "RunIISummer20UL16APV")
Eras=("RunIISummer20UL18")

# set first (SampleNumber_First) to last (SampleNumber_Last) MC sample file numbers to be produced in this round of submission/execution.
SampleNumber_First=0
SampleNumber_Last=0


	  
### USERS settings ENDS --------------------------------------------------------------------------------

### Information
# GEN-filter efficiency: 
#     0.057 for SUSY_GluGluH_01J_HToAATo4B_Pt150
#     0.173 for SUSY_VBFH_HToAATo4B_Pt150
#     0.132 for SUSY_WH_WToAll_HToAATo4B_Pt150
#     0.129 for SUSY_ZH_ZToAll_HToAATo4B_Pt150
#     0.285 for SUSY_TTH_TTToAll_HToAATo4B_Pt150


UserName=$(whoami)
XRootDRedirector="xrootd-cms.infn.it"
sFParams="params_MCGeneration_HToAATo4B_M-x.txt"


## Data taking years
for ERA in "${Eras[@]}"
do
	
	EraYear=2018
	## ERA: RunIISummer20UL18, RunIISummer20UL17, RunIISummer20UL16, RunIISummer20UL16APV
	if   [[ ${ERA} == *"16"*  && ${ERA} == *"APV"* ]]; then 
		EraYear="2016APV"
	elif [[ ${ERA} == *"16"* ]]; then 
		EraYear="2016"
	elif [[ ${ERA} == *"17"* ]]; then
		EraYear=2017
	elif [[ ${ERA} == *"18"* ]]; then
		EraYear=2018
	fi

	## Loop over all Higgs production modes
	for prod in "${prodmodes[@]}"
	do
		## Loop over all "a" boson mass points
		for mA in "${mApoints[@]}"
		do

            ## Loop over HiggsPtMinList
            for HiggsPtMin in "${HiggsPtMinList[@]}"
            do

                # /eos/cms/store/group/phys_susy/HToaaTo4b/NanoAOD/2018/MC/PNet_v2_2024_11_22/SUSY_VBFH_HToAATo4B_Pt150_M-18.5_TuneCP5_13TeV_madgraph_pythia8/r1/20251107_000000/0000/PNet_v1_14_Skim.root
                nanoAOD_dir="/eos/cms/store/group/phys_susy/HToaaTo4b/NanoAOD/${EraYear}/MC/PNet_v2_2024_11_22/${prod}_Pt${HiggsPtMin}_M-${mA}_TuneCP5_13TeV_madgraph_pythia8/r1"
                crabDir_timeStamp="20251107_000000"
                printf " time python3 haddnano_Hto4b.py ${nanoAOD_dir} ${crabDir_timeStamp} : "
                time python3 haddnano_Hto4b.py ${nanoAOD_dir} ${crabDir_timeStamp}
                printf "\n"
                                
            done
		done
	done
done
	    
