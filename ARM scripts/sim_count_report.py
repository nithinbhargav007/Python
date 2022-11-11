#!/usr/bin/env python3
################################################################################
#
# The confidential and proprietary information contained in this file may
# only be used by a person authorised under and to the extent permitted
# by a subsisting licensing agreement from Arm Limited or its affiliates.
#
#        (C) COPYRIGHT 2019 Arm Limited or its affiliates.
#                    ALL RIGHTS RESERVED
#
# This entire notice must be reproduced on all copies of this file
# and copies of this file may only be made by a person if such person is
# permitted to do so under the terms of a subsisting license agreement
# from Arm Limited or its affiliates.
#
################################################################################
import sys
import os
import glob
import time
import csv
import xlsxwriter

#usage will be python sim_count_report.py V8INT v1_work_dir_path v2_work_dir_path V1_list.list V2_list.list
suite_name = sys.argv[1]
work_dir_v1 = sys.argv[2]
work_dir_v2 = sys.argv[3]
v1_report_name = sys.argv[4]
v2_report_name = sys.argv[5]

suite_names_mod = suite_name.split(",")
num_suites = len(suite_names_mod)

cwd = os.getcwd()

my_target_list_v1 = os.listdir(work_dir_v1)
my_target_list_v1.sort()
my_target_list_v1 = [x for x in my_target_list_v1 if x.startswith("tgt")] 
m=len(my_target_list_v1)
print("v1 list of targets are" + str(my_target_list_v1))

my_target_list_v2 = os.listdir(work_dir_v2)
my_target_list_v2.sort()
my_target_list_v2 = [y for y in my_target_list_v2 if y.startswith("tgt")]
n=len(my_target_list_v2)
print("v2 list of targets are" +str(my_target_list_v2))

os.chdir(cwd)
wb = xlsxwriter.Workbook('main_tgt_report.xlsx')
for e in range(0,num_suites):
    suite_name = suite_names_mod[e]
    filename = suite_name+"_sim_count_mapping.csv"
    f = open(filename, "w+")
    f.close()
    
    firstrow = [ 'Target Name','Number of sims (V1)','Number of Sims (V2)', 'Sim count difference ( V2-V1)']
    with open(filename, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(firstrow)
        csvFile.close()
    
    for i in range(m-1):
        v1_path = work_dir_v1 +  ''.join(my_target_list_v1[i])
        os.chdir(v1_path)
        #print("target picked is" + my_target_list_v1[i])
        #v1_count_command = "grep -ir" + " 'bindir/" + suite_name+"'" + " " +v1_report_name+" | wc -l"
        v1_count_command = "grep " + " 'ARCH64/CORE/" + suite_name+"/'" + " " +v1_report_name+" | wc -l"
        print(v1_count_command)
        sim_count_v1 = os.popen(v1_count_command).readlines()
        sim_count_v1[:]= [line1.rstrip('\n') for line1 in sim_count_v1]
        sim_count_v1x = sim_count_v1[0]
        print("sim count in v1 is" + sim_count_v1x) 
        
        v2_path = work_dir_v2 +  ''.join(my_target_list_v1[i])
        os.chdir(v2_path)
        #v2_count_command = "grep -ir" + " 'bindir/" + suite_name+"'" + " " +v2_report_name+" | wc -l"
        v2_count_command = "grep " + " 'ARCH64/CORE/" + suite_name+"/'" + " " +v2_report_name+" | wc -l"
        #print(v2_count_command)
        sim_count_v2 = os.popen(v2_count_command).readlines()
        sim_count_v2[:]= [line.rstrip('\n') for line in sim_count_v2]
        sim_count_v2x = sim_count_v2[0]
        #print(sim_count_v2x)
        print("sim count in v2 is" + sim_count_v2x)

        sim_count_diff = int(sim_count_v2x) - int(sim_count_v1x)
        my_row = [my_target_list_v1[i], sim_count_v1x , sim_count_v2x, sim_count_diff]
        print(my_row)
    
        os.chdir(cwd)
        with open(filename, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(my_row)
            csvFile.close()
