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

        # General SLIM header
        worksheet.merge_range("B1:J1", "SLIM", cell_formatter)
        worksheet.merge_range("O1:V1", "SLIM", cell_formatter)

        # Write Project Header 
        worksheet.merge_range("B2:B4", "Project", cell_formatter)

        # Write SLOC Header
        worksheet.merge_range("C2:C4", "Source Lines \n of Code \n (SLOC)", cell_formatter)
        worksheet.merge_range("O2:O4", "Source Lines \n of Code \n (SLOC)", cell_formatter)

        # Write Effort Header
        worksheet.merge_range("D2:D4", "Effort \n (Labor Yrs) \n K", cell_formatter)
        worksheet.merge_range("P2:P4", "Effort \n (Labor Yrs) \n K", cell_formatter)

        # Write Gaffney Header
        worksheet.merge_range("E2:E4", "Gaffney \n  \n (P)", cell_formatter)
        worksheet.merge_range("Q2:Q4", "Gaffney \n  \n (P)", cell_formatter)

        # Write Effort^p Header
        worksheet.merge_range("F2:F4", "\n K^p \n ", cell_formatter)
        worksheet.merge_range("R2:R4", "\n K^p \n ", cell_formatter)

        # Write Development Time Header
        worksheet.merge_range("G2:G4", "Dev Time \n (Yrs) \n t_d", cell_formatter)
        worksheet.merge_range("S2:S4", "Dev Time \n (Yrs) \n t_d", cell_formatter)

        # Write Second Gaffney Header
        worksheet.merge_range("H2:H4", "Gaffney \n  \n (Q)", cell_formatter)
        worksheet.merge_range("T2:T4", "Gaffney \n  \n (Q)", cell_formatter)

        #Write t_d^q header
        worksheet.merge_range("I2:I4", " \n t_d^q \n", cell_formatter)
        worksheet.merge_range("U2:U4", " \n t_d^q \n", cell_formatter)

        # Write Technology Constant header
        worksheet.merge_range("J2:J4", " \n C \n", cell_formatter)
        worksheet.merge_range("V2:V4", " \n C \n", cell_formatter)

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

        letter_map_data = ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        letter_map_place = ['O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V']

        worksheet.write("N{}".format(start_pos), "AVERAGE", cell_formatter)
        for letter, placeLetter in zip(letter_map_data, letter_map_place):
            worksheet.write_formula("{}{}".format(placeLetter, start_pos), 
                                    "=AVERAGE({0}{1}:{0}{2})".format(letter, start_pos, end_data_pos), data_cell_formatter)

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

        var_pos = 6
        worksheet.write("N{}".format(var_pos), "Variance", cell_formatter)

        worksheet.write("P{}".format(var_pos), "{}".format(round(var(var_K),4)), data_cell_formatter)
        worksheet.write("R{}".format(var_pos), "{}".format(round(var(var_k_p),4)), data_cell_formatter)
        worksheet.write("S{}".format(var_pos), "{}".format(round(var(var_t_d),4)), data_cell_formatter)
        worksheet.write("U{}".format(var_pos), "{}".format(round(var(var_t_d_q),4)), data_cell_formatter)
        worksheet.write("V{}".format(var_pos), "{}".format(round(var(var_C),4)), data_cell_formatter)

        worksheet.merge_range("O13:O14", "SLOC(X) and K(Y)", cell_formatter)
        worksheet.merge_range("P13:P14", "SLOC(X) and td(Y)", cell_formatter)
        worksheet.merge_range("Q13:Q14", "SLOC(X) and C(Y)", cell_formatter)
        worksheet.merge_range("R13:R14", "K(X) and td(Y)", cell_formatter)
        worksheet.merge_range("S13:S14", "Kp(X) and tdq(Y)", cell_formatter)
        worksheet.merge_range("T13:T14", "K(X) and C(Y)", cell_formatter)
        worksheet.merge_range("U13:U14", "td(X) and C(Y)", cell_formatter)

        r2_pos = 15
        worksheet.write("N{}".format(r2_pos), "R^2", cell_formatter)

        worksheet.write_formula("O{}".format(r2_pos), 
                                    "=RSQ(D{0}:D{1}, C{0}:C{1})".format(start_pos, end_data_pos), data_cell_formatter)
        worksheet.write_formula("P{}".format(r2_pos), 
                                    "=RSQ(G{0}:G{1}, C{0}:C{1})".format(start_pos, end_data_pos), data_cell_formatter)
        worksheet.write_formula("Q{}".format(r2_pos), 
                                    "=RSQ(J{0}:J{1}, C{0}:C{1})".format(start_pos, end_data_pos), data_cell_formatter)
        worksheet.write_formula("R{}".format(r2_pos), 
                                    "=RSQ(G{0}:G{1}, D{0}:D{1})".format(start_pos, end_data_pos), data_cell_formatter)
        worksheet.write_formula("S{}".format(r2_pos), 
                                    "=RSQ(I{0}:I{1}, F{0}:F{1})".format(start_pos, end_data_pos), data_cell_formatter)
        worksheet.write_formula("T{}".format(r2_pos), 
                                    "=RSQ(J{0}:J{1}, D{0}:D{1})".format(start_pos, end_data_pos), data_cell_formatter)
        worksheet.write_formula("U{}".format(r2_pos), 
                                    "=RSQ(J{0}:J{1}, G{0}:G{1})".format(start_pos, end_data_pos), data_cell_formatter)
        workbook.close()