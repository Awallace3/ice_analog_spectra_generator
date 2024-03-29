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


def rm_mexc(method_mexc,
            basis_set_mexc,
            nStates,
            SCRF='',
            spectroscopy_type='mexc',
            path="./data/40_co3h2"
            ):
    """
    if method_mexc == 'PBE0':
        path_mexc = 'pbe0'
    elif method_mexc == 'wB97XD':
        path_mexc = 'wb97xd'
    elif method_mexc == 'B3LYP':
        path_mexc = 'mexc'
    else:
        print("This method is not supported for TD-DFT yet.")
    """

    if spectroscopy_type == 'mexc':
        if basis_set_mexc == '6-311G(d,p)':
            basis_dir_name = ''
        else:
            basis_dir_name = '_' + basis_set_mexc
    elif spectroscopy_type == 'vib':
        basis_dir_name = '_vib'
        if basis_set_mexc == '6-311G(d,p)':
            pass
        else:
            basis_dir_name += '_' + basis_set_mexc

    if nStates == '25':
        pass
    else:
        basis_dir_name += '_n%s' % nStates
    if SCRF != '':
        basis_dir_name += '_SCRF_%s' % SCRF

    if method_mexc == 'B3LYP':
        path_mexc = 'mexc' + basis_dir_name
    else:
        path_mexc = method_mexc.lower() + basis_dir_name
        #path_mexc = path_mexc.replace("(", "\(").replace(")", "\)")

    # location = os.getcwd().split('/')[-1]
    # if location == 'src':
    #     os.chdir("../calc_zone")
    # elif location == 'calc_zone':
    #     pass
    # else:
    #     os.chdir("calc_zone")
    os.chdir(path)

    directories = glob.glob("geom*")
    cmd = 'rm -r "%s"' % path_mexc
    for i in directories:
        os.chdir(i)
        print('Removing %s from %s' % (path_mexc, i))
        subprocess.call(cmd, shell=True)
        os.chdir("..")

    os.chdir("..")


# DELETES PERMANENTLY:::USE FOR SPECIAL CASES


def main():
    # method_mexc = "b3lyp"
    method_mexc = "B3LYP"
    #method_mexc = "pbe0"
    #method_mexc = "wb97xd"
    # method_mexc = "cam-b3lyp"
    #method_mexc = "b3lypd3"
    #method_mexc = 'b97d3'

    basis_set_mexc = '6-311++G(2d,2p)'
    basis_set_mexc = '6-311G(d,p)'
    # basis_set_mexc = 'aug-cc-pVDZ'

    # nStates = '25'
    nStates = '50'
    #nStates = '150'
    #nStates = '125'

    SCRF = ''
    #SCRF='PCM'

    # rm_mexc(method_mexc,
    #         basis_set_mexc,
    #         nStates,
    #         SCRF=SCRF,
    #         spectroscopy_type='vib')
    rm_mexc(method_mexc,
            basis_set_mexc,
            nStates,
            SCRF=SCRF,
            spectroscopy_type='mexc')


main()
#if __name__ == "__main__":
#    main()
