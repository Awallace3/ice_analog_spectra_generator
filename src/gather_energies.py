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



def freq_hf_zero(lines, filename):
    frequency = "Frequencies --"
    freqs = []
    HF = "HF="
    HFs = []
    zero_point = " Zero-point correction="
    zeros = []

    with open(filename) as search:
        for num, line in enumerate(search, 1):

            if frequency in line:
                freqs.append(line)

            if HF in line:
                start = 'HF='
                # end = '\RMSD='
                # a = re.search(r'\b(HF=)\b', line)
                index = line.index(start)

                HFs.append(line[index:])

            if zero_point in line:
                zeros.append(line)
    print(zeros[0])
    if len(HFs) == 1:
        return freqs[0], HFs[0], 0, zeros[0]
    else:
        return freqs[0], HFs[0], HFs[1], zeros[0]
    

def clean_energies(hf_1, hf_2, zero_point):
    zero_point = zero_point[30:].replace(" (Hartree/Particle)", "")
    for i in range(10):
        zero_point = zero_point.replace("  ", " ")
    zero_point = float(zero_point)
    hf_1 = (hf_1[3:].replace("\n", "").split('\\'))

    if hf_2 != 0:
        hf_2 = (hf_2[3:].replace("\n", "").split('\\'))
        # print(hf_1[0], hf_2[0])

        if hf_1[0] > hf_2[0]:
            return float(hf_1[0]) + zero_point
        else:
            return float(hf_2[0]) + zero_point
    else:
        return float(hf_1[0]) + zero_point

def main():
    os.chdir("../calc_zone")

    directories = glob.glob("geom*")
    for i in directories:
        print(i)
        os.chdir(i)
        out_files = glob.glob("*.out*")
        out_completion = glob.glob("mex_o.*")
        #print(out_files)
        #print(out_completion)
        if len(out_files) > 0:
            if len(out_files) == 1:
                filename = out_files[-1]
            else:
                filename = '0'
                for i in out_files:
                    if i[-1] == 't':
                        continue
                    elif i[-1] > filename[-1]:
                        filename = i

            print("filename:", filename)
            
            f = open(filename, 'r')
            lines = f.readlines()
            f.close()

            freq, hf_1, hf_2, zero_point = freq_hf_zero(
                lines, filename=filename)
            print(freq, hf_1, hf_2, zero_point)
            sum_energy = clean_energies(hf_1, hf_2, zero_point)
            print("Sum Energy:",sum_energy)
            os.chdir("..")

main()