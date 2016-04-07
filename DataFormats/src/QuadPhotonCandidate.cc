#include "flashgg/DataFormats/interface/QuadPhotonCandidate.h"

using namespace flashgg;

QuadPhotonCandidate::QuadPhotonCandidate() 
    : photons_(new std::vector<flashgg::Photon>),
      vertex_(0)
{}

QuadPhotonCandidate::~QuadPhotonCandidate() 
{}

QuadPhotonCandidate::QuadPhotonCandidate( const std::vector<flashgg::Photon>* photons, const reco::Vertex* vtx )
    : vertex_(vtx) {
    
    photons_ = const_cast<std::vector<flashgg::Photon>* >(photons);
    std::sort(photons_->begin(), photons_->end(), etComparator);
}

float QuadPhotonCandidate::photonIDMVA(unsigned int i) const {
    return (*photons_)[i].phoIdMvaWrtVtx0();
}

int QuadPhotonCandidate::genMatch(unsigned int i) const {
    return int ((*photons_)[i].hasGenMatchType() && 
                ((*photons_)[i].genMatchType() == 1));
}

// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

