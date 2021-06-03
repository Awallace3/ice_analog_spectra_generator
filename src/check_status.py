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

def find_error_mexc(path_calc_zone):
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
                with open("mexc.out", 'r') as fp:
                    data = fp.read()
                with open("mexc.out", 'r') as fp:
                    lines = fp.readlines()

                #print(lines)
                if 'Error' in data or len(lines) < 470:
                    del_lst.append(i)
                else:
                    keep_lst.append(i)
            os.chdir("..")
        os.chdir('..')
    print("Keep:\n", keep_lst, '\nlen:', len(keep_lst))
    print("\nDelete:", del_lst)

if __name__ == "__main__":
    path = '../calc_zone'
    path = '../calc_zone1'
    #check_status(path)
    find_error_mexc(path)