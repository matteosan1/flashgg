#ifndef flashgg_QuadPhotonDumper_h
#define flashgg_QuadPhotonDumper_h

#include "flashgg/DataFormats/interface/QuadPhotonCandidate.h"
#include "flashgg/Taggers/interface/CollectionDumper.h"

namespace flashgg {
    typedef CollectionDumper<std::vector<QuadPhotonCandidate>, QuadPhotonCandidate,
                             CutBasedClassifier<QuadPhotonCandidate> > CutBasedQuadPhotonDumper;
}

#endif

// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
