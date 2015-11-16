#ifndef FlashggSampleInfoTree_h
#define FlashggSampleInfoTree_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "DataFormats/Common/interface/MergeableDouble.h"
#include "DataFormats/Common/interface/MergeableHisto.h"

#include <vector>

#include <TTree.h>
#include <TH1F.h>

namespace tnp {
  class FlashggSampleInfoTree : public edm::EDAnalyzer, boost::noncopyable {
  public:
    explicit FlashggSampleInfoTree(const edm::ParameterSet& config);
    ~FlashggSampleInfoTree() {};

  private:
    void analyze(const edm::Event&, const edm::EventSetup&) {};
    void endJob();
    virtual void endLuminosityBlock(edm::LuminosityBlock const& iLumi, edm::EventSetup const& iSetup) override;
        
    TTree * addTree_;
    double totalGenWeight_;
    double nEvents_; 
    float min_;
    float max_;
    std::vector<float> values_;
    TH1F* hnPU;    
  };
}

#endif
