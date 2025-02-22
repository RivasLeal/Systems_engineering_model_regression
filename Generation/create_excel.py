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

from xlsxwriter.workbook import Workbook
from numpy import var

class CreateSlimExcel:
    def __init__(self, proj_dict):
        workbook = Workbook(r"C:\Users\Rivas\Desktop\Coding\Python\repository\Systems_engineering_model_regression\UpdatedHistoricalData.xlsx")
        worksheet = workbook.add_worksheet("FIT Historical Performance")

        # Create Formatter
        cell_formatter = workbook.add_format()
        cell_formatter.set_fg_color("#B7C9E2")
        cell_formatter.set_align('center_across')
        cell_formatter.set_border_color("#000000")
        cell_formatter.set_border(2)
        cell_formatter.set_text_wrap()

        letter_map = ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

        # General SLIM header
        worksheet.merge_range("B1:J1", "SLIM", cell_formatter)

        # Write Project Header 
        worksheet.merge_range("B2:B4", "Project", cell_formatter)

        # Write SLOC Header
        worksheet.merge_range("C2:C4", "Source Lines \n of Code \n (SLOC)", cell_formatter)

        # Write Effort Header
        worksheet.merge_range("D2:D4", "Effort \n (Labor Yrs) \n K", cell_formatter)

        # Write Gaffney Header
        worksheet.merge_range("E2:E4", "Gaffney \n  \n (P)", cell_formatter)

        # Write Effort^p Header
        worksheet.merge_range("F2:F4", "\n K^p \n ", cell_formatter)

        # Write Development Time Header
        worksheet.merge_range("G2:G4", "Dev Time \n (Yrs) \n t_d", cell_formatter)

        # Write Second Gaffney Header
        worksheet.merge_range("H2:H4", "Gaffney \n  \n (Q)", cell_formatter)

        #Write t_d^q header
        worksheet.merge_range("I2:I4", " \n t_d^q \n", cell_formatter)

        # Write Technology Constant header
        worksheet.merge_range("J2:J4", " \n C \n", cell_formatter)

        # Position after headers 
        start_pos = 5
        pos_ = 5

        data_cell_formatter = workbook.add_format()
        data_cell_formatter.set_border(2)
        for key, proj in proj_dict.items():

            worksheet.write("B{}".format(pos_), key, data_cell_formatter)
            worksheet.write("C{}".format(pos_), proj.S, data_cell_formatter)
            worksheet.write("D{}".format(pos_), proj.K, data_cell_formatter)
            worksheet.write("E{}".format(pos_), proj.func.p, data_cell_formatter)
            worksheet.write_formula("F{}".format(pos_), "={}^{}".format(proj.K, proj.func.p), data_cell_formatter)
            worksheet.write("G{}".format(pos_), proj.t_d, data_cell_formatter)
            worksheet.write("H{}".format(pos_), proj.func.q, data_cell_formatter)
            worksheet.write_formula("I{}".format(pos_), "={}^{}".format(proj.t_d, proj.func.q), data_cell_formatter)
            worksheet.write("J{}".format(pos_), proj.C, data_cell_formatter)
            pos_ += 1

        end_data_pos = pos_ - 1 
        worksheet.write("A{}".format(pos_), "AVERAGE")
        for letter in letter_map:
            worksheet.write_formula("{}{}".format(letter, pos_), "=AVERAGE({0}{1}:{0}{2})".format(letter, start_pos, end_data_pos), data_cell_formatter)
        pos_ += 1

        var_K = []
        var_t_d = []
        var_C = []
        var_t_d_q = []
        var_k_p = []

        for proj in proj_dict.values():
            var_K.append(proj.K)
            var_t_d.append(proj.t_d)
            var_C.append(proj.C)
            var_t_d_q.append(proj.solve_for_t_d_q())
            var_k_p.append(proj.solve_for_K_p())

        worksheet.write("A{}".format(pos_), "Variance")
        worksheet.write("D{}".format(pos_), "{}".format(round(var(var_k_p),4)), data_cell_formatter)
        worksheet.write("F{}".format(pos_), "{}".format(round(var(var_k_p),4)), data_cell_formatter)
        worksheet.write("G{}".format(pos_), "{}".format(round(var(var_t_d),4)), data_cell_formatter)
        worksheet.write("I{}".format(pos_), "{}".format(round(var(var_t_d_q),4)), data_cell_formatter)
        worksheet.write("J{}".format(pos_), "{}".format(round(var(var_C),4)), data_cell_formatter)
        # for letter in letter_map
        #     worksheet.write("{}{}".format(letter, pos_), "{}".format(var(0)), data_cell_formatter)
        pos_ += 1
        # worksheet.write("A{}".format(pos_), "R^2")
        # for letter in letter_map:
        #     worksheet.write_formula("{}{}".format(letter, pos_), "=RSQ({0}{1}:{0}{2})".format(letter, start_pos, end_data_pos))

        workbook.close()