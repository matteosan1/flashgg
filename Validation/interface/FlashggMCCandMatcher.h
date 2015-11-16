//
// Original Author:  Matteo Sani
//

#ifndef _FLASHGGMCCANDMATCHER_H_
#define _FLASHGGMCCANDMATCHER_H_

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Common/interface/RefProd.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include <DataFormats/Math/interface/deltaR.h>

#include <iostream> 

template<typename T>
class FlashggMCCandMatcher : public edm::EDProducer {
  
  typedef std::vector<T> TCollection;
  typedef edm::Ref<TCollection> TRef;
  typedef edm::RefVector<TCollection> TRefVector;
  typedef edm::Association<reco::GenParticleCollection> MCTruthMap;

public:
  explicit FlashggMCCandMatcher(const edm::ParameterSet&);
  ~FlashggMCCandMatcher();

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

  /// The RECO objects
  edm::EDGetTokenT<TRefVector> srcToken_;
  //edm::EDGetTokenT<reco::CandidateView> srcToken_;

  /// The MC objects to match against
  edm::EDGetTokenT<std::vector<reco::GenParticle> > matchedToken_;

  /// Preselection cut on MC objects
  StringCutObjectSelector<reco::GenParticle>  mcSel_;

  float dRMin_;
  int pdgId_;
  // FIXME add checkCharge...
};

template<typename T>
FlashggMCCandMatcher<T>::FlashggMCCandMatcher(const edm::ParameterSet &iConfig) :
  srcToken_(consumes<TRefVector>(iConfig.getParameter<edm::InputTag>("inputs"))),
  matchedToken_(consumes<std::vector<reco::GenParticle> >(iConfig.getParameter<edm::InputTag>("matched"))),
  mcSel_(iConfig.getParameter<std::string>("matchedSelector")),
  dRMin_(iConfig.getParameter<double>("dRmin")),
  pdgId_(iConfig.getParameter<int>("pdgId")) {

  produces<MCTruthMap> ();
}

template<typename T>
FlashggMCCandMatcher<T>::~FlashggMCCandMatcher()
{}


template<typename T>
void FlashggMCCandMatcher<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  typedef std::vector<reco::GenParticle> MCColl;
  edm::Handle<TRefVector> src;
  edm::Handle<MCColl> cands;
  iEvent.getByToken(srcToken_,     src);
  iEvent.getByToken(matchedToken_, cands);

  //std::vector<uint8_t> candGood(cands->size(),1);
  //std::transform(cands->begin(), cands->end(), candGood.begin(), mcSel_);
  std::vector<int>   matches(src->size(),-1);
    
  for (size_t i = 0; i < src->size(); ++i) {
    TRef ref = (*src)[i];
    //reco::CandidateBaseRef ref2 = ref->originalPhoton()->masterClone();
    
    std::cout << ref.id() << " " << ref.key() << std::endl;
    std::cout << ref->pt() << std::endl;
    //for (size_t gp=0; gp<candGood.size(); gp++) {
    for (size_t gp=0; gp<cands->size(); gp++) {
      //reco::GenParticle p = (*cands)[candGood[gp]];
      const reco::GenParticleRef p(cands, gp);

      std::cout << p->pdgId() << " " << p->pt() << " " << p->isPromptFinalState() << std::endl;
      if (p->status() == 1 and abs(p->pdgId()) == pdgId_) {// and p->isPromptFinalState()) {
	
	float dR = deltaR(p->p4(), ref->p4());
	if (dR < dRMin_) {
	  std::cout << dR << std::endl;
	  matches[i] = gp;
	  //break;
	}
      }
    }
  }
  
  //typedef edm::Association<std::vector<reco::GenParticle> > MCAsso;
  std::auto_ptr<MCTruthMap> matchesMap(new MCTruthMap(cands));
				       //new MCTruthMap(edm::RefProd<std::vector<reco::GenParticle> >(cands)));
  MCTruthMap::Filler matchesFiller(*matchesMap);
  matchesFiller.insert(src, matches.begin(), matches.end());
  matchesFiller.fill();
  iEvent.put(matchesMap);
}

#endif 
