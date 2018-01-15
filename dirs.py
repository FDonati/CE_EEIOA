# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 13:03:52 2017

Description: Calling all variables contained within SUT pickled document

Scope: MSc research Modelling circular economy policies in EEIOA

@author: Franco Donati
@institution: Leiden University CML, TU Delft TPM
"""
import pickle as pk

SUT = pk.load(open("SUTs/mrSUT_EU_ROW.pkl", "rb"))
BP = pk.load(open("SUTs/BP.pkl", "rb"))

scen_file = "scenarios.xls"

where_r_results = ["S", "Y", "E", "Be", "Br", "Bm", "YBe", "YBr", "YBm"]

index = "resources/index.xls"


def specs():

    research = "Modelling circular economy policies in EEIOA"
    name = "Franco Donati"
    institution = "Leiden University CML & TU Delft TPM"
    course = "MSc Industrial Ecology"
    
    specs = {"research":research,
             "name":name,
             "institution": institution,
             "course":course
                }
    return(specs)

specs = specs()