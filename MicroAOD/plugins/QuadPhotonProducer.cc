#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/Handle.h"

#include "flashgg/DataFormats/interface/QuadPhotonCandidate.h"

#include <vector>

using namespace edm;
using namespace std;

namespace flashgg {

    class QuadPhotonProducer : public EDProducer {
    public:
        QuadPhotonProducer( const ParameterSet & );
        
    private:
        void produce( Event &, const EventSetup & ) override;
        EDGetTokenT<std::vector<flashgg::Photon> > photonToken_;
        EDGetTokenT<std::vector<reco::Vertex> > vertexToken_;
    };
    
    QuadPhotonProducer::QuadPhotonProducer( const ParameterSet &iConfig ) :
        photonToken_( consumes<std::vector<flashgg::Photon> >( iConfig.getParameter<InputTag> ( "photonTag" ) ) ),
        vertexToken_( consumes<std::vector<reco::Vertex> >( iConfig.getParameter<InputTag> ( "vertexTag" ) ) )
    {
        produces<std::vector<flashgg::QuadPhotonCandidate> >();
    }

    void QuadPhotonProducer::produce( Event &evt, const EventSetup & )
    {
        auto_ptr<std::vector<flashgg::QuadPhotonCandidate> > quadColl( new std::vector<flashgg::QuadPhotonCandidate> );
        
        Handle<std::vector<flashgg::Photon> > photons;
        evt.getByToken( photonToken_, photons );
  
        Handle<std::vector<reco::Vertex> > vertices;
        evt.getByToken( vertexToken_, vertices );
                 
        if (photons->size() > 0 and vertices->size() > 0) {
            QuadPhotonCandidate quadPhoton( photons.product(), &((*(vertices.product()))[0]));
            quadColl->push_back(quadPhoton);
        }
        
        evt.put( quadColl );                               
    }
}

typedef flashgg::QuadPhotonProducer FlashggQuadPhotonProducer;
DEFINE_FWK_MODULE( FlashggQuadPhotonProducer );

// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
