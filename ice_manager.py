import matplotlib.pyplot as plt
from src import ice_build_geoms
#from src import error_mexc_v9
from src import error_mexc_v11
from src import gather_energies
from src import vibrational_frequencies
from src import df_latexTable as df_latex
from src import discrete_to_art as dis_art
import time
import glob
import os
import sys
import pandas as pd
import subprocess
import numpy as np
import scipy.signal
import math
import matplotlib
matplotlib.use('Agg')
# print(sys.path)

# NEED TO CHECK IF Q SUBMITTED BEFORE RESUBMITTING


def jobResubmit(min_delay, number_delays,
                method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                nStates
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
            if basis_set_mexc == '6-311G(d,p)':
                basis_dir_name = ''
            else:
                basis_dir_name = '_' + basis_set_mexc
            
            if nStates == '25':
                pass
            else:
                basis_dir_name += '_n%s' % nStates

            if method_mexc == 'B3LYP':
                mexc_check = glob.glob("mexc" + basis_dir_name)
                path_mexc = 'mexc' + basis_dir_name
                print(method_mexc.lower() + basis_dir_name)
            else:
                mexc_check = glob.glob(method_mexc.lower() + basis_dir_name)
                path_mexc = method_mexc.lower() + basis_dir_name
                print(method_mexc.lower() + basis_dir_name)

            #print(mexc_check)
            if len(mexc_check) > 0:
                print('{0} entered mexc checkpoint 1'.format(num+1))
                complete[num] = 1

                #mexc_check_out = glob.glob("mexc/mexc.o*")
                #mexc_check_out_complete = glob.glob("mexc_o/mexc.o*")
                mexc_check_out = glob.glob("%s/mexc.o*" % path_mexc)
                mexc_check_out_complete = glob.glob("%s/mexc_o.o*" % path_mexc)

                #if complete[num] != 2 and len(mexc_check_out) > 1:
                if complete[num] != 2 and len(mexc_check_out) > 0 and len(mexc_check_out_complete) > 0:
                    print('{0} entered mexc checkpoint 2'.format(num+1))
                    complete[num] = 2
            if complete[num] < 1:
                action, resubmissions = error_mexc_v11.main(
                    num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                    method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                    resubmissions, delay, nStates
                )
                #print(resubmissions)
           
            mexc_check = []
            os.chdir('../..')
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            if stage == len(complete)*2:
                calculations_complete = True

        if calculations_complete == True:
            print(complete)
            print('\nCalculations are complete.')
            print('Took %.2f hours' % (i*min_delay / 60))
            return complete
        print('Completion List\n', complete, '\n')
        print('delay %d' % (i))
        time.sleep(min_delay)
    return complete


def boltzmannAnalysisSetup(complete, method_mexc='B3LYP', 
                basis_set_mexc='6-311G(d,p)', nStates='25', acquiredStates='25'):

    analysis_ready = []
    if "results" not in glob.glob("results"):
        os.mkdir("results")
    os.chdir("results")
    if "mexc_values" not in glob.glob("mexc_values"):
        os.mkdir("mexc_values")
        os.chdir("..")
    else:
        os.chdir("..")
    
    if basis_set_mexc == '6-311G(d,p)':
        basis_dir_name = ''
    else:
        basis_dir_name = '_' + basis_set_mexc
    
    if nStates == '25':
        pass
    else:
        basis_dir_name += '_n%s' % nStates

    if method_mexc == 'PBE0':
        path_mexc = method_mexc.lower() + basis_dir_name
        method_mexc = 'PBE1PBE'
    elif method_mexc == 'wB97XD':
        new_dir = "wb97xd"
        path_mexc = method_mexc.lower()+ basis_dir_name
    elif method_mexc == 'B3LYP':
        path_mexc = "mexc" + basis_dir_name
        #print("B3LYP here")
    elif method_mexc == 'B3LYPD3':
        new_dir = 'b3lypd3'
        path_mexc = method_mexc.lower()+ basis_dir_name
        method_mexc = 'B3lYP empiricaldispersion=gd3 '
    elif method_mexc == 'CAM-B3LYP':
        new_dir = 'cam-b3lyp'
        path_mexc = method_mexc.lower()+ basis_dir_name
        method_mexc = 'CAM-B3LYP'
    elif method_mexc == 'B97D3':
        new_dir = 'b97d3'
        path_mexc = method_mexc.lower()+ basis_dir_name
        method_mexc = 'B97D3'
    else:
        print("This method is not supported for TD-DFT yet.")
    
    path_mexc = path_mexc.replace("(", "\(").replace(")", "\)")

    print("\nPATH::: ", path_mexc, method_mexc)

    for i in range(len(complete)):
        if complete[i] == 2:
            analysis_ready.append(i)
        else:
            #print('geom%d/mexc %d is not finished with TD-DFT' % (i+1, i+1))
            print('geom%d/%s %d is not finished with TD-DFT' % (i+1, path_mexc, i+1))
    os.chdir("calc_zone")
    for i in analysis_ready:
        
        #cmd = '''awk '/Excited State/ {print $7, $9}' geom%d/%s/mexc.out | sed 's/f=//g' > ../results/mexc_values/mexc_out%d.csv''' % (
        #    i+1, path_mexc, i+1)
        cmd = '''awk '/Excited State/ {print $7, $9}' geom%d/%s/mexc.out | sed 's/f=//g' | tac | tail -n %s > ../results/mexc_values/mexc_out%d.csv''' % (
            i+1, path_mexc, acquiredStates, i+1)
        
        failure = subprocess.call(cmd, shell=True)
    os.chdir("..")
    print(cmd)
    print('\nBoltzmann Analysis Setup Complete.\n')
    return


def boltzmannAnalysis(T, energy_levels='electronic', DeltaN='2', x_range=[50, 4100], overtones=False):
    if energy_levels == 'electronic':
        os.chdir('results/mexc_values')
        csv_name = 'mexc_out'
        cmd = "perl ../../../src/specsim.pl"
    elif energy_levels == 'vibrational':
        os.chdir('results/vibrational_values')
        csv_name = 'vib'
        cmd = "perl ../../../src/specsim_xrange.pl 50 4100"
        cmd = "perl ../../../src/specsim_args.pl %d %d %s" % (x_range[0], x_range[1], DeltaN)
    #print(os.getcwd())
    mexc_out_names = glob.glob("*.csv")
    #print(mexc_out_names)
    mexc_dict = {}
    #print(mexc_out_names)
    for i in mexc_out_names:
        val = i[:-4]
        #print("val")
        #print(val)
        #print(np.genfromtxt(i, delimiter=" "))
        mexc_dict['{0}'.format(val)] = np.genfromtxt(i, delimiter=" ")
    os.chdir('../energies')
    energy_all = np.genfromtxt('energy_all.csv', delimiter=",")
    energy_all = energy_all[np.argsort(energy_all[:, 0])]
    lowest_energy = np.amin(energy_all[:, 1])
    lowest_energy_ind = (np.where(energy_all[:, 1] == lowest_energy))[0][0]
    print("LOWEST_ENERGY", lowest_energy)
    lowest_energy = lowest_energy * 4.3597E-18  # convert hartrees to joules
    print("lowest energy:", lowest_energy, lowest_energy_ind)
    kb = 1.380649E-23
    
    #combining_mexc = mexc_dict['mexc_out{0}'.format(lowest_energy_ind+1)]
    combining_mexc = mexc_dict['{0}'.format(csv_name + str(lowest_energy_ind+1))]

    # print(combining_mexc)
    #print("energy_all:\n", energy_all)
    for key, value in mexc_dict.items():
        if key == 'mexc_out{0}'.format(lowest_energy_ind+1):
            continue
        #print(key) # crashes if not all mexc_out*.csv accounted for
        # remember energy_all array index starts at zero
        if energy_levels == 'electronic':
            current_energy_ind = int(key[8:]) - 1
        elif energy_levels == 'vibrational':
            current_energy_ind = int(key[3:]) - 1
        #print(current_energy_ind)
        # find current energy and convert hartrees to joules
        current_energy = ((energy_all[current_energy_ind, :])[1]) * 4.3597E-18

        #print(lowest_energy)
        #print(current_energy)

        ni_nj = math.exp((lowest_energy - current_energy) / (T * kb))
        '''
        print("n%d / n%d = %.10f" %
              (lowest_energy_ind+1, current_energy_ind + 1, ni_nj))
        '''
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
    print("\ndata file made for specsim.pl\n")
    subprocess.call(cmd, shell=True)
    
    if overtones:
        x, y = collectSpecSimData(x_units='cm-1', path_to_data='./')        
        
        arr_y = np.array(y)
        print("local maxima")
        peaks_dat, _ = scipy.signal.find_peaks(arr_y, height=0)
        with open("extra_bands", 'w') as fp:
            for j in peaks_dat:
                #print(round(x[i],2), arr_y[i])
                height = arr_y[j]
                frequency = round(x[j], 4)
                fp.write(str(height) + ' ' + str(frequency) + '\n')
        
        a = vibrational_frequencies.overtones('extra_bands', T=T)
        a = vibrational_frequencies.combine_modes_overtones('spec', a)
        #time_data
        np.savetxt("data", a, fmt="%s")
        print("\ndata file made for specsim.pl after overtones\n")
        subprocess.call(cmd, shell=True)
            
    os.chdir("../../../")
    return


def generateGraph(spec_name, T, title, filename, x_range=[100,300], x_units='nm', peaks=False):
    #print(os.getcwd())
    fig, ax1 = plt.subplots()

    data = np.genfromtxt("results/final/data/" + spec_name, delimiter=" ")
    data = data.tolist()
    # print(data)
    x = []
    y = []
    highest_y = 0
    for i in data:
        #print(i)
        x.append(i[0])
        y.append(i[1])
        if i[1] > highest_y:
            highest_y = i[1]
    
    for i in range(len(y)):
        y[i] /= highest_y
    if x_units == 'eV' or x_units=='ev':
        h = 6.626E-34
        c = 3E17
        ev_to_joules = 1.60218E-19
        x = [ h*c/(i*ev_to_joules) for i in x ]
        x.reverse()
        y.reverse()
    elif x_units == 'cm-1':
        x.reverse()
        y.reverse()
        #maxima = scipy.signal.argrelextrema(y, np.greater)
        
    # print(x)
    #print('\n', y)
    ax1.plot(x, y, "k-", label="T = {0} K".format(T))
    #ax1.set_xlim([x[0], x[-1]])
    ax1.set_xlim(x_range)
    ax1.set_ylim(0, 1.2)

    plt.title(title)
    if x_units == 'ev' or x_units=='eV':
        plt.xlabel("Electronvolts (eV)")
        ax1.legend(shadow=True, fancybox=True)
        if peaks:
            arr_y = np.array(y)
            print("local maxima")
            peaks, _ = scipy.signal.find_peaks(arr_y, height=0)
            for i in peaks:
                print(round(x[i],2), arr_y[i])
                height = arr_y[i]
                frequency = round(x[i], 2)
                if height > 0.02:
                    plt.text(frequency - 0.08, arr_y[i]+0.05, '%.2f' % frequency )

    elif x_units == 'cm-1':
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
                    plt.text(frequency+100, arr_y[i]+0.1, '%d' % frequency )
    else:
        plt.xlabel("Wavelength (nm)")
        ax1.legend(shadow=True, fancybox=True)

    plt.ylabel("Oscillator Strength")
    #plt.grid(b=None, which='major', axis='y', linewidth=1)
    #plt.grid(b=None, which='major', axis='x', linewidth=1)
    # os.chdir("results/final/graphs")
    os.chdir("results/final")
    if "graphs" not in glob.glob("graphs"):
        os.mkdir("graphs")
    if x_units == 'cm-1':
        ax1.yaxis_inverted()
    os.chdir("graphs")
    plt.savefig(filename)
    os.chdir("../../..")

    return

def collectSpecSimData(x_units='eV', spec_name='spec', normalize=True, path_to_data='results/final/data/'):
    data = np.genfromtxt(path_to_data + spec_name, delimiter=" ")
    data = data.tolist()
    # print(data)
    x = []
    y = []
    highest_y = 0
    for i in data:
        #print(i)
        x.append(i[0])
        y.append(i[1])
        if i[1] > highest_y:
            highest_y = i[1]

    print(highest_y, "HIGHEST")
    cam_b3lyp_n125_y = 4.98005616
    #cam_b3lyp_n125_y = 1.9835017
    #cam_b3lyp_n125_y = 10.17985964

    #print("CAM-B3LYP:", highest_y)
    for i in range(len(y)):
        y[i] /= highest_y
        #y[i] /= cam_b3lyp_n125_y 
    if x_units == 'eV' or x_units=='ev':
        h = 6.626E-34
        c = 3E17
        ev_to_joules = 1.60218E-19
        x = [ h*c/(i*ev_to_joules) for i in x ]
        x.reverse()
        y.reverse()
    elif x_units == 'cm-1':
        x.reverse()
        y.reverse()
        #maxima = scipy.signal.argrelextrema(y, np.greater) 
    return x, y

def latexTable_addLine (path, line):
    if os.path.exists(path):
        with open(path, 'r') as fp:
            lines = fp.readlines()
            lines.insert(-4, '\t'+line)
            
        with open(path, 'w') as fp:
            for i in lines:
                fp.write(i)
    else:
        with open(path, 'w') as fp:
            fp.write('\\begin{center}\n\\begin{tabular}{ |c|c|c|c| }\n\t\\hline\n')
            fp.write('\tMethod & Basis Set & Excitation (eV) &')
            fp.write('\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}\\\\\n\t\\hline\n')
            fp.write('\t' + line)
            fp.write('\t\\hline\n\\end{tabular}\n\\end{center}')


def electronicMultiPlot(methods_lst, 
            T, title, filename, 
            x_range=[2,16], x_units='eV', 
            peaks=False, spec_name='spec',
            complete=[], basis_set_mexc='6-31G(d,p)',
            nStates='25', 
            ):

    location = os.getcwd().split('/')[-1]
    if location == 'src' or location == 'calc_zone':
        os.chdir("..")

    # only pass blank complete if all TD-DFT calculations are complete since it is assumed
    if complete == []:
        num_geom = glob.glob("calc_zone/geom*")
        for i in range(len(num_geom)):
            complete.append(2)
    
    fig, ax1 = plt.subplots()
    
    if peaks:
        print(os.path.exists('latex_df_6-311++G(2d,2p)'))
        if os.path.exists('latex_df_6-311++G(2d,2p).tex'):

            headers = ['Method', 'Basis Set', 'Excitation (eV)',
                '\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}']
            df = df_latex.latexTable_df('latex_df_6-311++G(2d,2p).tex', headers)
        elif os.path.exists('latex_df_6-311G(d,p).tex'):
            headers = ['Method', 'Basis Set', 'Excitation (eV)',
                '\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}']
            df = df_latex.latexTable_df('latex_df_6-311G(d,p).tex', headers)

        else:
            df = {'Method': [], 'Basis Set': [], 
                'Excitation (eV)': [],
                '\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}': []
                } # 4 col
            df = pd.DataFrame(df)


    for i in methods_lst:
        gather_energies.main()
        boltzmannAnalysisSetup(complete, i, basis_set_mexc, nStates, nStates)
        boltzmannAnalysis(T, energy_levels='electronic')    
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
                #print(round(x[i],2), arr_y[i])
                height = arr_y[j]
                frequency = round(x[j], 2)
                print("x, y = %.2f, %.2f" % (frequency, height))
                line = "%s & %s & %.2f & %.2f \\\\\n" % (i, basis_set_mexc, frequency, height) 
                latexTable_addLine('latexTable.tex', line)
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
            df_latex.df_latexTable('latex_df_%s.tex' % basis_set_mexc, df)

    #ax1.set_xlim([x[0], x[-1]])
    ax1.set_xlim(x_range)
    ax1.set_ylim(0, 1.2)

    plt.title(title)
    if x_units == 'ev' or x_units=='eV':
        #print(x)
        plt.xlabel("Electronvolts (eV)")
        ax1.legend(shadow=True, fancybox=True, loc='upper right')

    elif x_units == 'cm-1':
        plt.xlabel(r"Wavenumbers cm$^{-1}$")
        
    else:
        plt.xlabel("Wavelength (nm)")
        ax1.legend(shadow=True, fancybox=True)

    plt.ylabel("Oscillator Strength")
    plt.grid(b=None, which='major', axis='y', linewidth=1)
    plt.grid(b=None, which='major', axis='x', linewidth=1)
    # os.chdir("results/final/graphs")
    os.chdir("results/final")
    if "graphs" not in glob.glob("graphs"):
        os.mkdir("graphs")
    os.chdir("graphs")
    plt.savefig(filename)
    os.chdir("../../..")

def electronicMultiPlot_Experiment(methods_lst, 
            T, title, filename, 
            x_range=[2,16], x_units='eV',
            peaks=False, spec_name='spec',
            complete=[], basis_set_mexc='6-31G(d,p)',
            nStates='25', acquiredStates='25', exp_data=[], 
            colors=[], sec_y_axis=False, rounding=1,
            extra_data=np.array([[-1, -1]])
            ):

    location = os.getcwd().split('/')[-1]
    if location == 'src' or location == 'calc_zone':
        os.chdir("..")

    # only pass blank complete if all TD-DFT calculations are complete since it is assumed
    if complete == []:
        num_geom = glob.glob("calc_zone/geom*")
        for i in range(len(num_geom)):
            complete.append(2)
    
    fig, ax1 = plt.subplots(dpi=400)
    
    if peaks:
        if os.path.exists('latex_df_6-311++G(2d,2p).tex'):

            headers = ['Method', 'Basis Set', 'Excitation (eV)',
                '\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}']
            df = df_latex.latexTable_df('latex_df_6-311++G(2d,2p).tex', headers)
        elif os.path.exists('latex_df_6-311G(d,p).tex'):
            headers = ['Method', 'Basis Set', 'Excitation (eV)',
                '\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}']
            df = df_latex.latexTable_df('latex_df_6-311G(d,p).tex', headers)

        else:
            df = {'Method': [], 'Basis Set': [], 
                'Excitation (eV)': [],
                '\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}': []
                } # 4 col
            df = pd.DataFrame(df)

    for n, i in enumerate(methods_lst):
        gather_energies.main()
        boltzmannAnalysisSetup(complete, i, basis_set_mexc, nStates, acquiredStates)
        boltzmannAnalysis(T, energy_levels='electronic')    
        x, y = collectSpecSimData(x_units=x_units)        
        """
        if i == 'B3LYP':
            print(x, y)
        """
        #ax1.plot(x, y, "-", label="%s" % i, zorder=2)
        # if i == 'wB97XD':
        #     i = r'$\omega$B97XD'
        # ax1.plot(x, y, "-", c="%s" % (colors[n]), label="%s (Amorphous)" % i, zorder=2)
        if i == "wB97XD":
            i = r'$\omega$B97XD'
        ax1.plot(x, y, "-", c="%s" % (colors[n]), label="%s" % i, zorder=2)
        
        if peaks:
            arr_y = np.array(y)
            print("local maxima")
            peaks_dat, _ = scipy.signal.find_peaks(arr_y, height=0)
            for j in peaks_dat:
                #print(round(x[i],2), arr_y[i])
                height = arr_y[j]
                frequency = round(x[j], 4)
                if rounding == 1:    
                    print("x, y = %.1f, %.1f" % (frequency, height))
                    line = "%s & %s & %.1f & %.1f \\\\\n" % (i, basis_set_mexc, frequency, height) 
                elif rounding == 2:
                    print("x, y = %.2f, %.2f" % (frequency, height))
                    line = "%s & %s & %.2f & %.2f \\\\\n" % (i, basis_set_mexc, frequency, height) 
                else:
                    print("x, y = %.4f, %.4f" % (frequency, height))
                    line = "%s & %s & %.4f & %.4f \\\\\n" % (i, basis_set_mexc, frequency, height) 

                #latexTable_addLine('latexTable.tex', line)
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
            df_latex.df_latexTable('latex_df_%s.tex' % basis_set_mexc, df, rounding )

    #exp_names = [ "Exp. Solid", "Exp. Gas"]
    exp_names = [ "Exp. Solid A", "Exp. Solid B"]
    exp_names = [ "Exp. Solid B"]
    #exp_names = [ "Exp. Solid", "Exp. Gas"]
    #exp_names = [ "Exp. Solid A", "Exp. Solid B"]
    exp_colors = [ "k","tab:grey"]
    #exp_colors = [ "tab:grey"]
    ax2 = ax1.twinx()

    if len(exp_data) > 0:
        for n, i in enumerate(exp_data):
            ymax = np.amax(i[:,1], axis=0)
            i[:,1] /= ymax
            #print(i)
            ax2.plot(i[:,0], i[:,1], "--", c='%s' % exp_colors[n], label="%s" % exp_names[n], zorder=2)
            if peaks:
                arr_y = i[:,1]
                print("local maxima")
                peaks_dat, _ = scipy.signal.find_peaks(arr_y, height=0)
                for j in peaks_dat:
                    #print(round(x[i],2), arr_y[i])
                    height = arr_y[j]
                    frequency = round(i[j,0], 2)
                    print("x, y = %.2f, %.2f" % (frequency, height))
                    line = "%s & %s & %.2f & %.2f \\\\\n" % (exp_names[n], basis_set_mexc, frequency, height) 
                    #latexTable_addLine('latexTable.tex', line)
                    df.loc[len(df.index)] = [exp_names[n], basis_set_mexc, frequency, height]
                df_latex.df_latexTable('latex_df_%s.tex' % basis_set_mexc, df, rounding)
    #ax1.set_xlim([x[0], x[-1]])
    if extra_data[0,0]!=-1 and extra_data[0,1]!=-1 :
        print("\n extra data\n")
        ymax = np.amax(extra_data[:,1], axis=0)
        for i in range(len(extra_data[:,1])):
            extra_data[i,1] /= ymax
        
        ax1.plot(extra_data[:,0], extra_data[:, 1], '-', label='CAM-B3LYP (Ribbon Octamer)', color='blue')
        if peaks:
            arr_y = extra_data[:,1]
            arr_x = extra_data[:,0]
            print(arr_y)
            peaks_dat, _ = scipy.signal.find_peaks(arr_y, height=0)
            print(peaks_dat)
            for j in peaks_dat:
                    #print(round(x[i],2), arr_y[i])
                    height = arr_y[j]
                    frequency = round(arr_x[j], 4)
                
                    print("x, y = %.1f, %.1f\n" % (frequency, height))
                    df.loc[len(df.index)] = ['8 Ribbon', basis_set_mexc, frequency, height]
        


    if sec_y_axis:
        #ax2.set_ylabel(r"Cross Section / cm$^2$ (Normalized)")
        ax2.set_ylim(0,1.3)

    ax1.set_xlim(x_range)
    ax1.set_ylim(0, 1.3)

    plt.title(title)
    ax1.legend(shadow=True, fancybox=True, loc='upper left')
    ax2.legend(shadow=True, fancybox=True, loc='upper right')
    if x_units == 'ev' or x_units=='eV':
        #print(x)
        plt.xlabel("Electronvolts (eV)")
        ax1.set_xlabel("Electronvolts (eV)")
        #ax1.legend(shadow=True, fancybox=True)

    elif x_units == 'cm-1':
        plt.xlabel(r"Wavenumbers cm$^{-1}$")
        
    else:
        plt.xlabel("Wavelength (nm)")
        #ax1.legend(shadow=True, fancybox=True)

    ax1.set_ylabel("Oscillator Strength")
    #plt.grid(zorder=0, b=None, which='major', axis='y', linewidth=1)
    #plt.grid(zorder=0, b=None, which='major', axis='x', linewidth=1)
    # os.chdir("results/final/graphs")
    os.chdir("results/final")
    if "graphs" not in glob.glob("graphs"):
        os.mkdir("graphs")
    os.chdir("graphs")
    plt.savefig(filename)

    os.chdir("../../..")


def method_update_selection(methods_lst, basis_set_mexc, nStates):
    if basis_set_mexc == '6-311G(d,p)':
        basis_dir_name = ''
    else:
        basis_dir_name = '_' + basis_set_mexc
    if nStates == '25':
        pass
    else:
        basis_dir_name += '_n%s' % nStates
    for n, i in enumerate(methods_lst):
        if i == 'B3LYP':
            i = 'mexc' + basis_dir_name
            print(i.lower() + basis_dir_name)
        else:
            i = i.lower() + basis_dir_name
            print(i.lower() + basis_dir_name) 
        methods_lst[n] = i
    return methods_lst

def sort_data (data):
    return data[data[:,0].argsort()]

def nmLst_evLst (nmData):
    h = 6.62607004E-34
    c = 299792458
    c = 3E17
    Joules_to_eV = 1.602E-19

    for i in range(len(nmData[:,0])):
        nmData[i,0] = h*c/(nmData[i,0]*Joules_to_eV)
    nmData = nmData[nmData[:,0].argsort()]
    return nmData

def main():
    mol_xyz1 = "mon_nh3.xyz"
    mol_xyz1 = "mon_h2o.xyz"
    mol_xyz1 = "mon_h2co3.xyz"
    mol_xyz1 = "mon_h2co3_ct.xyz"
    mol_xyz2 = "mon_h2co3_tt.xyz"
    #mol_xyz2 = "mon_methanol.xyz"
    number_clusters = 1
    # enter the number of molecules of each geometry in the respective index
    molecules_in_cluster = [4, 4]
    box_length = 9               # in angstroms
    minium_distance_between_molecules = 3.0

    resubmit_delay_min = 0.01
    resubmit_max_attempts = 3


    # geometry optimization options
    method_opt = "wB97XD"
    basis_set_opt = "6-31G(d)"
    mem_com_opt = "1600"  # mb
    mem_pbs_opt = "15"  # gb

    
    # TD-DFT methods
    #method_mexc = "B3LYP"
    #method_mexc = "PBE0"
    #method_mexc = "wB97XD"
    method_mexc = "CAM-B3LYP"
    #method_mexc = "B3LYPD3"
    #method_mexc = "B97D3"

    # TD-DFT basis sets
    basis_set_mexc = "6-311G(d,p)"
    #basis_set_mexc = "6-311++G(2d,2p)"

    # TD-DFT NSTATES
    nStates = '25'
    #nStates = '50'
    #nStates = '100'
    #nStates = '150'
    #nStates = '125'

    # TD-DFT memory
    mem_com_mexc = "2500"  # mb
    mem_pbs_mexc = "25"  # gb"

    #moleculeName = 'nh3'
    #moleculeNameLatex = r'NH$_3$'
    #moleculeName = 'co2'
    #moleculeNameLatex = r'CO$_2$'
    #moleculeName = 'h2o'
    #moleculeNameLatex = r'H$_2$O'
    moleculeName = 'co3h2'
    moleculeNameLatex = r'CO$_3$H$_2$'

    # Temperatures (K)
    #T = 100  
    # T comes from the binding energy of the dimers for each strucutres converted from Hartrees to Kelvin
    #T = 1348.768    # nh3
    #T = 457.088     # co2
    #T = 2071.104    # h2o
    T = 9259.3       # co3h2

    if basis_set_mexc == '6-311G(d,p)':
        basis_dir_name = ''
    else:
        basis_dir_name = '_' + basis_set_mexc

    if nStates == '25':
        pass
    else:
        basis_dir_name += nStates

    filename = "30_8_rand_%s_%s%s.png" % ( moleculeName, method_mexc, basis_dir_name)
    title = r"30 Randomized Clusters of 8 %s Molecules %s" % (moleculeNameLatex, basis_dir_name)

    # for generating the structures
    ice_build_geoms.main(molecules_in_cluster, number_clusters, box_length, minium_distance_between_molecules,
                        mol_xyz1, mol_xyz2, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt)
    """
    
    complete = jobResubmit(resubmit_delay_min, resubmit_max_attempts,
                           method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                           method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                           nStates
                           )  # delay_min, num_delays
    """
    # for standard usage
    """
    boltzmannAnalysisSetup(complete, method_mexc, nStates=nStates)
    gather_energies.main()

    boltzmannAnalysis(T)
    generateGraph("spec", T, title, filename, x_range=[5,10], x_units='ev', peaks=True)
    """
    ### NH3 6-311++G(d,p) need to test nstates==50

    # to combine total electronic calculations
    methods_lst = ["B3LYP", "PBE0", "wB97XD", "CAM-B3LYP", "B3LYPD3", "B97D3"]
    
    methods_lst = ["B3LYP", "PBE0", "wB97XD", "CAM-B3LYP", "B97D3"]
    colors = ["blue", 'orange', 'green', 'red', 'cyan']
    #methods_lst = ["CAM-B3LYP"]
    colors = [ 'red', 'green']
    methods_lst = ["CAM-B3LYP", "wB97XD"]
    methods_lst = ["CAM-B3LYP"]
    #methods_lst = []
    colors = ["red", 'green']
    #methods_lst = ["CAM-B3LYP", "wB97XD"]
    #colors = ["red", 'green']
    #methods_lst = ["B3LYP"]
    #colors = ["blue"]

    title = r"30 Randomized Clusters of 8 %s Molecules with %s" % (moleculeNameLatex, basis_dir_name[1:].replace(nStates, '')) +  "\nat N=%s and T=%s K" % (nStates, T)
    filename = "30_8_%s_elec_n%s_%s_%sK.pdf" % ( moleculeName, nStates, basis_dir_name[1:].replace(nStates, ''), T, )
    if len(methods_lst) == 1:
        filename = "30_8_%s_elec_%s_n%s_%s_%sK.pdf" % ( moleculeName, method_mexc, nStates, basis_dir_name[1:].replace(nStates, ''), T, )
    #filename = "30_8_%s_test_%sk.pdf" % ( moleculeName, T)

    filename = "30_8_%s_elec_n%s_%s_%sK.pdf" % ( moleculeName, nStates, basis_set_mexc , T, )
    filename = "30_8_%s_elec_n%s_%s_%sK.png" % ( moleculeName, nStates, basis_set_mexc , T, )
    title = r"30 Randomized Clusters of 8 %s Molecules with %s" % (moleculeNameLatex, basis_set_mexc) + "\nat %s K" % T 
    
    #methods_lst = method_update_selection(methods_lst, basis_set_mexc, nStates)
    #print(methods_lst)

    """
    electronicMultiPlot(methods_lst, 
            T, title, filename, 
            x_range=[5, 10], x_units='eV', 
            peaks=True, spec_name='spec', 
            complete=complete, basis_set_mexc=basis_set_mexc, nStates=nStates

            )
    print("OUTPUT =\n", filename)
    """
    acquiredStates = nStates
    acquiredStates = '15' 
    """
    filename = "30_8_%s_elec_n%s_%s_%sK_exp.pdf" % ( moleculeName, nStates, basis_set_mexc , T, )
    filename = "30_8_%s_elec_n%s_%s_%sK_exp.png" % ( moleculeName, nStates, basis_set_mexc , T, )
    title = r"30 Randomized Clusters of 8 %s Molecules with %s" % (moleculeNameLatex, basis_set_mexc) + "\nat %s K compared with experiment" % T 
    title = '' 
    filename = "30_8_%s_elec_n%s_%s_%sK_exp_STATES_%s_B.png" % ( moleculeName, nStates, basis_set_mexc , T, acquiredStates)
    filename = "30_8_%s_elec_n%s_%s_%sK_exp_STATES_%s_EXP_RIB_AM.png" % ( moleculeName, nStates, basis_set_mexc , T, acquiredStates)
    #filename = "105_32_%s_elec_n%s_%s_%sK_exp_STATES_%s.png" % ( moleculeName, nStates, basis_set_mexc , T, acquiredStates)
    filename = "30_8_%s_elec_n%s_%s_%sK_expD1.png" % ( moleculeName, nStates, basis_set_mexc , T, )
    #filename = "105_32_%s_elec_n%s_%s_%sK.pdf" % ( moleculeName, nStates, basis_set_mexc , T, )
    #filename = "105_32_%s_elec_n%s_%s_%sK.png" % ( moleculeName, nStates, basis_set_mexc , T, )
    filename = "30_8_%s_elec_n%s_%s_%sK_exp.png" % ( moleculeName, nStates, basis_set_mexc , T, )
    filename = "30_8_%s_elec_n%s_%s_%sK_exp_STATES.png" % ( moleculeName, nStates, basis_set_mexc , T, )
    filename = "legend.png" 
    filename = "105_32_%s_elec_n%s_%s_%sK_exp_STATES.png" % ( moleculeName, nStates, basis_set_mexc , T, )
    #exp_gas = np.genfromtxt('../../exp_data/%s_gas.csv' % moleculeName, delimiter=', ')
    #exp_solid = np.genfromtxt('../../exp_data/%s_solid.csv'% moleculeName, delimiter=', ')
    exp_solid1 = np.genfromtxt('../../exp_data/%s_200k.csv'% moleculeName, delimiter=', ')
    exp_solid1 = nmLst_evLst(exp_solid1)
    #exp_solid1 = sort_data(exp_solid1)
    exp_solid2 = np.genfromtxt('../../exp_data/%s_80_200k.csv'% moleculeName, delimiter=', ')
    #exp_solid2 = sort_data(exp_solid2)
    exp_solid2 = nmLst_evLst(exp_solid2)
    #exp_data = [ exp_solid ]

    exp_data = [exp_solid1, exp_solid2]
    #exp_data = [ exp_solid2 ]
    exp_x_units = ['nm']
    #print(exp_da#ta)
    
    octa_rib = dis_art.discrete_to_art('../ribbon/8rib_cam.dat', ['nm', 'eV'], [100, 320], 2)
    #octa_rib = dis_art.discrete_to_art('../ribbon/8rib_cam.dat', ['nm', 'nm'], [100, 320], 2)
    #print(octa_rib)
    electronicMultiPlot_Experiment(methods_lst, 
        T, title, filename, 
        x_range=[4,10.5], x_units='eV',
        peaks=True, spec_name='spec', 
        complete=complete, basis_set_mexc=basis_set_mexc, nStates=nStates, acquiredStates=acquiredStates,
        exp_data=exp_data, 
        colors=colors, sec_y_axis=True, rounding=2,
        extra_data=octa_rib
        )
    print("OUTPUT =\n", filename)
    """

    
    """
    overTones = False
    overTonesBoltzmannAnalysis = True
    if overTones: 
        filename = "30_8_rand_%s_vib_wB97XD_overtones.png" % moleculeName
        title = "30 8 rand %s with overtones" % moleculeName
    else: 
        filename = "30_8_rand_%s_vib_wB97XD_none.png" % moleculeName
        title = "30 8 rand %s with no" % moleculeName

    if overTonesBoltzmannAnalysis:
        filename = "30_8_rand_%s_vib_wB97XD_overtones_from_maximas.png" % moleculeName
    # for vibrational frequency standard usage

    vibrational_frequencies.main(overTones, T=500)
    boltzmannAnalysis(T, energy_levels='vibrational', DeltaN='10', x_range=[50, 4100], overtones=overTonesBoltzmannAnalysis)
    generateGraph("spec", T, title, filename, x_range=[4000, 400], x_units='cm-1', peaks=False)
    """
    
    # useful bash commands below
        # ps aux | grep test.py
        # kill <pid> -9
        # python3 -u ./ice_manager.py > output.log & disown -h

    print("OUTPUT =\n", filename)
if __name__ == '__main__':
    main()

