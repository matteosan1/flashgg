import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
#from FWCore.ParameterSet.VarParsing import VarParsing
import sys

process = cms.Process("tnp")

###################################################################
myoptions = dict()
isMC = False

myoptions['HLTProcessName']        = "HLT"

#options['PHOTON_COLL']           = "slimmedPhotons"
myoptions['DIPHOTON_COLL']         = "flashggDiPhotons"
myoptions['PHOTON_CUTS']           = "(abs(superCluster.eta)<2.5) && ((superCluster.energy*sin(superCluster.position.theta))>20.0) && !(1.4442<=abs(superCluster.eta)<=1.566)"
myoptions['PHOTON_TAG_CUTS']       = "(abs(superCluster.eta)<=2.1) && !(1.4442<=abs(superCluster.eta)<=1.566) && (superCluster.energy*sin(superCluster.position.theta))>30.0"
myoptions['MAXEVENTS']             = cms.untracked.int32(-1) 
myoptions['useAOD']                = cms.bool(False)
myoptions['OUTPUTEDMFILENAME']     = 'edmFile.root'
myoptions['DEBUG']                 = cms.bool(False)
myoptions['LEADING_PRESELECTION']  = """(abs(leadingPhoton.superCluster.eta) < 2.5 && abs(subLeadingPhoton.superCluster.eta) < 2.5) &&
                                        (leadingPhoton.pt > 20) &&
                                        (leadingPhoton.hadronicOverEm < 0.1) &&
                                        ((leadingPhoton.full5x5_r9 > 0.5 && leadingPhoton.isEB) || (leadingPhoton.full5x5_r9 > 0.8 && leadingPhoton.isEE)) &&
                                        ((subLeadingPhoton.full5x5_r9 > 0.5 && subLeadingPhoton.isEB) || (subLeadingPhoton.full5x5_r9 > 0.8 && subLeadingPhoton.isEE)) &&
                                        ((leadingPhoton.isEB &&
                                        (leadingPhoton.full5x5_r9>0.85 ||
                                        (leadingPhoton.full5x5_sigmaIetaIeta < 0.015 && leadingPhoton.pfPhoIso03 < 4.0 && leadingPhoton.trkSumPtHollowConeDR03 < 6.0 ))) ||
                                        (leadingPhoton.isEE &&
                                        (leadingPhoton.full5x5_r9>0.9 ||
                                        (leadingPhoton.full5x5_sigmaIetaIeta < 0.035 && leadingPhoton.pfPhoIso03 < 4.0 && leadingPhoton.trkSumPtHollowConeDR03 < 6.0 )))) &&
                                        (leadingPhoton.pt > 14 && leadingPhoton.hadTowOverEm()<0.15 &&
                                        (leadingPhoton.r9()>0.8 || leadingPhoton.chargedHadronIso()<20 || leadingPhoton.chargedHadronIso()<0.3*leadingPhoton.pt()))                                                                                                                                                   
"""

myoptions['SUBLEADING_PRESELECTION'] = """(abs(leadingPhoton.superCluster.eta) < 2.5 && abs(subLeadingPhoton.superCluster.eta) < 2.5) &&
                                          (subLeadingPhoton.pt > 20) && 
                                          (subLeadingPhoton.hadronicOverEm < 0.1) &&
                                          ((leadingPhoton.full5x5_r9 > 0.5 && leadingPhoton.isEB) || (leadingPhoton.full5x5_r9 > 0.8 && leadingPhoton.isEE)) &&
                                          ((subLeadingPhoton.full5x5_r9 > 0.5 && subLeadingPhoton.isEB) || (subLeadingPhoton.full5x5_r9 > 0.8 && subLeadingPhoton.isEE)) &&
                                          (( subLeadingPhoton.isEB &&
                                          (subLeadingPhoton.full5x5_r9>0.85 ||
                                          (subLeadingPhoton.full5x5_sigmaIetaIeta < 0.015 && subLeadingPhoton.pfPhoIso03 < 4.0 && subLeadingPhoton.trkSumPtHollowConeDR03 < 6.0 ))) ||
                                          (subLeadingPhoton.isEE &&
                                          (subLeadingPhoton.full5x5_r9>0.9 ||
                                          (subLeadingPhoton.full5x5_sigmaIetaIeta < 0.035 && subLeadingPhoton.pfPhoIso03 < 6.0 && subLeadingPhoton.trkSumPtHollowConeDR03 < 6.0 )))) &&
                                          (subLeadingPhoton.pt > 14 && subLeadingPhoton.hadTowOverEm()<0.15 &&
                                          (subLeadingPhoton.r9()>0.8 || subLeadingPhoton.chargedHadronIso()<20 || subLeadingPhoton.chargedHadronIso()<0.3*subLeadingPhoton.pt()))
"""

from flashgg.Validation.treeMakerOptionsPhotons_cfi import *

if (isMC):
    myoptions['INPUT_FILE_NAME']       = ("/store/group/phys_higgs/cmshgg/sethzenz/flashgg/RunIISpring15-ReMiniAOD-BetaV6-25ns/Spring15BetaV6/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8//RunIISpring15-ReMiniAOD-BetaV6-25ns-Spring15BetaV6-v1-RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151015_170625/0000/myMicroAODOutputFile_1.root")

    myoptions['OUTPUT_FILE_NAME']      = "TnPTree_mc.root"
    myoptions['TnPPATHS']              = cms.vstring("HLT_Ele22_eta2p1_WP75_Gsf_v*")
    myoptions['TnPHLTTagFilters']      = cms.vstring("hltSingleEle22eta2p1WP75GsfTrackIsoFilter")
    myoptions['TnPHLTProbeFilters']    = cms.vstring()
    myoptions['HLTFILTERTOMEASURE']    = cms.vstring("")
    myoptions['GLOBALTAG']             = '74X_mcRun2_asymptotic_v2'
    myoptions['EVENTSToPROCESS']       = cms.untracked.VEventRange()
else:
    myoptions['INPUT_FILE_NAME']       = ("file:/afs/cern.ch/user/s/sani/eos//cms/store/group/phys_higgs/cmshgg/sethzenz/flashgg/RunIISpring15-ReMiniAOD-BetaV7-25ns/Spring15BetaV7/DoubleEG/RunIISpring15-ReMiniAOD-BetaV7-25ns-Spring15BetaV7-v0-Run2015D-05Oct2015-v1/151021_151712/0000/myMicroAODOutputFile_1.root")
    myoptions['OUTPUT_FILE_NAME']      = "TnPTree_data.root"
    myoptions['TnPPATHS']              =  cms.vstring("HLT_Ele22_eta2p1_WPLoose_Gsf_v*")
    myoptions['TnPHLTTagFilters']      =  cms.vstring("hltEle22WPLooseL1SingleIsoEG20erGsfTrackIsoFilter")
    myoptions['TnPHLTProbeFilters']    = cms.vstring()
    myoptions['HLTFILTERTOMEASURE']    = cms.vstring("")
    myoptions['GLOBALTAG']             = '74X_dataRun2_Prompt_v2'
    myoptions['EVENTSToPROCESS']       = cms.untracked.VEventRange()

###################################################################

setModules(process, myoptions)
from flashgg.Validation.treeContentPhotons_cfi import *

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = myoptions['GLOBALTAG']

process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(myoptions['INPUT_FILE_NAME']),
                            eventsToProcess = myoptions['EVENTSToPROCESS']
                            )

process.maxEvents = cms.untracked.PSet( input = myoptions['MAXEVENTS'])

###################################################################
## ID
###################################################################

from flashgg.Validation.photonIDModules_cfi import *
setIDs(process, myoptions)

###################################################################
## SEQUENCES
###################################################################

process.egmPhotonIDs.physicsObjectSrc = cms.InputTag("photonFromDiPhotons")

process.pho_sequence = cms.Sequence(
    process.photonFromDiPhotons +
    process.goodPhotonTags +
    process.goodPhotonProbes +
    process.goodPhotonProbesPreselection +
    process.goodPhotonProbesIDMVA +
    process.goodPhotonTagsIDMVA +
    process.goodPhotonsTagHLT +
    process.goodPhotonsProbeHLT +
    process.goodPhotonProbesL1
    )

###################################################################
## TnP PAIRS
###################################################################

process.allTagsAndProbes = cms.Sequence()
process.allTagsAndProbes *= process.tagTightRECO

process.mc_sequence = cms.Sequence()

if (isMC):
    process.mc_sequence *= (process.McMatchTag + process.McMatchRECO)

##########################################################################
## TREE MAKER OPTIONS
##########################################################################
if (not isMC):
    mcTruthCommonStuff = cms.PSet(
        isMC = cms.bool(False)
        )
    
process.PhotonToRECO = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                      mcTruthCommonStuff, CommonStuffForPhotonProbe,
                                      tagProbePairs = cms.InputTag("tagTightRECO"),
                                      arbitration   = cms.string("Random2"),
                                      flags         = cms.PSet(passingPresel  = cms.InputTag("goodPhotonProbesPreselection"),
                                                               passingIDMVA   = cms.InputTag("goodPhotonProbesIDMVA"),
                                                               ),                                               
                                      allProbes     = cms.InputTag("goodPhotonsProbeHLT"),
                                      )

if (isMC):
    process.PhotonToRECO.probeMatches  = cms.InputTag("McMatchRECO")
    process.PhotonToRECO.eventWeight   = cms.InputTag("generator")
    process.PhotonToRECO.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")
    process.PhotonToRECO.variables.Pho_dRTau  = cms.InputTag("GsfDRToNearestTauProbe")
    process.PhotonToRECO.tagVariables.probe_dRTau    = cms.InputTag("GsfDRToNearestTauProbe")

process.tree_sequence = cms.Sequence(process.PhotonToRECO)

##########################################################################
## PATHS
##########################################################################

process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string(myoptions['OUTPUTEDMFILENAME']),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
process.outpath = cms.EndPath(process.out)
if (not myoptions['DEBUG']):
    process.outpath.remove(process.out)

##########################################################################################
###### MICROAOD STUFF
##########################################################################################

process.load("flashgg/Taggers/flashggDiPhotonMVA_cfi")
process.flashggDiPhotonMVA.DiPhotonTag = cms.InputTag('flashggDiPhotons')

if (isMC):
    process.p = cms.Path(
        process.flashggDiPhotonMVA +
        process.sampleInfo +
        process.hltFilter +
        process.pho_sequence + 
        process.allTagsAndProbes +
        process.pileupReweightingProducer +
        process.mc_sequence + 
        process.GsfDRToNearestTauProbe + 
        process.GsfDRToNearestTauTag + 
        process.tree_sequence
        )
else:
    process.p = cms.Path(
        process.flashggDiPhotonMVA +
        process.sampleInfo +
        process.hltFilter +
        process.pho_sequence + 
        process.allTagsAndProbes +
        process.mc_sequence +
        process.tree_sequence
        )

process.TFileService = cms.Service("TFileService", 
                                   #fileName = cms.string(myoptions['OUTPUT_FILE_NAME']),
                                   fileName = cms.string("TnP.root"),
                                   closeFileFast = cms.untracked.bool(True)
                                   )

from flashgg.MetaData.JobConfig import JobConfig

customize = JobConfig(crossSections=["$CMSSW_BASE/src/flashgg/MetaData/data/cross_sections.json"])
customize.setDefault("maxEvents", 100)
customize.setDefault("targetLumi", 1)
customize(process)