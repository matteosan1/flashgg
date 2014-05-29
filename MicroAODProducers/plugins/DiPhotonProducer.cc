#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "flashgg/MicroAODFormats/interface/DiPhotonCandidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

using namespace edm;
using namespace std;

namespace flashgg {

  class DiPhotonProducer : public EDProducer {
    
  public:
    DiPhotonProducer( const ParameterSet & );
  private:
    void produce( Event &, const EventSetup & ) override;
    EDGetTokenT<View<reco::Vertex> > vertexToken_;
    EDGetTokenT<View<flashgg::Photon> > photonToken_;
  };

  DiPhotonProducer::DiPhotonProducer(const ParameterSet & iConfig) :
    vertexToken_(consumes<View<reco::Vertex> >(iConfig.getUntrackedParameter<InputTag> ("VertexTag", InputTag("offlineSlimmedPrimaryVertices")))),
    photonToken_(consumes<View<flashgg::Photon> >(iConfig.getUntrackedParameter<InputTag> ("PhotonTag", InputTag("flashggPhotons"))))
  {
    produces<vector<flashgg::DiPhotonCandidate> >();
  }

  void DiPhotonProducer::produce( Event & evt, const EventSetup & ) {
    
    Handle<View<reco::Vertex> > primaryVertices;
    evt.getByToken(vertexToken_,primaryVertices);
    const PtrVector<reco::Vertex>& pvPointers = primaryVertices->ptrVector();
    
    Handle<View<flashgg::Photon> > photons;
    evt.getByToken(photonToken_,photons);
    const PtrVector<flashgg::Photon>& photonPointers = photons->ptrVector();
    
    auto_ptr<vector<DiPhotonCandidate> > diPhotonColl(new vector<DiPhotonCandidate>);
    
    for (unsigned int i = 0 ; i < photonPointers.size() ; i++) {
      Ptr<flashgg::Photon> pp1 = photonPointers[i];
      for (unsigned int j = i+1 ; j < photonPointers.size() ; j++) {
	Ptr<flashgg::Photon> pp2 = photonPointers[j];
	for (unsigned int k = 0 ; k < pvPointers.size() ; k++) {
	  Ptr<reco::Vertex> pvx = pvPointers[k];
	  diPhotonColl->push_back(DiPhotonCandidate(pp1,pp2,pvx));
	}
      }
    }
    
    evt.put(diPhotonColl);
  }
}

typedef flashgg::DiPhotonProducer FlashggDiPhotonProducer;
DEFINE_FWK_MODULE(FlashggDiPhotonProducer);