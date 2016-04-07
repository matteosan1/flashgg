#ifndef FLASHgg_QuadriPhotonCandidate_h
#define FLASHgg_QuadriPhotonCandidate_h

#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "flashgg/DataFormats/interface/Photon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

namespace flashgg {
    class QuadPhotonCandidate : public reco::CompositeCandidate
    {
    public:
        QuadPhotonCandidate();
        QuadPhotonCandidate( const std::vector<flashgg::Photon>* photons, const reco::Vertex* vertex );
        ~QuadPhotonCandidate();
        
        const flashgg::Photon photon(unsigned int i) const { return (*photons_)[i]; }
        const reco::Vertex* vtx() const { return vertex_; }

        float photonIDMVA(unsigned int i) const;
        size_t size() const { return photons_->size(); }
        int genMatch(unsigned int i) const;

        struct CompareEt {
            bool operator()( flashgg::Photon t1, flashgg::Photon t2 ) const {
                return t1.et() > t2.et();
            }
        } etComparator;

    private:        
        std::vector<flashgg::Photon>* photons_;
        const reco::Vertex* vertex_;
    };
}
#endif
// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

