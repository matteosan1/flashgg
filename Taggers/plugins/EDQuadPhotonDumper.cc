#include "FWCore/Framework/interface/MakerMacros.h"
#include "PhysicsTools/UtilAlgos/interface/EDAnalyzerWrapper.h"

#include "flashgg/Taggers/interface/QuadPhotonDumper.h"

typedef edm::AnalyzerWrapper<flashgg::CutBasedQuadPhotonDumper> CutBasedQuadPhotonDumper;

DEFINE_FWK_MODULE( CutBasedQuadPhotonDumper );

// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
