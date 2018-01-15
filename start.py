 # -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 16:29:23 2016

Description: Outputting scenarios

Scope: MSc research Modelling circular economy policies in EEIOA


@author: Franco Donati
@institution: Leiden University CML, TU Delft TPM
"""
from save_ import Save
from results import Results

    
class Start:
    """
    From start you can launch all the analysis specifications listed under
    scenarios.xls
    
    All directories and base data are specified in dirs.py
    
    Results will be saved in the output folder
    
    The programme only considers two regions EU and Rest-Of-World (ROW)
    
    Permitted SUT transformation Methods are
    
    method = 0 >> Prod X Prod Ind-Tech Assumption Technical Coeff method
    method = 1 >> Prod X Prod Ind-Tech Assumption Market Share Coeff method
    
    results_only = True >> output only results (spec'd in scenarios.xls)
    results_only = False >> output all IOTs and results
    
    scen_no = 0-7 (0 = baseline)
        "scenario_1" is also allowed for scenarios
        None, 0, base and baseline are also accepted for baseline 
    
    """
    
    def __init__(self, method):        
        self.method = method # 0 or 1
        self.directory = "outputs/"
        self.init_res = Results(method)
        
    def run_one_scenario(self, scen_no, results_only = True):
        """
        Run to check specific scenario
        
        results_only = False, True
            - True, output results for analysis 
            - False, output all tables plus results for analysis
        """
        scenario = self.init_res.one_scen(scen_no, results_only)

        return(scenario)
        
    def all_results(self):
        """
        Output all results in a table
        """
        results_table = self.init_res.table_res()

        return(results_table)
    
    
    def save_one_scenario(self, scen_no, results_only = False):
        """
        Output all results in a table
        """
        init_save = Save(self.directory, self.method)
        scenario = self.init_res.one_scen(scen_no, results_only)
        init_save.save_(scenario, scen_no)
    
    
    def save_all_scenarios(self):
        """
        Save all results in separate files and sheets
        data e.g. all_results.all_tables
        """
        init_save = Save(self.directory, self.method)
        data = self.init_res.table_res(False)
        init_save.save_everything(data)
                

    def save_results(self):
        """
        Save results
        """
        init_save = Save(self.directory, self.method)
        data = self.init_res.table_res()
        init_save.save_results(data)
    
    def save_everything(self):
        """
        Save all scenarios and results
        """
        self.save_results()
        self.save_all_scenarios()
        
        
# uncomment to save results in method 0
#==============================================================================
# strt = Start(0)
# save_results = strt.save_results()
#==============================================================================

# uncomment to save results in method 1
#==============================================================================
# strt = Start(1)
# save_results = strt.save_results()
#==============================================================================
