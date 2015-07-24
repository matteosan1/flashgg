import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils

process = cms.Process("FLASHggMicroAODAndTag")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = 'MCRUN2_74_V9A'

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1000 )

#process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/mc/Spring14miniaod/GluGluToHToGG_M-125_13TeV-powheg-pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v2/00000/24926621-F11C-E411-AB9A-02163E008D0B.root"))
#process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/mc/Spring14miniaod/TTbarH_HToGG_M-125_13TeV_amcatnlo-pythia8-tauola/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/049C0F9C-E61E-E411-9388-D8D385AE8466.root"))                                                                                                                            
process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/group/phys_higgs/cmshgg/mdonega/flashgg/RunIISpring15-50ns/Spring15BetaV2/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/RunIISpring15-50ns-Spring15BetaV2-v0-RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/150716_154944/0000/myMicroAODOutputFile_10.root"))

#fixme selectedFlashggJets
process.load("flashgg/MicroAOD/flashggMicroAODSequence_cff")
process.load("flashgg/Taggers/flashggTagSequence_cfi")
process.load("flashgg/Taggers/flashggTagTester_cfi")

process.commissioning = cms.EDAnalyzer('FlashggFlashggTreeMakerWithTagSorter',
                                       VertexTag=cms.untracked.InputTag('offlineSlimmedPrimaryVertices'),
                                       VertexCandidateMapTagDz=cms.InputTag('flashggVertexMapUnique'),
                                       VertexCandidateMapTagAOD = cms.InputTag('flashggVertexMapValidator'),
                                       JetTagDz=cms.InputTag("flashggJets"),
                                       DiPhotonTag = cms.InputTag('flashggDiPhotons'),
                                       rhoFixedGridCollection=cms.InputTag('fixedGridRhoAll'),
                                       lumiWeight = cms.double(1.0),
                                       sampleIndex = cms.int32(0)
                                       )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("~/mounteos/cms/store/group/phys_higgs/soffi/flashgg/testMonoHLivia/Phys14MicroAODV3-55-gc1f8d91/Higgs_scalar/testMonoHLivia-Phys14MicroAODV3-55-gc1f8d91-v0-soffi-Higgs_scalar_nohdecay_gg_10GeV_13TeV_MINIAODSIM_v6-7d492cb64f2cdaff326f939f96e45c96/150703_144622/0000/myMicroAODOutputFile_10.root")
)

process.p = cms.Path(process.flashggTagSequence*process.commissioning)

from flashgg.MetaData.JobConfig import JobConfig

customize = JobConfig(crossSections=["$CMSSW_BASE/src/flashgg/MetaData/data/cross_sections.json"])
customize.setDefault("maxEvents", 100)
customize.setDefault("targetLumi", 1)
customize(process)
