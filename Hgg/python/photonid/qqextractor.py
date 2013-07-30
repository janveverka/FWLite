'''
Implements the QQExtractor class.
Jan Veverka, MIT, jan.veverka@cern.ch
29 July 2019
'''
import os
import sys
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases
import FWLite.Tools.dataset as datasetly
import FWLite.Hgg.trees as trees

from FWLite.Hgg.photonid.variables import config_map
from FWLite.Hgg.photonid.corrector import PhotonIdCorrector

#______________________________________________________________________________
class DataSource:
    '''
    Holds data related to a given data source.
    '''
    #__________________________________________________________________________
    def __init__(self, name, varname, option, max_entries):
        self.name = name
        self.varname = varname
        #self.max_entries = max_entries
        #self.option = self.option
        tree = trees.get(name, option)
        cfg = config_map[varname]
        datasets = []
        ## Get a dataset for each expression-selection pair
        for expr, cuts in zip(cfg.expressions, cfg.selections):
            if hasattr(cfg, 'binning') and len(cfg.binning.split(',')) == 3:
                nbins, varmin, varmax = map(float, cfg.binning.split(','))
                variable = ROOT.RooRealVar(cfg.name, expr, varmin, varmax)
                variable.setBins(int(nbins))
            else:
                variable = ROOT.RooRealVar(cfg.name, expr)
            cuts = [cuts]
            if max_entries > 0:
                cuts.append('Entry$ < %d' % max_entries)
            dataset = datasetly.get(tree=tree, variable=variable, cuts=cuts)
            variable = dataset.get().first()
            variable.SetTitle(cfg.title)
            variable.setUnit(cfg.unit)
            datasets.append(dataset)
        ## End of loop over expressions and selections
        dataset = datasets[0]
        for further_dataset in datasets[1:]:
            dataset.append(further_dataset)
        dataset.SetTitle('Raw ' + name.split('-')[0].capitalize())
        dataset.SetName('raw_' + name.split('-')[0])
        self.data = dataset
        self.xvar = dataset.get().first()
    ## End of DataSource.__init__(..)
## End of class DataSource
  

#______________________________________________________________________________
class QQExtractor:
    '''
    Extracts the Q-Q corrections for photon ID variables.
    '''
    #__________________________________________________________________________
    def __init__(self, varname, raw_name, target_name, option='noskim',
                 max_entries=-1, rho=0.7):
        self.raw    = DataSource(raw_name   , varname, option, max_entries)
        self.target = DataSource(target_name, varname, option, max_entries)
        self.corrector = PhotonIdCorrector(self.raw.data, self.target.data, 
                                           rho)
        self.postprocess_corrector()
    ## End of QQExtractor.__init__(..)
    
    #__________________________________________________________________________
    def postprocess_corrector(self):
        '''
        Customizes corrector name and title and updetes raw and target sources
        with corrector pdfs.
        '''
        name = '_'.join([self.raw.xvar.GetName(),
                         self.raw.name.split('-')[0], 'to',
                         self.target.name.split('-')[0], 'qqcorrector'])
        title = ' '.join([self.raw.xvar.GetTitle(),
                          self.raw   .name.split('-')[0].capitalize(), 'to',
                          self.target.name.split('-')[0].capitalize(),
                          'Q-Q Corrector'])                 
        self.corrector.SetName(name)
        self.corrector.SetTitle(title)
        self.raw   .pdf = self.corrector.xpdf
        self.target.pdf = self.corrector.ypdf
    ## End of QQExtractor.postprocess_corrector()
    
    #__________________________________________________________________________
    def make_plots(self):
        '''
        Makes plots of the raw and target source, the corrector function,
        and the corrected data.
        '''
        for src in [self.raw, self.target]:
            canvases.next(src.varname + '_' + src.data.GetName()).SetGrid()
            self.draw_and_append(self.get_plot_of_source(src))
        
        canvases.next(self.corrector.GetName()).SetGrid()
        self.draw_and_append(self.corrector.get_correction_plot())
        
        canvases.next(self.corrector.GetName() + '_validation').SetGrid()
        self.draw_and_append(self.corrector.get_validation_plot())
    ## End of QQExtractor.make_plots(..)
    
    #__________________________________________________________________________
    def get_plot_of_source(self, source):
        plot = source.xvar.frame(roo.Title(source.data.GetTitle()))
        source.data.plotOn(plot)
        source.pdf.plotOn(plot)        
        return plot
    ## End of QQExtractor.get_plot_of_source()
    
    #__________________________________________________________________________
    def draw_and_append(self, plot):
        if not hasattr(self, 'plots'):
            self.plots = []
        plot.Draw()
        self.plots.append(plot)
    ## End of QQExtractor.draw_and_append(plot)
    
## End of class QQExtractor


#______________________________________________________________________________
def main(varnames = 'r9b sieieb setab'.split(),
         raw_name = 's12-zllm50-v7n',
         target_name = 'r12a-pho-j22-v1',
         option = 'skim10k',
         max_entries = 1000):
    '''
    Main entry point of execution.
    '''
    global extractors
    extractors = []
    name = '_'.join([raw_name.split('-')[0], 'to',
                     target_name.split('-')[0], 'qqcorrector'])
    out_file_name = '_'.join([raw_name.split('-')[0], 'to',
                              target_name.split('-')[0], 'qqcorrections.root'])
    if os.path.isfile(out_file_name):
        os.remove(out_file_name)
    for varname in varnames:
        print 'QQ QQ QQ Processing', varname, '...'
        extractor = QQExtractor(varname, raw_name, target_name, option)
        extractor.make_plots()
        canvases.update()
        corr = extractor.corrector
        corr.SetName(corr.GetName().replace(name, 'qq'))
        corr.write_to_file(out_file_name, False)
        graph = corr.get_interpolation_graph()
        out_file = ROOT.TFile.Open(out_file_name, "update")
        graph.Write()
        out_file.Write()
        extractors.append(extractor)
        out_file.Close()
## End of main()


#______________________________________________________________________________
def save_and_cleanup(outdir = 'plots'):    
    if not os.path.exists(outdir):
        print "Creating folder `%s'" % outdir
        os.mkdir(outdir)
    canvases.make_pdf_from_eps(outdir)
    trees.close_files()
## End of save_and_cleanup()


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
    ## Clean up to prevent horrible root crashes.
    if ROOT.gROOT.IsBatch():
        save_and_cleanup()
    