# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 11:02:52 2017

Description: Save data to xls

Scope: MSc research Modelling circular economy policies in EEIOA


@author: Franco Donati
@institution: Leiden University CML, TU Delft TPM
"""
import pandas as pd
from dirs import specs
from pandas import DataFrame as df
import datetime
now = datetime.datetime.now()
import os

class Save:
    
    def __init__(self, directory, method):
        
        self.directory = directory + str(now.month) + "_" + str(now.day) + "_" +str(now.hour) + "_" + str(now.minute) + "/"

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        self.method = method
        
        
    def gen_specs(self, scen_no):
        
        research = specs["research"]
        name = specs["name"]
        institution = specs["institution"]
        course = specs["course"]
        year, month, day = str(now.date()).split("-")
        
        index = ["Research", "Name", "Institution","Course", "Date [d-m-y]", "Scenario no", "Method"]
        general = df([research, name, institution, course, (day + "/" + month + "/" + year), scen_no, self.method], index = index, columns = ["General_info"])
        
        return(general)
    
    
    def save_(self, data, scen_no):
        
        if scen_no == "summary_results":
            file = self.directory + scen_no + ".xlsx" 
        
        elif scen_no in ["baseline", 0, "base"]:
            file = self.directory + "baseline.xlsx"

        elif scen_no not in ["baseline", 0, "base"]:

            scen_no = str(scen_no)
            file = self.directory + "scenario_" + scen_no[-1] + ".xlsx"       

        writer = pd.ExcelWriter(file, engine="xlsxwriter")

        specs = self.gen_specs(scen_no)
        specs.to_excel(writer, sheet_name = "general_specs")

        for l,value in data.items():
            value.to_excel(writer, l)      
        
        writer.save()
        
        
  
    def save_everything(self, data):
        """
        saves all scenarios + baseline + comparable file
        """
        for l,v in data.items():
            out = self.save_(v, l)
        
        return(out)
        
    
    def save_results(self, data):
        """
        Save one excel with all results
        """
        data = {"results":data}
    
        out = self.save_(data, "summary_results")

        return(out)


    
    
    