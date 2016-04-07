import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
import FWCore.ParameterSet.VarParsing as VarParsing

from flashgg.MetaData.samples_utils import SamplesManager

process = cms.Process("mytest")

process.load("HLTrigger.HLTfilters.hltHighLevel_cfi")
process.hltFilter = process.hltHighLevel.clone()
process.hltFilter.throw = cms.bool(True)

from flashgg.MetaData.JobConfig import  JobConfig
customize = JobConfig(crossSections=["$CMSSW_BASE/src/flashgg/MetaData/data/cross_sections.json"])
customize.setDefault("maxEvents",15000)
customize.setDefault("targetLumi",2.6e+4)
customize.parse()

if ("data" in customize.processId):
    process.hltFilter.HLTPaths = cms.vstring("HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v*",
                                             "HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v*",
                                             "HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v*")
else :
    process.hltFilter.HLTPaths = cms.vstring("*")

process.load('RecoMET.METFilters.eeBadScFilter_cfi')
process.eeBadScFilter.EERecHitSource = cms.InputTag("reducedEgamma","reducedEERecHits") # Saved MicroAOD Collection (data only)
process.dataRequirements = cms.Sequence()
process.dataRequirements += process.hltHighLevel

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 10000 )

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService")

if ("data" in customize.processId):
    process.GlobalTag.globaltag = '76X_dataRun2_v15'
else:
    process.GlobalTag.globaltag = '76X_mcRun2_asymptotic_v12'

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/s/sani/mounteos/cms/store/group/phys_higgs/cmshgg/ferriff/flashgg/RunIIFall15DR76-1_3_0-25ns_ext1/1_3_1/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/160127_023250/0000/myMicroAODOutputFile_1.root",
))

# IN THIS TREE THE PHOTON CORRECTIONS ARE MISSING !!!
# USELESS FOR THE MOMENT SINCE THE photonIDMVA for vtx 0 is not accessible through the cut string below
#process.flashggPhotonSelector = cms.EDFilter("FlashggPhotonSelector",
#                                             src = cms.InputTag('flashggPhotons'),
#                                             cut = cms.string("")
#                                             )
    
process.load("flashgg/MicroAOD/flashggQuadPhotonProducer_cfi")
process.flashggQuadPhotonProducer.photonTag = cms.InputTag('flashggRandomizedPhotons')

process.load("flashgg/Taggers/quadPhotonDumper_cfi")
process.quadPhotonDumper.src = cms.InputTag("flashggQuadPhotonProducer")

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("histo.root"),
                                   closeFileFast = cms.untracked.bool(True)
                                   )

import flashgg.Taggers.dumperConfigTools as cfgTools
cfgTools.addCategories(process.quadPhotonDumper,
                       ## categories definition
                       ## cuts are applied in cascade. Events getting to these categories have already failed the "Reject" selection
                       [("All", 
"""
size>=4 && 
photonIDMVA(0)>-.9 && photon(0).et>25 && 
photonIDMVA(1)>-.9 && photon(1).et>25 &&
photonIDMVA(2)>-.9 && photon(2).et>25 &&
photonIDMVA(3)>-.9 && photon(3).et>25 
"""
                         , 0)],
                       variables=["et1 := photon(0).et",
                                  "eta1 := photon(0).eta",
                                  "phi1 := photon(0).phi",
                                  "r91 := photon(0).full5x5_r9",
                                  "e1x31 :=  photon(0).e1x3",
                                  "e2x51 :=  photon(0).e2x5",
                                  "e3x31 :=  photon(0).e3x3",
                                  "e5x51 :=  photon(0).e5x5",                                  
                                  "sieie1 := photon(0).full5x5_sigmaIetaIeta",
                                  "hoe1 := photon(0).hadronicOverEm",
                                  "sigmaEoE1 := photon(0).sigEOverE",
                                  "chisow1 := photon(0).pfChgIsoWrtWorstVtx04",
                                  "phoiso1 := photon(0).pfPhoIso03",
                                  "pfcluecal03_1 := photon(0).ecalPFClusterIso",
                                  "pfcluhcal03_1 := photon(0).hcalPFClusterIso",
                                  "trkiso03_1 := photon(0).trkSumPtHollowConeDR03",
                                  "pfchiso02_1 := photon(0).pfChgIso02WrtVtx0",
                                  "chiso1 := photon(0).pfChgIso03WrtVtx0",
                                  "isEB1 := photon(0).isEB",
                                  "csev1 := photon(0).passElectronVeto",
                                  "haspixelseed1 := photon(0).hasPixelSeed",
                                  "sieip1 := photon(0).sieip",
                                  "etawidth1 := photon(0).superCluster.etaWidth",
                                  "phiwidth1 := photon(0).superCluster.phiWidth",
                                  "regrerr1 := photon(0).sigEOverE * photon(0).energy",
                                  "s4ratio1 :=  photon(0).s4",
                                  "effSigma1 :=  photon(0).esEffSigmaRR",
                                  "scraw1 :=  photon(0).superCluster.rawEnergy",
                                  "ese1 :=  photon(0).superCluster.preshowerEnergy",                                  
                                  "idmva1 := photonIDMVA(0)",
                                  "genmatch1 := genMatch(0)",

                                  "et2 := photon(1).et",
                                  "eta2 := photon(1).eta",
                                  "phi2 := photon(1).phi",
                                  "r92 := photon(1).full5x5_r9",
                                  "e1x32 :=  photon(1).e1x3",
                                  "e2x52 :=  photon(1).e2x5",
                                  "e3x32 :=  photon(1).e3x3",
                                  "e5x52 :=  photon(1).e5x5",                                  
                                  "sieie2 := photon(1).full5x5_sigmaIetaIeta",
                                  "hoe2 := photon(1).hadronicOverEm",
                                  "sigmaEoE2 := photon(1).sigEOverE",
                                  "chisow2 := photon(1).pfChgIsoWrtWorstVtx04",
                                  "phoiso2 := photon(1).pfPhoIso03",
                                  "pfcluecal03_2 := photon(1).ecalPFClusterIso",
                                  "pfcluhcal03_2 := photon(1).hcalPFClusterIso",
                                  "trkiso03_2 := photon(1).trkSumPtHollowConeDR03",
                                  "pfchiso02_2 := photon(1).pfChgIso02WrtVtx0",
                                  "chiso2 := photon(1).pfChgIso03WrtVtx0",
                                  "isEB2 := photon(1).isEB",
                                  "csev2 := photon(1).passElectronVeto",
                                  "haspixelseed2 := photon(1).hasPixelSeed",
                                  "sieip2 := photon(1).sieip",
                                  "etawidth2 := photon(1).superCluster.etaWidth",
                                  "phiwidth2 := photon(1).superCluster.phiWidth",
                                  "regrerr2 := photon(1).sigEOverE * photon(1).energy",
                                  "s4ratio2 :=  photon(1).s4",
                                  "effSigma2 :=  photon(1).esEffSigmaRR",
                                  "scraw2 :=  photon(1).superCluster.rawEnergy",
                                  "ese2 :=  photon(1).superCluster.preshowerEnergy",                                  
                                  "idmva2 := photonIDMVA(1)",
                                  "genmatch2 := genMatch(1)",

                                  "et3 := photon(2).et",
                                  "eta3 := photon(2).eta",
                                  "phi3 := photon(2).phi",
                                  "r93 := photon(2).full5x5_r9",
                                  "e1x33 :=  photon(2).e1x3",
                                  "e2x53 :=  photon(2).e2x5",
                                  "e3x33 :=  photon(2).e3x3",
                                  "e5x53 :=  photon(2).e5x5",                                  
                                  "sieie3 := photon(2).full5x5_sigmaIetaIeta",
                                  "hoe3 := photon(2).hadronicOverEm",
                                  "sigmaEoE3 := photon(2).sigEOverE",
                                  "chisow3 := photon(2).pfChgIsoWrtWorstVtx04",
                                  "phoiso3 := photon(2).pfPhoIso03",
                                  "pfcluecal03_3 := photon(2).ecalPFClusterIso",
                                  "pfcluhcal03_3 := photon(2).hcalPFClusterIso",
                                  "trkiso03_3 := photon(2).trkSumPtHollowConeDR03",
                                  "pfchiso02_3 := photon(2).pfChgIso02WrtVtx0",
                                  "chiso3 := photon(2).pfChgIso03WrtVtx0",
                                  "isEB3 := photon(2).isEB",
                                  "csev3 := photon(2).passElectronVeto",
                                  "haspixelseed3 := photon(2).hasPixelSeed",
                                  "sieip3 := photon(2).sieip",
                                  "etawidth3 := photon(2).superCluster.etaWidth",
                                  "phiwidth3 := photon(2).superCluster.phiWidth",
                                  "regrerr3 := photon(2).sigEOverE * photon(2).energy",
                                  "s4ratio3 :=  photon(2).s4",
                                  "effSigma3 :=  photon(2).esEffSigmaRR",
                                  "scraw3 :=  photon(2).superCluster.rawEnergy",
                                  "ese3 :=  photon(2).superCluster.preshowerEnergy",                                  
                                  "idmva3 := photonIDMVA(2)",
                                  "genmatch3 := genMatch(2)",

                                  "et4 := photon(3).et",
                                  "eta4 := photon(3).eta",
                                  "phi4 := photon(3).phi",
                                  "r94 := photon(3).full5x5_r9",
                                  "e1x34 :=  photon(3).e1x3",
                                  "e2x54 :=  photon(3).e2x5",
                                  "e3x34 :=  photon(3).e3x3",
                                  "e5x54 :=  photon(3).e5x5",                                  
                                  "sieie4 := photon(3).full5x5_sigmaIetaIeta",
                                  "hoe4 := photon(3).hadronicOverEm",
                                  "sigmaEoE4 := photon(3).sigEOverE",
                                  "chisow4 := photon(3).pfChgIsoWrtWorstVtx04",
                                  "phoiso4 := photon(3).pfPhoIso03",
                                  "pfcluecal03_4 := photon(3).ecalPFClusterIso",
                                  "pfcluhcal03_4 := photon(3).hcalPFClusterIso",
                                  "trkiso03_4 := photon(3).trkSumPtHollowConeDR03",
                                  "pfchiso02_4 := photon(3).pfChgIso02WrtVtx0",
                                  "chiso4 := photon(3).pfChgIso03WrtVtx0",
                                  "isEB4 := photon(3).isEB",
                                  "csev4 := photon(3).passElectronVeto",
                                  "haspixelseed4 := photon(3).hasPixelSeed",
                                  "sieip4 := photon(3).sieip",
                                  "etawidth4 := photon(3).superCluster.etaWidth",
                                  "phiwidth4 := photon(3).superCluster.phiWidth",
                                  "regrerr4 := photon(3).sigEOverE * photon(3).energy",
                                  "s4ratio4 :=  photon(3).s4",
                                  "effSigma4 :=  photon(3).esEffSigmaRR",
                                  "scraw4 :=  photon(3).superCluster.rawEnergy",
                                  "ese4 :=  photon(3).superCluster.preshowerEnergy",                                  
                                  "idmva4 := photonIDMVA(3)",
                                  "genmatch4 := genMatch(3)",                                  
                                  # VTX 
                                  "vtx_x := vtx.x", 
                                  "vtx_y := vtx.y", 
                                  "vtx_z := vtx.z", 
                                  ],
                       histograms=[]                                   
                       )
process.quadPhotonDumper.nameTemplate ="opttree_$SQRTS_$LABEL_$SUBCAT"

process.p = cms.Path(process.flashggQuadPhotonProducer*process.quadPhotonDumper)

customize(process)

