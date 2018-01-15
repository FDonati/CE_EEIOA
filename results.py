# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 09:26:43 2017

Description: module to perform results analysis

Scope: MSc research Modelling circular economy policies in EEIOA


@author: Franco Donati
@institution: Leiden University CML, TU Delft TPM
"""
import pandas as pd
import numpy as np
from labels import Labels as lb
from pandas import DataFrame as df
from dirs import scen_file
from dirs import BP
from dirs import SUT
from dirs import where_r_results as wrr
from SUTops import SUTops as sops
from base_n_scen import Base_n_scen as bns
import warnings as warn 
lb = lb()

class GatherResults:
    """ 
    Group results for a specific scenario or all scenarios + baseline
    """       
    
    def __init__(self, method):
        
        scenarios = pd.ExcelFile(scen_file)
        self.method = method
        sheet_names = scenarios.sheet_names    
        self.sheets = [f for f in sheet_names if f.startswith("scenario_")]
        self.bns = bns(method)
        self.base = self.bns.baseIOT()
        self.analyse = pd.read_excel(scen_file, "analyse", header = 0, index = None)


    def select_(self, ext, reg, prod, M):
        """
        Select extension by region and prod according to specifications
        """
        if pd.isnull(ext) is False:
            x = (ext)
            if pd.isnull(prod) is True:
                if pd.isnull(reg) is True:
                    y = slice(None)
                elif pd.isnull(reg) is False:
                    M.columns = M.columns.swaplevel(0, 1)
                    y = reg
            
            elif pd.isnull(prod) is False:
                if pd.isnull(reg) is False:
                    y = (prod, reg)
                elif pd.isnull(reg) is True:
                    y = (prod)
        
        elif pd.isnull(ext) is True:
            x = slice(None)
            if pd.isnull(prod) is False:
                
                if pd.isnull(reg) is False:
                    y = (prod, reg)
                if pd.isnull(reg) is True:
                    y = prod
            elif pd.isnull(prod) is True:
                if pd.isnull(reg) is False:
                    M.columns = M.columns.swaplevel(0, 1)
                    y = reg
        
        try:
            a = M.loc[x, y]
        except KeyError:
            a = M.loc[x, [y]]

        if y == reg:
             M.columns = M.columns.swaplevel(0, 1)
             a = df(a.sum(axis = 1))
        
        if x == reg:
             M.index = M.index.swaplevel(0, 1)
             a = df(a.sum(axis = 0))
        return(a)
        
    def sep_bas_scen(self, data, fltrd_anls, scen_no):
        """
        Separate collect and rename results for baseline and scenarios according
        to specifications on scenarios.xls
        """    
        D = {}
        if len(fltrd_anls) > 0:

            for l, row in fltrd_anls.iterrows():
 
                M_name = row["matrix"]
                ext = row["ext"]
                stageA = row["stageA"]
                stageB = row["stageB"]
                regA = row["regA"]
                regB = row["regB"]
                
                if pd.isnull(stageA) is False:
                    if pd.isnull(stageB) is True:
                        warn.warn("stageB assummed as stageA - Can't compare a stage against an entire supply chain - ref: "+ scen_no + ", " + M_name + ", " + ext)
                        stageB = stageA
                
                if pd.isnull(regA) is False:
                    if pd.isnull(regB) is True:
                        warn.warn("regB assummed as regA - Can't compare a reg against the whole world - ref: "+ scen_no + ", " + M_name + ", " + ext)
                        regB = regA

                M = data[M_name]
                
                if scen_no == "baseline":
                    select = self.select_(ext, regA, stageA, M)
                    key = [M_name, ext, regA, str(stageA)]
                    
                else:
                    select = self.select_(ext, regB, stageB, M)
                    key = [M_name, ext, regB, str(stageB)]
                
                key =  ", ".join(key)
                
                D[key] = select
                
        return(D)
        
        
    def iter_thru_for_results(self, data, scen_no):
        """
        filter policy interventions from scenario file according to specified 
        matrix and return the respective matrix with it
        Output only specified (see scenario.xls) results to be analysed
        """
        res = {}
        for l in wrr:
            fltr = self.analyse.loc[self.analyse['matrix'] == l]
            m = []                
            if len(fltr) > 0:
                matrix = fltr.loc[:,"matrix"]
                for l,mat in matrix.items():
                    if mat not in m:
                        m.append(mat)    
                for l in m:
                    res_ = self.sep_bas_scen(data, fltr, scen_no)
                    for ll,vv in res_.items(): 
                        for lll, vvv in vv.items():
                            for llll,value in vvv.items():
                                name = str(ll) + ", " + str(lll) 
                                res[name] = value
                        
        columns = res.keys()
        
        results = df(res, index = [scen_no], columns = columns).transpose()
        return(results)
                
                
                        
        
class Results:
    
    def __init__(self, method = 0):
        self.method = method
        self.gr = GatherResults(self.method)

    def one_scen(self, scen_no = None, results_only = True):
        """
        save results for baseline or specific scenario
        """
        if scen_no in [0,"baseline", "base", None]:
            sc = self.gr.base
        else:
            sc = self.gr.bns.sceneIOT(scen_no)
        
        results = self.gr.iter_thru_for_results(sc, scen_no)
        
        if results_only == True:
            sc = results
            if scen_no not in [0,"baseline", "base"]:
                sc.columns = ["sc_" + str(scen_no)]
        
        elif results_only == False:
            sc["results"] = results
            

                
        return(sc)
        
    
    def table_res(self, results_only = True):
        """
        Take a dictionary of all scenarios' results
        and organise them in table
        """        

        
        if results_only == False:
            C = {}
        
        n = 1   
        while n <= len(self.gr.sheets):
            print(n)
            if n == 1:
                t = self.one_scen(n, results_only)
                if results_only == False:
                    name = "sc_" + str(n)
                    C[name] = t
 
            elif n > 1:
                t2 = self.one_scen(n, results_only)
                
                if results_only == True:
                    t = pd.concat([t,t2], axis = 1 )

                elif results_only == False:
                    name = "sc_" + str(n)
                    C[name] = t2
            n +=1
            
        baseline =  self.one_scen("baseline", results_only)
        if results_only == False:
            C["baseline"] = baseline
        else:
            C = pd.concat([baseline,t], axis = 1).transpose()
                    
        return(C)     


        
