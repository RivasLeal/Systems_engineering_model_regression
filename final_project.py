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
#test
from sys import argv
from numpy import log
from Data_Fitting import Model_Fitting
from json import load
from Model_Types.COCOMO import COCOMO_ENUM, COCOMO
from Model_Types.SLIM import SLIM
from random import randint, uniform
from math import ceil
from Generation import create_excel

def main(args):
    
    # First Argument is the Data JSON File
    with open(r'{}'.format(args[0]), 'r') as data_file:
        data = load(data_file)

    # Sections Found in the JSON
    project_string = "Projects"
    sloc_string = "SLOC"
    dev_time_string = "Development Time"
    effort_string = "Effort"
    labor_hours_string = "Labor Hours in a Month"
    env_mode_string = "Environment Mode"
    gener_iter = "Generation Iterations"
    min_sloc = "Min SLOC Generation"
    max_sloc = "MAX SLOC Generation"

    # Storage of the data
    data_array = []
    data_array_temp = []

    all_effort = []
    all_dev_time = []
    all_c = []
    all_C = []
    slim_proj_dict  = dict()

    # Sum of all projects
    total_src_code  = 0
    total_dev_time  = 0
    total_effort    = 0

    # Environment Vars found in the JSON
    labor_hours_to_months  = data[labor_hours_string]
    env_mode = data[env_mode_string]

    # Create a COCOMO ENUM of UNDEFINED
    cocomo_enum = COCOMO_ENUM.UNDEFINED
    cocomo_enum = cocomo_enum.get_model_type_from_string(env_mode)
    cocomo_proj_dict  = dict()

    # Iterate throught all Projects
    for proj in data[project_string]:
        # Get Values from the json
        sloc = data[project_string][proj][sloc_string]
        dev_time = data[project_string][proj][dev_time_string]
        eff = data[project_string][proj][effort_string]
        slim_proj_dict[proj] = SLIM(env_mode)

        # Convert SLOC -> KSLOC
        cocomo_proj_dict[proj] = COCOMO((sloc / (10**3)), cocomo_enum)

        data_array.append((sloc,dev_time))
        data_array_temp.append((eff, dev_time))
        all_effort.append(eff)
        all_dev_time.append(dev_time)

        slim_proj_dict[proj].S = sloc
        slim_proj_dict[proj].K = eff
        slim_proj_dict[proj].t_d = dev_time
        slim_proj_dict[proj].C = slim_proj_dict[proj].solve_for_constant()

        all_C.append(slim_proj_dict[proj].C)
        all_c.append((sloc / slim_proj_dict[proj].C))

        total_src_code += sloc
        total_dev_time += dev_time
        total_effort   += eff

    temp = SLIM(env_mode)
    if(len(args) > 1):
        try:
            num_entries = int(args[1])
            print("Generating: {} data points".format(args[1]))
            generate_new_data(min_sloc, max_sloc, (sum(all_C) / len(all_C)), temp.func.p, temp.func.q, slim_proj_dict , num_entries, total_src_code, total_dev_time)
        except:
            print("Not a valid int")
    iter = 0
    iter_limit = data[gener_iter]

    # Make sure it cant be non zero
    if(iter_limit < 1):
        iter_limit = 100
    
    best_p = temp.func.p
    best_q = temp.func.q
    best_c = (sum(all_C) / len(all_C))

    try:
        while(iter < iter_limit):
            all_effort, all_dev_time, all_c, data_array_temp, data_array, \
            total_src_code, total_dev_time, total_effort  = get_new_total_values(slim_proj_dict)

            p, q, c = run_analysis(env_mode, all_effort, all_dev_time, all_c, data_array_temp, data_array, 
                total_src_code, total_dev_time, total_effort, slim_proj_dict)
            
            if(p > best_p and q > best_q and c > best_c):

                best_p = p
                best_q = q
                best_c = c
            
            iter +=1
    except:
        print("Couldn't continue calculating, using last known P and Q values")

    for proj in slim_proj_dict.values():

        proj.C = best_c
        proj.func.p = best_p
        proj.func.q = best_q
        proj.K = round(proj.solve_for_K(), 4)

    # for key, val in cocomo_proj_dict.items():

    #     print("slim_k: ",  (slim_proj_dict[key].K * 12))
    #     print("slim_t_d: ", (slim_proj_dict[key].solve_for_t_d() * 12))

    #     print("coco_k: ",  cocomo_proj_dict[key].effort_months)
    #     print("coco_t_d: ", cocomo_proj_dict[key].dev_time_months)

    #     cocomo_proj_dict[key].effort_months   = (slim_proj_dict[key].K * 12)
    #     cocomo_proj_dict[key].dev_time_months = (slim_proj_dict[key].solve_for_t_d() * 12)

    #     print("a: ", cocomo_proj_dict[key].solve_for_a())
    #     print("b: ", cocomo_proj_dict[key].solve_for_b())

    #     print("--------------------------------------------")
 
    if(len(args) > 2):
        createEx = create_excel.CreateSlimExcel(slim_proj_dict, args[2])

    print("New P: {}, New Q: {}".format(best_p, best_q))

def generate_new_data(min_sloc, max_sloc, best_c, best_p, best_q, slim_proj_dict, num_entries, total_src_code, total_dev_time):
    
    try:
        lowerLimit = int(min_sloc)
    except:
        lowerLimit = 45000
        print("Lower Limit couldn't be read in, using 45000")
    try:
        upperLimit = int(max_sloc)
    except:
        upperLimit = 900000
        print("Upper Limit couldn't be read in, using 900000")

    ratio = total_dev_time / total_src_code
    itr = 1

    while num_entries > 0 and ratio != 0:
        project = "project{}".format(itr)

        slim_proj_dict[project] = SLIM()
        slim_proj_dict[project].S = int(ceil(randint(lowerLimit, upperLimit) / 100.0)) * 100

        estimated_development_time = (ratio* slim_proj_dict[project].S)
        variance = 0
        
        while variance == 0:
           variance = 1 + uniform(-0.10,0.10)

        slim_proj_dict[project].t_d = round(estimated_development_time, 2) 

        slim_proj_dict[project].func.p =  best_p
        slim_proj_dict[project].func.q =  best_q

        slim_proj_dict[project].C =  best_c

        slim_proj_dict[project].K = round(slim_proj_dict[project].solve_for_K() * variance,4)

        itr += 1
        num_entries -=1

def get_new_total_values(slim_proj_dict):
    '''
    @param slim_proj_dict   - dictionary of SLIM models

    @return all_effort      - Lists of all projects Effort
    @return all_dev_time    - Lists of all project development time
    @return all_c           - Lists of all projects technology constant
    @return data_array_temp - 2D list containing Effort and development time for each project
    @return data_array      - 2D list Source Lines of Code and development time for each project
    @return total_src_code  - Total number of source code throughout all projects
    @return total_dev_time  - Total number of development time throughout all projects
    @return total_effort    - Total number of effort throughout all projects
    '''
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

    for proj in slim_proj_dict.values():

        data_array.append((proj.S,proj.t_d))
        data_array_temp.append((proj.K, proj.t_d))
        all_effort.append(proj.K)
        all_dev_time.append(proj.t_d)

        total_src_code += proj.S
        total_dev_time += proj.t_d
        total_effort   += proj.K

        all_c.append(proj.S / proj.C)

    return all_effort, all_dev_time, all_c, data_array_temp, data_array, \
            total_src_code, total_dev_time, total_effort

def run_analysis(env_mode, all_effort, all_dev_time, all_c, data_array_temp, data_array, 
              total_src_code, total_dev_time, total_effort, slim_proj_dict):
    '''
    @param env_mode        - Whether we are running Gafney or Putnam
    @param slim_proj_dict  - dictionary of SLIM models
    @param all_effort      - Lists of all projects Effort
    @param all_dev_time    - Lists of all project development time
    @param all_c           - Lists of all projects technology constant
    @param data_array_temp - 2D list containing Effort and development time for each project
    @param data_array      - 2D list Source Lines of Code and development time for each project
    @param total_src_code  - Total number of source code throughout all projects
    @param total_dev_time  - Total number of development time throughout all projects
    @param total_effort    - Total number of effort throughout all projects

    @return newAvgP - New Calculated P value
    @return newAvgQ - New Calculated Q value
    @return tempC   - New Calculated Technology Constant value
    '''
    temp_SLIM = SLIM(env_mode)

    cur_pl = Model_Fitting.Model_Fitting()

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
    SLOC_avg     = total_src_code / len(slim_proj_dict)
    dev_time_avg = total_dev_time / len(slim_proj_dict)
    effort_avg   = total_effort   / len(slim_proj_dict)

    # Plug in Values into SLIM as if it where a solo project
    temp_SLIM.S = SLOC_avg
    temp_SLIM.K = effort_avg
    temp_SLIM.t_d = dev_time_avg
    temp_SLIM.func.p = newAvgP
    temp_SLIM.func.q = newAvgQ

    # Solve for the company C value
    tempC = round(temp_SLIM.solve_for_constant(), 4)

    for proj in slim_proj_dict.values():

        # Insert the New P, Q, and C values into all project and revaluate the effort
        proj.func.p = newAvgP
        proj.func.q = newAvgQ
        proj.C = tempC

        # insert new Technology Constant
        proj.K = proj.solve_for_K()

    return newAvgP, newAvgQ, tempC

if __name__ == '__main__':

    if(len(argv) < 2):
        print("Missing Argument")
    else:
        main(argv[1:])