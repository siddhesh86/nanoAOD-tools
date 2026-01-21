'''
    Hadd nanoaod ntuples in batch of, say, 50 files.

    To run:
    python3 haddnano_Hto4b.py <NanoAOD crab output base directory>  <crab directory name having time-stamp>

    For e.g.
    python3 haddnano_Hto4b.py  /eos/cms/store/group/phys_susy/HToaaTo4b/NanoAOD/2017/data/PNet_v2_2024_11_22/BTagCSV/r1_Run2017D    250625_193635

    or for /eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/SUSY_TTH_TTToAll_HToAATo4B_Pt150_M-11.0_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/0001/MiniAODv2_*.root
    python3 haddnano_Hto4b.py  /eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/SUSY_TTH_TTToAll_HToAATo4B_Pt150_M-11.0_TuneCP5_13TeV_madgraph_pythia8    RunIISummer20UL18
'''

import os
import sys
import subprocess
from pathlib import Path
import json
import glob
import argparse
import numpy as np


nFilesPerHadd = 100 #50
isDryRun = True




if __name__ == '__main__':

    

    print(sys.argv)
    sHaddDir = sys.argv[1]
    sCrabDir = sys.argv[2]

    print("sHaddDir: ", sHaddDir)
    print("sCrabDir: ", sCrabDir)
    print("nFilesPerHadd: ",nFilesPerHadd)

    #sIpNtuples = "PNet_v1_Skim_*.root"
    sIpNtuples = "PNet_v1_*_Skim.root" # PNet_v1_14_Skim.root
    sOpNtuples = "%s/PNet_v1_Skim_%d.root"
    if 'MiniAOD' in sHaddDir:
        # /eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/SUSY_TTH_TTToAll_HToAATo4B_Pt150_M-11.0_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/0001/MiniAODv2_199_nEvents500.root
        sIpNtuples = "MiniAODv2_*.root" # MiniAODv2_53_nEvents500.root
        sOpNtuples = "%s/MiniAODv2_%d.root"

    sIpNtupleFullName = "%s/%s/*/%s" % (sHaddDir, sCrabDir, sIpNtuples)
    print("sIpNtupleFullName: ", sIpNtupleFullName)

    ipFiles_list = glob.glob(sIpNtupleFullName)
    print("sIpNtupleFullName all: ", len(ipFiles_list), " \t :", ipFiles_list)


    nSplits = int(len(ipFiles_list) / nFilesPerHadd) + 1 if (nFilesPerHadd > 0) and (len(ipFiles_list) != nFilesPerHadd) else 1
    print("nSplits: ", nSplits)

    ipFiles_splitted = np.array_split(ipFiles_list, nSplits)
    print("ipFiles_splitted: ",ipFiles_splitted)

    for iJob in range(len(ipFiles_splitted)):
        sOpNtuple_i = sOpNtuples % (sHaddDir, iJob)
        sIpNtuples_i = ""
        for jIpFile in ipFiles_splitted[iJob]:
            sIpNtuples_i += " %s" % (jIpFile)

        command_i = "time haddnano.py %s   %s" % (sOpNtuple_i, sIpNtuples_i)
        print("\n\n\n iJob: ",iJob, ", len(ipFiles_splitted[iJob]): ", len(ipFiles_splitted[iJob]))
        print("\n command ", iJob, " : ", command_i, flush=True)
        if not isDryRun: os.system( command_i )

    print("haddnano.py is done for ", sHaddDir, flush=True)
    command_i = "ls -lh %s/*.root" % (sHaddDir)
    print("\n command  : ", command_i, flush=True)
    if not isDryRun: os.system( command_i )

