import FWCore.ParameterSet.Config as cms

flashggQuadPhotonProducer = cms.EDProducer('FlashggQuadPhotonProducer',
                                           photonTag = cms.InputTag('flashggRandomizedPhotons'),
                                           vertexTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
                                           )

