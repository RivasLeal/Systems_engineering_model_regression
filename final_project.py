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

    # Sections Found in the JSON
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

    # Environment Vars found in the JSON
    labor_hours_to_months  = data[labor_hours_string]
    env_mode = data[env_mode_string]

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

        slim_proj_dict[proj] = SLIM(env_mode)

        slim_proj_dict[proj].S = sloc
        slim_proj_dict[proj].K = eff
        slim_proj_dict[proj].t_d = dev_time
        slim_proj_dict[proj].C = slim_proj_dict[proj].solve_for_constant()

        all_c.append((sloc / slim_proj_dict[proj].C))

        total_src_code += sloc
        total_dev_time += dev_time
        total_effort   += eff

    temp_SLIM = SLIM(env_mode)

    p, q, c = temp_func(env_mode, all_effort, all_dev_time, all_c, data_array_temp, data_array, 
              total_src_code, total_dev_time, total_effort, slim_proj_dict, data, project_string)
    
    iter = 0

    init_C = c
    
    while((p <= temp_SLIM.func.p or q <=temp_SLIM.func.q or c < init_C) and iter < 100):

        all_effort, all_dev_time, all_c, data_array_temp, data_array, \
        total_src_code, total_dev_time, total_effort  = get_new_total_values(data, project_string, slim_proj_dict)

        p, q, c = temp_func(env_mode, all_effort, all_dev_time, all_c, data_array_temp, data_array, 
              total_src_code, total_dev_time, total_effort, slim_proj_dict, data, project_string)
        
        iter +=1

    print(iter, p, q)
    print("-----------------------------")
    for proj in data[project_string]:
        print(round(slim_proj_dict[proj].K, 4))

def get_new_total_values(data, project_string, slim_proj_dict):

    # Storage of the data
    data_array = []
    data_array_temp = []

    all_effort = []
    all_dev_time = []
    all_c = []

    # Sum of all projects
    total_src_code  = 0
    total_dev_time  = 0
    total_effort    = 0 

    for proj in data[project_string]:

        data_array.append((slim_proj_dict[proj].S,slim_proj_dict[proj].t_d))
        data_array_temp.append((slim_proj_dict[proj].K, slim_proj_dict[proj].t_d))
        all_effort.append(slim_proj_dict[proj].K)
        all_dev_time.append(slim_proj_dict[proj].t_d)

        total_src_code += slim_proj_dict[proj].S
        total_dev_time += slim_proj_dict[proj].t_d
        total_effort   += slim_proj_dict[proj].K

        all_c.append((slim_proj_dict[proj].S / slim_proj_dict[proj].C))

    return all_effort, all_dev_time, all_c, data_array_temp, data_array, \
            total_src_code, total_dev_time, total_effort

def temp_func(env_mode, all_effort, all_dev_time, all_c, data_array_temp, data_array, 
              total_src_code, total_dev_time, total_effort, slim_proj_dict, data, project_string):
    temp_SLIM = SLIM(env_mode)

    # Create a COCOMO ENUM of UNDEFINED
    cocomo_enum = COCOMO_ENUM(0)

    cur_pl = Curve_plot.DataStorage()

    # Fit the Data into a linear model
    a, b = cur_pl.fit_exponential_equation(all_effort, all_dev_time, all_c)

    c = []

    # Get the (S/C)^2 values and save off the values
    for sloc_, dev_ in data_array_temp:
        cal_c = cur_pl.get_C( a, b, sloc_, dev_)
        c.append(cal_c)

    # The values obtained are currently (S/C)^2, so need to convert to S/C
    sqrt_c_vals = []
    for _ in c:
        sqrt_c_vals.append(_ ** 0.5)

    # Get all the C values
    new_C_values = []
    for c , a in zip(sqrt_c_vals,data_array):
       new_C_values.append(a[0] / c)

    # Store the New P and Q values
    newPs = []
    newQs = []

    # Find all the P and Q values from the data
    for newC, arTemp, daTemp in zip(new_C_values, data_array_temp, data_array):
        ln_K = log(arTemp[0])
        ln_td = log(arTemp[1])
        ln_SLOC_newC = log(daTemp[0]/newC)

        temp11 = ln_SLOC_newC - (temp_SLIM.func.p * ln_K)
        temp12 = ln_SLOC_newC - (temp_SLIM.func.q * ln_td)
        
        newPs.append(temp11 / ln_td )
        newQs.append(temp12 / ln_K )

    # Get the average P and Q values for all projects
    newAvgP = round(sum(newPs) / len(newPs), 4)
    newAvgQ = round(sum(newQs) / len(newQs), 4)

    # Get the Average values for all projects to get an overall C value
    SLOC_avg     = total_src_code / len(data[project_string])
    dev_time_avg = total_dev_time / len(data[project_string])
    effort_avg   = total_effort   / len(data[project_string])

    # Plug in Values into SLIM as if it where a solo project
    temp_SLIM.S = SLOC_avg
    temp_SLIM.K = effort_avg
    temp_SLIM.t_d = dev_time_avg
    temp_SLIM.func.p = newAvgP
    temp_SLIM.func.q = newAvgQ

    # Solve for the company C value
    tempC = round(temp_SLIM.solve_for_constant(), 4)

    for proj in data[project_string]:

        # Insert the New P, Q, and C values into all project and revaluate the effort
        slim_proj_dict[proj].func.p = newAvgP
        slim_proj_dict[proj].func.q = newAvgQ
        slim_proj_dict[proj].C = tempC

        slim_proj_dict[proj].K = slim_proj_dict[proj].solve_for_K()

    return newAvgP, newAvgQ, tempC
if __name__ == '__main__':

    main()