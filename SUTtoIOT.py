# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:29:47 2017

Description: Uses methods within SUTops to calculate IOT and Extensions

Scope: MSc research Modelling circular economy policies in EEIOA


@author: Franco Donati
@institution: Leiden University CML, TU Delft TPM
"""
from SUTops import SUTops as sops
import numpy as np

class Transform:
    
    def __init__(self, SUTs):
        
        # Baseline monetary data
        self.V = SUTs["V"] # Supply matrix 
        self.U = SUTs["U"] # Intermediate use        
        self.Y = SUTs["Y"] # Final demand
        self.Tm = SUTs["Tm"] # Trade margins
        self.E = SUTs["E"] # Primary input !!! always check that it's only E[0:9] if you want to do a balance !!!
        self.Be = SUTs["Be"] # Environmental extension 
        self.YBe = SUTs["YBe"] # Environmental extension final demand
        self.Br = SUTs["Br"] # Resources extension 
        self.YBr = SUTs["YBr"] # Resources extension final demand
        self.Bm = SUTs["Bm"] # Materials extension 
        self.YBm = SUTs["YBm"] # Materials extension final demand
        
        # baseline variables
        self.e = np.sum(self.E[:9], axis = 0)    
        self.yi = np.array(np.sum(self.Y, axis = 1)) # row sum of final demand
        self.yj = np.array(np.sum(self.Y, axis = 0)) # column sum of final demand
        self.q = np.sum(self.V, axis = 1) # total product output
        self.g = np.sum(self.V, axis = 0) # total industry output
        
        # bv diagonals
        self.diag_q = np.diag(self.q) # diagonal of q
        self.diag_g = np.diag(self.g) # diagonal of g
        self.diag_yi = np.diag(self.yi) # diagonal of yi         
        self.diag_yj = np.diag(self.yj) # diagonal of yj
        
        # bv inverses
        self.inv_diag_yi = sops.inv(self.diag_yi)
        self.inv_diag_yj = sops.inv(self.diag_yj)
        self.inv_diag_q = sops.inv(self.diag_q)
        self.inv_diag_g = sops.inv(self.diag_g)        
        
    def IOTpxpSTA_TCm(self):
        """ 
        IOT prod x prod Single tech Industry-technology as. 
        Technical coef method
        """
        
        T = sops.TC_STA.T(self.inv_diag_g, self.V.transpose()) # transformation matrix
        L = sops.TC_STA.L(self.U, T, self.inv_diag_q) # leontief inverse
        RE = sops.TC_STA.R(self.E, T, self.inv_diag_q) # primary inputs coefficients
        E = sops.TC_STA.B(RE, self.diag_q) # primary inputs
    
        RBe = sops.TC_STA.R(self.Be, T, self.inv_diag_q) # Be coefficient matrix
        Be = sops.TC_STA.B(RBe, self.diag_q) # environmental extensions
        
        RBr = sops.TC_STA.R(self.Br, T, self.inv_diag_q) # Br coefficient matrix
        Br = sops.TC_STA.B(RBr, self.diag_q) # resource extensions
    
        RBm = sops.TC_STA.R(self.Bm, T, self.inv_diag_q) # Bm coefficient matrix
        Bm = sops.TC_STA.B(RBm, self.diag_q) # Material extension
       
        S = sops.TC_STA.S(T, self.U) # intermediates
        q = sops.IOT.q_IAy(L, self.yi) # total product ouput
        
        A = sops.IOT.A(S,self.inv_diag_q)
        
        Y = self.Y        
        
        ver_base = sops.verifyIOT(S, Y, E)
        
        IOT = {"q":q,
               "T":T, 
               "Y": Y,
               "A":A,
               "RE":RE,
               "Be":Be,
               "RBe":RBe,
               "Br":Br,
               "RBr":RBr,
               "Bm":Bm,
               "RBm":RBm,
               "L":L,
               "E":E,
               "S":S,
               "ver":ver_base
               }
               
        return(IOT)
        
    def IOTpxpSTA_MSCm(self):
        """ 
        IOT prod x prod Single tech Industry-technology as. 
        Market share coef method
        """
        
        Z = sops.MSC_STA.Z(self.U, self.inv_diag_g) # industry intermediates coefficients
        D = sops.MSC_STA.D(self.V.transpose(), self.inv_diag_q) # Market shares
        A = sops.MSC_STA.A(Z, D) # technical coefficient matrix 
        L = sops.MSC_STA.L(A) # leontief inverse
        RE = sops.MSC_STA.R(self.E, D, self.inv_diag_g) # primary inputs    
        E = sops.MSC_STA.B(RE, self.diag_q)
    
        RBe = sops.MSC_STA.R(self.Be, D, self.inv_diag_g) # Be coefficient matrix
        Be = sops.MSC_STA.B(RBe, self.diag_q) # environmental extensions
        
        RBr = sops.MSC_STA.R(self.Br, D, self.inv_diag_g) # Br coefficient matrix
        Br = sops.MSC_STA.B(RBr, self.diag_q) # resource extensions
    
        RBm = sops.MSC_STA.R(self.Bm, D, self.inv_diag_g) # Bm coefficient matrix
        Bm = sops.MSC_STA.B(RBm, self.diag_q) # Material extension
    
        S = sops.MSC_STA.S(Z, D, self.diag_q) # intermediates
        q = sops.IOT.q_IAy(L, self.yi) # total product output
        
        A = sops.IOT.A(S,self.inv_diag_q)
        
        Y = self.Y  
        
        ver_base = sops.verifyIOT(S, Y, E)
        
        IOT = {"RE":RE,
               "A":A,
               "D":D,
               "Be":Be,
               "RBe":RBe,
               "Br":Br,
               "RBr":RBr,
               "Bm":Bm,
               "RBm":RBm,
               "L":L,
               "S":S,
               "E":E,
               "q":q,
               "ver":ver_base
               }
               
        return(IOT)
    
    
    @staticmethod
    def IOT(S, Y, E, Be, Br, Bm):
        """ 
        IOT
        """
        q = sops.IOT.q(S, Y) # total product output
        diag_q = np.diag(q)
        inv_diag_q = sops.inv(diag_q)
        
        y = np.sum(Y, axis = 1)
        
        A = sops.IOT.A(S, inv_diag_q) # technical coefficient matrix 
        L = sops.IOT.L(A) # leontief inverse
        
        RE = sops.IOT.R(E, inv_diag_q) # primary inputs coef
        E = sops.IOT.B(RE, diag_q)
        
        RBe = sops.IOT.R(Be, inv_diag_q) # Be coefficient matrix
        Be = sops.IOT.B(RBe, diag_q) # environmental extensions
        
        RBr = sops.IOT.R(Br, inv_diag_q) # Br coefficient matrix
        Br = sops.IOT.B(RBr, diag_q) # resource extensions
    
        RBm = sops.IOT.R(Bm, inv_diag_q) # Bm coefficient matrix
        Bm = sops.IOT.B(RBm, diag_q) # Material extension
    
        S = sops.IOT.S(A, diag_q) # intermediates
        q = sops.IOT.q_IAy(L, y)
    
        ver_base = sops.verifyIOT(S, Y, E)
    
        IOT = {"A":A,
               "S":S,
               "L":L,
               "S":S,
               "Y":Y,
               "RE":RE,
               "E":E,
               "q":q,
               "Be":Be,
               "RBe":RBe,
               "Br":Br,
               "RBr":RBr,
               "Bm":Bm,
               "RBm":RBm,
               "ver":ver_base
               }
               
        return(IOT)
               
    @staticmethod
    def FD_EXT(YB, diag_yj):
        """
        Calculates extensions for final demand
        """  
        inv_diag_yj = sops.inv(diag_yj)
        
        RYB = sops.fdext.RYB(inv_diag_yj, YB)
        YB = sops.fdext.YB(RYB, diag_yj)
        
        EXT = {
               "RYB":RYB,
               "YB":YB
                }
               
        return(EXT)


