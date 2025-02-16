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

from json import load
from Model_Types.SLIM import SLIM
from numpy import var

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
    slim_proj_dict  = dict()

    # Sum of all projects
    total_src_code  = 0
    total_dev_time  = 0
    total_effort    = 0



    # Iterate throught all Projects
    for proj in data[project_string]:
        sloc = data[project_string][proj][sloc_string]
        dev_time = data[project_string][proj][dev_time_string]
        eff = data[project_string][proj][effort_string]
        slim_proj_dict[proj] = SLIM()

        slim_proj_dict[proj].S = sloc
        slim_proj_dict[proj].K = eff
        slim_proj_dict[proj].t_d = dev_time

        total_src_code += sloc
        total_dev_time += dev_time
        total_effort   += eff


    total_slim = SLIM()

    # Find the overall SLIM values
    total_slim.S   = total_src_code / len(data[project_string])
    total_slim.K   = total_effort   / len(data[project_string])
    total_slim.t_d = total_dev_time / len(data[project_string])

    print(total_slim.solve_for_constant())

if __name__ == '__main__':
    main()