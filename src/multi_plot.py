import glob
import os
import sys
import subprocess
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

sys.path.insert(1, '../.')
import gather_energies
from ice_manager import boltzmannAnalysisSetup

def electronic(methods_lst, 
            T, title, filename, 
            x_range=[2,16], x_units='eV', 
            peaks=False, spec_name='spec'
            ):
    location = os.getcwd().split('/')[-1]
    if location == 'src':
        os.chdir("..")
    elif location == 'calc_zone':
        os.chdir("..")
    else:
        pass
    
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
        #print(x)
        plt.xlabel("Electronvolts (eV)")
        ax1.legend(shadow=True, fancybox=True)
        if peaks:
            arr_y = np.array(y)
            #print("local maxima")
            peaks, _ = scipy.signal.find_peaks(arr_y, height=0)
            for i in peaks:
                #print(round(x[i],2), arr_y[i])
                height = arr_y[i]
                frequency = round(x[i], 2)
                if height > 0.02:
                    plt.text(frequency - 0.08, arr_y[i]+0.05, '%.2f' % frequency )

    elif x_units == 'cm-1':
        plt.xlabel(r"Wavenumbers cm$^{-1}$")
        if peaks:
            arr_y = np.array(y)
            #print("local maxima")
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
    plt.grid(b=None, which='major', axis='y', linewidth=1)
    plt.grid(b=None, which='major', axis='x', linewidth=1)
    # os.chdir("results/final/graphs")
    os.chdir("results/final")
    if "graphs" not in glob.glob("graphs"):
        os.mkdir("graphs")
    os.chdir("graphs")
    plt.savefig(filename)
    os.chdir("../../..")

