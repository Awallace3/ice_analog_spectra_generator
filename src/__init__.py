import matplotlib.pyplot as plt

# import error_mexc_v11
from .error_mexc_v11 import main as err_mexc
from .error_mexc_vib import main as err_vib
from .gather_energies import main as gather_energies
from .vibrational_frequencies import overtones as overtones_func
from .vibrational_frequencies import combine_modes_overtones
from .df_latexTable import df_latexTable
from .df_latexTable import latexTable_df
from .ice_build import ice_build
import time
import glob
import os
import pandas as pd
import subprocess
import numpy as np
import scipy.signal
import math
import matplotlib

matplotlib.use("Agg")


def jobResubmit(
    config={
        "enable": {"exc": True, "vib": False},
        "qmgr": {"minDelay": 360, "maxResub": 100},
        "optResub": {
            "optMethod": "B3LYP",
            "optBasisSet": "6-31G(d)",
            "memComFile": "1600",
            "memPBSFile": "15",
        },
        "excCreate": [
            {
                "excMethod": "CAM-B3LYP",
                "excBasisSet": "6-311G(d,p)",
                "memComFile": "1600",
                "memPBSFile": "15",
                "nStates": 25,
                "SCRF": "",
            },
            {
                "excMethod": "CAM-B3LYP",
                "excBasisSet": "6-311G(d,p)",
                "memComFile": "1600",
                "memPBSFile": "15",
                "nStates": 50,
                "SCRF": "",
            },
            {
                "excMethod": "wB97XD",
                "excBasisSet": "6-311G(d,p)",
                "memComFile": "1600",
                "memPBSFile": "15",
                "nStates": 25,
                "SCRF": "",
            },
        ],
        "vibCreate": [
            {
                "excMethod": "CAM-B3LYP",
                "excBasisSet": "6-31+G(d,p)",
                "memComFile": "1600",
                "memPBSFile": "15",
            }
        ],
    },
):
    min_delay = config["qmgr"]["minDelay"]
    number_delays = config["qmgr"]["maxResub"]
    method_opt = config["optResub"]["optMethod"]
    basis_set_opt = config["optResub"]["optBasisSet"]
    mem_com_opt = config["optResub"]["memComFile"]
    mem_pbs_opt = config["optResub"]["memPBSFile"]

    method_mexc = config["excCreate"][0]["excMethod"]
    basis_set_mexc = config["excCreate"][0]["excBasisSet"]
    mem_com_mexc = config["excCreate"][0]["memComFile"]
    mem_pbs_mexc = config["excCreate"][0]["memPBSFile"]
    nStates = config["excCreate"][0]["nStates"]
    SCRF = config["excCreate"][0]["SCRF"]

    min_delay = min_delay * 60
    cluster_list = glob.glob("calc_zone/geom*")
    print(cluster_list)
    complete = []
    resubmissions = []
    for i in range(len(cluster_list)):
        complete.append(0)
        resubmissions.append(2)
    calculations_complete = False

    for i in range(number_delays):

        for num, j in enumerate(cluster_list):
            os.chdir(j)
            print(j)
            delay = i
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

            if method_mexc == "B3LYP":
                mexc_check = glob.glob("mexc" + basis_dir_name)
                path_mexc = "mexc" + basis_dir_name
                print(method_mexc.lower() + basis_dir_name)
            else:
                mexc_check = glob.glob(method_mexc.lower() + basis_dir_name)
                path_mexc = method_mexc.lower() + basis_dir_name
                print(method_mexc.lower() + basis_dir_name)

            # print(mexc_check)
            if len(mexc_check) > 0:
                print("{0} entered mexc checkpoint 1".format(num + 1))
                complete[num] = 1

                # mexc_check_out = glob.glob("mexc/mexc.o*")
                # mexc_check_out_complete = glob.glob("mexc_o/mexc.o*")
                mexc_check_out = glob.glob("%s/mexc.o*" % path_mexc)
                mexc_check_out_complete = glob.glob("%s/mexc_o.o*" % path_mexc)

                # if complete[num] != 2 and len(mexc_check_out) > 1:
                if (
                    complete[num] != 2
                    and len(mexc_check_out) > 0
                    and len(mexc_check_out_complete) > 0
                ):
                    print("{0} entered mexc checkpoint 2".format(num + 1))
                    complete[num] = 2
            if complete[num] < 1:
                action, resubmissions = err_mexc(
                    num,
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
                    nStates,
                    SCRF=SCRF,
                )
                # print(resubmissions)

            mexc_check = []
            os.chdir("../..")
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            if stage == len(complete) * 2:
                calculations_complete = True

        if calculations_complete:
            print(complete)
            print("\nCalculations are complete.")
            print("Took %.2f hours" % (i * min_delay / 60))
            return complete
        print("Completion List\n", complete, "\n")
        print("delay %d" % (i))
        time.sleep(min_delay)
    return complete


def vibrational_resubmit(
    min_delay,
    number_delays,
    method_opt,
    basis_set_opt,
    mem_com_opt,
    mem_pbs_opt,
    method_vib,
    basis_set_vib,
    mem_com_vib,
    mem_pbs_vib,
    SCRF="",
    overall_name="vib",
):
    min_delay = min_delay * 60
    cluster_list = glob.glob("calc_zone/geom*")
    print(cluster_list)
    complete = []
    resubmissions = []
    for i in range(len(cluster_list)):
        complete.append(0)
        resubmissions.append(2)
    calculations_complete = False

    for i in range(number_delays):
        for num, j in enumerate(cluster_list):
            os.chdir(j)
            print(j)
            delay = i
            basis_dir_name = "_vib"
            if basis_set_vib == "6-311G(d,p)":
                pass
            else:
                basis_dir_name = "_" + basis_set_vib

            if SCRF != "":
                basis_dir_name += "_SCRF_%s" % SCRF

            if method_vib == "B3LYP":
                mexc_check = glob.glob("mexc" + basis_dir_name)
                path_mexc = "mexc" + basis_dir_name
                print(method_vib.lower() + basis_dir_name)
            else:
                mexc_check = glob.glob(method_vib.lower() + basis_dir_name)
                path_mexc = method_vib.lower() + basis_dir_name
                print(method_vib.lower() + basis_dir_name)

            # print(mexc_check)
            if len(mexc_check) > 0:
                print("{0} entered mexc checkpoint 1".format(num + 1))
                complete[num] = 1
                mexc_check_out = glob.glob("%s/mexc.o*" % path_mexc)
                mexc_check_out_complete = glob.glob("%s/mexc_o.o*" % path_mexc)

                if (
                    complete[num] != 2
                    and len(mexc_check_out) > 0
                    and len(mexc_check_out_complete) > 0
                ):
                    print("{0} entered mexc checkpoint 2".format(num + 1))
                    complete[num] = 2
            if complete[num] < 1:
                action, resubmissions = err_vib(
                    num,
                    method_opt,
                    basis_set_opt,
                    mem_com_opt,
                    mem_pbs_opt,
                    method_vib,
                    basis_set_vib,
                    mem_com_vib,
                    mem_pbs_vib,
                    resubmissions,
                    delay,
                    "25",
                    SCRF=SCRF,
                    spectroscopy_type="vib",
                    overall_name=overall_name,
                )

            mexc_check = []
            os.chdir("../..")
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            if stage == len(complete) * 2:
                calculations_complete = True

        if calculations_complete:
            print(complete)
            print("\nCalculations are complete.")
            print("Took %.2f hours" % (i * min_delay / 60))
            return complete
        print("Completion List\n", complete, "\n")
        print("delay %d" % (i))
        time.sleep(min_delay)
    return complete


def boltzmannAnalysisSetup(
    complete,
    method_mexc="B3LYP",
    basis_set_mexc="6-311G(d,p)",
    nStates="25",
    acquiredStates="25",
    SCRF="",
):

    analysis_ready = []
    if "results" not in glob.glob("results"):
        os.mkdir("results")
    os.chdir("results")
    if "mexc_values" not in glob.glob("mexc_values"):
        os.mkdir("mexc_values")
        os.chdir("..")
    else:
        os.chdir("..")

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

    if method_mexc == "PBE0":
        path_mexc = method_mexc.lower() + basis_dir_name
        method_mexc = "PBE1PBE"
    elif method_mexc == "wB97XD":
        new_dir = "wb97xd"
        path_mexc = method_mexc.lower() + basis_dir_name
    elif method_mexc == "B3LYP":
        path_mexc = "mexc" + basis_dir_name
        # print("B3LYP here")
    elif method_mexc == "B3LYPD3":
        new_dir = "b3lypd3"
        path_mexc = method_mexc.lower() + basis_dir_name
        method_mexc = "B3lYP empiricaldispersion=gd3 "
    elif method_mexc == "CAM-B3LYP":
        new_dir = "cam-b3lyp"
        path_mexc = method_mexc.lower() + basis_dir_name
        method_mexc = "CAM-B3LYP"
    elif method_mexc == "B97D3":
        new_dir = "b97d3"
        path_mexc = method_mexc.lower() + basis_dir_name
        method_mexc = "B97D3"
    else:
        print("This method is not supported for TD-DFT yet.")

    path_mexc = path_mexc.replace("(", "\(").replace(")", "\)")

    print("\nPATH:::", path_mexc)

    for i in range(len(complete)):
        if complete[i] == 2:
            analysis_ready.append(i)
        else:
            # print('geom%d/mexc %d is not finished with TD-DFT' % (i+1, i+1))
            print(
                "geom%d/%s %d is not finished with TD-DFT" % (i + 1, path_mexc, i + 1)
            )
    os.chdir("calc_zone")
    for i in analysis_ready:

        cmd = (
            """awk '/Excited State/ {print $7, $9}' geom%d/%s/mexc.out | sed 's/f=//g' | tac | tail -n %s > ../results/mexc_values/mexc_out%d.csv"""
            % (i + 1, path_mexc, acquiredStates, i + 1)
        )

        failure = subprocess.call(cmd, shell=True)
    os.chdir("..")
    return


def boltzmannAnalysis(
    T, energy_levels="electronic", DeltaN="2", x_range=[50, 4100], overtones=False
):
    if energy_levels == "electronic":
        os.chdir("results/mexc_values")
        csv_name = "mexc_out"
        cmd = "perl ../../../src/specsim.pl"
    elif energy_levels == "vibrational":
        os.chdir("results/vibrational_values")
        csv_name = "vib"
        cmd = "perl ../../../src/specsim_xrange.pl 50 4100"
        cmd = "perl ../../../src/specsim_args.pl %d %d %s" % (
            x_range[0],
            x_range[1],
            DeltaN,
        )
    # print(os.getcwd())
    mexc_out_names = glob.glob("*.csv")
    # print(mexc_out_names)
    mexc_dict = {}
    # print(mexc_out_names)
    for i in mexc_out_names:
        val = i[:-4]
        # print("val")
        # print(val)
        # print(np.genfromtxt(i, delimiter=" "))
        mexc_dict["{0}".format(val)] = np.genfromtxt(i, delimiter=" ")
    os.chdir("../energies")
    energy_all = np.genfromtxt("energy_all.csv", delimiter=",")
    energy_all = energy_all[np.argsort(energy_all[:, 0])]
    lowest_energy = np.amin(energy_all[:, 1])
    lowest_energy_ind = (np.where(energy_all[:, 1] == lowest_energy))[0][0]
    print("LOWEST_ENERGY", lowest_energy, "hartrees")
    lowest_energy = lowest_energy * 4.3597e-18  # convert hartrees to joules
    kb = 1.380649e-23

    # combining_mexc = mexc_dict['mexc_out{0}'.format(lowest_energy_ind+1)]
    combining_mexc = mexc_dict["{0}".format(csv_name + str(lowest_energy_ind + 1))]

    # print(combining_mexc)
    # print("energy_all:\n", energy_all)
    for key, value in mexc_dict.items():
        if key == "mexc_out{0}".format(lowest_energy_ind + 1):
            continue
        # print(key) # crashes if not all mexc_out*.csv accounted for
        # remember energy_all array index starts at zero
        if energy_levels == "electronic":
            current_energy_ind = int(key[8:]) - 1
        elif energy_levels == "vibrational":
            current_energy_ind = int(key[3:]) - 1
        # print(current_energy_ind)
        # find current energy and convert hartrees to joules
        current_energy = ((energy_all[current_energy_ind, :])[1]) * 4.3597e-18

        # print(lowest_energy)
        # print(current_energy)

        ni_nj = math.exp((lowest_energy - current_energy) / (T * kb))
        """
        print("n%d / n%d = %.10f" %
              (lowest_energy_ind+1, current_energy_ind + 1, ni_nj))
        """
        for i in range(len(value)):

            value[i][1] = value[i][1] * ni_nj
            # print(value[i][1])
            # print(value[i])
        # if want only certain number randomly, modify here
        combining_mexc = np.concatenate((combining_mexc, value), axis=0)
    # print(combining_mexc)

    # os.chdir("../final/data")
    os.chdir("..")
    if "final" not in glob.glob("final"):
        os.mkdir("final")
    os.chdir("final")
    if "data" not in glob.glob("data"):
        os.mkdir("data")
    os.chdir("data")

    np.savetxt("data", combining_mexc, fmt="%s")
    subprocess.call(cmd, shell=True)

    if overtones:
        x, y = collectSpecSimData(x_units="cm-1", path_to_data="./")

        arr_y = np.array(y)
        print("local maxima")
        peaks_dat, _ = scipy.signal.find_peaks(arr_y, height=0)
        with open("extra_bands", "w") as fp:
            for j in peaks_dat:
                # print(round(x[i],2), arr_y[i])
                height = arr_y[j]
                frequency = round(x[j], 4)
                fp.write(str(height) + " " + str(frequency) + "\n")

        a = overtones_func("extra_bands", T=T)
        a = combine_modes_overtones("spec", a)
        # time_data
        np.savetxt("data", a, fmt="%s")
        subprocess.call(cmd, shell=True)

    os.chdir("../../../")
    return


def generateGraph(
    spec_name, T, title, filename, x_range=[100, 300], x_units="nm", peaks=False
):
    # print(os.getcwd())
    fig, ax1 = plt.subplots()

    data = np.genfromtxt("results/final/data/" + spec_name, delimiter=" ")
    data = data.tolist()
    # print(data)
    x = []
    y = []
    highest_y = 0
    for i in data:
        # print(i)
        x.append(i[0])
        y.append(i[1])
        if i[1] > highest_y:
            highest_y = i[1]

    for i in range(len(y)):
        y[i] /= highest_y
    if x_units == "eV" or x_units == "ev":
        h = 6.626e-34
        c = 3e17
        ev_to_joules = 1.60218e-19
        x = [h * c / (i * ev_to_joules) for i in x]
        x.reverse()
        y.reverse()
    elif x_units == "cm-1":
        x.reverse()
        y.reverse()
        # maxima = scipy.signal.argrelextrema(y, np.greater)

    # print(x)
    # print('\n', y)
    ax1.plot(x, y, "k-", label="T = {0} K".format(T))
    # ax1.set_xlim([x[0], x[-1]])
    ax1.set_xlim(x_range)
    ax1.set_ylim(0, 1.4)

    plt.title(title)
    if x_units == "ev" or x_units == "eV":
        plt.xlabel("Electronvolts (eV)")
        ax1.legend(shadow=True, fancybox=True)
        if peaks:
            arr_y = np.array(y)
            print("local maxima")
            peaks, _ = scipy.signal.find_peaks(arr_y, height=0)
            for i in peaks:
                print(round(x[i], 2), arr_y[i])
                height = arr_y[i]
                frequency = round(x[i], 2)
                if height > 0.02:
                    plt.text(frequency - 0.08, arr_y[i] + 0.05, "%.2f" % frequency)

    elif x_units == "cm-1":
        plt.xlabel(r"Wavenumbers cm$^{-1}$")
        if peaks:
            arr_y = np.array(y)
            print("local maxima")
            peaks, _ = scipy.signal.find_peaks(arr_y, height=0)
            for i in peaks:
                print(round(x[i]), arr_y[i])
                height = arr_y[i]
                frequency = round(x[i])
                if height > 0.02:
                    plt.text(frequency + 100, arr_y[i] + 0.1, "%d" % frequency)
    else:
        plt.xlabel("Wavelength (nm)")
        ax1.legend(shadow=True, fancybox=True)

    plt.ylabel("Oscillator Strength")
    # plt.grid(b=None, which='major', axis='y', linewidth=1)
    # plt.grid(b=None, which='major', axis='x', linewidth=1)
    # os.chdir("results/final/graphs")
    os.chdir("results/final")
    if "graphs" not in glob.glob("graphs"):
        os.mkdir("graphs")
    if x_units == "cm-1":
        ax1.yaxis_inverted()
    os.chdir("graphs")
    plt.savefig(filename)
    os.chdir("../../..")

    return


def collectSpecSimData(
    x_units="eV", spec_name="spec", normalize=True, path_to_data="results/final/data/"
):
    data = np.genfromtxt(path_to_data + spec_name, delimiter=" ")
    data = data.tolist()
    # print(data)
    x = []
    y = []
    highest_y = 0
    for i in data:
        # print(i)
        x.append(i[0])
        y.append(i[1])
        if i[1] > highest_y:
            highest_y = i[1]

    print(highest_y, "HIGHEST")
    cam_b3lyp_n125_y = 4.98005616
    # cam_b3lyp_n125_y = 1.9835017
    # cam_b3lyp_n125_y = 10.17985964

    # print("CAM-B3LYP:", highest_y)
    for i in range(len(y)):
        y[i] /= highest_y
        # y[i] /= cam_b3lyp_n125_y
    if x_units == "eV" or x_units == "ev":
        h = 6.626e-34
        c = 3e17
        ev_to_joules = 1.60218e-19
        x = [h * c / (i * ev_to_joules) for i in x]
        x.reverse()
        y.reverse()
    elif x_units == "cm-1":
        x.reverse()
        y.reverse()
        # maxima = scipy.signal.argrelextrema(y, np.greater)
    return x, y


def latexTable_addLine(path, line):
    if os.path.exists(path):
        with open(path, "r") as fp:
            lines = fp.readlines()
            lines.insert(-4, "\t" + line)

        with open(path, "w") as fp:
            for i in lines:
                fp.write(i)
    else:
        with open(path, "w") as fp:
            fp.write("\\begin{center}\n\\begin{tabular}{ |c|c|c|c| }\n\t\\hline\n")
            fp.write("\tMethod & Basis Set & Excitation (eV) &")
            fp.write(
                "\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}\\\\\n\t\\hline\n"
            )
            fp.write("\t" + line)
            fp.write("\t\\hline\n\\end{tabular}\n\\end{center}")


def electronicMultiPlot(
    methods_lst,
    T,
    title,
    filename,
    x_range=[2, 16],
    x_units="eV",
    peaks=False,
    spec_name="spec",
    complete=[],
    basis_set_mexc="6-31G(d,p)",
    nStates="25",
):

    location = os.getcwd().split("/")[-1]
    if location == "src" or location == "calc_zone":
        os.chdir("..")

    # only pass blank complete if all TD-DFT calculations are complete since it is assumed
    if complete == []:
        num_geom = glob.glob("calc_zone/geom*")
        for i in range(len(num_geom)):
            complete.append(2)

    fig, ax1 = plt.subplots()

    if peaks:
        print(os.path.exists("latex_df_6-311++G(2d,2p)"))
        if os.path.exists("latex_df_6-311++G(2d,2p).tex"):

            headers = [
                "Method",
                "Basis Set",
                "Excitation (eV)",
                "\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}",
            ]
            df = latexTable_df("latex_df_6-311++G(2d,2p).tex", headers)
        elif os.path.exists("latex_df_6-311G(d,p).tex"):
            headers = [
                "Method",
                "Basis Set",
                "Excitation (eV)",
                "\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}",
            ]
            df = latexTable_df("latex_df_6-311G(d,p).tex", headers)

        else:
            df = {
                "Method": [],
                "Basis Set": [],
                "Excitation (eV)": [],
                "\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}": [],
            }  # 4 col
            df = pd.DataFrame(df)

    for i in methods_lst:
        gather_energies()
        boltzmannAnalysisSetup(complete, i, basis_set_mexc, nStates, nStates)
        boltzmannAnalysis(T, energy_levels="electronic")
        x, y = collectSpecSimData(x_units=x_units)
        """
        if i == 'B3LYP':
            print(x, y)
        """
        ax1.plot(x, y, "-", label="%s" % i)

        if peaks:
            arr_y = np.array(y)
            print("local maxima")
            peaks_dat, _ = scipy.signal.find_peaks(arr_y, height=0)
            for j in peaks_dat:
                # print(round(x[i],2), arr_y[i])
                height = arr_y[j]
                frequency = round(x[j], 2)
                print("x, y = %.2f, %.2f" % (frequency, height))
                line = "%s & %s & %.2f & %.2f \\\\\n" % (
                    i,
                    basis_set_mexc,
                    frequency,
                    height,
                )
                latexTable_addLine("latexTable.tex", line)
                df.loc[len(df.index)] = [i, basis_set_mexc, frequency, height]
                """
                with open('latexTabel.tex', 'a') as fp:
                    fp.write("%s/%s,%.2f,%.2f\n" % (i, basis_set_mexc, frequency, height))
                print(os.getcwd())
                """

                """
                if height > 0.02:
                    plt.text(frequency - 0.08, arr_y[i]+0.05, '%.2f' % frequency )
                """
            df_latexTable("latex_df_%s.tex" % basis_set_mexc, df)

    # ax1.set_xlim([x[0], x[-1]])
    ax1.set_xlim(x_range)
    ax1.set_ylim(0, 1.4)

    plt.title(title)
    if x_units == "ev" or x_units == "eV":
        # print(x)
        plt.xlabel("Electronvolts (eV)")
        ax1.legend(shadow=True, fancybox=True, loc="upper right")

    elif x_units == "cm-1":
        plt.xlabel(r"Wavenumbers cm$^{-1}$")

    else:
        plt.xlabel("Wavelength (nm)")
        ax1.legend(shadow=True, fancybox=True)

    plt.ylabel("Oscillator Strength")
    plt.grid(b=None, which="major", axis="y", linewidth=1)
    plt.grid(b=None, which="major", axis="x", linewidth=1)
    # os.chdir("results/final/graphs")
    os.chdir("results/final")
    if "graphs" not in glob.glob("graphs"):
        os.mkdir("graphs")
    os.chdir("graphs")
    plt.savefig(filename)
    os.chdir("../../..")


def electronicMultiPlotExpSetup(
    config={
        "enable": True,
        "temperature": 273.15,
        "type": "exc",
        "output": {
            "numerical": {
                "enable": True, "type": "json", "outFile": "tmp.json"
                },
            "plot": {
                "enable": True,
                "range": {"x": [1, 12], "y": [0, 1]},
                "x_units": "eV",
                "fileName": "data",
                "title": "",
                "excColors": ["red", "green"],
                "exp": {
                    "enable": True,
                    "expData": [
                        {
                            "path": "exp_data/nh3_gas.csv",
                            "units": {"input": "nm", "output": "eV"},
                            "line": {"color": "black", "type": "dotted"},
                        },
                        {
                            "path": "exp_data/nh3_solid.csv",
                            "units": {"input": "nm", "output": "eV"},
                            "line": {"color": "black", "type": "line"},
                        },
                    ],
                },
            },
        },
        "excList": [
            {
                "excMethod": "CAM-B3LYP",
                "excBasisSet": "6-311G(d,p)",
                "nStates": 25,
                "acquiredStates": "25",
                "SCRF": "",
            },
            {
                "excMethod": "wB97XD",
                "excBasisSet": "6-31G(d,p)",
                "nStates": 25,
                "acquiredStates": "25",
                "SCRF": "",
            },
        ],
    }
):
    methods_lst = []
    nStates = ""
    basis_set_mexc = ""
    SCRF = ""
    # colors = config["output"]["plot"]["excColors"]
    colors = []
    methods_lst = config['output']['plot']["dft"]["excList"]
    # for n, i in enumerate(config['output']['plot']["dft"]["excList"]):
    #     print(i)
    #     if n == 0:
    #         nStates = str(i["nStates"])
    #         acquiredStates = str(i["acquiredStates"])
    #         basis_set_mexc = i["excBasisSet"]
    #         SCRF = i["SCRF"]
    #     methods_lst.append(i["excMethod"])
    #     colors.append(i["color"])
    T = config["temperature"]
    title = config["output"]["plot"]["title"]
    x_range = config["output"]["plot"]["range"]["x"]
    x_units = config["output"]["plot"]["x_units"]
    # y_range = config["output"]["plot"]["range"]["y"]
    peaks = {
            "exp": config["output"]["plot"]["exp"]["peaks"],
            "dft": config["output"]["plot"]["dft"]["peaks"],
            }
    spec_name = "spec"
    complete = []
    filename = config["output"]["plot"]["fileName"]

    exp_data = []
    if config["output"]["plot"]["exp"]["enable"]:
        exp_data = config["output"]["plot"]["exp"]["expData"]

    dpi = config["output"]["plot"]["dpi"]
    legendLabelBasisSet = config["output"]["plot"]["dft"]["legendLabelBasisSet"]

    electronicMultiPlot_Experiment(
        methods_lst,
        T,
        title,
        filename,
        x_range,
        x_units,
        peaks,
        spec_name,
        complete,
        exp_data,
        colors,
        sec_y_axis=True,
        rounding=1,
        extra_data=np.array([[-1, -1]]),
        dpi=dpi,
        legendLabelBasisSet=legendLabelBasisSet,
    )


def electronicMultiPlot_Experiment(
    methods_lst,
    T,
    title,
    filename,
    x_range=[2, 16],
    x_units="eV",
    peaks={
        "exp": False,
        "dft": False,
        },
    spec_name="spec",
    complete=[],
    exp_data=[],
    colors=[],
    sec_y_axis=False,
    rounding=1,
    extra_data=np.array([[-1, -1]]),
    dpi=400,
    legendLabelBasisSet=True
):

    location = os.getcwd().split("/")[-1]
    if location == "src" or location == "calc_zone":
        os.chdir("..")

    # only pass blank complete if all TD-DFT calculations are complete since
    # it is assumed
    if complete == []:
        num_geom = glob.glob("calc_zone/geom*")
        for i in range(len(num_geom)):
            complete.append(2)

    fig, ax1 = plt.subplots(dpi=dpi)

    if peaks['dft']:
        if os.path.exists("peaks.tex"):
            headers = [
                "Method",
                "Basis Set",
                "Excitation (eV)",
                "\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}",
            ]
            df = latexTable_df("peaks.tex", headers)
        else:
            df = {
                "Method": [],
                "Basis Set": [],
                "Excitation (eV)": [],
                "\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}": [],
            }  # 4 col
            df = pd.DataFrame(df)

    for n, i in enumerate(methods_lst):
        print(i)
        basis_set_mexc = i["excBasisSet"]
        method = i["excMethod"]
        nStates = str(i["nStates"])
        acquiredStates = str(i["acquiredStates"])
        SCRF = i["SCRF"]
        color = i["line"]["color"]
        l_type = i["line"]["type"]

        gather_energies()
        boltzmannAnalysisSetup(
            complete, method, basis_set_mexc, nStates, acquiredStates, SCRF
        )
        boltzmannAnalysis(T, energy_levels="electronic")
        x, y = collectSpecSimData(x_units=x_units)

        if method == "wB97XD":
            method = r"$\omega$B97XD"
        if legendLabelBasisSet:
            label = method + '/' + basis_set_mexc
        else:
            label = method
        ax1.plot(
                x, y,
                l_type, c=color,
                label=label,
                zorder=2
                )

        if peaks["dft"]:
            arr_y = np.array(y)
            print("local maxima")
            peaks_dat, _ = scipy.signal.find_peaks(arr_y, height=0)
            for j in peaks_dat:
                # print(round(x[i],2), arr_y[i])
                height = arr_y[j]
                frequency = round(x[j], 4)
                if rounding == 1:
                    print("x, y = %.1f, %.1f" % (frequency, height))
                    line = "%s & %s & %.1f & %.1f \\\\\n" % (
                        method,
                        basis_set_mexc,
                        frequency,
                        height,
                    )
                elif rounding == 2:
                    print("x, y = %.2f, %.2f" % (frequency, height))
                    line = "%s & %s & %.2f & %.2f \\\\\n" % (
                        method,
                        basis_set_mexc,
                        frequency,
                        height,
                    )
                else:
                    print("x, y = %.4f, %.4f" % (frequency, height))
                    line = "%s & %s & %.4f & %.4f \\\\\n" % (
                        method,
                        basis_set_mexc,
                        frequency,
                        height,
                    )

                # latexTable_addLine('latexTable.tex', line)
                df.loc[len(df.index)] = [i, basis_set_mexc, frequency, height]
            df_latexTable("latex_df_%s.tex" % basis_set_mexc, df, rounding)

    ax2 = ax1.twinx()

    if len(exp_data) > 0:
        for n, i in enumerate(exp_data):
            print(i)
            dat = np.genfromtxt(i["path"], delimiter=", ")
            In = i["units"]["input"]
            Out = i["units"]["output"]
            if In == "nm" and Out == "eV":
                dat = nmLst_evLst(dat)
            elif In == "eV" and Out == "nm":
                dat = nmLst_evLst(dat)
            ymax = np.amax(dat[:, 1], axis=0)
            dat[:, 1] /= ymax
            # print(i)
            ax2.plot(
                dat[:, 0],
                dat[:, 1],
                i["line"]["type"],
                c=i["line"]['color'],
                label=i['legendLabel'],
                zorder=2,
            )
            if peaks['exp']:
                arr_y = dat[:, 1]
                print("local maxima")
                peaks_dat, _ = scipy.signal.find_peaks(arr_y, height=0)
                for j in peaks_dat:
                    # print(round(x[i],2), arr_y[i])
                    height = arr_y[j]
                    frequency = round(dat[j, 0], 2)
                    print("x, y = %.2f, %.2f" % (frequency, height))
                    line = "%s & %s & %.2f & %.2f \\\\\n" % (
                        i['legendLabel'],
                        basis_set_mexc,
                        frequency,
                        height,
                    )
                    # latexTable_addLine('latexTable.tex', line)
                    df.loc[len(df.index)] = [
                        i['legendLabel'],
                        basis_set_mexc,
                        frequency,
                        height,
                    ]
                df_latexTable("latex_df_%s.tex" % basis_set_mexc, df, rounding)
    # ax1.set_xlim([x[0], x[-1]])
    if extra_data[0, 0] != -1 and extra_data[0, 1] != -1:
        print("\n extra data\n")
        ymax = np.amax(extra_data[:, 1], axis=0)
        for i in range(len(extra_data[:, 1])):
            extra_data[i, 1] /= ymax

        ax1.plot(
            extra_data[:, 0],
            extra_data[:, 1],
            "-",
            label="CAM-B3LYP (Ribbon Octamer)",
            color="blue",
        )
        if peaks['dft']:
            arr_y = extra_data[:, 1]
            arr_x = extra_data[:, 0]
            print(arr_y)
            peaks_dat, _ = scipy.signal.find_peaks(arr_y, height=0)
            print(peaks_dat)
            for j in peaks_dat:
                # print(round(x[i],2), arr_y[i])
                height = arr_y[j]
                frequency = round(arr_x[j], 4)

                print("x, y = %.1f, %.1f\n" % (frequency, height))
                df.loc[len(df.index)] = ["8 Ribbon", basis_set_mexc, frequency, height]

    if sec_y_axis:
        # ax2.set_ylabel(r"Cross Section / cm$^2$ (Normalized)")
        ax2.set_ylim(0, 1.5)

    ax1.set_xlim(x_range)
    ax1.set_ylim(0, 1.5)

    plt.title(title)
    ax1.legend(shadow=True, fancybox=True, loc="upper left")
    ax2.legend(shadow=True, fancybox=True, loc="upper right")
    if x_units == "ev" or x_units == "eV":
        # print(x)
        plt.xlabel("Electronvolts (eV)")
        ax1.set_xlabel("Electronvolts (eV)")
        # ax1.legend(shadow=True, fancybox=True)

    elif x_units == "cm-1":
        plt.xlabel(r"Wavenumbers cm$^{-1}$")

    else:
        plt.xlabel("Wavelength (nm)")
        # ax1.legend(shadow=True, fancybox=True)

    ax1.set_ylabel("Oscillator Strength")
    # plt.grid(zorder=0, b=None, which='major', axis='y', linewidth=1)
    # plt.grid(zorder=0, b=None, which='major', axis='x', linewidth=1)
    # os.chdir("results/final/graphs")
    os.chdir("results/final")
    if "graphs" not in glob.glob("graphs"):
        os.mkdir("graphs")
    os.chdir("graphs")
    plt.savefig(filename)

    os.chdir("../../..")


def method_update_selection(methods_lst, basis_set_mexc, nStates, SCRF=""):
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
    for n, i in enumerate(methods_lst):
        if i == "B3LYP":
            i = "mexc" + basis_dir_name
            print(i.lower() + basis_dir_name)
        else:
            i = i.lower() + basis_dir_name
            print(i.lower() + basis_dir_name)
        methods_lst[n] = i
    return methods_lst


def sort_data(data):
    return data[data[:, 0].argsort()]


def nmLst_evLst(nmData):
    h = 6.62607004e-34
    c = 299792458
    c = 3e17
    Joules_to_eV = 1.602e-19

    for i in range(len(nmData[:, 0])):
        nmData[i, 0] = h * c / (nmData[i, 0] * Joules_to_eV)
    nmData = nmData[nmData[:, 0].argsort()]
    return nmData


def testing(val=1):
    print(val)
