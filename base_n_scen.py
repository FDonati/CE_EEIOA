 # -*- coding: utf-8 -*-
"""
Created on Tue Feb 7 16:29:23 2017

Description: Calculate baseline and scenarios in IOT

Scope: MSc research Modelling circular economy policies in EEIOA


@author: Franco Donati
@institution: Leiden University CML, TU Delft TPM
"""

from apply_policy import Apply_policy
from dirs import SUT
import SUTtoIOT as si
from SUTops import SUTops as sops
from labels import Labels as lb
import numpy as np
import warnings as warn
lb = lb()

class Base_n_scen:
    
    def __init__(self, method = 0):
        
        self.SUTs = si.Transform(SUT)
        
        self.ap = Apply_policy()
        
        self.FD_EXT = si.Transform.FD_EXT
        
        if method == 0:
            self.IOT = self.SUTs.IOTpxpSTA_TCm()
        elif method == 1:
            self.IOT = self.SUTs.IOTpxpSTA_MSCm()
    
    
    def baseIOT(self):
        """
        method = 0 (Technical coefficient method)
                 1 (market share coefficient method)
                 
        baseline IOT calculated with Technical Coefficient method
        """

        
        E = self.IOT["E"]
        RE = self.IOT["RE"]
        L = self.IOT["L"]
        S = self.IOT["S"]
        q = self.IOT["q"]
        A = self.IOT["A"]
    
        RBe = self.IOT["RBe"]
        RBr = self.IOT["RBr"]
        RBm = self.IOT["RBm"]
    
        Be = self.IOT["Be"]
        Br = self.IOT["Br"]
        Bm = self.IOT["Bm"]
        ver_base = self.IOT["ver"]
        
        YBe = self.FD_EXT(self.SUTs.YBe, self.SUTs.diag_yj)
        YBr = self.FD_EXT(self.SUTs.YBr, self.SUTs.diag_yj)
        YBm = self.FD_EXT(self.SUTs.YBm, self.SUTs.diag_yj)
    
        L = lb._400x400(L)
        S = lb._400x400(S)
        A = lb._400x400(A)
        RE = lb._E(RE)
        
        E = lb._E(E)
    
        RBe = lb._Be(lb._Rcol(RBe)) #extension coefficients
        RYBe = lb._FD(lb._Be(YBe["RYB"])) # Final demand extension coefficients
        YBe = lb._FD(lb._Be(YBe["YB"]))
        Be = lb._Pr(lb._Be(Be))
        
        RBr = lb._Br(lb._Rcol(RBr))
        RYBr = lb._FD(lb._Br(YBr["RYB"]))
        YBr = lb._FD(lb._Br(YBr["YB"]))
        Br = lb._Pr(lb._Br(Br))
        
        RBm = lb._Bm(lb._Rcol(RBm))
        RYBm = lb._FD(lb._Bm(YBm["RYB"]))
        YBm = lb._FD(lb._Bm(YBm["YB"]))
        Bm = lb._Pr(lb._Bm(Bm))
        
        q = lb._Pr(q)
        
        ver_base = lb._Pr(ver_base)
            
        IOT = {"Y":self.SUTs.Y,
               "L":L,
               "A":A,
               "S":S,
               "q":q,
               "RE": RE,
               "E":E,
               "YBe":YBe,
               "YBr":YBr,
               "YBm":YBm,
               "RYBe":RYBe,
               "RYBr":RYBr,
               "RYBm":RYBm,
               "RBe":RBe,
               "RBr":RBr,
               "RBm":RBm,
               "Be":Be,
               "Br":Br,
               "Bm":Bm,
               "ver":ver_base
               }
        
        return(IOT)
          
    def sceneIOT(self, scen_no, base = None):
        """
        baseline IOT calculated with Technical Coefficient or Market coefficient method
        """        
        
        if scen_no in [0, "baseline", "base"]:
            warn.warn("You specified the baseline so no changes were made. Baseline was returned. Possible scenarios [1,2,...]")
            return(base)
        
        if base == None:
            base = self.baseIOT()
            
        #A_ = base["A"].copy(True)
        Y_ = base["Y"].copy(True)
        S_ = base["S"].copy(True)
        RE_ = base["RE"].copy(True)    
        #ver_base_ = base["ver"].copy(True)      
        RBe_ = base["RBe"].copy(True)
        RBr_ = base["RBr"].copy(True)
        RBm_ = base["RBm"].copy(True)
        Be_ = base["Be"].copy(True)
        Br_ = base["Br"].copy(True)
        Bm_ = base["Bm"].copy(True)        
        RYBe_ = base["RYBe"].copy(True)
        RYBr_ = base["RYBr"].copy(True)
        RYBm_ = base["RYBm"].copy(True)
        
        # Apply policy to economic matrices
        S_ = self.ap.apply_policy(scen_no, S_, "S")
    
        inv_diag_q_ = sops.inv(np.diag(sops.IOT.q(S_,Y_)))
        
        A_ = sops.IOT.A(S_, inv_diag_q_ )

        A_ = lb._400x400(A_)
        A_ = self.ap.apply_policy(scen_no, A_, "A")
        
        Y_ = self.ap.apply_policy(scen_no, Y_, "Y")

        RE_ = lb._E(RE_)    
        RE_ = self.ap.apply_policy(scen_no, RE_, "RE")
            
            
        # Apply policy to intermediate extension coefficient matrices
        RBe_ = self.ap.apply_policy(scen_no, RBe_, "RBe")
        RBr_ = self.ap.apply_policy(scen_no, RBr_, "RBr")
        RBm_ = self.ap.apply_policy(scen_no, RBm_, "RBm")
       
        # Apply policy to  final demand extension coefficient matrices
        RYBe_ = self.ap.apply_policy(scen_no, RYBe_, "RYBe")
        RYBr_ = self.ap.apply_policy(scen_no, RYBr_,"RYBr")
        RYBm_ = self.ap.apply_policy(scen_no, RYBm_, "RYBm")  
        
        # Scenario
      
        L_ = sops.IOT.L(A_) # total product output according to full scenario with S and Y modified
        
        yi_ = np.sum(Y_, axis = 1)
        diag_yj_ = np.diag(Y_.sum(axis = 0))
        q_ = sops.IOT.q_IAy(L_, yi_)
        diag_q_ = np.diag(q_)
        S_ = sops.IOT.S(A_, diag_q_)        
   
        E_ = sops.IOT.B(RE_, diag_q_) # primary inputs
        
        Be_ = sops.IOT.B(RBe_, diag_q_) # environmental ext
        Br_ = sops.IOT.B(RBr_, diag_q_) # resource ext
        Bm_ = sops.IOT.B(RBm_, diag_q_) # material ext
        
        YBe_ = sops.fdext.YB(RYBe_, diag_yj_) # environmental ext
        YBr_ = sops.fdext.YB(RYBr_, diag_yj_) # resource ext
        YBm_ = sops.fdext.YB(RYBm_, diag_yj_) # material ext
        
        # labelling
    
        S = lb._400x400(S_)
        E = lb._E(E_)
        Y = lb._Y(Y_)
        
        Be = lb._Pr(lb._Be(Be_))
        Bm = lb._Pr(lb._Bm(Bm_))   
        Br = lb._Pr(lb._Br(Br_))
        
        YBm = lb._FD(lb._Bm(YBm_))
        YBr = lb._FD(lb._Br(YBr_))
        YBe = lb._FD(lb._Be(YBe_))
        
        ver = sops.verifyIOT(S_, Y_, E_) # ver_new_IOT
        ver = lb._Pr(ver)
        
#==============================================================================
#         # Uncomment to check both base and scenario balance
#         # Beware that some functionalities may not work if you untoggle it
#         ver = {"ver1":ver_base_,
#                "ver2":ver
#                 }
#==============================================================================
        
        IOT = {"Y":Y,
               "S":S,
               "E":E,
               "Be":Be,
               "Br":Br,
               "Bm":Bm,
               "YBe":YBe,
               "YBr":YBr,
               "YBm":YBm,
               "ver":ver
               }
                   
        return(IOT)    