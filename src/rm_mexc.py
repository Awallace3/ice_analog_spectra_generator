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

def rm_mexc(method_mexc):
    if method_mexc == 'PBE0':
        path_mexc = 'pbe0'
    elif method_mexc == 'wB97XD':
        path_mexc = 'wb97xd'
    elif method_mexc == 'B3LYP':
        path_mexc = 'mexc'
    else:
        print("This method is not supported for TD-DFT yet.")

    location = os.getcwd().split('/')[-1]
    if location == 'src':
        os.chdir("../calc_zone")
    elif location == 'calc_zone':
        pass
    else:
        os.chdir("calc_zone")

    directories = glob.glob("geom*")
    cmd = 'rm -r %s' % path_mexc
    for i in directories:
        os.chdir(i)
        print("Removing %s from %s" % (path_mexc, i))
        subprocess.call(cmd, shell=True)
        os.chdir("..")
        
    os.chdir("..")
# DELETES PERMANENTLY:::USE FOR SPECIAL CASES
def main():
    method_mexc = 'PBE0'
    rm_mexc(method_mexc)
main()