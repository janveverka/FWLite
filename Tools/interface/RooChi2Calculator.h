#ifndef FWLITE_TOOLS_ROOCHI2CALCULATOR_H
#define FWLITE_TOOLS_ROOCHI2CALCULATOR_H

#include "TObject.h"
#include "RooHist.h"
#include "RooPlot.h"

/**
  * Calculates the chi2, residuals and pulls. Provides the same functionality
  * as chiSquare(..), pullHist(..) and residHist(..) of RooPlot with the
  * the difference that the number of expected entries per bin is obtained
  * from an integral over the bin rather than from the value at the bin
  * center.
  * 
  * TODO: Complete the transition of the class from JPsi/MuMu to FWLite/Tools
  * and put it back in the cit namespace.
  * 
  * Jan Veverka, Caltech,  1 November 2011
  * Last Modified: 9 March 2012
  */

// namespace cit {
  class RooChi2Calculator : public TObject {
    public:
      RooChi2Calculator() {};
      RooChi2Calculator(RooPlot const* plot);
      virtual ~RooChi2Calculator();

      RooHist* residHist(const char* histname = 0, const char* curvename = 0,
                         bool normalize = false) const;

      RooHist* pullHist(const char* histname = 0,
                        const char* pdfname = 0) const
        { return residHist(histname, pdfname, true); }

      Double_t chiSquare(int nFitParam = 0) const { 
	return chiSquare(0, 0, nFitParam); 
      }      

      Double_t chiSquare(const char* pdfname, const char* histname,
                         int nFitParam = 0) const;

    private:
      RooPlot const* plot_;
      double _nominalBinWidth;

      /// Make this a ROOT class.
      /// Use 1 as the 2nd arg to store class in a ROOT file.
      ClassDef(RooChi2Calculator,0)

  };  /// end of declaration of class RooChi2Calculator
//} /// end of namespace cit

#endif
