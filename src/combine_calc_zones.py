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
    combine_calcs(1)
    #delete_nested_geoms('../calc_zone1')
main()