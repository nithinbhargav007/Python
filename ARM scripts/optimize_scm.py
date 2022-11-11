
####################################################################################
# This will format the scm file automatically 
# Example Cmd : 
#                 python optimize_scm.py /arm/projectscratch/pd/shatranj/users/amijan01/v8a/validation/ARCH64/MEM/V8MP/tests/source_config_map
#
#  Output : optimized_scm file will be generated in the same directory

####################################################################################
import sys

scm_path = sys.argv[1]  # full path of input scm file 

scm = open(scm_path , 'r')

optimized_scm = open('optimized_scm','w')
scm_lines = scm.readlines();
print(scm_lines[1])

for line in scm_lines:
    if line.startswith('v8core_ip'):
        test_name = line.split(",",2)[0]
        test_name = test_name.strip()
        scm_eq    = line.split(",",2)[1]
        scm_eq = scm_eq.strip()
        scfg =    line.split(",",2)[2]
        scfg = scfg.strip()
        space = ' '

        #print(str(scm_eq[1]))
        optimized_scm.write(test_name + '                       ,'+ ( (70-len(test_name)) *space) + ((200 - len(scm_eq) -70 ) *space) + ','  + scfg + '\n')
   # else:
   #     optimized_scm.write(line)

    

