# -*- coding: utf-8 -*-
"""
Created on sat Jan 28 2017

Description: Labelling elements for SUTs and IOTs

Scope: MSc research Modelling circular economy policies in EEIOA

@author:Franco Donati
@institution:Leiden University CML, TU Delft TPM
"""
from pandas import DataFrame as df
from pandas import MultiIndex as mi
import pandas as pd
from dirs import index as f
from pandas import read_excel as re

class Labels:
    
    def __init__(self):
        """
        country and region labels
        """
        co_in = re(f,"countries", 0)
        self.CI = co_in[["CountryName","CountryCode","CountryGroup"]]
        
        self.eu = (self.CI[self.CI["CountryGroup"]=="EU"])
        self.row = (self.CI[self.CI["CountryGroup"]!="EU"])
        self.EUcc = self.eu[["CountryGroup","CountryCode"]] #selected list of country codes for EU
        self.ROWcc = self.row[["CountryGroup","CountryCode"]] #selected list of country codes for ROW
            
        ind_ = re(f,"Industries")
        prod_ = re(f,"Products")
        Be_ = re(f,"Be")
        Y_ = re(f,"Y")
        E_ = re(f,"E")
        Bm_ = re(f,"Bm")
        Br_ = re(f,"Br")
        
        self.ind = ind_.loc[:,["Synonym","Code","Name"]]
        self.prod = prod_.loc[:,["Synonym","Code","Name"]]
        self.Be = Be_.loc[:,["Synonym","Code","Name", "Unit"]]
        self.Y = Y_.loc[:,["Synonym","Code","Name"]]
        self.E = E_.loc[:,["Synonym","Code","Name","Unit"]]
        self.Bm = Bm_.loc[:,["Code","Name","Unit"]]
        self.Br = Br_.loc[:,["Code","Name"]]
        

    
    def _2x(self):
        """
        make labels for double region system
        """      
        ind_ = self.ind
        prod_= self.prod
        Y_= self.Y
    
        # EU
        ind_["Region"] = pd.Series("EU" ,index = ind_.index)
        EUind = ind_[['Synonym','Region', 'Code', 'Name']]
        
        prod_["Region"] = pd.Series("EU" ,index = prod_.index)
        EUprod = prod_[['Synonym','Region', 'Code', 'Name']]
    
        Y_["Region"] = pd.Series("EU" ,index = Y_.index)
        EU_Y = Y_[['Synonym','Region', 'Code', 'Name']]
        
        # ROW
        
        ind_["Region"] = pd.Series("ROW" ,index = ind_.index) 
        ROWind = ind_[['Synonym','Region', 'Code', 'Name']]
        
        prod_["Region"] = pd.Series("ROW" ,index = prod_.index)
        ROWprod = prod_[['Synonym','Region', 'Code', 'Name']]
        
        Y_["Region"] = pd.Series("ROW" ,index = Y_.index)
        ROW_Y = Y_[['Synonym','Region', 'Code', 'Name']]
          
        # EU + ROW
        self.indER =  pd.concat([EUind, ROWind], axis = 0, ignore_index = True, copy=False)
        self.prodER =  pd.concat([EUprod, ROWprod], axis = 0, ignore_index = True, copy=False)
        self.YER =  pd.concat([EU_Y, ROW_Y], axis = 0, ignore_index = True, copy=False)
        
        
        return(self)
    
    
    # all the needed types of labelling automatation
    
    def _326x400(self, matrix):   
        matrix = df(matrix) 
        ind = self._2x().indER
        prod = self._2x().prodER
        
        try:
            matrix.columns = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"])
        except ValueError:    
            matrix.columns = mi.from_arrays(ind.values.T, names = ["abb","reg","code","name"])
            matrix.index = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"])
        else:
            matrix.index = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"])
            
        return (matrix)    
    
    def _400x400(self, matrix):   
        matrix = df(matrix)
        prod = self._2x().prodER
        matrix.columns = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"])
        matrix.index = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"])
        return(matrix)
    
    def _E(self, matrix): # primary input
        matrix = df(matrix)
        ind = self._2x().indER
        prod = self._2x().prodER
        E_ = self.E
        
        try:
            matrix.index = mi.from_arrays(ind.values.T, names = ["abb","reg","code","name"])
        except ValueError:
            try:
                matrix.index = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"])
            except ValueError:       
                matrix.index = mi.from_arrays(E_.values.T, names = ["abb","reg","code","name"]) 
        finally:
            try:
                matrix.columns = mi.from_arrays(ind.values.T, names = ["abb","reg","code","name"])
            except ValueError:
                try:
                    matrix.columns = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"])
                except ValueError:        
                    matrix.columns = mi.from_arrays(E_.values.T, names = ["abb","reg","code","name"]) 
        
        return(matrix)
        
    def _Y(self, matrix):
        matrix = df(matrix)
        YER = self._2x().YER
        prod = self._2x().prodER
        
        try:
            matrix.index = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"])
        except ValueError:
            matrix.index = mi.from_arrays(YER.values.T, names = ["abb","reg","code","name"]) 
            matrix.columns = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"]) 
        else:
            matrix.columns = mi.from_arrays(YER.values.T, names = ["abb","reg","code","name"]) 
        return(matrix)
    
    def _Pr(self, matrix):
        matrix = df(matrix)
        prod = self._2x().prodER
        
        try:
            matrix.index = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"])
        except ValueError:
            matrix.columns = mi.from_arrays(prod.values.T, names = ["abb","reg","code","name"])
        return(matrix)
    
    def _Pr_short(self, matrix):
        matrix = df(matrix)
        prod_ = self.prod
        
        try:
            matrix.index = mi.from_arrays(prod_.values.T, names = ["abb","code","name"])
        except ValueError:
            matrix.columns = mi.from_arrays(prod_.values.T, names = ["abb","code","name","reg"])
        return(matrix)
    
    def _Ind(self, matrix):
        matrix = df(matrix)
        ind = self._2x().indER
        
        try:
            matrix.index = mi.from_arrays(ind.values.T, names = ["abb","reg","code","name"])
        except ValueError:
            matrix.columns = mi.from_arrays(ind.values.T, names = ["abb","reg","code","name"]) 
        return(matrix)
    
    def _FD(self, matrix):
        matrix = df(matrix)
        Y = self._2x().YER
        
        try:
            matrix.index = mi.from_arrays(Y.values.T, names = ["abb","reg","code","name"])
        except ValueError:
            matrix.columns = mi.from_arrays(Y.values.T, names = ["abb","reg","code","name"]) 
        return(matrix)
        
    def _Rcol(self, matrix):
        matrix = df(matrix)
        prod_ = self._2x().prodER
        ind_ = self._2x().indER
        
        try:
            matrix.index = mi.from_arrays(prod_.values.T, names = ["abb","code","name", "reg"])
        except ValueError:
            matrix.columns = mi.from_arrays(prod_.values.T, names = ["abb","code","name", "reg"])
        except ValueError:
            try:
                matrix.index = mi.from_arrays(ind_.values.T, names = ["abb","code","name", "reg"])
            except ValueError:
                matrix.columns = mi.from_arrays(ind_.values.T, names = ["abb","code","name", "reg"])
        return(matrix)
    
    def _Bm(self, matrix):
        matrix = df(matrix)
        Bm = self.Bm
        try:
            matrix.index = mi.from_arrays(Bm.values.T, names = ["abb", "name", "unit"])
        except ValueError:
            matrix.columns = mi.from_arrays(Bm.values.T, names = ["abb", "name", "unit"]) 
        return(matrix)
    
    def _Be(self, matrix):
        matrix = df(matrix)
        
        Be = self.Be
        try:
            matrix.index = mi.from_arrays(Be.values.T, names = ["abb","code","name","unit"])
        except ValueError:
            matrix.columns = mi.from_arrays(Be.values.T, names = ["abb","code","name", "unit"]) 
        return(matrix)
        
    def _Br(self, matrix):
        matrix = df(matrix)
        Br = self.Br
        try:
            matrix.index = mi.from_arrays(Br.values.T, names = ["abb","name"])
        except ValueError:
            matrix.columns = mi.from_arrays(Br.values.T, names = ["abb","name"])
            
        return(matrix)


