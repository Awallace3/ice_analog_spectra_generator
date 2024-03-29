import numpy as np
import os
import math
import random
from numpy import genfromtxt
import numpy as npimport
from numpy import genfromtxt
import pandas as pd
# import re
import glob
import subprocess
import check_status


def combine_calcs(num_calcs):
    calc_names = []
    if not os.path.exists('../calc_zone'):
        os.mkdir('../calc_zone')
    for i in range(num_calcs):
        calc_names.append('calc_zone%d' % (i+1))
    print(os.getcwd())
    os.chdir("..")
    cnt = 1
    for i in calc_names:
        os.chdir(i)
        directories = glob.glob("geom*")
        for i in directories:
            cmd = "cp -r %s ../calc_zone/geom%d" % (i, cnt)
            subprocess.call(cmd, shell=True)
            cnt += 1
        os.chdir("..")

def combine_calcs_no_errors(calc_names, mexc_check='mexc'):
    if not os.path.exists('../calc_zone'):
        os.mkdir('../calc_zone')
    os.chdir("..")
    cnt = 1
    #print(calc_names)
    for i in calc_names:
        os.chdir(i)
        del_lst, keep_lst = check_status.find_error_mexc('.', mexc_check)
        print(keep_lst)
        for i in keep_lst:
            cmd = "cp -r %s ../calc_zone/geom%d" % (i, cnt)
            subprocess.call(cmd, shell=True)
            print(cmd)
            cnt += 1
        os.chdir("..")

def delete_nested_geoms(path):
    os.chdir(path)
    directories = glob.glob("geom*")
    for i in directories:
        os.chdir(i)
        dup = glob.glob("geom*")
        if len(dup) > 0:
            #os.chdir(dup[0])
            print(os.getcwd())
            print(dup[0])
            cmd = 'rm -r %s' % dup[0]
            subprocess.call(cmd, shell=True)
            #os.chdir("..")
        os.chdir("..")
def main():
    #combine_calcs(1)
    #delete_nested_geoms('../calc_zone1')
    calc_names = ['og_calc_zone']
    mexc_check = 'cam-b3lyp_n50'
    mexc_check = 'cam-b3lyp'
    combine_calcs_no_errors(calc_names, mexc_check)

main()
