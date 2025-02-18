# cmsDriver.py --python_filename HIG-RunIISummer20UL18NanoAODv9-02146_1_cfg.py --eventcontent NANOAODSIM --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02146.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --era Run2_2016,run2_nanoAOD_106Xv2 --no_exec --mc -n 100

MAX_EVT  = 1000  ## Maximum number of events to process
PRT_EVT  = 1    ## Print every Nth event
SAMP     = 'HtoAA_MH-125_MA-50'  ## Sample to process
#SAMP     = 'QCD_BGen_HT700to1000'  ## Sample to process
## HToAA_Pt350_mH-70_mA-12, HtoAA_MH-125_MA-20
## QCD_BGen_HT700to1000, QCD_bEnr_HT700to1000
## ZJetsToQQ_HT-200to400, ZJetsToQQ_HT-400to600, ZJetsToQQ_HT-600to800

SEL_FAT_PT        = 170    ## Minimum pT for selected AK8 jets
SEL_FAT_ETA       = 2.4    ## Maximum |eta| for selected AK8 jets
SEL_FAT_MASS      = -99    ## Minimum mass for selected AK8 jets
SEL_FAT_MSOFT     =  10    ## Minimum soft-drop mass for selected AK8 jets
CAND_FAT_XBB      = 0.6    ## Minimum Xbb score for Haa4b candidate AK8 jets
CAND_FAT_HAA34B   = -99    ## Minimum Haa34b score for Haa4b candidate AK8 jets
CAND_FAT_HAA4B    = -99    ## Minimum Haa4b score for Haa4b candidate AK8 jets
CAND_FAT_GENB     = -99    ## Minimum number of GEN b-hadrons for Haa4b candidate
SKIM_FAT          = True  ## Discard events with 0 AK8 jets
SKIM_FAT_SEL      = True  ## Discard events with 0 selected AK8 jets
SKIM_FAT_CAND     = True  ## Discard events with 0 Haa4b candidate AK8 jets

import os
import sys
import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run2_2016_cff import Run2_2016
from Configuration.Eras.Modifier_run2_nanoAOD_106Xv2_cff import run2_nanoAOD_106Xv2

process = cms.Process('NANO',Run2_2016,run2_nanoAOD_106Xv2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_addHto4bPlus_cff')
#process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(MAX_EVT)
)
process.MessageLogger.cerr.FwkReport.reportEvery = PRT_EVT


in_files = ['/store/mc/RunIISummer20UL16MiniAODv2/SUSY_GluGluH_01J_HToAATo4B_Pt150_M-12_TuneCP5_13TeV_madgraph_pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/2550000/E9443C37-2553-0C47-84D5-8316ADD6BAE6.root']

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(in_files[0]),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--python_filename nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output file name
out_file = 'file:output/HtoAA_addHto4bPlus_'+SAMP
#out_file = 'file:output/HtoAA_noHto4bPlus_'+SAMP

if SEL_FAT_PT > 0:      out_file += ('_Pt%d' % SEL_FAT_PT)
if SEL_FAT_ETA < 9.9:   out_file += ('_Eta'+str(SEL_FAT_ETA).replace('.','p'))
if SEL_FAT_MASS > 0:    out_file += ('_Mass%d' % SEL_FAT_MASS)
if SEL_FAT_MSOFT > 0:   out_file += ('_Msoft%d' % SEL_FAT_MSOFT)
if CAND_FAT_XBB > 0:    out_file += ('_Xbb'+str(CAND_FAT_XBB).replace('.','p'))
if CAND_FAT_HAA34B > 0: out_file += ('_Haa34b'+str(CAND_FAT_HAA34B).replace('.','p'))
if CAND_FAT_HAA4B > 0:  out_file += ('_Haa4b'+str(CAND_FAT_HAA4B).replace('.','p'))
if CAND_FAT_GENB > 0:   out_file += ('_Gen%db' % CAND_FAT_GENB)

if SKIM_FAT_CAND:  out_file += ('_skimFatCand')
elif SKIM_FAT_SEL: out_file += ('_skimFatSel')
elif SKIM_FAT:     out_file += ('_skimFat')

if MAX_EVT > 0: out_file += '_%dk' % (MAX_EVT / 1000)
out_file += '.root'

# Output definition
process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    selFatJetPt = cms.untracked.double(SEL_FAT_PT),
    selFatJetEta = cms.untracked.double(SEL_FAT_ETA),
    selFatJetMass = cms.untracked.double(SEL_FAT_MASS),
    selFatJetMsoft = cms.untracked.double(SEL_FAT_MSOFT),
    candFatJetXbb = cms.untracked.double(CAND_FAT_XBB),
    candFatJetHaa34b = cms.untracked.double(CAND_FAT_HAA34B),
    candFatJetHaa4b = cms.untracked.double(CAND_FAT_HAA4B),
    candFatJetGenNb = cms.untracked.int32(CAND_FAT_GENB),
    skimFatJet = cms.untracked.bool(SKIM_FAT),
    skimFatJetSel = cms.untracked.bool(SKIM_FAT_SEL),
    skimFatJetCand = cms.untracked.bool(SKIM_FAT_CAND),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    # fileName = cms.untracked.string(out_file),  ## Unique, local file name
    fileName = cms.untracked.string('PNet_v1.root'),  ## Basic name for CRAB jobs
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_v17', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# Customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_addHto4bPlus_cff
from PhysicsTools.NanoAOD.nano_addHto4bPlus_cff import nanoAOD_customizeMC 

# Call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_addHto4bPlus_cff
process = nanoAOD_customizeMC(process,SEL_FAT_PT,SEL_FAT_ETA,SEL_FAT_MASS,SEL_FAT_MSOFT,
                              CAND_FAT_XBB,CAND_FAT_GENB,SKIM_FAT,SKIM_FAT_CAND)

#from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC
#process = nanoAOD_customizeMC(process)

# Add PFNano branches for Lund Plane reweighting
from PhysicsTools.PFNano.pfnano_cff import PFnano_customizeMC_Haa4b
process = PFnano_customizeMC_Haa4b(process, SKIM_FAT_SEL)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

process.options.numberOfThreads=cms.untracked.uint32(4)
process.options.numberOfStreams=cms.untracked.uint32(0)
