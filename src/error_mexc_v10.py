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


def Convert(string):
    li = list(string.split(" "))
    return li

def cleanLine(line):
    aList = []
    cropped_line = line.rstrip()
    for i in range(2,10):
        k = ' ' * i
        cropped_line = cropped_line.replace(k, " ")
    cropped_line = cropped_line.split(" ")
    for i in cropped_line:
        if i == '':
            continue
        else: 
            aList.append(float(i))
    return aList



def conv_num(string):
    li = list(string.split(" "))
    return li


def clean_many_txt():
    """ This will replace the numerical forms of the elements as their letters numbered in order """

    f = open('tmp.txt', 'r')
    a = ['6.0 ', '8.0 ', '1.0 ', '7.0 ']
    table = {
        '6.0 ': 'C', '8.0 ': 'O', '1.0 ': 'H', '7.0 ': 'N'
    }

    lst = []
    cnt2 = 0
    for line in f:
        cnt2 += 1
        for word in a:
            if word in line:
                convert_wrd = table[word]
                line = line.replace(word, convert_wrd + str(cnt2) + " ")

        lst.append(line)
    f.close()
    
    f = open('tmp.txt', 'w')
    for line in lst:
        f.write(line)
    f.close()


def i_freq_check(filename):
    imaginary = False
    frequency = "Frequencies --"
    dif = 0
    freq_lst_len = []
    with open(filename) as search:

        freq_clean = []
        for num, line in enumerate(search):
            if frequency in line:
                freq_lst_len.append(num)
                freq_line = line[16:].split(" ")
                for k in freq_line:
                    k = k.rstrip()
                    try:
                        k = float(k)
                        # print(k)
                        if k < 0:
                            imaginary = True
                        freq_clean.append(k)
                    except:
                        pass
            if len(freq_lst_len) > 1:
                break

        # print(freq_clean)
    try:
        freq_lst_len = [freq_lst_len[0]+5, freq_lst_len[1]-2]
    except:
        pass
    # print(freq_lst_len)

    return imaginary, freq_clean, freq_lst_len


def add_imaginary(freq_clean, freq_lst_len, filename):
    # print(freq_clean)
    cnt = 0
    for k in freq_clean:
        if k < 0:
            cnt += 1
            if cnt > 2:
                break

    f = open(filename)
    lines = f.readlines()
    f.close()
    imag_values = lines[freq_lst_len[0]: freq_lst_len[1]]
    for num, i in enumerate(imag_values):
        i = i.replace("  ", " ")
        i = i.replace("  ", " ")
        i = i.replace("  ", " ")
        i = i.replace("\n", "")
        i = (i.split(" "))[3:3+cnt*3]
        for k in range(len(i)):
            i[k] = float(i[k])
        imag_values[num] = i
    # print(imag_values)
    carts = genfromtxt('tmp.txt')
    carts_no_atom = carts[:, 1:4]
    imag_values = np.array(imag_values)
    # print(imag_values)
    # print('\n')
    # print(carts_no_atom, '\n')
    print(imag_values)
    print(carts_no_atom)
    print(len(imag_values[0,:])//3)
    for i in range(len(imag_values[0, :]) // 3):
        print(i)
        print(imag_values[:,i:i+3])
        carts_no_atom = np.add(carts_no_atom, imag_values[:, i: i+3])
        print("carts_no_atom: ", carts_no_atom)
    # print(carts_no_atom)
    carts[:, 1:4] = carts_no_atom

    carts = np.around(carts, 6)
    """    carts = carts.astype(str)
        carts = carts.tolist() """
    np.savetxt("tmp.txt", carts,
               fmt="%s")

    clean_many_txt()


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
    if len(HFs) == 1:
        return freqs[0], HFs[0], 0, zeros[0]
    else:
        return freqs[0], HFs[0], HFs[1], zeros[0]


def find_geom(lines, error, filename, imaginary):
    #geom_start = "Standard orientation:"
    #geom_end = " Standard basis:"
    print("Opening..." + filename)
    found = False
    geom_size = 0
    geom_list = []
    with open(filename) as search:
        for num, line in enumerate(search, 1):
            if " Charge =  0 Multiplicity = 1" in line:
                geom_size = num + 1
                found = True
            elif found == True and num < geom_size + 200:
                #print(line, end="")
                geom_list.append(line)
            elif found == True and line == ' \n':
                #geom_size = num - geom_size
                break
    clean_geom_size = []
    for i in geom_list:
        if not " \n" == i:
            clean_geom_size.append(i)
        elif i == ' \n':
            break
    geom_size = len(clean_geom_size)
    if error == True:
        print("Error == True")
        pop_2 = "Population analysis using the SCF Density."
        pops = []
        pop_2_test = False
        with open(filename) as search:
            for line in search:
                if pop_2 in line:
                    pops.append(1)
                if len(pops) == 2:
                    pop_2_test = True
        if pop_2_test == True:
            print(pop_2_test, "occuring")
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_start in line:
                        standards.append(num + 5)

            geom_end_pops = " Rotational constants (GHZ):"
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_end_pops in line:
                        orientation.append(num - 1)
            print("if")
        else:
            print('else')
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_start in line:
                        standards.append(num + 5)
                        

            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_end in line:
                        orientation.append(num - 2)
            #print(standards[-5:], orientation[-5:])
    else:
        print("No error")
        """
        #to return to normal, use this
        with open(filename) as search:
            for num, line in enumerate(search, 1):
                if geom_start in line:
                    standards.append(num + 5)

        with open(filename) as search:
            for num, line in enumerate(search, 1):
                if geom_end in line:
                    orientation.append(num - 2)
        """
        with open(filename) as search:
            for num, line in enumerate(search, 1):
                if geom_start in line:
                    standards.append(num + 5)

        with open(filename) as search:
            for num, line in enumerate(search, 1):
                if geom_end in line:
                    orientation.append(num - 2)
    if len(orientation) < 6:
        orien = len(orientation)
    else:
        orien = 5
    if len(standards) < 6:
        stand = len(standards)
    else:
        stand = 5
    for i in range(-1, -orien, -1):
        for j in range(-1, -stand, -1):
            length = orientation[i] - standards[j]
            if length == geom_size:
                orien = i
                stand = j
                break
    if stand == 5:
        stand = -1
    del lines[standards[stand] - 1 + length:]
    del lines[:standards[stand] - 1]
    """
    for i in range(1, 10, 1):
        k = "  " * i
        lines = [item.replace(k, " ") for item in lines]
        #print(lines)
    """
    cleaned_lines = []
    for i in range(len(lines)):
        clean = cleanLine(lines[i])
        cleaned_lines.append(clean)

    """
    start_ls = []
    for i in lines:
        # i = i.strip()
        i = i.rstrip()
        print(i)
        k = Convert(i)
        #print(k)
        if "----------------------------------" in k[1]:
            break
        #print(k)
        start_ls.append(k)
    
    #print(len(start_ls))
    #print(len(start_ls[0]))
    start_array = np.array(start_ls)
    """
    start_array = np.array(cleaned_lines)
    new_geom = np.zeros(((int(len(start_array[:, 3]))), 4))
    new_geom[:, 0] = start_array[:, 1]
    new_geom[:, 1] = start_array[:, 3]
    new_geom[:, 2] = start_array[:, 4]
    new_geom[:, 3] = start_array[:, 5]

    out_file = "tmp.txt"
    np.savetxt(out_file, new_geom,
               fmt="%s")
    if not imaginary:
        clean_many_txt()
    elif error:
        clean_many_txt()


def make_input_files_no_constraints(output_num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt):
    """ Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory """

    data = ""

    with open('tmp.txt') as fp:
        data = fp.read()

    # Reading data from file2
    charges = "0 1"

    with open('mex.com', 'w') as fp:
        fp.write("%mem={0}mb\n".format(mem_com_opt))
        fp.write("%nprocs=4\n")
        fp.write("#N {0}".format(method_opt) +
                 "/{0} OPT FREQ\n".format(basis_set_opt))
        fp.write("\n")
        fp.write("Name ModRedundant - Minimalist working constrained optimisation\n")
        fp.write("\n")
        fp.write(charges + "\n")
        fp.write(data)
        fp.write("\n")

    with open('mex.pbs', 'w') as fp:
        fp.write("#!/bin/sh\n")
        fp.write("#PBS -N mex_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l")
        fp.write("mem={0}gb\n".format(mem_pbs_opt))
        fp.write(
            "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
        fp.write(
            "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
        fp.write(
            """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n""")
        fp.write("then\n")
        fp.write(
            "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n")
        fp.write(
            """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n""")
        fp.write(
            "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n")
        fp.write("""  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n""")
        fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
        fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
        fp.write("cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mex.com mex.out" +
                 str(output_num) + "\n\nrm -r $scrdir\n")


def make_mexc(method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc):
    """ Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory """

    data = ""

    with open('tmp.txt') as fp:
        data = fp.read()

    # Reading data from file2
    charges = "0 1"
    if method_mexc == 'PBE0':
        new_dir = "pbe0"
        method_mexc = 'PBE1PBE'
    elif method_mexc == 'wB97XD':
        new_dir = "wb97xd"
    elif method_mexc == 'B3LYP':
        new_dir = "mexc"
    elif method_mexc == 'B3LYPD3':
        new_dir = 'b3lypd3'
        method_mexc = 'B3lYP empiricaldispersion=gd3 '
    elif method_mexc == 'CAM-B3LYP':
        new_dir = 'cam-b3lyp'
        method_mexc = 'CAM-B3LYP'
    elif method_mexc == 'B97D3':
        new_dir = 'b97d3'
        method_mexc = 'B97D3'
    else:
        print("This method is not supported for TD-DFT yet.")
    os.mkdir(new_dir)

    with open(new_dir + '/mexc.com', 'w') as fp:
        fp.write("%mem={0}mb\n".format(mem_com_mexc))
        fp.write("%nprocs=4\n")
        fp.write("#N TD(NStates=25) {0}".format(
            method_mexc) + "/{0}\n".format(basis_set_mexc))
        fp.write("\n")
        fp.write("Name ModRedundant - Minimalist working constrained optimisation\n")
        fp.write("\n")
        fp.write(charges + "\n")
        fp.write(data)
        fp.write("\n")

    with open(new_dir + '/mexc.pbs', 'w') as fp:
        fp.write("#!/bin/sh\n")
        fp.write(
            "#PBS -N mexc_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l")
        fp.write("mem={0}gb\n".format(mem_pbs_mexc))
        fp.write(
            "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
        fp.write(
            "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
        fp.write(
            """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n""")
        fp.write("then\n")
        fp.write(
            "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n")
        fp.write(
            """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n""")
        fp.write(
            "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n")
        fp.write("""  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n""")
        fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
        fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
        fp.write(
            "cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mexc.com mexc.out\n\nrm -r $scrdir\n")


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


word_error = "Error"
geom_start = "Standard orientation:"

geom_end = " Standard basis:"
standards = []
orientation = []


def main(index,
         method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
         method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
         resubmissions, delay
         ):
    print(os.getcwd())
    out_files = glob.glob("*.out*")
    out_completion = glob.glob("mex_o.*")
    print(out_files)
    print(out_completion)
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

        #filename = out_files[-1]
        print("filename:", filename)
        output_num = list(filename)
        output_num = output_num[-1]

        if output_num == "t":
            output_num = 2

        else:
            output_num = int(output_num[-1]) + 1
            if delay == 0:
                resubmissions[index] = output_num

                # if not starting from the beginning, the resubmission[index] needs to be set to current output number
        if len(out_completion) < len(out_files):
            print("Not finished yet")
            return True, resubmissions
        if resubmissions[index] > output_num:
            print("Awaiting queue")
            return True, resubmissions
        """         if existing_output < resubmissions[index]:
            print('exit without submission')
            return True, resubmissions """

        # print("Input file: " + filename)
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        error = False

        imaginary, freq_clean, freq_lst_len = i_freq_check(filename)

        with open(filename) as search:
            for num, line in enumerate(search, 1):
                if word_error in line:
                    error = True
        cmd = "qsub mex.pbs"
        print("here")
        #try:
        if error == True:
            find_geom(lines, error=True, filename=filename,
                        imaginary=imaginary)
            make_input_files_no_constraints(
                output_num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt)
            #os.system("qsub mex.pbs")
            failure = subprocess.call(cmd, shell=True)
            resubmissions[index] += 1
            return False, resubmissions

        elif imaginary == True:
            find_geom(lines, error=False, filename=filename,
                        imaginary=imaginary)
            add_imaginary(freq_clean, freq_lst_len, filename)
            print("Imaginary!")
            make_input_files_no_constraints(
                output_num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt)
            #os.system("qsub mex.pbs")
            failure = subprocess.call(cmd, shell=True)
            print('imaginary frequency handling...')
            resubmissions[index] += 1
            return False, resubmissions
        else:
            cmd = "qsub mexc.pbs"
            find_geom(lines, error=False, filename=filename,
                        imaginary=imaginary)
            freq, hf_1, hf_2, zero_point = freq_hf_zero(
                lines, filename=filename)
            # print("\n")
            # print(freq)

            # print(hf_1)
            # print(hf_2)
            # print(zero_point)
            sum_energy = clean_energies(hf_1, hf_2, zero_point)
            print('Total energy {0}: '.format(index+1), sum_energy)
            make_mexc(method_mexc, basis_set_mexc,
                        mem_com_mexc, mem_pbs_mexc)
            if method_mexc == 'PBE0':
                os.chdir("pbe0")
            elif method_mexc == 'wB97XD':
                os.chdir("wb97xd")
            elif method_mexc == 'B3LYP':
                os.chdir("mexc")
            elif method_mexc == 'B3LYPD3':
                os.chdir('b3lypd3')
            elif method_mexc == 'CAM-B3LYP':
                os.chdir('cam-b3lyp')
            elif method_mexc == 'B97D3':
                os.chdir('b97d3')
            else:
                print("This method is not supported for TD-DFT yet.")
            #os.system("qsub mexc.pbs")
            # os.path.abspath(os.getcwd())
            failure = subprocess.call(cmd, shell=True)
            resubmissions[index] += 1
            os.chdir("..")
            os.remove("tmp.txt")

            os.chdir("../..")
            if "results" not in glob.glob("results"):
                os.mkdir("results")
            os.chdir("results")
            if "energies" not in glob.glob("energies"):
                os.mkdir("energies")
            os.chdir("energies")

            # os.chdir("../../results/energies")
            print(os.getcwd())
            f = open("energy{0}.txt".format(index+1), 'w')
            f.write(str(sum_energy))
            f.close()
            if "energy_all.csv" not in glob.glob("energy_all.csv"):
                ft = open("energy_all.csv", "w")
                ft.write("%d,%.14f\n" % (index+1, sum_energy))
                ft.close()
            else:

                ft = open("energy_all.csv", "a")
                ft.write("%d,%.14f\n" % (index+1, sum_energy))
                ft.close()
            return False, resubmissions
        """
        except:
            print('Calculation still running')
            return True, resubmissions
        """
    else:
        print('No output files detected for geom%d' % (index+1))
        return True, resubmissions

# main()
