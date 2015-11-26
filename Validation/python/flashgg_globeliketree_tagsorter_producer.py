import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils

process = cms.Process("FLASHggMicroAODAndTag")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = 'MCRUN2_74_V9A'

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1000 )

process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring(
"/store/group/phys_higgs/cmshgg/sethzenz/flashgg/RunIISpring15-ReMiniAOD-BetaV7-25ns/Spring15BetaV7//DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15-ReMiniAOD-BetaV7-25ns-Spring15BetaV7-v0-RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151021_151505/0000/myMicroAODOutputFile_99.root", 
#"/store/group/phys_higgs/cmshgg/sethzenz/flashgg/RunIISpring15-ReMiniAOD-BetaV7-25ns/Spring15BetaV7/DoubleEG/RunIISpring15-ReMiniAOD-BetaV7-25ns-Spring15BetaV7-v0-Run2015D-05Oct2015-v1/151021_151712/0000/myMicroAODOutputFile_99.root"
))


process.load("flashgg/MicroAOD/flashggMicroAODSequence_cff")
process.load("flashgg/Taggers/flashggTagSequence_cfi")

process.flashggTagSorter.massCutUpper=cms.untracked.double(180.)
process.flashggTagSorter.massCutLower=cms.untracked.double(0.)
process.flashggUntagged.Boundaries=cms.untracked.vdouble(-99999.,0.31,0.62,0.86,0.98)

process.load("flashgg/Taggers/flashggTagTester_cfi")

from flashgg.MicroAOD.flashggJets_cfi import flashggBTag, maxJetCollections

flashggUnpackedJets = cms.EDProducer("FlashggVectorVectorJetUnpacker",
                                     JetsTag = cms.InputTag("flashggFinalJets"),
                                     NCollections = cms.uint32(maxJetCollections)
                                     )

UnpackedJetCollectionVInputTag = cms.VInputTag()
for i in range(0,maxJetCollections):
    UnpackedJetCollectionVInputTag.append(cms.InputTag('flashggUnpackedJets',str(i)))


process.commissioning = cms.EDAnalyzer('FlashggFlashggTreeMakerWithTagSorter',
                                       genEventInfoName = cms.untracked.InputTag('generator'),
                                       VertexTag = cms.untracked.InputTag('offlineSlimmedPrimaryVertices'),
                                       VertexCandidateMapTagDz = cms.InputTag('flashggVertexMapUnique'),
                                       VertexCandidateMapTagAOD = cms.InputTag('flashggVertexMapValidator'),
                                       inputTagJets = UnpackedJetCollectionVInputTag,
                                       DiPhotonTag = cms.InputTag('flashggDiPhotons'),
                                       rhoFixedGridCollection = cms.InputTag('fixedGridRhoAll'),
                                       #PileUpTag = cms.untracked.InputTag( "addPileupInfo"),
                                       lumiWeight = cms.double(1.0),
                                       sampleIndex = cms.int32(-1000),
                                       #processId = cms.string("poppo"),                                       
                                       puReWeight = cms.bool(True),
                                       dataPu = cms.vdouble(),
                                       mcPu = cms.vdouble(),
                                       #puBins = cms.int32(50),
                                       #minpu = cms.double(0),
                                       #maxpu = cms.double(100),
                                       )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("~/mounteos/cms/store/group/phys_higgs/soffi/flashgg/testMonoHLivia/Phys14MicroAODV3-55-gc1f8d91/Higgs_scalar/testMonoHLivia-Phys14MicroAODV3-55-gc1f8d91-v0-soffi-Higgs_scalar_nohdecay_gg_10GeV_13TeV_MINIAODSIM_v6-7d492cb64f2cdaff326f939f96e45c96/150703_144622/0000/myMicroAODOutputFile_10.root")
)

process.p = cms.Path(process.flashggTagSequence*process.commissioning)

from flashgg.MetaData.JobConfig import JobConfig

customize = JobConfig(crossSections=["$CMSSW_BASE/src/flashgg/MetaData/data/cross_sections.json"])
#customize.setDefault("maxEvents", 100)
#customize.setDefault("targetLumi", 1)
customize(process)
