import numpy as np
import os
from numpy import genfromtxt
import glob
import subprocess


def CFOUR_input_files(
    method,
    basis_set,
    mem_ZMAT,
    mem_pbs,
    data,
    dir_name,
    cluster="map",
    baseName="mexc",
):
    if cluster == "map":
        with open("%s/ZMAT" % (dir_name), "w") as fp:
            fp.write("%s\n" % (dir_name))
            fp.write(data)
            fp.write("\n\n")
            fp.write(
                "*CFOUR(CHARGE=0,REFERENCE=RHF,SPHERICAL=ON,BASIS=%s\n" % basis_set
            )
            fp.write("LINDEP_TOL=7,LINEQ_CONV=7,SCF_CONV=6,SCF_MAXCYC=250\n")
            fp.write(
                "CALC=%s,EXCITE=EOMEE,ESTATE_SYM=5\nESTATE_PROP=EXPECTATION\nCOORDS=CARTESIAN\n"
                % method
            )
            fp.write(
                "FROZEN_CORE=ON,ABCDTYPE=AOBASIS\nCONVERGENCE=7,MEMORY_SIZE=%s,MEM_UNIT=GB)\n"
                % mem_ZMAT
            )
        with open("%s/%s.pbs" % (dir_name, baseName), "w") as fp:
            fp.write("#!/bin/csh\n#\n#PBS -N %s\n" % baseName)
            fp.write(
                "#PBS -S /bin/csh\n#PBS -j oe\n#PBS -W umask=022\n#PBS -l cput=2400:00:00\n#PBS -l mem=%sgb\n#PBS -l nodes=1:ppn=2\n#PBS -q gpu"
                % mem_pbs
            )
            fp.write(
                '\n\ncd $PBS_O_WORKDIR\nsetenv NUM $NCPUS\necho "$NUM cores requested in PBS file"\necho " "\nsource /ddn/home1/r1621/.tschrc\n/ddn/home1/r1621/maple/bin/tempQC/bin/c4ext_old.sh 20\n'
            )
    return


def gaussianInputFiles(
    output_num,
    method_opt,
    basis_set_opt,
    mem_com_opt,
    mem_pbs_opt,
    cluster,
    baseName="mexc",
    procedure="OPT",
    data="",
    dir_name="",
    solvent="",
    outName="mexc_o",
):
    # baseName = baseName.com / baseName.pbs / baseName.out
    # dir_name = directory name
    output_num = str(output_num)
    if output_num == "0":
        output_num = ""

    if dir_name == "":
        dir_name = baseName

    if solvent != "":
        # dir_name += '_%s'%solvent
        print(dir_name)
        solvent_line = "SCRF=(Solvent=%s)" % solvent
        print(dir_name)

    if data == "":
        with open("tmp.txt") as fp:
            data = fp.read()

    # Reading data from file2
    charges = "0 1"

    if cluster == "map":
        print('map here', dir_name, baseName, os.getcwd())
        with open("%s/%s.com" % (dir_name, baseName), "w") as fp:
            fp.write("%mem={0}mb\n".format(mem_com_opt))
            fp.write("%nprocs=4\n")
            if solvent == "":
                fp.write("#N %s/%s %s" % (method_opt, basis_set_opt, procedure))
            else:
                fp.write(
                    "#N %s/%s %s %s"
                    % (method_opt, basis_set_opt, procedure, solvent_line)
                )

            fp.write("\n\n")
            fp.write(
                "Name\n"
            )
            fp.write("\n")
            fp.write(charges + "\n")
            fp.write(data)
            fp.write("\n")

        with open("%s/%s.pbs" % (dir_name, baseName), "w") as fp:
            fp.write("#!/bin/sh\n")
            fp.write(
                "#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l "
                % outName.replace("-", "").replace(",", "_")
            )
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            # r410 node
            # fp.write("#PBS -q r410\n")
            fp.write("#PBS -q gpu\n")
            fp.write("#PBS -W umask=022\n")
            # fp.write("#PBS -l nodes=1:ppn=1\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
            fp.write("#PBS -l nodes=1:ppn=1\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
            fp.write(
                "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n"
            )
            fp.write(
                """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n"""
            )
            fp.write("then\n")
            fp.write(
                "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n"
            )
            fp.write(
                """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n"""
            )
            fp.write(
                "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n"
            )
            fp.write(
                """  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n"""
            )
            fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
            fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
            fp.write(
                "cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 {0}.com {0}.out".format(
                    baseName, baseName
                )
                + str(output_num)
                + "\n\nrm -r $scrdir\n"
            )
    elif cluster == "seq":
        print('seq here', dir_name, baseName, os.getcwd())
        if dir_name == "./":
            fn = "%s.com" % baseName
        else:
            fn = "%s/%s.com" % (dir_name, baseName)
        with open(fn, "w") as fp:
            fp.write("%mem=8gb\n")
            if solvent == "":
                fp.write("#N %s/%s %s" % (method_opt, basis_set_opt, procedure))
            else:
                fp.write(
                    "#N %s/%s %s %s"
                    % (method_opt, basis_set_opt, procedure, solvent_line)
                )

            fp.write("\n\n")
            fp.write("Name \n")
            fp.write("\n")
            fp.write(charges + "\n")
            fp.write(data)
            fp.write("\n")

        if dir_name == "./":
            fn = "%s.pbs" % baseName
        else:
            fn = "%s/%s.pbs" % (dir_name, baseName)
        with open(fn, "w") as fp:
            fp.write("#!/bin/sh\n")
            fp.write(
                "#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -W umask=022\n#PBS -j oe\n#PBS -m abe\n#PBS -l cput=1000:00:00\n#PBS -l "
                % outName.replace("-", "").replace(",", "_")
            )
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            fp.write("#PBS -l nodes=1:ppn=2\n#PBS -l file=100gb\n\n")
            fp.write(
                "export g09root=/usr/local/apps/\n. $g09root/g09/bsd/g09.profile\n\n"
            )
            fp.write(
                "scrdir=/tmp/bnp.$PBS_JOBID\n\nmkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n"
            )
            fp.write(
                "printf 'exec_host = '\nhead -n 1 $PBS_NODEFILE\n\ncd $PBS_O_WORKDIR\n\n"
            )
            fp.write(
                "/usr/local/apps/bin/g09setup %s.com %s.out%s"
                % (baseName, baseName, output_num)
            )
        print('seq finished writing')


# from ice_analogs, but modified input files
def Convert(string):
    li = list(string.split(" "))
    return li


def cleanLine(line):
    aList = []
    cropped_line = line.rstrip()
    for i in range(2, 10):
        k = " " * i
        cropped_line = cropped_line.replace(k, " ")
    cropped_line = cropped_line.split(" ")
    for i in cropped_line:
        if i == "":
            continue
        else:
            aList.append(float(i))
    return aList


def conv_num(string):
    li = list(string.split(" "))
    return li


def clean_many_txt(geomDirName, numbered=True):
    """This will replace the numerical forms of the elements as their letters numbered in order"""

    f = open("tmp.txt", "r")
    """
    a = ['14.0 ','30.0 ' ,
            '16.0 ', '6.0 ',
            '8.0 ', '1.0 ',
            '7.0 '
        ]
    table = {
        '6.0 ': 'C', '8.0 ': 'O',
        '1.0 ': 'H', '7.0 ': 'N',
        '16.0 ': 'S', '30.0 ': 'Zn',
        '14.0 ': 'Si'
    }
    """
    a = [
        "14.000000 ",
        "30.000000 ",
        "16.000000 ",
        "6.000000 ",
        "8.000000 ",
        "1.000000 ",
        "7.000000 ",
        "35.000000",
    ]
    table = {
        "6.000000 ": "C",
        "8.000000 ": "O",
        "1.000000 ": "H",
        "7.000000 ": "N",
        "16.000000 ": "S",
        "30.000000 ": "Zn",
        "14.000000 ": "Si",
        "35.000000": "F",
    }

    xyzToMolLst = []
    lst = []
    cnt2 = 0
    for line in f:
        cnt2 += 1
        for word in a:
            if word in line:
                convert_wrd = table[word]
                line2 = line.replace(word, convert_wrd + " ")
                if numbered:
                    line = line.replace(word, convert_wrd + str(cnt2) + " ")
                else:
                    line = line.replace(word, convert_wrd + " ")

        lst.append(line)
        xyzToMolLst.append(line2)
    f.close()
    f = open("tmp.txt", "w")
    length = 0
    for line in lst:
        f.write(line)
        length += 1
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
                        if k < 0:
                            imaginary = True
                        freq_clean.append(k)
                    except:
                        pass
            if len(freq_lst_len) > 1:
                break
    try:
        freq_lst_len = [freq_lst_len[0] + 5, freq_lst_len[1] - 2]
    except:
        pass

    return imaginary, freq_clean, freq_lst_len


def add_imaginary(freq_clean, freq_lst_len, filename, geomDirName):
    cnt = 0
    for k in freq_clean:
        if k < 0:
            cnt += 1
            if cnt > 2:
                break

    f = open(filename)
    lines = f.readlines()
    f.close()
    imag_values = lines[freq_lst_len[0] : freq_lst_len[1]]
    for num, i in enumerate(imag_values):
        i = i.replace("  ", " ")
        i = i.replace("  ", " ")
        i = i.replace("  ", " ")
        i = i.replace("\n", "")
        i = (i.split(" "))[3 : 3 + cnt * 3]
        for k in range(len(i)):
            i[k] = float(i[k])
        imag_values[num] = i
    carts = genfromtxt("tmp.txt")
    carts_no_atom = carts[:, 1:4]
    imag_values = np.array(imag_values)

    for i in range(len(imag_values[0, :]) // 3):
        carts_no_atom = np.add(carts_no_atom, imag_values[:, i : i + 4])
    carts[:, 1:4] = carts_no_atom

    carts = np.around(carts, 6)
    """    carts = carts.astype(str)
        carts = carts.tolist() """
    np.savetxt("tmp.txt", carts, fmt="%f")

    clean_many_txt(geomDirName)


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
                index = line.index(start)
                HFs.append(line[index:])

            if zero_point in line:
                zeros.append(line)
    print("hf", HFs, "freqs", freqs, "zeros", zeros)
    if len(freqs) == 0 and len(zeros) == 0:
        freqs.append("0")
        zeros.append(" (Hartree/Particle)0")
    if len(HFs) == 1:
        return freqs[0], HFs[0], 0, zeros[0]
    else:
        return freqs[0], HFs[0], HFs[1], zeros[0]


def find_geom(
    lines, error, filename,
    imaginary, geomDirName,
    numberedClean=True
):
    found = False
    geom_size = 0
    geom_list = []
    with open(filename) as search:
        for num, line in enumerate(search, 1):
            if " Charge =  0 Multiplicity = 1" in line:
                geom_size = num + 1
                found = True
            elif found == True and num < geom_size + 200:
                geom_list.append(line)
            elif found == True and line == " \n":
                # geom_size = num - geom_size
                break
    clean_geom_size = []
    for i in geom_list:
        if not " \n" == i:
            clean_geom_size.append(i)
        elif i == " \n":
            break
    geom_size = len(clean_geom_size)
    if error == True:
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
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_start in line:
                        standards.append(num + 5)

            geom_end_pops = " Rotational constants (GHZ):"
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_end_pops in line:
                        orientation.append(num - 1)
        else:
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_start in line:
                        standards.append(num + 5)

            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_end in line:
                        orientation.append(num - 2)
    else:

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
    del lines[standards[stand] - 1 + length :]
    del lines[: standards[stand] - 1]

    cleaned_lines = []
    for i in range(len(lines)):
        clean = cleanLine(lines[i])
        cleaned_lines.append(clean)

    start_array = np.array(cleaned_lines)
    new_geom = np.zeros(((int(len(start_array[:, 3]))), 4))
    new_geom[:, 0] = start_array[:, 1]
    new_geom[:, 1] = start_array[:, 3]
    new_geom[:, 2] = start_array[:, 4]
    new_geom[:, 3] = start_array[:, 5]

    out_file = "tmp.txt"
    np.savetxt(out_file, new_geom, fmt="%f")

    if not imaginary:
        clean_many_txt(geomDirName, numberedClean)
    elif error:
        clean_many_txt(geomDirName, numberedClean)


def make_input_files_no_constraints(
    output_num, method_opt,
    basis_set_opt, mem_com_opt,
    mem_pbs_opt, cluster
):
    """Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory"""
    data = ""
    with open("tmp.txt") as fp:
        data = fp.read()
    charges = "0 1"

    if cluster == "map":
        print("map only")
        with open("mex.com", "w") as fp:
            fp.write("%mem={0}mb\n".format(mem_com_opt))
            fp.write("%nprocs=4\n")
            fp.write("#N {0}".format(method_opt) + "/{0} OPT\n".format(basis_set_opt))
            fp.write("\n")
            fp.write(
                "Name\n"
            )
            fp.write("\n")
            fp.write(charges + "\n")
            fp.write(data)
            fp.write("\n")

        with open("mex.pbs", "w") as fp:
            fp.write("#!/bin/sh\n")
            fp.write(
                "#PBS -N mex_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l "
            )
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            fp.write(
                "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n"
            )
            fp.write(
                "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n"
            )
            fp.write(
                """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n"""
            )
            fp.write("then\n")
            fp.write(
                "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n"
            )
            fp.write(
                """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n"""
            )
            fp.write(
                "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n"
            )
            fp.write(
                """  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n"""
            )
            fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
            fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
            fp.write(
                "cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mex.com mex.out"
                + str(output_num)
                + "\n\nrm -r $scrdir\n"
            )
    elif cluster == "seq":
        gaussianInputFiles(
            output_num,
            method_opt,
            basis_set_opt,
            mem_com_opt,
            mem_pbs_opt,
            cluster,
            dir_name="./",
            baseName="mex",
            procedure="OPT",
        )

        # qsub()


def clean_name(name):
    return name.replace("-", "_").replace(",", "")


def clean_input_name(method, basis_set, solvent):
    clean = method
    if basis_set != "6-311G(d,p)":
        clean += basis_set.replace("(", "").replace(")", "").replace(",", "_")
    if solvent != "":
        clean += "_%s" % (clean_name(solvent))
    return solvent


def qsub(path="."):
    resetDirNum = len(path.split("/"))
    if path != ".":
        os.chdir(path)
    pbs_file = glob.glob("*.pbs")[0]
    cmd = "qsub %s" % pbs_file
    print(os.getcwd(), "cmd", cmd)
    failure = subprocess.call(cmd, shell=True)
    if path != ".":
        for i in range(resetDirNum):
            os.chdir("..")


# def clean_dir_name(dir_name):
#     dir_name = dir_name.replace("-", "").replace(",", "")
#     dir_name = dir_name.replace("(", "").replace(")", "")
#     return dir_name

def clean_dir_name(dir_name):
    return dir_name.replace("-", "").replace(",", "")


def make_exc(
    method_mexc,
    basis_set_mexc,
    mem_com_mexc,
    mem_pbs_mexc,
    cluster,
    geomDirName,
    SCRF="",
    nStates="25",
    spec_type="electronic",
    outName=""
):

    if spec_type == 'electronic':
        baseName = 'mexc'
        dir_name = construct_dir_name(
                basis_set_mexc,
                nStates,
                SCRF,
                method_mexc,
                clean=False
                )
        procedure = "TD(NStates=%s)" % (str(nStates))
    elif spec_type == 'vibrational':
        baseName = 'vib'
        dir_name = construct_dir_name(
                basis_set_mexc,
                nStates,
                SCRF,
                method_mexc,
                clean=False,
                spec_type="vibrational"
                )
        procedure = "OPT FREQ"

    if os.path.exists(dir_name):
        print(dir_name, "already exists")
        return 'None'

    os.mkdir(dir_name)
    output_num = 0
    # basis_set_mexc='CAM-B3LYP'

    # solvent = 'SCRF=(Solvent=dichloromethane)'

    if outName == '':
        outName = geomDirName + "_%s_%s" % (baseName, SCRF)
    else:
        outName += "_" + geomDirName + "_%s_%s" % (baseName, SCRF)

    gaussianInputFiles(
        output_num,
        method_mexc,
        basis_set_mexc,
        mem_com_mexc,
        mem_pbs_mexc,
        cluster,
        baseName=baseName,
        procedure=procedure,
        data="",
        dir_name=dir_name,
        solvent=SCRF,
        outName=outName,
    )
    # path = "%s" % dir_name
    # qsub(path)
    return dir_name


def clean_energies(hf_1, hf_2, zero_point):
    zero_point = zero_point[30:].replace(" (Hartree/Particle)", "")
    for i in range(10):
        zero_point = zero_point.replace("  ", " ")
    zero_point = float(zero_point)
    hf_1 = hf_1[3:].replace("\n", "").split("\\")

    if hf_2 != 0:
        hf_2 = hf_2[3:].replace("\n", "").split("\\")

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


def main(
    index,
    method_opt,
    basis_set_opt,
    mem_com_opt,
    mem_pbs_opt,
    method_mexc,
    basis_set_mexc,
    mem_com_mexc,
    mem_pbs_mexc,
    resubmissions,
    delay,
    cluster,
    geomDirName,
    solvent="",
):

    out_files = glob.glob("*.out*")
    out_completion = glob.glob("*_o.*")
    if method_mexc == "CAM-B3LYP":
        qsub_dir = "mexc"
    else:
        qsub_dir = method_mexc
    if solvent != "":
        qsub_dir += "_%s" % solvent

    qsub_dir = clean_dir_name(qsub_dir)

    print("v2 %s %s" % (solvent, qsub_dir))

    if len(out_files) > 0:

        filename = out_files[-1]

        output_num = list(filename)
        output_num = output_num[-1]

        if output_num == "t":
            output_num = 2

        else:
            output_num = int(output_num[-1]) + 1
            if delay == 0:
                resubmissions[index] = output_num
        if len(out_completion) != len(out_files):
            return True, resubmissions, "None"
        if resubmissions[index] > output_num:
            return True, resubmissions, "None"

        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        error = False

        imaginary, freq_clean, freq_lst_len = i_freq_check(filename)

        with open(filename) as search:
            for num, line in enumerate(search, 1):
                if word_error in line:
                    error = True
        cmd = "qsub mex.pbs"
        if error == True:

            print("ERROR == TRUE")
            find_geom(
                lines,
                error=True,
                filename=filename,
                imaginary=imaginary,
                geomDirName=geomDirName,
            )
            make_input_files_no_constraints(
                output_num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt, cluster
            )
            # os.system("qsub mex.pbs")
            failure = subprocess.call(cmd, shell=True)
            resubmissions[index] += 1
            qsub_dir = "./"
            return False, resubmissions, qsub_dir

        elif imaginary == True:
            find_geom(
                lines,
                error=False,
                filename=filename,
                imaginary=imaginary,
                geomDirName=geomDirName,
            )
            add_imaginary(freq_clean, freq_lst_len, filename, geomDirName=geomDirName)

            make_input_files_no_constraints(
                output_num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt, cluster
            )
            # os.system("qsub mex.pbs")
            failure = subprocess.call(cmd, shell=True)
            print("imaginary frequency handling...")
            resubmissions[index] += 1
            qsub_dir = "./"
            return False, resubmissions, qsub_dir
        else:
            print("ELSE")
            cmd = "qsub mexc.pbs"
            find_geom(
                lines,
                error=False,
                filename=filename,
                imaginary=imaginary,
                geomDirName=geomDirName,
            )
            """
            freq, hf_1, hf_2, zero_point = freq_hf_zero(
                lines, filename=filename)
            """
            print("entering make_exc")
            make_exc(
                method_mexc,
                basis_set_mexc,
                mem_com_mexc,
                mem_pbs_mexc,
                cluster,
                geomDirName,
                solvent,
            )

            os.remove("tmp.txt")

            return False, resubmissions, qsub_dir

    else:
        print("No output files detected for geom%d" % (index + 1))
        return True, resubmissions, "None"


def get_final_out(files):
    if len(files) == 0:
        return 'false'
    val, ind = 0, 0
    for n, i in enumerate(files):
        if i[-1] == 't':
            continue
        elif i[-1] == '0':
            print("Doomed")
        else:
            c = int(i[-1]) - 1
            if c > val:
                val = c
                ind = n
    return files[ind]


def construct_dir_name(
        basis_set_mexc,
        nStates,
        SCRF,
        method_mexc,
        clean=True,
        spec_type="electronic"
        ):
    if basis_set_mexc == "6-311G(d,p)":
        basis_dir_name = ""
    else:
        basis_dir_name = "_" + basis_set_mexc

    if nStates == "25":
        pass
    else:
        basis_dir_name += "_n%s" % nStates

    if SCRF != "":
        basis_dir_name += "_SCRF_%s" % SCRF

    if spec_type == 'vibrational':
        basis_dir_name = '_vib' + basis_dir_name

    if method_mexc == "PBE0":
        path_mexc = method_mexc.lower() + basis_dir_name
        method_mexc = "PBE1PBE"
    elif method_mexc == "wB97XD":
        path_mexc = method_mexc.lower() + basis_dir_name
    elif method_mexc == "B3LYP":
        path_mexc = "mexc" + basis_dir_name
    elif method_mexc == "B3LYPD3":
        path_mexc = method_mexc.lower() + basis_dir_name
        method_mexc = "B3lYP empiricaldispersion=gd3 "
    elif method_mexc == "CAM-B3LYP":
        path_mexc = method_mexc.lower() + basis_dir_name
        method_mexc = "CAM-B3LYP"
    elif method_mexc == "B97D3":
        path_mexc = method_mexc.lower() + basis_dir_name
        method_mexc = "B97D3"
    else:
        print("This method is not supported for TD-DFT yet.")

    if clean:
        path_mexc = path_mexc.replace("(", "\(").replace(")", "\)")
    return path_mexc


def job_progression(
    config={
            'dataPath': 'data/30_8_co2',
            "outName": "co2",
            'optResub': {
                'optMethod': 'B3LYP',
                'optBasisSet': '6-31G(d)',
                'memComFile': '1600',
                'memPBSFile': '15'
                },
            'excList': [
                {
                    'excMethod': 'CAM-B3LYP',
                    'excBasisSet': '6-311G(d,p)',
                    'memComFile': '1600',
                    'memPBSFile': '15',
                    'nStates': 25,
                    'SCRF': ''
                    }
                ],
            "vibList": [
              {
                "excMethod": "CAM-B3LYP",
                "excBasisSet": "6-31+G(d,p)",
                "memComFile": "1600",
                "memPBSFile": "15",
                'SCRF': ""
              }
            ]
        },
    delay=True,
    stat=['data/30_8_co2/geom1', -1, 2, 1, 1],
    cluster='map',
    geomDirName='geom',
    spec_type='electronic',
    vib_only=False,
):
    outName = config["outName"]
    method_opt = config['optResub']['optMethod']
    basis_set_opt = config['optResub']['optBasisSet']
    mem_com_opt = config['optResub']['memComFile']
    mem_pbs_opt = config['optResub']['memPBSFile']

    if spec_type == 'electronic':
        excList = config['excList']
        if stat[1] == -1:
            excStep = 0
        elif stat[1] > len(excList):
            print('excStep higher than excList')
            return True, stat, "None"
        else:
            excStep = stat[1]
        method_mexc = config['excList'][excStep]['excMethod']
        basis_set_mexc = config['excList'][excStep]['excBasisSet']
        mem_com_mexc = config['excList'][excStep]['memComFile']
        mem_pbs_mexc = config['excList'][excStep]['memPBSFile']
        nStates = str(config['excList'][excStep]['nStates'])
        SCRF = config['excList'][excStep]['SCRF']

    elif spec_type == 'vibrational':
        if stat[1] == -1:
            excStep = 0
        elif vib_only:
            excStep = stat[1]
        else:
            excStep = stat[1] - stat[3]
        method_mexc = config['vibList'][excStep]['excMethod']
        basis_set_mexc = config['vibList'][excStep]['excBasisSet']
        mem_com_mexc = config['vibList'][excStep]['memComFile']
        mem_pbs_mexc = config['vibList'][excStep]['memPBSFile']
        SCRF = config['vibList'][excStep]['SCRF']

    out_files = glob.glob("*.out*")
    out_completion = glob.glob("*_o.*")
    if method_mexc == "CAM-B3LYP":
        qsub_dir = "mexc"
    else:
        qsub_dir = method_mexc
    if SCRF != "":
        qsub_dir += "_%s" % SCRF

    qsub_dir = clean_dir_name(qsub_dir)

    if len(out_files) > 0:
        # filename = out_files[-1]
        filename = get_final_out(out_files)

        output_num = list(filename)
        output_num = output_num[-1]

        if output_num == "t":
            output_num = 2

        else:
            output_num = int(output_num[-1]) + 1
            # print('out num', output_num)
            if not delay:
                stat[2] = output_num
        if len(out_completion) != len(out_files):
            print('lengths do not match!')
            return True, stat, "None"
        if stat[2] > output_num:
            # print('this case!')
            return True, stat, "None"

        # print('reading', filename)
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        error = False

        imaginary, freq_clean, freq_lst_len = i_freq_check(filename)

        with open(filename) as search:
            for num, line in enumerate(search, 1):
                if word_error in line:
                    error = True
        if error:
            # print("ERROR == TRUE")
            find_geom(
                lines,
                error=True,
                filename=filename,
                imaginary=imaginary,
                geomDirName=geomDirName,
            )
            make_input_files_no_constraints(
                output_num, method_opt,
                basis_set_opt, mem_com_opt,
                mem_pbs_opt, cluster
            )
            # os.system("qsub mex.pbs")
            stat[2] += 1
            qsub_dir = "./"
            os.remove("tmp.txt")
            return False, stat, qsub_dir

        elif imaginary:
            find_geom(
                lines,
                error=False,
                filename=filename,
                imaginary=imaginary,
                geomDirName=geomDirName,
            )
            add_imaginary(
                    freq_clean,
                    freq_lst_len, filename,
                    geomDirName=geomDirName)

            make_input_files_no_constraints(
                output_num, method_opt,
                basis_set_opt, mem_com_opt,
                mem_pbs_opt, cluster
            )
            # os.system("qsub mex.pbs")
            # print("imaginary frequency handling...")
            stat[2] += 1
            qsub_dir = "./"
            os.remove("tmp.txt")
            return False, stat, qsub_dir
        else:
            find_geom(
                lines,
                error=False,
                filename=filename,
                imaginary=imaginary,
                geomDirName=geomDirName,
            )
            if spec_type == "electronic":
                dir_name = make_exc(
                    method_mexc,
                    basis_set_mexc,
                    mem_com_mexc,
                    mem_pbs_mexc,
                    cluster,
                    geomDirName,
                    SCRF,
                    nStates=nStates,
                    outName=outName
                )
                qsub_dir = dir_name
            elif spec_type == "vibrational":
                dir_name = make_exc(
                    method_mexc,
                    basis_set_mexc,
                    mem_com_mexc,
                    mem_pbs_mexc,
                    cluster,
                    geomDirName,
                    SCRF,
                    spec_type='vibrational',
                    outName=outName
                )
                qsub_dir = dir_name
            else:
                print("spec_type is not supported.")
                return False, stat, 'None'

            stat[1] += 1
            os.remove("tmp.txt")
            return False, stat, qsub_dir

    else:
        print("No output files detected for %s" % (stat[0]))
        return True, stat, "None"
