import numpy as np
import os
# import re
import glob
import subprocess

def check_status(path_calc_zone):
    os.chdir(path_calc_zone)
    geom_dirs = glob.glob("geom*")
    del_lst = []
    keep_lst = []
    for i in geom_dirs:
        os.chdir(i)
        local_files = glob.glob("*")
        mexc = glob.glob("mexc")
        print(i)
        print("\tlocal files number:", len(local_files) )
        if len(mexc) < 1:
            del_lst.append(i)
        else:
            os.chdir('mexc')
            mexc_outs = glob.glob("mexc.o*")
            mexc_completes = glob.glob("mexc_o.o*")
            print("\tmexc:", len(mexc_outs))
            if len(mexc_outs) > 0 and len(mexc_completes) > 0:
                keep_lst.append(i)
            else:
                del_lst.append(i)
            os.chdir("..")

        os.chdir('..')
    print("Keep:\n", keep_lst, '\nlen:', len(keep_lst))
    print("\nDelete:", del_lst)

def find_error_mexc(path_calc_zone, base_dir_name='mexc'):
    os.chdir(path_calc_zone)
    geom_dirs = glob.glob("geom*")
    del_lst = []
    keep_lst = []
    for i in geom_dirs:
        os.chdir(i)
        local_files = glob.glob("*")
        mexc = glob.glob("mexc")
        print(i)
        print("\tlocal files number:", len(local_files) )
        if len(mexc) < 1:
            del_lst.append(i)
        else:
            if os.path.exists(base_dir_name):
                #print(base_dir_name)
                os.chdir(base_dir_name)
                mexc_outs = glob.glob("mexc.o*")
                mexc_completes = glob.glob("mexc_o.o*")
                print("\tmexc:", len(mexc_outs))
                if len(mexc_outs) > 0 and len(mexc_completes) > 0:
                    with open("mexc.out", 'r') as fp:
                        data = fp.read()
                    with open("mexc.out", 'r') as fp:
                        lines = fp.readlines()
                    #print(lines)
                    if 'Error' in data or len(lines) < 470:
                        del_lst.append(i)
                    elif "Normal termination of Gaussian" in data:
                        keep_lst.append(i)
                    else:
                        del_lst.append(i)
                    
                os.chdir("..")
            else:
                print(i, "does not have base_dir_name given")
                del_lst.append(i)
        os.chdir('..')
    print("Keep:\n", keep_lst, '\nlen:', len(keep_lst))
    print("\nDelete:", del_lst, '\nlen:', len(del_lst))
    
    return del_lst, keep_lst

def resubmit_mem(jobs_lst, base_dir_name, inc=500):
   for i in jobs_lst:
        os.chdir("%s/%s" %(i,base_dir_name))
        with open('mexc.com', 'r') as fp:
            data = fp.readlines()
            mem = int(data[0][5:-3]) + inc
            print(mem)
            mem = "%"+'mem=%dmb\n' % mem
            data[0] = mem
        with open('mexc.com', 'w') as fp:
            for j in data:
                fp.write(j)
        with open('mexc.pbs', 'r') as fp:
            data = fp.readlines()
            pos = 0
            for n, j in enumerate(data):
                if '#PBS -l' in j and "mem=" in j:
                    pos = n
                    break
            mem = int(data[pos][-5:-3]) + inc*4/1000
            #print(mem)
            mem = '#PBS -l mem=%dgb\n' % mem
            data[pos] = mem
        with open('mexc.pbs', 'w') as fp:
            for j in data:
                fp.write(j)

        cmd = 'qsub mexc.pbs'
        subprocess.call(cmd, shell=True)
        os.chdir("../..")
def day_hour_minutes_seconds_to_seconds(time_lst):
    seconds = 0
    
    for n, i in enumerate(time_lst):
        i=float(i)
        if n==0:
            seconds += 24*60*60*i
        elif n==1:
            seconds += 60*60*i
        elif n==2:
            seconds += 60*i
        else:
            seconds += i
    return seconds

def check_times(base_dir_name):
    location = os.getcwd().split('/')[-1]
    if location == 'src':
        os.chdir("../calc_zone")
    elif location == 'calc_zone':
        pass
    else:
        os.chdir("calc_zone")
    geoms = glob.glob("geom*")
    times = []
    for i in geoms:
        os.chdir("%s/%s"%(i,base_dir_name))
        with open("mexc.out", 'r') as fp:
            data = fp.readlines()
            time_line = ''
        for n, j in enumerate(data):
            if 'Job cpu time:' in j:
                time_line = j
                break
        if len(time_line) > 5:
            time_line = time_line.replace("days", ":").replace("hours", ':').replace("minutes",":").replace("seconds",":")
            time_line = time_line.split(":")[1:-1]
            times.append(day_hour_minutes_seconds_to_seconds(time_line))
        os.chdir("../..")
    avg = sum(times) / len(times)
    print("\n%s took an average time of..." % (base_dir_name))
    print("seconds: %.2f\nhours: %.2f\n" % (avg, avg/60/60))
    return avg
            
def check_times_multi (base_dir_names):
    times = []
    for i in base_dir_names:
        times.append(check_times(i))
    return times
            

if __name__ == "__main__":
    
    path = '../calc_zone'
    #path = '../calc_zone1'
    #check_status(path)
    base_dir_name = 'cam-b3lyp_n50'
    base_dir_name = 'cam-b3lyp_6-311++G(2d,2p)_n125'
    base_dir_name = 'wb97xd_6-311++G(2d,2p)_n125'
    base_dir_names = ['cam-b3lyp_6-311++G(2d,2p)_n125', 'wb97xd_6-311++G(2d,2p)_n125', 'cam-b3lyp_6-311++G(2d,2p)', 'wb97xd_6-311++G(2d,2p)', 'cam-b3lyp', 'wb97xd'  ]
    #resubmit_lst = find_error_mexc(path, base_dir_name)
    #resubmit_mem(resubmit_lst, base_dir_name)
    #check_times(base_dir_name)
    check_times_multi(base_dir_names)
    #resubmit_lst, keep_lst = find_error_mexc(path, base_dir_name)
    #resubmit_mem(resubmit_lst, base_dir_name)
