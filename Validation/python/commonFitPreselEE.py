import FWCore.ParameterSet.Config as cms

all_pdfs = cms.PSet(
passingPresel_0p0To0p9_1p479To2p5 = cms.vstring(
"RooGaussian::signalResPass(mass, meanP[1.0,-5.000,5.000],sigmaP[0.5,0.001,5.000])",
"RooGaussian::signalResFail(mass, meanF[1.0,-5.000,5.000],sigmaF[0.5,0.001,5.000])",
"ZGeneratorLineShape::signalPhyPass(mass,\"templatePreselEE.root\", \"hMass_0.0To0.9_1.479To2.5_Pass\")",
"ZGeneratorLineShape::signalPhyFail(mass,\"templatePreselEE.root\", \"hMass_0.0To0.9_1.479To2.5_Fail\")",
"RooCMSShape::backgroundPass(mass, alphaPass[60.,50.,70.], betaPass[0.05, 0.001,0.1], gammaPass[0.1, 0, 1], peakPass[50.0, 10, 100])",
"RooCMSShape::backgroundFail(mass, alphaFail[80.,55.,90.], betaFail[0.05, 0.001,0.1], gammaFail[0.1, 0, 1], peakFail[50.0, 10, 100])",
"FCONV::signalPass(mass, signalPhyPass, signalResPass)",
"FCONV::signalFail(mass, signalPhyFail, signalResFail)",
"efficiency[0.5,0,1]",
"signalFractionInPassing[1.0]"
),

passingPresel_0p9To1p0_1p479To2p5 = cms.vstring(
"RooGaussian::signalResPass(mass, meanP[1.0,-5.000,5.000],sigmaP[0.5,0.001,5.000])",
"RooGaussian::signalResFail(mass, meanF[1.0,-5.000,5.000],sigmaF[0.5,0.001,5.000])",
"ZGeneratorLineShape::signalPhyPass(mass,\"templatePreselEE.root\", \"hMass_0.9To1.0_1.479To2.5_Pass\")",
"ZGeneratorLineShape::signalPhyFail(mass,\"templatePreselEE.root\", \"hMass_0.9To1.0_1.479To2.5_Fail\")",
"RooCMSShape::backgroundPass(mass, alphaPass[60.,50.,70.], betaPass[0.05, 0.001,0.1], gammaPass[0.1, 0, 1], peakPass[50.0, 10, 100])",
"RooCMSShape::backgroundFail(mass, alphaFail[80.,55.,90.], betaFail[0.05, 0.001,0.1], gammaFail[0.1, 0, 1], peakFail[50.0, 10, 100])",
"FCONV::signalPass(mass, signalPhyPass, signalResPass)",
"FCONV::signalFail(mass, signalPhyFail, signalResFail)",
"efficiency[0.5,0,1]",
"signalFractionInPassing[1.0]"
),

)
