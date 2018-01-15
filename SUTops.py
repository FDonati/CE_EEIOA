# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 12:05:08 2016

Description: Class to perform SUT and IOT transforming and balancing calculations

Scope: MSc research Modelling circular economy policies in EEIOA


@author:Franco Donati
@institution:Leiden University CML, TU Delft TPM
"""
import numpy as np
from numpy import linalg as ln


class SUTops:
    
    def inv(x):
        """
        Returns inverse by dividing by 1 and eliminating inf and nan values
        """
        x = 1/x
        x[x == np.inf ] = 0
        x[x == np.nan ] = 0

        return(x)
    
    
    def var(self,V, U, Y, E):
        """
        Returns variables that are useful in all calculations
        """
        V = np.mat(V)
        U = np.mat(U)
        Y = np.mat(Y)
        E = np.mat(E)

        e = E[:9].sum(axis = 0).getA1() 
        yi = Y.sum(axis = 1).getA1()
        yj = Y.sum(axis = 0).getA1()
        q = V.sum(axis = 1).getA1()
        g = V.sum(axis = 0).getA1()
                   
        diag_yi = np.diag(yi)
        inv_diag_yi = self.inv(diag_yi)
        
        
        diag_yj = np.diag(yj)
        inv_diag_yj = self.inv(diag_yj)

        diag_q = np.diag(q)
        inv_diag_q = self.inv(diag_q)

        diag_g = np.diag(g)
        inv_diag_g = self.inv(diag_g)

        p = {"e":e,
             "yi":yi,
             "yj":yj,
             "q":q,
             "g":g,
             "diag_q":diag_q,
             "diag_g":diag_g,
             "diag_yi":diag_yi,
             "diag_yj":diag_yj,
             "inv_diag_q":inv_diag_q,
             "inv_diag_g":inv_diag_g,
             "inv_diag_yi":inv_diag_yi,
             "inv_diag_yj":inv_diag_yj
             }
		 
        return(p)
    
    

        
    class TC_STA:
        """
        Model with Transformation Coef. 
        ProdxProd Industry Technology assumption
        """

        def T(inv_diag_g, V):
            """ 
            Transformation matrix
            T = inv(diag(g)) * V
            """
            T = inv_diag_g @ V
            
            return (T)

        def L(U, T, inv_diag_q):
            """ 
            Input coefficients intermediates            
            A = U * T * inv[diag (q)] 
            
            Multiplier matrix            
            L =  (I-A)^-1 
            """                
            A = U @ T @ inv_diag_q # technical coefficient matrix         
            I = np.identity(len(A))         
            IA = I - A
            L = ln.inv(IA) 
            
            return(L)

        def R(B, T, inv_diag_q):
            """
            Value added and extension requirement matrix
            R = E * inv(diag(g)) 
            
            """            
            BT = B @ T 
            R = BT @ inv_diag_q  # Input coefficients 
            return (R)
				                      

        def B(R, diag_q):
            """ 
            Extensions and primary input for IO tables 
            """           
            B = R @ diag_q 
            
            return (B)
			   
        def S(T, U):
            """
            Intemediates
            S = U * T 
            """      
            S = U @ T 
            
            return(S)
		
    class MSC_STA:        

        """
        Model with Market Share Coef. 
        Prod x Prod Industry Technology assumption
        """

        def Z(U, inv_diag_g):
            """ 
            Input requirements 
            Z = U * inv(diag(g)) 
            """
            Z = U @ inv_diag_g            
            
            return(Z)


        def D(V, inv_diag_q):
            
            """ 
            Market share coefficients            
            D = V * inv(diag(q)) 
            """
            D = V @ inv_diag_q
            
            return(D)
        
        def A(Z, D):
            """            
            Total requirement multipliers
            A = Z * D
            """
            A = Z @ D
            return(A)

        def L(A):
            """
            Leontief inverse
            L = (I-A)^-1
            """
            I = np.identity(len(A)) 
            IA = I - A
            L= ln.inv(IA) 

            return(L)   

        def R(B, D, inv_diag_g):
            """
            Input coefficients ext_matrix            
            R = E * inv(diag(g)) 
            
            """            
            R_ = B @ inv_diag_g 
            R = R_ @ D
            return (R)
        
        def B(R, diag_q):
            """ 
            Extensions and primary input for IO tables 
            """           
            B = R @ diag_q 
            
            return (B)
            
        def S(Z, D, diag_q):
            """
            Intermediates
            S = Z * D * diag(q) 
            """

            S = Z @ D @ diag_q 
            
            return (S)
            
    class IOT:
        """
        General IOT operations subclass
        some methods repeat from other subclasses
        but it's good to have them divided for clarity
        """

        def q(S,Y):
            """
            total product output s the sum of Si and y
            """
            q =  np.sum(S, axis = 1) + np.sum(Y, axis = 1)
            
            return(q)

        def R(B, inv_diag_q):
            """
            Primary input and intermediates extensions coefficient matrix
            """
            R = B @ inv_diag_q

            return(R)
        
        def B(R, diag_q):
            """
            Primary input and intermediates extensions matrix
            """
            B = R @ diag_q

            return(B)

        def q_IAy(L, y):
            """
            Total product ouput        
            q = inv(I - A) * yi
            """
            q = np.dot(L, y)
            
            return (q)
        
        
        def S(A, diag_q):
            """
            Total product ouput        
            S = A * diag_q
            """
            S = A @ diag_q
            
            return (S)	
        
        def A(S, inv_diag_q):
            
            """ 
            Technical coefficient matrix          
            A = S * inv(diag(q)) 
            """            
            A = S @ inv_diag_q
            
            return(A)

        def L(A):
            """
            Leontief inverse
            L = (I-A)^-1
            """
            I = np.identity(len(A)) 
            IA = I - A
            L = ln.inv(IA)

            return(L)   
            
    class fdext:
        
        def RYB(inv_diag_yj, YB):
            """ 
            Method for transformation matrix of YB
            (e.g. final demand emissions)
            RB = YB * inv(diag(yj))
            """
            YRB = YB @ inv_diag_yj
            
            return (YRB)
    				                      
        def YB(YRB, diag_yj):
            """ 
            Extensions and primary input for IO tables 
            """
            YB = YRB @ diag_yj
        
            return (YB)

    class difference:
        """ 
        This class is used to calculate the difference between scenarios        
        """
        
        def delta_Y(Y, Yalt):
            """
            method to calculate difference in Y
            Y = final demand baseline
            Yalt = final demand scenario    				        
            """
            delta_Y = Y - Yalt
		
            return (delta_Y)

        def delta_q(L, Lalt, y):
            """
            method to calculate difference in q
            L = Leontief of baseline
            Lalt = Leontief of scenario    				        
            """
            delta_q = (L-Lalt) @ y
            
            return (delta_q)

    def verifyIOT(S, Y, E):
        
        q1 = np.sum(S, axis = 1) + np.sum(Y, axis = 1)
        q2 = np.sum(S, axis = 0) + np.sum(E[:9], axis = 0)
        
        ver = q1/q2 * 100
        ver = ver.fillna(0)
        
        return(ver)
        
            
            
