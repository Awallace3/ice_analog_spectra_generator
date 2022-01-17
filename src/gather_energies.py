import os
import glob
import subprocess
from .job_progression import get_final_out


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
        if hf_1[0] > hf_2[0]:
            return float(hf_1[0]) + zero_point, hf_1[0]
        else:
            return float(hf_2[0]) + zero_point, hf_2[0]
    else:
        return float(hf_1[0]) + zero_point, hf_1[0]


def main():
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
    lowest_energy = [0, 0, 0]
    cmd = "rm ../results/energies/energy_all.csv"
    subprocess.call(cmd, shell=True)
    for i in directories:
        n = i[4:]
        os.chdir(i)
        out_files = glob.glob("*.out*")
        out_completion = glob.glob("mex_o.*")
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
            f = open(filename, "r")
            lines = f.readlines()
            f.close()

            freq, hf_1, hf_2, zero_point = freq_hf_zero(
                lines, filename=filename
            )
            sum_energy, hf = clean_energies(hf_1, hf_2, zero_point)
            if sum_energy < lowest_energy[2]:
                lowest_energy = [hf, zero_point, sum_energy]

            path = "../../results/energies/"
            f = open(path + "energy%s.txt" % n, "w")
            f.write(str(sum_energy))
            f.close()
            line = "%s,%s\n" % (n, sum_energy)
            f = open(path + "energy_all.csv", "a")
            f.write(line)
            f.close()
            os.chdir("..")
    os.chdir("..")


def gather_default(path):
    def_dir = os.getcwd()
    path_r_e = def_dir + "/results/energies"

    if not os.path.exists(path_r_e):
        os.mkdir(path_r_e)
    cmd = "rm %s/energy_all.csv" % path_r_e
    subprocess.call(cmd, shell=True)

    os.chdir(path)
    directories = glob.glob("geom*")
    lowest_energy = [0, 0, 0]
    for i in directories:
        n = i[4:]
        os.chdir(i)
        out_files = glob.glob("*.out*")
        if len(out_files) > 0:
            filename = get_final_out(out_files)
            f = open(filename, "r")
            lines = f.readlines()
            f.close()
            freq, hf_1, hf_2, zero_point = freq_hf_zero(
                lines, filename=filename
            )
            sum_energy, hf = clean_energies(hf_1, hf_2, zero_point)
            if sum_energy < lowest_energy[2]:
                lowest_energy = [hf, zero_point, sum_energy]
            f = open(path_r_e + "/energy%s.txt" % n, "w")
            f.write(str(sum_energy))
            f.close()
            line = "%s,%s\n" % (n, sum_energy)
            f = open(path_r_e + "/energy_all.csv", "a")
            f.write(line)
            f.close()
        os.chdir("..")
    os.chdir(def_dir)
