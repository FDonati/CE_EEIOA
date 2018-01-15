# Program for the calculation of Circular Economy policies in input-output analysis starting from multi-regional supply-use tables

[![DOI](https://zenodo.org/badge/70050557.svg)](https://zenodo.org/badge/latestdoi/70050557)

## start
Initiates the operations to set scenarios and to create IOT from SUT based on prodxprod Industry-Technology assumption both under Market Share Coefficient method and Technical Coefficient method.

From here it is possible to check results and save them in xls files

## scenarios
From this .xls file it is possible to set different types of interventions and the analysis to perform:
* direct policy interventions 
	* sharing
	* recycling
	* life extension
* market penetration of the direct policy interventions
* indirect effects of policy interventions:
    * rebound effects
    * substituion
* market expansion uncoupled from policy interventions and their indirect effects

These can be set for:
* product category (e.g. basic iron, pulp, raw milk, etc.)
* final demand category (e.g. households, government, etc.)
* primary input category (e.g. employment, etc.)
* emissions extensions
* material extensions
* resource extension

The tables in which it is possible to apply the interventions are:
* total requirement matrix (A)
* final demand (Y)
* primary inputs coefficients (RE)
* emission intermediate extentions coefficients (RBe)
* material intermediate extensions coefficients (RBm)
* resource intermediate extensions coefficients (RBr)
* emission final demand extension coefficients (RYBe)
* material final demand extension coefficients (RYBm)

Additionally it is possible to specify:
* region of the intervention
* whether the intervention affects domestic, import transactions or both

Furthemore, from the analysis sheet you can set the following variables to be compared in the analysis:
* product categories
* primary input categories
* emissions extensions
* material extensions
* resource extensions
* region of interest
    

## results
Class to assemble results for analysis as specified in scenario.xls analysis sheet
* Output product content in other products
* Output results for each scenario
* Output results and all IO tables and extensions 

## save_
Save class
* Save one scenario results
* Save one scenario results + IOTs
* Save all scenarios + IOTs
* Save all results

	

## apply_policy
Policy interventions class
* Recreate any matrix in IOT from policy interventions listed in the scenarios scenarios.xls

## base_n_scen
Calculate IOT for baseline and scenarios from SUTs

## SUTtoIO
Assemblying IOTs and Extensions from 
* Prod x prod industry technology assumption in market share coefficient method
* Prod x prod industry technology assumption in technical coefficient method

## SUTops 
Class for fundamental mathematical operations of IOA and SUT

## labels 
General labels for tables

## dirs
Directories and loading primary data sources

## Aggregate folder
Contains the following (N.B. module import to be fixed)

- parse_mrSUTs
  	- Parse all SUTs from EXIOBASE and outputs them as pickles to facilitate operations.
  	- It also adds regional label EU or ROW to faciliate slicing

- agg_MrSUTs
	- aggregates and separates them by EU-27 and ROW.
	- It reapplies multiindexes to be able to sort by region, code, name, abbreviation on all tables
	
- basic_price_wavg
	- weighted average of products basic prices across the world
