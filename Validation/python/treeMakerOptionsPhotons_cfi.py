import FWCore.ParameterSet.Config as cms

def setModules(process, options):

    process.sampleInfo = cms.EDProducer("tnp::FlashggSampleInfoTree",
                                        )

    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    process.hltFilter = hltHighLevel.clone()
    process.hltFilter.throw = cms.bool(True)
    process.hltFilter.HLTPaths = options['TnPPATHS']
    
    
   
    #### MC PU DISTRIBUTIONS
    from SimGeneral.MixingModule.mix_2015_25ns_Startup_PoissonOOTPU_cfi import mix as mix_2015_25ns
    from SimGeneral.MixingModule.mix_2015_50ns_Startup_PoissonOOTPU_cfi import mix as mix_2015_50ns
    pu_distribs = { "74X_mcRun2_asymptotic_v2" : mix_2015_25ns.input.nbPileupEvents.probValue }

    #### DATA PU DISTRIBUTIONS
    data_pu_distribs = { "Jamboree_golden_JSON" : [5.97e+04,4.03e+05,5.12e+05,5.48e+05,8.19e+05,1.31e+06,3.41e+06,1.55e+07,6.4e+07,1.45e+08,2.29e+08,2.92e+08,3.04e+08,2.56e+08,1.72e+08,9.35e+07,4.17e+07,1.64e+07,6.89e+06,3.77e+06,2.29e+06,1.19e+06,4.79e+05,1.47e+05,3.5e+04,7.26e+03,1.77e+03,646,293,135,59.7,25.2,10.1,3.86,1.4,0.486,0.16,0.0502,0.015,0.00425,0.00115,0.000296,7.24e-05,1.69e-05,3.74e-06,7.9e-07,1.59e-07,3.04e-08,5.52e-09,9.62e-10,1.57e-10,2.79e-11]}
    #5.12e+04,3.66e+05,5.04e+05,4.99e+05,7.5e+05,1.1e+06,2.53e+06,9.84e+06,4.4e+07,1.14e+08,1.94e+08,2.63e+08,2.96e+08,2.74e+08,2.06e+08,1.26e+08,6.38e+07,2.73e+07,1.1e+07,5.2e+06,3.12e+06,1.87e+06,9.35e+05,3.64e+05,1.1e+05,2.64e+04,5.76e+03,1.53e+03,594,278,131,59.8,26,10.8,4.29,1.62,0.587,0.203,0.0669,0.0211,0.00633,0.00182,0.000498,0.00013,3.26e-05,7.77e-06,1.77e-06,3.85e-07,7.99e-08,1.58e-08,3e-09,5.43e-10] }
    
    process.pileupReweightingProducer = cms.EDProducer("PileupWeightProducer",
                                                       #hardcodedWeights = cms.untracked.bool(True),
                                                       pileupInfoTag    = cms.InputTag("slimmedAddPileupInfo"),
                                                       PileupMC = cms.vdouble(pu_distribs["74X_mcRun2_asymptotic_v2"]),
                                                       PileupData = cms.vdouble(data_pu_distribs["Jamboree_golden_JSON"]),
                                                       )
         
    #process.GsfDRToNearestTauProbe = cms.EDProducer("DeltaRNearestGenPComputer",
    #                                                probes = cms.InputTag("photonFromDiPhotons"),
    #                                                objects = cms.InputTag('flashggPrunedGenParticles'),
    #                                                objectSelection = cms.string("abs(pdgId)==15"),
    #                                                )
    #
    #process.GsfDRToNearestTauSC = cms.EDProducer("DeltaRNearestGenPComputer",
    #                                             probes = cms.InputTag("superClusterCands"),
    #                                             objects = cms.InputTag('flashggPrunedGenParticles'),
    #                                             objectSelection = cms.string("abs(pdgId)==15"),
    #                                             )
    #
    #process.GsfDRToNearestTauTag = cms.EDProducer("DeltaRNearestGenPComputer",
    #                                              probes = cms.InputTag("photonFromDiPhotons"),
    #                                              objects = cms.InputTag('flashggPrunedGenParticles'),
    #                                              objectSelection = cms.string("abs(pdgId)==15"),
    #                                              )
    ###################################################################
    ## ELECTRON MODULES
    ###################################################################
    
    process.photonFromDiPhotons = cms.EDProducer("FlashggPhotonFromDiPhotonProducer",
                                                 src = cms.InputTag(options['DIPHOTON_COLL']),
                                                 cut = cms.string(options['PHOTON_CUTS']),
                                                 leadingPreselection = cms.string(options['LEADING_PRESELECTION']),
                                                 subleadingPreselection = cms.string(options['SUBLEADING_PRESELECTION']),
                                                 vertexSelection = cms.int32(-1), # -1 means take the chosen vertex, otherwise use the index to select 2it
                                                 diPhotonMVATag = cms.InputTag("flashggDiPhotonMVA"),
                                                 diphotonMVAThreshold = cms.double(-1.0)
                                                 )

    process.goodPhotonTagL1 = cms.EDProducer("FlashggPhotonL1CandProducer",
                                             inputs = cms.InputTag("goodPhotonTags"),
                                             isoObjects = cms.InputTag("goodPhotonTags"),
                                             nonIsoObjects = cms.InputTag(""),
                                             minET = cms.double(25),
                                             dRmatch = cms.double(0.2),
                                             isolatedOnly = cms.bool(False)
                                             )
    
    process.goodPhotonTags = cms.EDFilter("FlashggPhotonRefSelector",
                                          src = cms.InputTag("photonFromDiPhotons"),
                                          cut = cms.string(options['PHOTON_TAG_CUTS'])
                                          )
    
    process.goodPhotonProbes = cms.EDFilter("FlashggPhotonRefSelector",
                                            src = cms.InputTag("photonFromDiPhotons"),
                                            cut = cms.string(options['PHOTON_CUTS'])
                                            )
    
    ###################################################################
    
    process.goodPhotonProbesPreselection = cms.EDProducer("FlashggPhotonSelectorByValueMap",
                                                          input     = cms.InputTag("goodPhotonProbes"),
                                                          cut       = cms.string(options['PHOTON_CUTS']),
                                                          selection = cms.InputTag("photonFromDiPhotons:preselection"),
                                                          id_cut    = cms.bool(True)
                                                          )
    
    process.goodPhotonProbesIDMVA = cms.EDProducer("FlashggPhotonSelectorByDoubleValueMap",
                                                   input     = cms.InputTag("goodPhotonProbes"),
                                                   cut       = cms.string(options['PHOTON_CUTS']),
                                                   selection = cms.InputTag("photonFromDiPhotons:idmva"),
                                                   id_cut    = cms.double(-0.984)
                                                   )
    
    process.goodPhotonTagsIDMVA = cms.EDProducer("FlashggPhotonSelectorByDoubleValueMap",
                                                 input     = cms.InputTag("goodPhotonTags"),
                                                 cut       = cms.string(options['PHOTON_CUTS']),
                                                 selection = cms.InputTag("photonFromDiPhotons:idmva"),
                                                 id_cut    = cms.double(0.0)
                                                 )
    
    ###################################################################

    process.goodPhotonsTagHLT = cms.EDProducer("FlashggPhotonTriggerCandProducer",
                                               filterNames = options['TnPHLTTagFilters'],
                                               inputs      = cms.InputTag("goodPhotonTagsIDMVA"),
                                               bits        = cms.InputTag('TriggerResults::HLT'),
                                               objects     = cms.InputTag('selectedPatTrigger'),
                                               dR          = cms.double(0.3),
                                               isAND       = cms.bool(True)
                                               )
    
    process.goodPhotonsProbeHLT = cms.EDProducer("FlashggPhotonTriggerCandProducer",
                                                 filterNames = options['TnPHLTProbeFilters'],
                                                 inputs      = cms.InputTag("goodPhotonProbes"),
                                                 bits        = cms.InputTag('TriggerResults::HLT'),
                                                 objects     = cms.InputTag('selectedPatTrigger'),
                                                 dR          = cms.double(0.3),
                                                 isAND       = cms.bool(True)
                                                 )
    
    process.goodPhotonProbesL1 = cms.EDProducer("FlashggPhotonL1CandProducer",
                                                inputs = cms.InputTag("goodPhotonProbes"),
                                                isoObjects = cms.InputTag("l1extraParticles:Isolated"),
                                                nonIsoObjects = cms.InputTag("l1extraParticles:NonIsolated"),
                                                minET = cms.double(40),
                                                dRmatch = cms.double(0.2),
                                                isolatedOnly = cms.bool(False)
                                                )
    
    ###################################################################
    ## PHOTON ISOLATION
    ###################################################################
    process.load("RecoEgamma/PhotonIdentification/PhotonIDValueMapProducer_cfi")

    process.tagTightRECO = cms.EDProducer("CandViewShallowCloneCombiner",
                                      decay = cms.string("goodPhotonsTagHLT goodPhotonsProbeHLT"), 
                                      checkCharge = cms.bool(False),
                                      cut = cms.string("40<mass<1000"),
                                      )

    
    ###################################################################
    ## MC MATCHING
    ###################################################################
    
    #process.McMatchTag = cms.EDProducer("FlashggPhotonMCCandMatcher",
    #                                    pdgId = cms.int32(11),
    #                                    inputs = cms.InputTag("goodPhotonsTagHLT"),
    #                                    dRmin = cms.double(0.2),
    #                                    matched = cms.InputTag("flashggPrunedGenParticles"),
    #                                    matchedSelector = cms.string(""),
    #                                    checkCharge = cms.bool(False)
    #                                    )
    #
    #process.McMatchRECO = cms.EDProducer("FlashggPhotonMCCandMatcher",
    #                                     pdgId = cms.int32(11),
    #                                     inputs = cms.InputTag("goodPhotonsProbeHLT"),
    #                                     dRmin = cms.double(0.2),
    #                                     matched = cms.InputTag("flashggPrunedGenParticles"),
    #                                     matchedSelector = cms.string(""),
    #                                     checkCharge = cms.bool(False)
    #                                     )

#    process.McMatchTag = cms.EDProducer("MCTruthDeltaRMatcherNew",
#                                        matchPDGId = cms.vint32(11),
#                                        src = cms.InputTag("goodPhotonTags"),
#                                        distMin = cms.double(0.2),
#                                        matched = cms.InputTag("flashggPrunedGenParticles"),
#                                        checkCharge = cms.bool(False)
#                                        )
#    
#    process.McMatchRECO = cms.EDProducer("MCTruthDeltaRMatcherNew",
#                                         matchPDGId = cms.vint32(11),
#                                         src = cms.InputTag("goodPhotonProbes"),
#                                         distMin = cms.double(0.2),
#                                         matched = cms.InputTag("flashggPrunedGenParticles"),
#                                         checkCharge = cms.bool(False)
#                                         )
