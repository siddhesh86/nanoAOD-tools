#!/bin/bash

## Run ./scripts/crab_TTJets.sh CMD [TST] [OPT1] ... [OPT7]
## Where CMD = 'submit' or 'status',
##   and TST = 'test' for test mode
## See crab/README.md for some typical options, or run
## 'crab --help' for a more complete list, including:
## <<< crab status >>>
## '--verboseErrors' : Additional info on failed jobs
## '--long'   : Lists status of each individual job
## <<< crab resubmit >>> and <<< crab getlog >>>
## '--jobids' : Comma-separated list of job IDs
## <<< crab resubmit >>>
## '--force'  : What it sounds like
## '--maxjobruntime=3000' : Allow job to run for 2 days


## Construct the string for 'JetHT' samples in 2016 in DAS (https://cmsweb.cern.ch/das/)
## dasgoclient --query="dataset=/JetHT*/Run2016*UL2016*MiniAODv2*/MINIAODD"
declare -a datasets=()

# Data
datasets+=(
    #"/JetHT/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD"
    "/JetHT/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD"
    #"/JetHT/Run2016C-HIPM_UL2016_MiniAODv2-v2/MINIAOD"
    #"/JetHT/Run2016D-HIPM_UL2016_MiniAODv2-v2/MINIAOD"
    #"/JetHT/Run2016E-HIPM_UL2016_MiniAODv2-v2/MINIAOD"
    #"/JetHT/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD"
    "/JetHT/Run2016F-UL2016_MiniAODv2-v2/MINIAOD"
    #"/JetHT/Run2016G-UL2016_MiniAODv2-v2/MINIAOD"
    #"/JetHT/Run2016H-UL2016_MiniAODv2-v2/MINIAOD"
) 




 

CMD=$1
TST=$2
if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
    OPTS="$2 $3 $4 $5 $6 $7 $8"
else
    OPTS="$3 $4 $5 $6 $7 $8 $9"
fi

## Run in "test mode" if 2nd command is "test"
if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
    echo -e "\nGoing to run: 'crab $CMD $OPTS'\n"
else
    echo -e "\nGoing to run: 'crab $CMD $OPTS' (in TEST mode)\n"
fi

## Check to make sure the CRAB command is valid
if [ "$CMD" != "submit" ] && [ "$CMD" != "status" ] && [ "$CMD" != "resubmit" ] && [ "$CMD" != "getlog" ]; then
    echo -e "\n'crab $CMD' not an option! Quitting.\n"
    exit
fi 


if [ ! -d "crab/r1" ]; then
    mkdir -p "crab/r1"
fi

# Loop over datasets
for dataset in "${datasets[@]}"
do
    printf "\n\nRunning crab job for ${dataset} \n"

    # Use first part of dataset as directory name for crab job.
    # Add 'ext1' suffix to the directory name if dataset name contains 'ext' substring  
    IFS='/' read -r -a datasetNameInParts <<< "${dataset}"   # split dataset by '/'      
    datasetNamePart1=${datasetNameInParts[1]} # dataset (physics) name is at index 1
    datasetNamePart2=${datasetNameInParts[2]}
    datasetNamePart3=${datasetNameInParts[3]}
    datasetName_toUse=$datasetNamePart1

    outputDatasetTag_ext=""
    # For data, used datasetNamePart1_datasetNamePart2 as datasetName_toUse
    if [[ ${testmystring} != *"SIM"* ]]; then
        # /JetHT/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD
        # /JetHT/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD
        # /JetHT/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD
        # /JetHT/Run2016F-UL2016_MiniAODv2-v2/MINIAOD
        IFS='-' read -r -a datasetNamePart2_subparts <<< "${datasetNamePart2}"
        datasetNamePart2_0=${datasetNamePart2_subparts[0]}

        # take substring before 'UL2016' from ${datasetNamePart2_subparts[0]}
        IFS='UL' read -r -a datasetNamePart2_1_subparts <<< "${datasetNamePart2_subparts[1]}"
        datasetNamePart2_1="_${datasetNamePart2_1_subparts[0]}"
        if [[ ${datasetNamePart2_1} = *_ ]]; then   # drop tailing '_' character
            datasetNamePart2_1=${datasetNamePart2_1::-1}            
        fi

        datasetName_toUse="${datasetNamePart1}_${datasetNamePart2_0}${datasetNamePart2_1}"
        outputDatasetTag_ext="_${datasetNamePart2_0}${datasetNamePart2_1}"
    fi

    # Check if datasetNamePart2 contains 'ext1' strin, and if so, then update datasetName_toUse  
    IFS='_' read -r -a datasetNamePart2_subparts <<< "${datasetNamePart2}"    # split dataset by '_' 
    for substr1 in "${datasetNamePart2_subparts[@]}"
    do
        IFS='-' read -r -a substr1_parts <<< "${substr1}"  # split dataset by '_' 
        for substr2 in "${substr1_parts[@]}"
        do
            if [[ $substr2 = *ext* ]]; then
                datasetName_toUse="${datasetName_toUse}_${substr2}"
            fi
        done
    done
    printf "datasetName_toUse: ${datasetName_toUse} \n" 


    ## <<< *********************************** >>>
    ## <<< ** crab status, resubmit, getlog ** >>>
    ## <<< *********************************** >>>
    if [ "$CMD" = "status" ] || [ "$CMD" = "resubmit" ] || [ "$CMD" = "getlog" ]; then
	    echo crab ${CMD} -d crab/r1/crab_${datasetName_toUse} $OPTS
	    if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
	        crab ${CMD} -d crab/r1/crab_${datasetName_toUse} $OPTS
	    fi
    fi


    ## <<< ***************** >>>
    ## <<< ** crab submit ** >>>
    ## <<< ***************** >>>
    if [ "$CMD" = "submit" ]; then
	    ## Submit crab jobs
	    echo crab submit -c crab_config.py $OPTS Data.inputDataset="${dataset}" General.requestName="${datasetName_toUse}" Data.outputDatasetTag="r1${outputDatasetTag_ext}"
	    if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
	        crab submit -c crab_config.py $OPTS Data.inputDataset="${dataset}" General.requestName="${datasetName_toUse}" Data.outputDatasetTag="r1${outputDatasetTag_ext}"
	    fi
    fi

done
