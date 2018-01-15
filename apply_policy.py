# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 12:13:29 2016

Description: Reading policy values and modifying SUTs or IOT matrices for scenarios
             
Scope: MSc research Modelling circular economy policies in EEIOA

@author: Franco Donati

@institution: Leiden University CML, TU Delft TPM
"""

import pandas as pd
import numpy as np
from dirs import scen_file

class Apply_policy:

    def __init__(self):
        
        self.regions = ["EU","ROW"]
    

    def select_(self, sheet_name, M_name):
        """
        separates policy interventions by matrix subject to intervention
        M_name = name of the matrix that is going to be modified
        """
        scenario = pd.read_excel(scen_file, sheet_name, header = 1, 
                                 index = None)
        
        fltr_policies = scenario.loc[scenario['matrix'] == M_name]
    
        return(fltr_policies)
    
    class ops:

        @staticmethod
        def direct(a, kt, kp):
            """
            Direct effects of policy intervention 
            a = a supply chain or a point in it subject to policy
            kt =  technical coefficient (max achievable technically)
            kp = penetration coefficient (level of market penet. of the policy)
            """
            kt = kt * 1e-2
            kp = kp * 1e-2
            totk = 1 - kt * kp
            d = a * totk
            d = np.nan_to_num(d)
            return(d)

        @staticmethod    
        def indirect(d, c, fx_kp):
            """
            Indirect effects of policy interventions such as substitution or 
            rebound effect that can be directly connected to the transaction 
            that is subject to the direct policy intervention
            
            d = transaction to expand
            c = transaction subject to the direct policy intervention
            fx_kp = size of c that is added on the transaction to expand d
            """
            fx_kp = fx_kp * 1e-2
            ind = d + (c * fx_kp)        
            ind = np.nan_to_num(ind)
            return(ind)
        
        @staticmethod     
        def expansion(a, expan):
            """
            Market expansion or rebound effect uncoupled from economic value 
            of direct policy interventions
            a = transaction of reference
            fx_kp = coefficient of market expansion
            """
            expan = 1 + (expan * 1e-2)
            x = a * expan
            x = np.nan_to_num(x)
            return(x)
    
    
    
    def policy_engine(self, inter, M, xa, ya, xb = None, yb =None, 
                      kt = None, kp = None, expan = None, fx_kp = None, 
                      ignore_rest = False):
        
        
        
        # I am not trusting lexsorting to keep keys position with the type 
        # of multindexing I have set up. So I am flipping the index levels
        # Ideally we would just work with numpy.matrix or numpy.array and assign
        # integers to string type keys.
        # This is in hindsight. Now it is what it is. It should be fixed in the
        # future, not just for cleanness but to improve speed in case one wants 
        # to work with a multiregional system that is bigger than two regions
        # I can imagine having 48 regions in a large dataframe would make 
        # handling this type of modelling an unneccessary challenge

       
        try:
            if type(xa) == tuple:
                if xa[0] in self.regions:
                    
                    if M.index.names[1] == "reg":
                        M.index = M.index.swaplevel(0, 1)
                elif xa[0] not in self.regions:

                    if M.index.names[0] == "reg":
                        M.index = M.index.swaplevel(0, 1)

            elif type(xa) == str:
                if xa in self.regions:
                    if M.index.names[1] == "reg":
                        M.index = M.index.swaplevel(0, 1)
                
                elif xa not in self.regions:
                    if M.index.names[0] == "reg":
                        M.index = M.index.swaplevel(0, 1)
        except TypeError:
            pass
        
        try:
            if type(ya) == tuple:
                if ya[0] in self.regions:
                    if M.columns.names[1] == "reg":
                        M.columns = M.columns.swaplevel(0, 1)
                elif ya[0] not in self.regions:
                    if M.columns.names[0] == "reg":
                        M.columns = M.columns.swaplevel(0, 1)

            elif type(ya) == str:
                if ya in self.regions:
                    if M.columns.names[1] == "reg":
                        M.columns = M.columns.swaplevel(0, 1)
                
                elif ya not in self.regions:
                    if M.columns.names[0] == "reg":
                        M.columns = M.columns.swaplevel(0, 1)
        except TypeError:
            pass
            
        try:
            a = np.array(M.loc[xa,ya])
        except KeyError:
            try:
                a = np.array(M.loc[xa,[ya]])
                t = str(M.columns.names)
                i = str(M.index.names)
            except KeyError:
                what = " : " + "index level name in position 0 (" + i + "), the keys you want to pass in the index are (" + str(xa) + ") - the column level name in position 0 (" + t +"), the keys you are tying to pass (" +  str(ya) +")" 
                raise KeyError("I tried but there is something wrong with the index. This is what I have been trying to process " + what)
                return(M)

        if inter != "expansion":
            b = self.ops.direct(a, kt, kp)
            
            if inter == "indirect":
                c = a - b
                d = np.array(M.loc[xb,yb])
                M.loc[xb,yb] = self.ops.indirect(d, c, fx_kp)
            
            elif inter == "direct":
                M.loc[xa,ya] = b
            


        
        elif inter == "expansion":
            b = self.ops.expansion(a, expan)
            M.loc[xa, ya] = b

        
        if ignore_rest == True:
            
            if inter == "direct":
                verify_application = M.loc[xa,ya]
                
                comp = {"kt":kt, 
                        "kp":kp, 
                        "original_value":a, 
                        "result_value":b, 
                        "verify_application":verify_application}

            elif inter == "indirect":
                verify_application = M.loc[xb,yb]

                comp = {"kt":kt, 
                        "kp":kp, 
                        "original_value":a, 
                        "result_value":b, 
                        "verify_application":verify_application}

            elif inter == "expansion":
                verify_application = M.loc[xa,ya]
                
                comp = {"expan":expan, 
                        "original_value":a, 
                        "result_value":b, 
                        "verify_application":verify_application}
            
            M = {"comp":comp,
                 "M":M}

        return(M)


    
    
    def intersect_n_apply(self, inter, M, kt, kp, expan, fx_kp, catA, regA1, stageA, 
                     regA2, catB, regB1, stageB, regB2, ignore_rest = False):        
    
        """
        Function to calculate single transaction or entire row 
        by technical and pentration coefficients.

        The logarithm is designed to apply the coefficients for a 
        specific value or a row of values in the matrix of interest
        
        -----------------------------------------------------------------------
        
        inter = direct - indirect - expansion              
                  - direct = intended policy
                          - Change the values in the matrix according to
                            scenario specifications
                  - indirect = rebound effect or secondary effects
                          - take change in transaction value resulting from 
                            DIRECT policy intervention.
                          - add it to the supply chain subject to the INDIRECT
                            policy intervention.
                          - The amount translation is regulated by the 
                            effects penetration coefficient (fx_kp)                  
                  - expansion = market expansion or contraction
                          - Apply a normal market expansion or contraction 
                            according to specified coefficients
        
        
        ignore_rest =  False - True       
            * False, output only the value that has been modified and verifies 
              that the change was successful
            
            * True, output the entire matrix
        
        """

        
        # Let's do some checks to make sure the scenario is set up right
        intervention_types = ["direct","indirect","expansion"]        
        if inter not in intervention_types:            
            raise KeyError("Only the following interventions are allowed =>" + intervention_types)
        
        if pd.isnull(regA2) == False:

            if regA2 not in self.regions:
                raise KeyError("Only this regions are allowed =>" + self.regions)

            if pd.isnull(regA1) == False:
                if regA1 not in self.regions:
                    raise KeyError("Only this regions are allowed =>" + self.regions)
        
        elif pd.isnull(regA2) == True:

            if pd.isnull(regA1) == True:
                raise KeyError("It's not allowed to leave region unspecified, please add at least regA1 =>" + str(self.regions))
        
        
        if isinstance(M, pd.DataFrame): 
        # confusing right? I put this here because if you select ignore_rest
        # it returns a dictionary storing a dataframe and a dictionary
        # so it needs to be unpacked
            pass
        else:
            M = M["M"]
                 
        
        if pd.isnull(catA) == False:

            if pd.isnull(regA1) == False:
                xa = ((catA) , (regA1))
            
            elif pd.isnull(regA1) == True:
                xa = catA        
        
        elif pd.isnull(catA) == True:

            if pd.isnull(regA1) == False:
                xa = regA1

            elif pd.isnull(regA1) == True:
                xa = slice(None)
                
        if pd.isnull(stageA) == False:
            
            if pd.isnull(regA2) == False:
                ya = ((stageA), (regA2))

            elif pd.isnull(regA2) == True:
                ya = stageA
                

        elif pd.isnull(stageA) == True:

            if pd.isnull(regA2) == False:
                ya = regA2
                
            elif pd.isnull(regA2) == True:
                ya = slice(None)
                
                
                
        if inter == "indirect":
            
            if pd.isnull(catB) == False:
    
                if pd.isnull(regB1) == False:
                    xb = ((catB),(regB1))
                
                elif pd.insull(regB1) == True:
                    xb = catB
            
            elif pd.isnull(catB) == True:
    
                if pd.isnull(regB1) == False:
                    xb = regB1
                
                elif pd.isnull(regB1) == True:
                    xb = slice(None)
                    
            if pd.isnull(stageB) == False:
                
                if pd.isnull(regB2) == False:
                    yb = ((stageB),(regB2))
                    
                elif pd.isnull(regB2) == True:
                    yb = stageB
    
            elif pd.isnull(stageB) == True:
                if pd.isnull(regB2) == False:
                    yb = regB2
                
                elif pd.isnull(regB2) == True:
                    yb = slice(None)
            
        
        if inter == "direct":
            exc = self.policy_engine(inter, M, xa, ya, kt = kt, kp = kp, ignore_rest = ignore_rest)
        
        elif inter == "indirect":
            exc = self.policy_engine(inter, M, xa, ya, xb, yb, kt = kt, kp = kp, fx_kp = fx_kp, ignore_rest = ignore_rest)
        
        elif inter == "expansion":
            exc = self.policy_engine(inter, M, xa, ya, expan = expan, fx_kp = fx_kp, ignore_rest = ignore_rest)


        return (exc)
        
        
    
    def make_new(self, fltr_policies, M, M_name, ignore_rest = False):
        
        """
        Calculates and reassembles
        SUT or IOT matrices based on policy scenarios
        policy interventions
        
        scenario = is the table with the policy intervations
        
        M = matrix on which to implement the policies
        
        note: it would be so much better/elegant if we made these 
        interventions through a coefficient matrix => something for a later time   
        """
            
        if len(fltr_policies) == 0:
            return (M)
            
        else:
            for l, row in fltr_policies.iterrows():
                
                inter = row["intervention"]
                
#==============================================================================
#                 ide = row["identifier"] # used during debugging
#==============================================================================
                catA = row["catA"]
                stageA = row["stageA"]
                
                catB = row["catB"]
                stageB = row["stageB"]
                
                regA1 = row["reg_A1"]
                regA2 = row["reg_A2"]
                
                regB1 = row["reg_B1"]
                regB2 = row["reg_B2"]
                
                life = row["life"]
                l_kp = row["l_kp"]
            
                share = row["share"]
                s_kp = row["s_kp"]
                    
                recycle = row["recycle"]
                r_kp = row["r_kp"]
                
                expan = row["expansion"]
                fx_kp = row["fx_kp"]    
                
                if inter in ["direct","indirect"]:
                    # Life
                    if  pd.isnull(life) == False:
                        M = self.intersect_n_apply(M = M,
                                                   inter = inter,
                                                   regA1 = regA1,
                                                   regA2 = regA2,
                                                   regB1 = regB1,
                                                   regB2 = regB2,
                                                   kt = life, 
                                                   kp = l_kp,
                                                   catA = catA, 
                                                   stageA = stageA,
                                                   catB = catB, 
                                                   stageB = stageB,
                                                   fx_kp = fx_kp,
                                                   expan = expan,
                                                   ignore_rest = ignore_rest)
                    
                    # Sharing
                    if pd.isnull(share) == False:
                        M = self.intersect_n_apply(M = M,
                                                   inter = inter,
                                                   regA1 = regA1,
                                                   regA2 = regA2,
                                                   regB1 = regB1,
                                                   regB2 = regB2,
                                                   kt = share, 
                                                   kp = s_kp,
                                                   catA = catA, 
                                                   stageA = stageA,
                                                   catB = catB, 
                                                   stageB = stageB,
                                                   fx_kp = fx_kp,
                                                   expan = expan,
                                                   ignore_rest = ignore_rest)
            
                    # Recycling   
                    if pd.isnull(recycle) == False:
                                                       
                        M = self.intersect_n_apply(M = M,
                                                   inter = inter,
                                                   regA1 = regA1,
                                                   regA2 = regA2,
                                                   regB1 = regB1,
                                                   regB2 = regB2,
                                                   kt = recycle, 
                                                   kp = r_kp,
                                                   catA = catA, 
                                                   stageA = stageA,
                                                   catB = catB, 
                                                   stageB = stageB,
                                                   fx_kp = fx_kp,
                                                   expan = expan,
                                                   ignore_rest = ignore_rest)
        
                # Expansion 
                if inter == "expansion":
                    if pd.isnull(expan) == False:                                             
                        M = self.intersect_n_apply(M = M,
                                                   inter = inter,
                                                   regA1 = regA1,
                                                   regA2 = regA2,
                                                   regB1 = regB1,
                                                   regB2 = regB2,
                                                   kt = recycle, 
                                                   kp = r_kp,
                                                   catA = catA, 
                                                   stageA = stageA,
                                                   catB = catB, 
                                                   stageB = stageB,
                                                   fx_kp = fx_kp,
                                                   expan = expan,
                                                   ignore_rest = ignore_rest)
                        
        return(M)
        
        
    
    def apply_policy(self, scen_no, M, M_name, ignore_rest = False):
        """ 
        Apply policy interventions on specific matrix    
          
        scen_no = specific scenario e.g "1" or "scenario_1" 
        M = matrix affected by the policies     
        M_name = matrix name as diplayed under sheet_name["matrix"]
        
        """
        if type(scen_no) is int:
            scen_no = "scenario_" + str(scen_no)
            
        elif scen_no.startswith("scenario_"):
            pass
        else:
            raise KeyError("only integer or explicit name (scenario_x) is allowed")
        
        select = self.select_(scen_no, M_name)
        matrix = self.make_new(select, M, M_name, ignore_rest)
        
        return (matrix)