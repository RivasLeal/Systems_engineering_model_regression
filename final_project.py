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
from numpy import array, var
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

    data_array.sort(key=lambda x: x[1])

    # Create a COCOMO ENUM of UNDEFINED
    cocomo_enum = COCOMO_ENUM(0)

    cur_pl = Curve_plot.DataStorage(data_array)
    # cur_pl.degree = 6
    # cur_pl.plot_data(show=True)

    a, b = cur_pl.fit_exponential_equation(all_effort, all_dev_time, all_c)

    c = []
    c_avg = 0

    for sloc_, dev_ in data_array_temp:
        cal_c = cur_pl.get_C( a, b, sloc_, dev_)
        c.append(cal_c)
        c_avg += cal_c

    c_avg /= len(data_array_temp)

    for c_vals in c:
        print(51000/c_vals)

    # print(e ** c_avg)

    # print(cur_pl.get_C(a, b, all_effort[0], all_dev_time[0]))

    # # Based on our JSON, get what our environment is
    # cocomo_enum = cocomo_enum.get_model_type_from_string(env_mode)

    # cocomo_model = COCOMO(64.5, cocomo_enum)

    # slim_model = SLIM()

    # slim_model.S = 64500
    # slim_model.K = 1.2543
    # slim_model.t_d = 1.50
    # slim_model.C = slim_model.solve_for_constant()

    # print(slim_model.solve_for_constant())

    # # # Dev Months -> Dev Years
    # # dev_time_years = cocomo_model.dev_time_months / 12

    
    # # lb_years = dev_time_years / 1.5 # cocomo_model.effort_months

    # # print("Effort: {}".format(lb_years))
    # # print("Dev Time (YRS): {}".format(dev_time_years))

if __name__ == '__main__':

    main()