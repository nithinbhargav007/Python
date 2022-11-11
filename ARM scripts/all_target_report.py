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
    filename = suite_name+"_all_target_report.csv"
    f = open(filename, "w+")
    f.close()
    
    firstrow = [ 'Target Name','Number of sims (V1)','Number of Sims (V2)','Number of tests picked(V1)', 'Number of tests picked(V2)', 'Sim count difference ( V2-V1)', 'Tests Picked difference (V2-V1)']
    with open(filename, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(firstrow)
        csvFile.close()
    
    for i in range(m-1):
        v1_path = work_dir_v1 +  ''.join(my_target_list_v1[i])
        os.chdir(v1_path)
        #print("target picked is" + my_target_list_v1[i])
        #v1_count_command = "grep -ir" + " 'bindir/" + suite_name+"'" + " " +v1_report_name+" | wc -l"
        v1_count_command = "grep " + " 'ARCH64/CORE/" + suite_name+"'" + " " +v1_report_name+" | wc -l"
        #print(v1_count_command)
        sim_count_v1 = os.popen(v1_count_command).readlines()
        sim_count_v1[:]= [line1.rstrip('\n') for line1 in sim_count_v1]
        sim_count_v1x = sim_count_v1[0]
        print("sim count in v1 is" + sim_count_v1x) 
    
        #v1_tests_command = "grep -ir" + " 'bindir/" + suite_name+"'" + " "+v1_report_name+" | cut -d '/' -f3 | sort -u | wc -l"
        v1_tests_command = "grep " + "'ARCH64/CORE/" + suite_name+"'" + " " +v1_report_name+" |cut -d ',' -f3 | sort -u | wc -l"
        #print(v1_tests_command)
        test_count_v1 = os.popen(v1_tests_command).readlines()
        test_count_v1[:]= [line1.rstrip('\n') for line1 in test_count_v1]
        test_count_v1x = test_count_v1[0]
        print("test count in v1 is" + str(test_count_v1x))

        #create_v1_sim_list = "cp -rf " + v1_report_name +" "+my_target_list_v1[m]+".list"
        #os.system(create_v1_sim_list)       
         
        v2_path = work_dir_v2 +  ''.join(my_target_list_v1[i])
        os.chdir(v2_path)
        #v2_count_command = "grep -ir" + " 'bindir/" + suite_name+"'" + " " +v2_report_name+" | wc -l"
        v2_count_command = "grep " + "'ARCH64/CORE/" + suite_name+"'" + " " +v2_report_name+" | wc -l"
        #print(v2_count_command)
        sim_count_v2 = os.popen(v2_count_command).readlines()
        sim_count_v2[:]= [line.rstrip('\n') for line in sim_count_v2]
        sim_count_v2x = sim_count_v2[0]
        #print(sim_count_v2x)
        print("sim count in v2 is" + sim_count_v2x)
    
        #v2_tests_command = "grep -ir" + " 'bindir/" + suite_name+"'" + " "+v2_report_name+" | cut -d '/' -f3 | sort -u | wc -l"
        v2_tests_command = "grep " + "'ARCH64/CORE/" + suite_name+"'" + " " +v2_report_name+" |cut -d ',' -f3 | sort -u | wc -l"
        #print(v2_tests_command)
        test_count_v2 = os.popen(v2_tests_command).readlines()
        test_count_v2[:]= [line.rstrip('\n') for line in test_count_v2]
        test_count_v2x = test_count_v2[0]
        print("test count in v2 is"+str(test_count_v2x))    
        #print(j)
        #print( "the value of v1x is" + sim_count_v1x)

        #create_v2_sim_list = "cp -rf " + v1_report_name +" "+my_target_list_v1[m]+".list"
        #os.system(create_v2_sim_list)

        sim_count_diff = int(sim_count_v2x) - int(sim_count_v1x)
        test_count_diff = int(test_count_v2x) - int(test_count_v1x)
        my_row = [my_target_list_v1[i], sim_count_v1x , sim_count_v2x, test_count_v1x, test_count_v2x, sim_count_diff, test_count_diff]
        print(my_row)
    
        os.chdir(cwd)
        with open(filename, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(my_row)
            csvFile.close()
    
      #  # if we read f.csv we will write f.xlsx
      #  wb = xlsxwriter.Workbook(filename.replace(".csv",".xlsx"))
      #  ws = wb.add_worksheet(filename)    # your worksheet title here
      #  with open(filename,'r') as csvfile:
      #          table = csv.reader(csvfile)
      #          increment = 0
      #  # write each row from the csv file as text into the excel file
      #  # this may be adjusted to use 'excel types' explicitly (see xlsxwriter doc)
      #          for row in table:
      #              ws.write_row(increment, 0, row)
      #              increment += 1
      #  wb.close()
    
      #  report_cmd = "rm -rf "+filename
      #  os.system(report_cmd)
