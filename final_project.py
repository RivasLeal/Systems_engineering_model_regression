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

# TODO
# from sys import argv
from numpy import array, var, log
from Data_Creation import Curve_plot
from json import load
from Model_Types.COCOMO import COCOMO_ENUM, COCOMO
from Model_Types.SLIM import SLIM
from math import e

def main():
    with open('data.json', 'r') as data_file:
        data = load(data_file)

    project_string = "Projects"
    sloc_string = "SLOC"
    dev_time_string = "Development Time"
    effort_string = "Effort"
    labor_hours_string = "Labor Hours in a Month"
    env_mode_string = "Environment Mode"

    # Storage of the data
    data_array = []
    data_array_temp = []

    all_effort = []
    all_dev_time = []
    all_c = []
    slim_proj_dict  = dict()

    # Sum of all projects
    total_src_code  = 0
    total_dev_time  = 0
    total_effort    = 0

    # Iterate throught all Projects
    for proj in data[project_string]:
        # Get Values from the json
        sloc = data[project_string][proj][sloc_string]
        dev_time = data[project_string][proj][dev_time_string]
        eff = data[project_string][proj][effort_string]

        data_array.append((sloc,dev_time))
        data_array_temp.append((eff, dev_time))
        all_effort.append(eff)
        all_dev_time.append(dev_time)

        slim_proj_dict[proj] = SLIM()

        slim_proj_dict[proj].S = sloc
        slim_proj_dict[proj].K = eff
        slim_proj_dict[proj].t_d = dev_time

        all_c.append((sloc / slim_proj_dict[proj].solve_for_constant()))

        total_src_code += sloc
        total_dev_time += dev_time
        total_effort   += eff

    labor_hours  = data[labor_hours_string]
    env_mode = data[env_mode_string]
    temp_SLIM = SLIM()

    # Create a COCOMO ENUM of UNDEFINED
    cocomo_enum = COCOMO_ENUM(0)

    cur_pl = Curve_plot.DataStorage(data_array)

    a, b = cur_pl.fit_exponential_equation(all_effort, all_dev_time, all_c)

    c = []
    c_avg = 0

    for sloc_, dev_ in data_array_temp:
        cal_c = cur_pl.get_C( a, b, sloc_, dev_)
        c.append(cal_c)
        c_avg += cal_c

    sqrt_c_vals = []
    for _ in c:
        sqrt_c_vals.append(_ ** 0.5)

    new_C_values = []
    for c , a in zip(sqrt_c_vals,data_array):
       new_C_values.append(a[0] / c)

    newPs = []
    newQs = []

    for newC, arTemp, daTemp in zip(new_C_values, data_array_temp, data_array):
        ln_K = log(arTemp[0])
        ln_td = log(arTemp[1])
        ln_SLOC_newC = log(daTemp[0]/newC)


        temp11 = ln_SLOC_newC - (temp_SLIM.func.p * ln_K)
        temp12 = ln_SLOC_newC - (temp_SLIM.func.q * ln_td)
        
        newPs.append(temp11 / ln_td )
        newQs.append(temp12 / ln_K )

    
    newAvgP = sum(newPs) / len(newPs)
    newAvgQ = sum(newQs) / len(newQs)

    print(newAvgP)
    print(newAvgQ)

    for proj in data[project_string]:
        slim_proj_dict[proj].func.p = newAvgP
        slim_proj_dict[proj].func.q = newAvgQ
        slim_proj_dict[proj].C = 51087.4267295428

        print(slim_proj_dict[proj].solve_for_K())


if __name__ == '__main__':

    main()