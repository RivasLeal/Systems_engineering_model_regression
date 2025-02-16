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

from enum import Enum

class COCOMO_ENUM(Enum):
    UNDEFINED = 0
    ORGANIC = 1
    EMBEDDED = 2
    SEMIDETACHED = 3

    def get_model_type_from_string(self , enumString):
        if enumString.lower() == "organic":
            return COCOMO_ENUM.ORGANIC
        if enumString.lower() == "embedded":
            return COCOMO_ENUM.EMBEDDED
        if enumString.lower() == "semidetached":
            return COCOMO_ENUM.SEMIDETACHED

class COCOMO:
    def __init__(self, KDSI, model_type):
        if model_type == COCOMO_ENUM.ORGANIC:
            self.a = 2.4
            self.b = 1.05
            self.c = 2.5
            self.d = 0.38
        elif model_type == COCOMO_ENUM.SEMIDETACHED:
            self.a = 3.0
            self.b = 1.12
            self.c = 2.5
            self.d = 0.35
        elif model_type == COCOMO_ENUM.EMBEDDED:
            self.a = 3.6
            self.b = 1.20
            self.c = 2.5
            self.d = 0.32
        else:
            raise ValueError("Invalid Model Type")
        
        self.effort_months = self.a * (KDSI ** self.b)
        self.dev_time_months = self.c * (self.effort_months ** self.d)