/***************************************************************************** 
 * Project: RooFit                                                           * 
 *                                                                           * 
 * This code was autogenerated by RooClassFactory                            * 
 * 
 * RooKeysPdf with rho as parameter.  
 *****************************************************************************/ 

// Your description goes here... 

#include "Riostream.h" 

#include "FWLite/Tools/interface/RooRhoKeysPdf.h" 
#include "RooAbsReal.h" 
#include "RooAbsCategory.h" 
#include <math.h> 
#include "TMath.h" 

ClassImp(RooRhoKeysPdf) 

 RooRhoKeysPdf::RooRhoKeysPdf(const char *name, const char *title, 
                        RooAbsReal& _x,
                        RooAbsReal& _rho) :
   RooAbsPdf(name,title), 
   x("x","x",this,_x),
   rho("rho","rho",this,_rho)
 { 
 } 


 RooRhoKeysPdf::RooRhoKeysPdf(const RooRhoKeysPdf& other, const char* name) :  
   RooAbsPdf(other,name), 
   x("x",this,other.x),
   rho("rho",this,other.rho)
 { 
 } 



 Double_t RooRhoKeysPdf::evaluate() const 
 { 
   // ENTER EXPRESSION IN TERMS OF VARIABLE ARGUMENTS HERE 
   return 42. ; 
 } 



