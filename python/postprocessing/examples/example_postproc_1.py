#!/usr/bin/env python
#from exampleModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
# soon to be deprecated
# new way of using jme uncertainty


# Function parameters
# (isMC=True, dataYear=2016, runPeriod="B", jesUncert="Total", redojec=False, jetType = "AK4PFchs", noGroom=False)
# All other parameters will be set in the helper module

#jmeCorrections = createJMECorrector(
#    True, "2016", "B", "Total", True, "AK4PFchs", False)
#jmeCorrections = createJMECorrector(
#    True, "2018", "D", "Total", True, "AK8PFchs", False)
jmeCorrections = createJMECorrector(
    True, "2018", "D", "Total", "AK8PFchs", False)

#fnames = ["/eos/cms/store/mc/RunIISummer16NanoAODv5/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7_ext2-v1/120000/FF69DF6E-2494-F543-95BF-F919B911CD23.root"]
fnames = ["/afs/cern.ch/work/s/ssawant/private/htoaa/NanoAODProduction_wPNetHToAATo4B/CMSSW_10_6_30/src/test/PNet_v1.root"] 

# p=PostProcessor(".",fnames,"Jet_pt>150","",[jetmetUncertainties2016(),exampleModuleConstr()],provenance=True)
#p = PostProcessor(".", fnames, "Jet_pt>150", "", [
#                  jmeCorrections(), exampleModuleConstr()], provenance=True)
p = PostProcessor(".", fnames, "",  modules=[
                  jmeCorrections()], provenance=True)
p.run()