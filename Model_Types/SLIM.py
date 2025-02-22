#/usr/bin/env python3
####################################################################################
#   Copyright (c) 2025
#
#   Team: System of a Down
#
#   Authors: Freddie Fraticelli, John Midkiff, Zack Popilek,
#            Ashley Porter, and Gerardo Rivas-Leal
#   
#   
#   This project is open source and can be utilized and referenced
#   as long as the team and all authors are credited.
#
#
#
####################################################################################

from numpy import log

class Gafney:
    def __init__(self):
        self.p = 0.6288
        self.q = 0.5555

class Putnam:
    def __init__(self):
        self.p = (1/3)
        self.q = (4/3)

class SLIM:
    def __init__(self, use_Gaf = True):
        # Source Lines of Code 
        self.S = 0

        #Technology Constant
        self.C = 0

        #Lifecycle effort in years
        self.K = 0

        #Development Time in years
        self.t_d = 0

        if use_Gaf:
            self.func = Gafney()
        else:
            self.func = Putnam()

    def solve_for_constant(self):
        # C = S / (K^p * t_d^q)
        k_p = self.K ** self.func.p
        t_d_q = self.t_d ** self.func.q
        return self.S / (k_p * t_d_q)
    
    def solve_for_S(self):
        # S = C * K^p * t_d^q
        k_p = self.K ** self.func.p
        t_d_q = self.t_d ** self.func.q
        return self.C * k_p * t_d_q
    
    def solve_for_K(self):
        # K = (S / (C * t_d^q)) ** (1/p)
        t_d_q = self.t_d ** self.func.q
        inverse_p  = 1/self.func.p
        return (self.S / (self.C * t_d_q)) ** inverse_p
    
    def solve_for_t_d(self):
        # t_d = (S / (C * K^p)) ** (1/q)
        k_p = self.K ** self.func.p
        inverse_q  = 1/self.func.q
        return (self.S / (self.C * k_p)) ** inverse_q
    
    def solve_for_q(self):
        # q = ln(S / (C * K^p)) / ln(t_d)
        k_p = self.K ** self.func.p
        isolated_var = self.S / (self.C * k_p)
        ln_iso_var = log(isolated_var)
        ln_t_d = log(self.t_d)

        return (ln_iso_var / ln_t_d)
    
    def solve_for_p(self):
        # p = ln(S / (C * t_d^q)) / ln(k)
        td_q = self.t_d ** self.func.q
        isolated_var = self.S / (self.C * td_q)
        ln_iso_var = log(isolated_var)
        ln_k = log(self.K)

        return (ln_iso_var / ln_k)
