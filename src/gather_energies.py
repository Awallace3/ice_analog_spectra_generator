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
                start = "HF="
                # end = '\RMSD='
                # a = re.search(r'\b(HF=)\b', line)
                index = line.index(start)

                HFs.append(line[index:])

            if zero_point in line:
                zeros.append(line)

    # print(zeros[0])
    if len(HFs) == 1:
        return freqs[0], HFs[0], 0, zeros[0]
    else:
        return freqs[0], HFs[0], HFs[1], zeros[0]


# testing
def clean_energies(hf_1, hf_2, zero_point):
    zero_point = zero_point[30:].replace(" (Hartree/Particle)", "")
    for i in range(10):
        zero_point = zero_point.replace("  ", " ")
    zero_point = float(zero_point)
    hf_1 = hf_1[3:].replace("\n", "").split("\\")

    if hf_2 != 0:
        hf_2 = hf_2[3:].replace("\n", "").split("\\")
        # print(hf_1[0], hf_2[0])
        if hf_1[0] > hf_2[0]:
            # -2119.1981428
            # if hf_1[0] < hf_2[0]:
            # -2119.1981419999997
            return float(hf_1[0]) + zero_point, hf_1[0]
        else:
            return float(hf_2[0]) + zero_point, hf_2[0]
    else:
        return float(hf_1[0]) + zero_point, hf_1[0]


def main():
    # print("Gathering Energies")
    location = os.getcwd().split("/")[-1]
    if location == "src":
        os.chdir("../calc_zone")
    elif location == "calc_zone":
        pass
    else:
        os.chdir("calc_zone")

    if not os.path.exists("../results/energies"):
        os.mkdir("../results/energies")

    directories = glob.glob("geom*")
    # print(os.getcwd())
    lowest_energy = [0, 0, 0]
    cmd = "rm ../results/energies/energy_all.csv"
    subprocess.call(cmd, shell=True)
    for i in directories:
        n = i[4:]
        # print(i)
        # print(i[5:])
        os.chdir(i)
        out_files = glob.glob("*.out*")
        out_completion = glob.glob("mex_o.*")
        # print(out_files)
        # print(out_completion)
        if len(out_files) > 0:
            if len(out_files) == 1:
                filename = out_files[-1]
            else:
                filename = "0"
                for i in out_files:
                    if i[-1] == "t":
                        continue
                    elif i[-1] > filename[-1]:
                        filename = i

            # print("filename:", filename)

            f = open(filename, "r")
            lines = f.readlines()
            f.close()

            freq, hf_1, hf_2, zero_point = freq_hf_zero(lines, filename=filename)
            # print(freq, hf_1, hf_2, zero_point)
            sum_energy, hf = clean_energies(hf_1, hf_2, zero_point)
            if sum_energy < lowest_energy[2]:
                lowest_energy = [hf, zero_point, sum_energy]

            # print("Sum Energy:",sum_energy)
            # os.chdir("../results/energies")
            path = "../../results/energies/"
            # print(os.getcwd())
            f = open(path + "energy%s.txt" % n, "w")
            f.write(str(sum_energy))
            # print(sum_energy)
            f.close()
            line = "%s,%s\n" % (n, sum_energy)
            f = open(path + "energy_all.csv", "a")
            f.write(line)
            f.close()

            os.chdir("..")

    os.chdir("..")
    # print("LOWEST ENERGY\nHF\tZPE\tSUM")
    # print(lowest_energy)


# main()
