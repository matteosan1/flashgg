#include "flashgg/Validation/plugins/FlashggSampleInfoTree.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <iostream>

tnp::FlashggSampleInfoTree::FlashggSampleInfoTree(const edm::ParameterSet& iConfig) {
  // make trees as requested
  edm::Service<TFileService> fs;
  addTree_ = fs->make<TTree>("sampleInfo", "sampleInfo");
  hnPU = fs->make<TH1F>("hnPU", "hnPU", 100, 0., 100.);

  totalGenWeight_ = 0.0;
  nEvents_ = 0;
  min_ = 0;
  max_ = 0;
  
  addTree_->Branch("sumWeight", &totalGenWeight_, "sumWeight/D");
  addTree_->Branch("nEvents", &nEvents_, "nEvents/D");
}

void tnp::FlashggSampleInfoTree::endLuminosityBlock(edm::LuminosityBlock const& iLumi, edm::EventSetup const& iSetup) {

  edm::Handle<edm::MergeableDouble> totWeight;
  iLumi.getByLabel(edm::InputTag("weightsCount","totalWeight"), totWeight);
  if (totWeight.isValid())
    totalGenWeight_ += (double)totWeight->value;

  edm::Handle<edm::MergeableCounter> nEventsH;
  iLumi.getByLabel(edm::InputTag("eventCount"), nEventsH);
  if (nEventsH.isValid())
    nEvents_ += (double)nEventsH->value;

  edm::Handle<edm::MergeableHisto<float> > nPUH;
  iLumi.getByLabel(edm::InputTag("weightsCount","obsPileup"), nPUH);
  if (nPUH.isValid()) {
    min_ = nPUH->min;
    max_ = nPUH->max;
    if (values_.size() == 0)
      values_.resize(nPUH->values.size(), 0);
    
    for (unsigned int i=0; i<values_.size(); i++)
      values_[i] += nPUH->values[i];
  }
}

void tnp::FlashggSampleInfoTree::endJob() {

  hnPU->SetBins(values_.size(), min_, max_);
  for (int i=0; i<hnPU->GetNbinsX(); i++)
    hnPU->SetBinContent(i, values_[i]);
  addTree_->Fill();
}

DEFINE_FWK_MODULE(tnp::FlashggSampleInfoTree);
