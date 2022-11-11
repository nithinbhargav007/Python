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
import gzip
import csv
import re
import operator
from shutil import copyfile
from collections import Counter
import xlsxwriter
from openpyxl import load_workbook

suite_name = sys.argv[1]
work_dir_v1 = sys.argv[2]
work_dir_v2 = sys.argv[3]
main_target = sys.argv[4]
partner_target= sys.argv[5]
partner_names = sys.argv[6]

suite_names_mod = suite_name.split(",")
num_suites = len(suite_names_mod)
#print(num_suites-1)

def weird_division(n, d):
    return n / d if d else 0
wb = xlsxwriter.Workbook('main_report.xlsx')
for e in range(0,num_suites):
        #print(e)
        #print("number of suites given is " + str(num_suites))
        #main_target = [main_target]
        partner_target_mod = partner_target.split(",")
        partner_names_mod= partner_names.split(",")
        suite_name = suite_names_mod[e]
        print( "suite picked is" + str(suite_name))
        #print(suite_names_mod)
        target_list_v1 = []
        target_list_v2 = []
        target_list_v1.append(main_target)
        target_list_v2.append(main_target)
        target_list_v1.extend(partner_target_mod)
        target_list_v2.extend(partner_target_mod)
        print(target_list_v1)
        
        num_arguments = len(sys.argv) - 1
        #print('number of arguments provided is' + str(num_arguments))
        
        v1_report_only =0
        if (num_arguments ==7):
            if(sys.argv[7] == 'v1_only'):
                v1_report_only=1
        
        
        cwd = os.getcwd()
        #print(cwd)
        test_list_path = "/arm/projectscratch/pd/shatranj/users/nitkum01/validation/ARCH64/CORE/"+suite_name+"/tests/"
        common_list_path = "/arm/projectscratch/pd/shatranj/common/arch_suites/a_profile/latest/validation/ARCH64/CORE/"+suite_name+"/tests/"
        scr_path = "/arm/projectscratch/pd/shatranj/users/nitkum01/validation/ARCH64/CORE/"+suite_name+"/tests/suite_config_rules.h"
        scr_command = "cat "+scr_path
        scr_mod = os.popen(scr_command).readlines()
        scr_mod[:]= [line.rstrip('\n') for line in scr_mod]
        scr_mod = [x for x in scr_mod if not x.startswith('//')]
        #print(scr_mod)


        my_test_list = os.listdir(test_list_path)
        common_test_list = os.listdir(common_list_path)
        #print(test_list_path)
        from pprint import pprint
        my_test_list.sort()
        suite_name_l = suite_name.lower()
        suite_name_n = suite_name_l.split("_")[0] 
        my_test_list = [x for x in my_test_list if x.startswith(suite_name_n)]  #filter the directory contents to get only list of tests
        common_test_list = [x for x in common_test_list if x.startswith(suite_name_n)] 
        #Create/empty the existing report file
        os.chdir(cwd)
        if v1_report_only ==0:
                filename = suite_name +"_report.csv"
                filename1 = suite_name+"_SCR_table.csv"
        elif v1_report_only==1:
                filename = suite_name +"v1_report.csv"
        # opening the file with w+ mode truncates the file
        f = open(filename, "w+")
        f.close()
        f1= open(filename1, "w+")
        f1.close()
        
        def sorted_nicely( l ):
            """ Sorts the given iterable in the way that is expected.
         
            Required arguments:
            l -- The iterable to be sorted.
         
            """
            convert = lambda text: int(text) if text.isdigit() else text
            alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
            return sorted(l, key = alphanum_key)
        
        #add the first row to the csv file
        if v1_report_only !=1:
                #print(partner_names_mod[0])
                firstrow = [ 'Serial No', 'Test Name',' Configs in V1', 'Configs in V2 ( pick_any = pick_all)','Configs in V2','Number of Sims (V1)', 'Number of Sims(V2)', 'Difference in Sims (V2-V1)','No of sims V1 ( partner targets)', 'No of sims V2 ( partner targets)', 'Difference in Partner Sims (V2-V1)',str(partner_names_mod[0]),str(partner_names_mod[1]),str(partner_names_mod[2]),str(partner_names_mod[3]),str(partner_names_mod[4]),'Test Equation in testdbv2 Flow' ]
                onerow = [suite_name + ' suite','Tgt1 (pick_any = pick_all)', 'Tgt1 (pick_any)', str(partner_names_mod[0]),str(partner_names_mod[1]),str(partner_names_mod[2]),str(partner_names_mod[3]),str(partner_names_mod[4])]
                #print(onerow) 
        if v1_report_only ==1:
                firstrow = [ 'Serial No', 'Test Name', ' Configs in V1','Number of Sims (V1)','No of sims V1 ( partner targets)' ]
        with open(filename, 'a') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(firstrow)
                        #writer.writerow(str(v1_config_count))
                        csvFile.close()
        with open(filename1, 'a') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(onerow)
                        #writer.writerow(str(v1_config_count))
                        csvFile.close()
        m=len(target_list_v1)
        n=len(target_list_v2)
        
        #go to V1 path and get the configs and config count for a particular test. Put it in list
        x = len(my_test_list)
        number_of_tests = len(common_test_list)
        
        vpx_config_count =[]
        V1_configs_test=[]
        V1_config_count=0
        for i in range(x):
                lst=[]
                lst2=[]
                lst3=[]
                lst4=[]
                os.chdir(test_list_path)
                my_test_name = my_test_list[i]
                grep_equation= "grep -irw " +str(my_test_name)+""" source_config_map_v2 | sed 's/,//' | cut -d\  -f2- | sed 's/  //g'"""
                test_equation = os.popen(grep_equation).readlines()
                test_eq= "".join(test_equation)
                for j in range(m):
                        #print(j)
                        st=''
                        #print(target_list_v1[j])
                        st= work_dir_v1 + ''.join(target_list_v1[j])
                        #print(st)
                        os.chdir(st)
                        v1_count_command = "wc -l "+suite_name+"_v1.list | awk '{print $1}'"
                        v1_picked_tests_command = "cat "+suite_name+"_v1.list | cut -d ',' -f3 | sort -u | wc -l"
                        #print(v1_count_command)
                        sort_v1_command= "sort -o "+suite_name+"_v1.list "+suite_name+"_v1.list"
                        #print(sort_v1_command)
                        sort_v1_list = os.system(sort_v1_command)
                        test_name = my_test_list[i]
                        #print("test name is" + test_name)
                        command= """ grep -irw """+ str(test_name)+ " "+suite_name+"""_v1.list | awk -F "," '{print $2}' """
                        if j==0:
                               v1_configs = os.popen(command).readlines()
                               v1_configs[:] = [line.rstrip('\n') for line in v1_configs]
                               v1_config_count = len(v1_configs)
                               v1_configs_test= "\n".join(v1_configs)
                               V1_configs_test= v1_configs_test
                               V1_config_count=v1_config_count
                               main_target_count_v1 = os.popen(v1_count_command).readlines()
                               main_target_count_v1[:]= [line.rstrip('\n') for line in main_target_count_v1]
                               main_target_count_v1x = main_target_count_v1[0]
                               #print("sim count 0f main target is " + str(main_target_count_v1x))
                               main_target_v1_picked = os.popen(v1_picked_tests_command).readlines()
                               main_target_v1_picked[:]= [line.rstrip('\n') for line in main_target_v1_picked]
                               main_target_v1_pickedx = main_target_v1_picked[0]
                               #print("number of tests picked in V1 is "+ str(main_target_v1_pickedx))
                               #print(V1_config_count)
                               #print('\n')
                        if j>0 and j< m:
                               vx_configs = os.popen(command).readlines()
                               vx_configs[:] = [line.rstrip('\n') for line in vx_configs]
                               vx_config_count = len(vx_configs)
                               vx_configs_test= "\n".join(vx_configs)
                               config_count_partner_v1 = [str((target_list_v1[j]).split('_')[0])+ " = " +str(vx_config_count)]
                               config_diff_list = [str(vx_config_count)]
                                
                               if j==1:
                                        lst.append(config_count_partner_v1)
                                        lst3.append(config_diff_list)
                                        first_sim_count_v1 = os.popen(v1_count_command).readlines()
                                        first_sim_count_v1[:]= [line.rstrip('\n') for line in first_sim_count_v1]
                                        first_sim_count_v1x = first_sim_count_v1[0]
                                        first_target_v1_picked = os.popen(v1_picked_tests_command).readlines()
                                        first_target_v1_picked[:]= [line.rstrip('\n') for line in first_target_v1_picked]
                                        first_target_v1_pickedx = first_target_v1_picked[0]

                               if j==2:
                                        lst.append(config_count_partner_v1)
                                        lst3.append(config_diff_list)
                                        second_sim_count_v1 = os.popen(v1_count_command).readlines()
                                        second_sim_count_v1[:]= [line.rstrip('\n') for line in second_sim_count_v1]
                                        second_sim_count_v1x = second_sim_count_v1[0]
                                        second_target_v1_picked = os.popen(v1_picked_tests_command).readlines()
                                        second_target_v1_picked[:]= [line.rstrip('\n') for line in second_target_v1_picked]
                                        second_target_v1_pickedx = second_target_v1_picked[0]
                               if j==3:
                                        lst.append(config_count_partner_v1)
                                        lst3.append(config_diff_list)
                                        third_sim_count_v1 = os.popen(v1_count_command).readlines()
                                        third_sim_count_v1[:]= [line.rstrip('\n') for line in third_sim_count_v1]
                                        third_sim_count_v1x = third_sim_count_v1[0]
                                        third_target_v1_picked = os.popen(v1_picked_tests_command).readlines()
                                        third_target_v1_picked[:]= [line.rstrip('\n') for line in third_target_v1_picked]
                                        third_target_v1_pickedx = third_target_v1_picked[0]
                               if j==4:
                                        lst.append(config_count_partner_v1)
                                        lst3.append(config_diff_list)
                                        fourth_sim_count_v1 = os.popen(v1_count_command).readlines()
                                        fourth_sim_count_v1[:]= [line.rstrip('\n') for line in fourth_sim_count_v1]
                                        fourth_sim_count_v1x = fourth_sim_count_v1[0]
                                        fourth_target_v1_picked = os.popen(v1_picked_tests_command).readlines()
                                        fourth_target_v1_picked[:]= [line.rstrip('\n') for line in fourth_target_v1_picked]
                                        fourth_target_v1_pickedx = fourth_target_v1_picked[0]
                               if j==5:
                                        lst.append(config_count_partner_v1)
                                        lst3.append(config_diff_list)
                                        fifth_sim_count_v1 = os.popen(v1_count_command).readlines()
                                        fifth_sim_count_v1[:]= [line.rstrip('\n') for line in fifth_sim_count_v1]
                                        fifth_sim_count_v1x = fifth_sim_count_v1[0]
                                        fifth_target_v1_picked = os.popen(v1_picked_tests_command).readlines()
                                        fifth_target_v1_picked[:]= [line.rstrip('\n') for line in fifth_target_v1_picked]
                                        fifth_target_v1_pickedx = fifth_target_v1_picked[0]
                #print(str(lst[3][0]))
                if m-1==5:        
                        partners = partner_names_mod[0]+'  '+str(lst[0][0]) +'\n'+ partner_names_mod[1]+'  ' + str(lst[1][0]) +'\n'+ partner_names_mod[2]+'  ' + str(lst[2][0])+'\n'+ partner_names_mod[3]+'  ' + str(lst[3][0])+' \n'+ partner_names_mod[4]+'  ' + str(lst[4][0]) 
                if m-1==4:
                        partners = partner_names_mod[0]+'  ' +str(lst[0][0]) +'\n'+ partner_names_mod[1]+'  ' + str(lst[1][0]) +'\n'+ partner_names_mod[2]+'  ' + str(lst[2][0])+'\n'+ partner_names_mod[3]+'  ' + str(lst[3][0])
                if m-1==3:
                        partners = partner_names_mod[0]+'  ' +str(lst[0][0]) +'\n'+ partner_names_mod[1]+'  ' + str(lst[1][0]) +'\n'+ partner_names_mod[2]+'  ' + str(lst[2][0])
                if m-1==2:
                        partners = partner_names_mod[0]+'  ' +str(lst[0][0]) +'\n'+ partner_names_mod[1]+'  ' + str(lst[1][0])
                if m-1==1:
                        partners = partner_names_mod[0]+'  ' +str(lst[0][0])
        
                #print(partners)
                for k in range(n):
                        st1=''
                        st1 = work_dir_v2 + ''.join(target_list_v2[k])
                        os.chdir(st1)
                        v2_count_command = "wc -l "+suite_name+"_v2.list | awk '{print $1}'"
                        v2_count_command_all = "wc -l "+suite_name+"_v2_pick_all.list | awk '{print $1}'"
                        v2_picked_tests_command = "cat "+suite_name+"_v2.list | cut -d ',' -f3 | sort -u | wc -l"
                        #print(v2_count_command)
                        sort_v2_command= "sort -o "+suite_name+"_v2.list "+suite_name+"_v2.list"
                        #print(sort_v2_command)
                        sort_v2_list= os.system(sort_v2_command)
                        test_name = my_test_list[i]
                        #print("test name is" + test_name)
                        command= """ grep -irw """+ str(test_name)+ " "+suite_name+"""_v2.list | awk -F "," '{print $2}' """
                        command_all= """ grep -irw """+ str(test_name)+ " "+suite_name+"""_v2_pick_all.list | awk -F "," '{print $2}' """
                        #print(command)
                        if k==0:
                               v2_configs = os.popen(command).readlines()
                               v2_configs[:] = [line.rstrip('\n') for line in v2_configs]
                               v2_config_count = len(v2_configs)
                               v2_configs_test= "\n".join(v2_configs)
                               V2_configs_test= v2_configs_test
                               V2_config_count= v2_config_count

                               v2_configs_all = os.popen(command_all).readlines()
                               v2_configs_all[:] = [line.rstrip('\n') for line in v2_configs_all]
                               v2_config_count_all = len(v2_configs_all)
                               v2_configs_test_all= "\n".join(v2_configs_all)
                               V2_configs_test_all= v2_configs_test_all
                               #V2_config_count_all= v2_config_count_all




                               main_target_count_v2 = os.popen(v2_count_command).readlines()
                               main_target_count_v2[:]= [line.rstrip('\n') for line in main_target_count_v2]
                               main_target_count_v2x = main_target_count_v2[0]
                               main_target_count_v2_all = os.popen(v2_count_command_all).readlines()
                               main_target_count_v2_all[:]= [line.rstrip('\n') for line in main_target_count_v2_all]
                               main_target_count_v2x_all = main_target_count_v2_all[0]

                               main_target_v2_picked = os.popen(v2_picked_tests_command).readlines()
                               main_target_v2_picked[:]= [line.rstrip('\n') for line in main_target_v2_picked]
                               main_target_v2_pickedx = main_target_v2_picked[0]
                               #print("number of tests picked in V1 is "+ str(main_target_v1_pickedx))
                               #print(v2_configs)
                               #print('\n')
                        if k>0 and k< n:
                               v2x_configs = os.popen(command).readlines()
                               v2x_configs[:] = [line.rstrip('\n') for line in v2x_configs]
                               v2x_config_count = len(v2x_configs)
                               v2x_configs_test= "\n".join(v2x_configs)
                               v2px_config_count=v2x_config_count
                               config_count_partner_v2 = [str((target_list_v2[k]).split('_')[0])+ " = " +str(v2x_config_count)]
                               mylst = list(zip(*lst3))
                               mylist = list(mylst[0])
                               #print(mylist[k-1])
                               partner_diff = v2x_config_count- int(mylist[k-1])
                               #print(partner_diff)
                               config_count_diff_partner = [str((target_list_v2[k]).split('_')[0])+ " = " +str(partner_diff)]
                               #print(config_count_diff_partner)
                               if k==1:
                                        lst2.append(config_count_partner_v2)
                                        lst4.append(config_count_diff_partner)
                                        partner_1_diff= str(partner_diff)
                                        first_sim_count_v2 = os.popen(v2_count_command).readlines()
                                        first_sim_count_v2[:]= [line.rstrip('\n') for line in first_sim_count_v2]
                                        first_sim_count_v2x = first_sim_count_v2[0]
                                        first_target_v2_picked = os.popen(v2_picked_tests_command).readlines()
                                        first_target_v2_picked[:]= [line.rstrip('\n') for line in first_target_v2_picked]
                                        first_target_v2_pickedx = first_target_v2_picked[0]
                               if k==2:
                                        lst2.append(config_count_partner_v2)
                                        lst4.append(config_count_diff_partner)
                                        partner_2_diff= str(partner_diff)
                                        second_sim_count_v2 = os.popen(v2_count_command).readlines()
                                        second_sim_count_v2[:]= [line.rstrip('\n') for line in second_sim_count_v2]
                                        second_sim_count_v2x = second_sim_count_v2[0]
                                        second_target_v2_picked = os.popen(v2_picked_tests_command).readlines()
                                        second_target_v2_picked[:]= [line.rstrip('\n') for line in second_target_v2_picked]
                                        second_target_v2_pickedx = second_target_v2_picked[0]
                               if k==3:
                                        lst2.append(config_count_partner_v2)
                                        lst4.append(config_count_diff_partner)
                                        partner_3_diff= str(partner_diff)
                                        third_sim_count_v2 = os.popen(v2_count_command).readlines()
                                        third_sim_count_v2[:]= [line.rstrip('\n') for line in third_sim_count_v2]
                                        third_sim_count_v2x = third_sim_count_v2[0]
                                        third_target_v2_picked = os.popen(v2_picked_tests_command).readlines()
                                        third_target_v2_picked[:]= [line.rstrip('\n') for line in third_target_v2_picked]
                                        third_target_v2_pickedx = third_target_v2_picked[0]
                               if k==4:
                                        lst2.append(config_count_partner_v2)
                                        lst4.append(config_count_diff_partner)
                                        partner_4_diff= str(partner_diff)
                                        fourth_sim_count_v2 = os.popen(v2_count_command).readlines()
                                        fourth_sim_count_v2[:]= [line.rstrip('\n') for line in fourth_sim_count_v2]
                                        fourth_sim_count_v2x = fourth_sim_count_v2[0]
                                        fourth_target_v2_picked = os.popen(v2_picked_tests_command).readlines()
                                        fourth_target_v2_picked[:]= [line.rstrip('\n') for line in fourth_target_v2_picked]
                                        fourth_target_v2_pickedx = fourth_target_v2_picked[0]
                               if k==5:
                                        lst2.append(config_count_partner_v2)
                                        lst4.append(config_count_diff_partner)
                                        partner_5_diff= str(partner_diff)
                                        fifth_sim_count_v2 = os.popen(v2_count_command).readlines()
                                        fifth_sim_count_v2[:]= [line.rstrip('\n') for line in fifth_sim_count_v2]
                                        fifth_sim_count_v2x = fifth_sim_count_v2[0]
                                        fifth_target_v2_picked = os.popen(v2_picked_tests_command).readlines()
                                        fifth_target_v2_picked[:]= [line.rstrip('\n') for line in fifth_target_v2_picked]
                                        fifth_target_v2_pickedx = fifth_target_v2_picked[0]
                
                if n-1==5: 
                        partners2 = partner_names_mod[0]+'  ' +str(lst2[0][0]) +'\n'+ partner_names_mod[1]+'  '+ str(lst2[1][0]) +'\n'+ partner_names_mod[2]+'  ' + str(lst2[2][0])+'\n'+ partner_names_mod[3]+'  '+ str(lst2[3][0])+'\n'+ partner_names_mod[4]+'  ' + str(lst2[4][0])        
                        partner_sim_diff = partner_names_mod[0]+'  ' +str(lst4[0][0]) +'\n'+ partner_names_mod[1]+'  ' + str(lst4[1][0]) +'\n'+ partner_names_mod[2]+'  ' + str(lst4[2][0])+'\n'+ partner_names_mod[3]+'  ' + str(lst4[3][0])+'\n'+ partner_names_mod[4]+'  ' + str(lst4[4][0])
                if n-1==4: 
                        partners2 = partner_names_mod[0]+'  ' +str(lst2[0][0]) +'\n'+ partner_names_mod[1]+'  '+ str(lst2[1][0]) +'\n'+ partner_names_mod[2]+'  ' + str(lst2[2][0])+'\n'+ partner_names_mod[3]+'  '+ str(lst2[3][0])    
                        partner_sim_diff = partner_names_mod[0] +'  '+str(lst4[0][0]) +'\n'+ partner_names_mod[1]+'  ' + str(lst4[1][0]) +'\n'+ partner_names_mod[2]+'  ' + str(lst4[2][0])+'\n'+ partner_names_mod[3]+'  ' + str(lst4[3][0])
                if n-1==3: 
                        partners2 = partner_names_mod[0]+'  ' +str(lst2[0][0]) +'\n'+ partner_names_mod[1]+'  '+ str(lst2[1][0]) +'\n'+ partner_names_mod[2]+'  ' + str(lst2[2][0])        
                        partner_sim_diff = partner_names_mod[0]+'  ' +str(lst4[0][0]) +'\n'+ partner_names_mod[1]+'  ' + str(lst4[1][0]) +'\n'+ partner_names_mod[2]+'  ' + str(lst4[2][0])
                if n-1==2: 
                        partners2 = partner_names_mod[0]+'  ' +str(lst2[0][0]) +'\n'+ partner_names_mod[1]+'  '+ str(lst2[1][0])         
                        partner_sim_diff = partner_names_mod[0]+'  ' +str(lst4[0][0]) +'\n'+ partner_names_mod[1]+'  ' + str(lst4[1][0]) 
                if n-1==1: 
                        partners2 = partner_names_mod[0]+'  ' +str(lst2[0][0])         
                        partner_sim_diff = partner_names_mod[0]+'  ' +str(lst4[0][0]) 
                            
                
                #print(partner_sim_diff)
                sim_diff = V2_config_count - V1_config_count
                v1_v2_row = [i+1,test_name, V1_configs_test ,V2_configs_test_all, V2_configs_test ,V1_config_count, V2_config_count, sim_diff,  partners, partners2, partner_sim_diff,partner_1_diff,partner_2_diff, partner_3_diff,partner_4_diff,partner_5_diff,test_eq ]
                #print(v1_v2_row)
                v1_row = [i+1,test_name, V1_configs_test ,V1_config_count,  partners ]
                os.chdir(cwd)
                with open(filename, 'a') as csvFile:
                        
                        if v1_report_only==0:
                                writer = csv.writer(csvFile)
                                writer.writerow(v1_v2_row)
                        elif v1_report_only ==1:
                                writer = csv.writer(csvFile)
                                writer.writerow(v1_row)
                        #writer.writerow(str(v1_config_count))
                                csvFile.close()
        #print("value of i is" + str(i))
        if i==x-1:
                main_target_reduction = (1-(weird_division(int(main_target_count_v2x),int(main_target_count_v1x))))*100
                main_target_reduction = round(main_target_reduction,2)
                #print(main_target_reduction)

                first_target_reduction = (1-(weird_division(int(first_sim_count_v2x),int(first_sim_count_v1x))))*100
                first_target_reduction = round(first_target_reduction,2)

                second_target_reduction = (1-(weird_division(int(second_sim_count_v2x),int(second_sim_count_v1x))))*100
                second_target_reduction = round(second_target_reduction,2)

                third_target_reduction = (1-(weird_division(int(third_sim_count_v2x),int(third_sim_count_v1x))))*100
                third_target_reduction = round(third_target_reduction,2)

                fourth_target_reduction = (1-(weird_division(int(fourth_sim_count_v2x),int(fourth_sim_count_v1x))))*100
                fourth_target_reduction = round(fourth_target_reduction,2)

                fifth_target_reduction = (1-(weird_division(int(fifth_sim_count_v2x),int(fifth_sim_count_v1x))))*100
                fifth_target_reduction = round(fifth_target_reduction,2)

                v1_count_row = ['V1 Count', main_target_count_v1x, main_target_count_v1x, first_sim_count_v1x,second_sim_count_v1x, third_sim_count_v1x,fourth_sim_count_v1x, fifth_sim_count_v1x]
                v2_count_row = ['V2 Count', main_target_count_v2x_all, main_target_count_v2x, first_sim_count_v2x,second_sim_count_v2x, third_sim_count_v2x,fourth_sim_count_v2x, fifth_sim_count_v2x] 
                expected_reduction= ['Original Reduction Estimation(%)','NA','NA','NA','NA','NA','NA','NA']
                actual_reduction =['Actual Reduction(%)','',main_target_reduction, first_target_reduction,second_target_reduction,third_target_reduction,fourth_target_reduction,fifth_target_reduction ]

                total_number_of_tests = ['Total Number of tests',number_of_tests,number_of_tests,number_of_tests,number_of_tests,number_of_tests,number_of_tests,number_of_tests]
                v1_tests_picked = ['Tests Picked in V1',main_target_v1_pickedx, main_target_v1_pickedx,first_target_v1_pickedx,second_target_v1_pickedx,third_target_v1_pickedx,fourth_target_v1_pickedx,fifth_target_v1_pickedx ]

                v2_tests_picked = ['Tests Picked in V2',main_target_v2_pickedx, main_target_v2_pickedx,first_target_v2_pickedx,second_target_v2_pickedx,third_target_v2_pickedx,fourth_target_v2_pickedx,fifth_target_v2_pickedx ]

                empty_row= ['','','','','','','','']
                #print(scr_mod)
                scr_row = '\n'.join(scr_mod)
                scr1_row = [scr_row]
                #print(scr_row)
                #scr_mod_row = print('\n'.join(scr_row))
                #print(scr_mod_row)
                with open(filename1, 'a') as csvFile:
                        
                        if v1_report_only==0:
                                writer = csv.writer(csvFile)
                                writer.writerow(v1_count_row)
                                writer.writerow(v2_count_row)
                                writer.writerow(expected_reduction)
                                writer.writerow(actual_reduction)
                                writer.writerow(total_number_of_tests)
                                writer.writerow(v1_tests_picked)
                                writer.writerow(v2_tests_picked)
                                writer.writerow(empty_row)
                                writer.writerow(empty_row)
                                writer.writerow(scr1_row)
                                
                        elif v1_report_only ==1:
                                writer = csv.writer(csvFile)
                                writer.writerow(v1_row)
                        #writer.writerow(str(v1_config_count))
                                csvFile.close()
                
                
                # if we read f.csv we will write f.xlsx
                
                ws = wb.add_worksheet(filename)    # your worksheet title here
                with open(filename,'r') as csvfile:
                        table = csv.reader(csvfile)
                        increment = 0
                # write each row from the csv file as text into the excel file
                # this may be adjusted to use 'excel types' explicitly (see xlsxwriter doc)
                        for row in table:
                            ws.write_row(increment, 0, row)
                            increment += 1

                ws = wb.add_worksheet(filename1)    # your worksheet title here
                with open(filename1,'r') as csvfile:
                        table = csv.reader(csvfile)
                        increment = 0
                # write each row from the csv file as text into the excel file
                # this may be adjusted to use 'excel types' explicitly (see xlsxwriter doc)
                        for row in table:
                            ws.write_row(increment, 0, row)
                            increment += 1
                report_cmd = "rm -rf "+filename
                os.system(report_cmd)
                scr_report_cmd = "rm -rf "+filename1
                os.system(scr_report_cmd)
                
wb.close()

