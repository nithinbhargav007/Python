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

suite_name = sys.argv[1]
work_dir_v1 = sys.argv[2]
work_dir_v2 = sys.argv[3]
main_target = sys.argv[4]
partner_target= sys.argv[5]
partner_names = sys.argv[6]

main_target = [main_target]
partner_target_mod = partner_target.split(",")
partner_names_mod= partner_names.split(",")
suite_names_mod = suite_name.split(",")
number_of_suites = len( suite_names_mod)
print(number_of_suites)
#print(partner_names_mod)
#print(partner_names_mod[1])
print(suite_names_mod)
target_list_v1 = main_target+partner_target_mod
target_list_v2 = main_target+partner_target_mod
#print(target_list_v1)
#print(target_list_v2)

num_arguments = len(sys.argv) - 1
#print(num_arguments)
#print(sys.argv)
#print( "number of arguments provided is" + str(num_arguments))

v1_report_only =0
if (num_arguments ==4):
    if(sys.argv[4] == 'v1_only'):
        v1_report_only=1


#-------------------------------------------------------------------------------------------------
cwd = os.getcwd()
#print(cwd)
test_list_path = "/arm/projectscratch/pd/shatranj/users/nitkum01/17jun_validation/validation/ARCH64/CORE/"+suite_names_mod[0]+"/tests/"
my_test_list = os.listdir(test_list_path)
from pprint import pprint
my_test_list.sort()
pprint(my_test_list)


suite_name_l = suite_name[0].lower()
suite_name_n = suite_name_l.split("_")[0] 
print(suite_name_n)
my_test_list = [x for x in my_test_list if x.startswith(suite_name_n)]  #filter the directory contents to get only list of tests
pprint(my_test_list)

#Create/empty the existing report file
os.chdir(cwd)
if v1_report_only ==0:
        filename = suite_names_mod[0] +"_report.xlsx"
        workbook = xlsxwriter.Workbook(filename)
elif v1_report_only==1:
        filename = suite_names_mod[0] +"v1_report.xlsx"
        workbook = xlsxwriter.Workbook(filename)
# opening the file with w+ mode truncates the file
worksheet = workbook.add_worksheet(suite_names_mod[0]+' report')  
#f = open(filename, "w+")
workbook.close()

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
        print(partner_names_mod[0])
        firstrow = [ 'Serial No', 'Test Name', ' Configs in V1', 'Configs in V2','Number of Sims (V1)', 'Number of Sims(V2)', 'Difference in Sims (V2-V1)','No of sims V1 ( partner targets)', 'No of sims V2 ( partner targets)', 'Difference in Partner Sims (V2-V1)',str(partner_names_mod[0]),str(partner_names_mod[1]),str(partner_names_mod[2]),str(partner_names_mod[3]),str(partner_names_mod[4]),'Test Equation in testdbv2 Flow' ]

if v1_report_only ==1:
        firstrow = [ 'Serial No', 'Test Name', ' Configs in V1','Number of Sims (V1)','No of sims V1 ( partner targets)' ]

worksheet.write(firstrow)
workbook.close()

#with open(filename, 'a') as csvFile:
#                writer = csv.writer(csvFile)
#                writer.writerow(firstrow)
#                #writer.writerow(str(v1_config_count))
#                csvFile.close()


#my_target_list_v1 = os.listdir(work_dir_v1)
#from pprint import pprint
#my_target_list_v1.sort()
#my_target_list_v1 = [x for x in my_target_list_v1 if x.startswith("tgt")]  #filter the directory contents to get only list of targets
#my_target_list_v1 = sorted_nicely(my_target_list_v1)
#pprint(my_target_list_v1)
#
#my_target_list_v2 = os.listdir(work_dir_v2)
#from pprint import pprint
#my_target_list_v2.sort()
#my_target_list_v2 = [y for y in my_target_list_v2 if y.startswith("tgt")]  #filter the directory contents to get only list of targets
#my_target_list_v2 = sorted_nicely(my_target_list_v2)
#pprint(my_target_list_v2)


m=len(target_list_v1)
n=len(target_list_v2)
print(target_list_v1)
#print(m,n)

#generate mklist for all targets in V1 work directory

#for i in range(m):
#          target_path_v1= work_dir_v1+my_target_list_v1[i]
#          #print(target_path_v1)
#          os.chdir(target_path_v1)
#          os.environ["VALIDATION_HOME"] = "/arm/projectscratch/pd/shatranj/users/nitkum01/17jun_validation/validation"
#          command_val_1 = "source /arm/projectscratch/pd/shatranj/users/nitkum01/17jun_validation/validation/dotcshrc" 
#          #print(command_val_1)
#          execute_val_1=os.system(command_val_1)
#          os.environ["AVKRUN_HOME"] = target_path_v1
#          #print(os.environ)
#          command_mklist_v1 = "val_report "+suite_name+" -nog -mklist " +suite_name+"_v1"
#          print(command_mklist_v1)
#          execute_v1_mklist=os.system(command_mklist_v1)
#
###generate mklist for all targets in V2 work directory
#
#for i in range(n):
#          target_path_v2= work_dir_v2+my_target_list_v2[i]
#          #print(target_path_v2)
#          os.chdir(target_path_v2)
#          os.environ["VALIDATION_HOME"] = "/arm/projectscratch/pd/shatranj/users/nitkum01/17jun_validation/validation"
#          command_val_2 = "source /arm/projectscratch/pd/shatranj/users/nitkum01/17jun_validation/validation/dotcshrc"
#          #print(command_val_2)
#          execute_val_2=os.system(command_val_2)
#          os.environ["AVKRUN_HOME"] = target_path_v2
#          command_mklist_v2 = "val_report "+suite_name+" -nog -mklist " +suite_name+"_v2"
#          #print(str(command_mklist_v2))
#          execute_v2_mklist=os.system(command_mklist_v2)


#go to V1 path and get the configs and config count for a particular test. Put it in list
x = len(my_test_list)
#print(x)

vpx_config_count =[]
V1_configs_test=[]
V1_config_count=0
for i in range(x):
        #getting the SCM equation
        lst=[]
        lst2=[]
        lst3=[]
        lst4=[]


        os.chdir(test_list_path)
        my_test_name = my_test_list[i]
        grep_equation= "grep -irw " +str(my_test_name)+""" source_config_map_v2 | sed 's/,//' | cut -d\  -f2- | sed 's/  //g'"""
        #print(grep_equation)
        test_equation = os.popen(grep_equation).readlines()
        #print("test_equation is" +  str(test_equation))
        test_eq= "".join(test_equation)
        for j in range(m):
                os.chdir(work_dir_v1+target_list_v1[j])
                sort_v1_command= "sort -o "+suite_names_mod[0]+"_v1.list "+suite_names_mod[0]+"_v1.list"
                print(sort_v1_command)
                sort_v1_list= os.system(sort_v1_command)
                test_name = my_test_list[i]
                #print("test name is" + test_name)
                command= """ grep -irw """+ str(test_name)+ " "+suite_names_mod[0]+"""_v1.list | awk -F "," '{print $2}' """
                if j==0:
                       v1_configs = os.popen(command).readlines()
                       v1_configs[:] = [line.rstrip('\n') for line in v1_configs]
                       v1_config_count = len(v1_configs)
                       v1_configs_test= "\n".join(v1_configs)
                       V1_configs_test= v1_configs_test
                       V1_config_count=v1_config_count
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
                       if j==2:
                                lst.append(config_count_partner_v1)
                                lst3.append(config_diff_list)
                       if j==3:
                                lst.append(config_count_partner_v1)
                                lst3.append(config_diff_list)
                       if j==4:
                                lst.append(config_count_partner_v1)
                                lst3.append(config_diff_list)
                       if j==5:
                                lst.append(config_count_partner_v1)
                                lst3.append(config_diff_list)
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
                os.chdir(work_dir_v2+target_list_v2[k])
                sort_v2_command= "sort -o "+suite_names_mod[0]+"_v2.list "+suite_names_mod[0]+"_v2.list"
                print(sort_v2_command)
                sort_v2_list= os.system(sort_v2_command)
                test_name = my_test_list[i]
                #print("test name is" + test_name)
                command= """ grep -irw """+ str(test_name)+ " "+suite_names_mod[0]+"""_v2.list | awk -F "," '{print $2}' """
                #print(command)
                if k==0:
                       v2_configs = os.popen(command).readlines()
                       v2_configs[:] = [line.rstrip('\n') for line in v2_configs]
                       v2_config_count = len(v2_configs)
                       v2_configs_test= "\n".join(v2_configs)
                       V2_configs_test= v2_configs_test
                       V2_config_count=v2_config_count
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
                       if k==2:
                                lst2.append(config_count_partner_v2)
                                lst4.append(config_count_diff_partner)
                                partner_2_diff= str(partner_diff)
                       if k==3:
                                lst2.append(config_count_partner_v2)
                                lst4.append(config_count_diff_partner)
                                partner_3_diff= str(partner_diff)
                       if k==4:
                                lst2.append(config_count_partner_v2)
                                lst4.append(config_count_diff_partner)
                                partner_4_diff= str(partner_diff)
                       if k==5:
                                lst2.append(config_count_partner_v2)
                                lst4.append(config_count_diff_partner)
                                partner_5_diff= str(partner_diff)
        
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
                    
        
        print(partner_sim_diff)
        sim_diff = V2_config_count - V1_config_count
        v1_v2_row = [i+1,test_name, V1_configs_test , V2_configs_test ,V1_config_count, V2_config_count, sim_diff,  partners, partners2, partner_sim_diff,partner_1_diff,partner_2_diff, partner_3_diff,partner_4_diff,partner_5_diff,test_eq ] 
        v1_row = [i+1,test_name, V1_configs_test ,V1_config_count,  partners ]
        
        
        
        #print(one_row)
        #print(tmp_v1)

        os.chdir(cwd)
        worksheet.write(v1_v2_row)
        workbook.close()
        #with open(filename, 'a') as csvFile:
        #        
        #        if v1_report_only==0:
        #                writer = csv.writer(csvFile)
        #                writer.writerow(v1_v2_row)
        #        elif v1_report_only ==1:
        #                writer = csv.writer(csvFile)
        #                writer.writerow(v1_row)
        #        #writer.writerow(str(v1_config_count))
        #                csvFile.close()
                

