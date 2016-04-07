import FWCore.ParameterSet.Config as cms

from flashgg.Taggers.quadPhotonDumpConfig_cff import quadPhotonDumpConfig

quadPhotonDumper = cms.EDAnalyzer('CutBasedQuadPhotonDumper',
                                  **quadPhotonDumpConfig.parameters_()
                                  )
