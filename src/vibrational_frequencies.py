import numpy as np
import os
import glob
import subprocess
import math
import matplotlib.pyplot as plt

def unit_conversion(data, x_units=['nm', 'eV']):
	if x_units[0]=='nm' and x_units[1]=='eV':
		h = 6.62607004E-34
		c = 3E17
		Joules_to_eV = 1.602E-19
		for i in range(len(data[:,0])):
			data[i,0] = h*c/(data[i,0]*Joules_to_eV)
		return data
	else:
		print("Unit conversion is not supported yet.")


def art_spec_from_nparray(data, path_src, x_range, broadening):
    np.savetxt('data', data, delimiter=' ')
    cmd = 'perl %sspecsim_args.pl %.2f %.2f %.2f' % (path_src, x_range[0], x_range[1], broadening) 
    subprocess.call(cmd, shell=True)
    data = np.genfromtxt('spec')
    os.remove('data')
    os.remove('spec')
    #print(data)
    return data

def overtone_energy_intensity(e1, e2, i1, i2, T):
    h = 6.626E-34 # J*s
    c = 2.998E10  # cm/s
    k = 1.38E-23  # J/K
    
    I_og =  ( i1 + i2 ) / 2
    e_1J = e1*h*c # J
    e_2J = e2*h*c # J
    e_fin = e_1J + e_2J
    exp = math.exp((e_1J-e_2J)/(k*T)) 
    if exp > 1:
        print(exp)
    I = I_og * math.exp((e_1J-e_fin)/(k*T))
    I = I_og * math.exp(((e_1J+e_2J)/2-e_fin)/(k*T))
    if I > 555:
        print("I greater than 555:", I)
    #I = I_og * math.exp( ((e_1J+e_2J)-(e_1J+e_2J)/2) /(k*T))
    return e1+e2, I


def overtones(filename, T=100):
    # double the fundamental for the first one
    data = np.genfromtxt(filename)
    h = 6.626E-34 # J*s
    c = 2.998E10  # cm/s
    k=1.38E-23    # J/K
    new_points = []
    number_modes = len(data[:,0]) -1
    for i in range(number_modes):
        for j in range(number_modes - i):
            e1 = data[i, 0]
            e2 = data[number_modes - j, 0]
            i1 = data[i, 1]
            i2 = data[number_modes - j, 1]
            e_fin, I_fin = overtone_energy_intensity(e1, e2, i1, i2, T )
            new_points.append([e_fin, I_fin])
    """
            
    for i in range(len(data[:,0])-1):
        for j in range(2):
            e_fin, I_fin = overtone_energy_intensity(data[i, 0], data[i+j, 0], data[i, 1], data[i+j,1], T )
            new_points.append([e_fin, I_fin])
            if I_fin > 100:
                print(I_fin, i, i+j)
    """


    #print(data)
    #print(new_points)
    a = np.array(new_points)
    a = trim_data(a)
    a = a[a[:, 0].argsort()]
    """
    fig, ax1 = plt.subplots()
    data = art_spec_from_nparray(data, './', [50, 4000], 1)
    a = trim_data(a)
    a = art_spec_from_nparray(a, './', [50, 4000], 1)
    #print(data)
    #print(a)
    ax1.plot(data[:,0], data[:,1], 'r')
    ax1.plot(a[:,0], a[:,1], 'b')
    ax1.set_xlim(4000, 50)
    #mngr = plt.get_current_fig_manager()
    # to put it into the upper left corner for example:
    #mngr.full_screen_toggle()
    #print(mngr)
    plt.show()
    """
    return a

def combine_modes_overtones(filename, overtones_array):
    modes = np.genfromtxt(filename)
    combined = np.concatenate((modes, overtones_array), axis=0)
    return combined[combined[:,0].argsort()]

def cleanLine(line, aList):
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

def vibrational_frequencies_gaussian(filename):
    frequency = " Frequencies -- "
    irInten = ' IR Inten    --'
    freqs = []
    ir_intensity = []
    with open(filename) as search:
        for num, line in enumerate(search, 1):
            if frequency in line:
                cropped_line = line[len(frequency):]
                freqs = cleanLine(cropped_line, freqs)

            elif irInten in line:
                cropped_line = line[len(irInten):]
                ir_intensity = cleanLine(cropped_line, ir_intensity)
    
    #print("freqs:", freqs)
    #print("raman", raman)
    #print("ir", ir_intensity)
    return freqs, ir_intensity

def trim_data(data, x_range=[50, 4500], y_range=[10, 10000]):
    data = data[np.logical_and(data[:,0] > x_range[0], data[:,0] < x_range[1])]
    data = data[np.logical_and(data[:,1] > y_range[0], data[:,1] < y_range[1])]
    return data

def main(overTones=True, T=100):
    
    location = os.getcwd().split('/')[-1]
    print(location)
    if location == 'src':
        os.chdir("../calc_zone")
    elif location == 'calc_zone':
        pass
    else:
        os.chdir("calc_zone")
    directories = glob.glob("geom*")
    paths = '../results/vibrational_values'
    if not os.path.exists(paths):
        subprocess.call('mkdir ../results/vibrational_values', shell=True)
    paths = '../../results/vibrational_values/'
    for i in directories:
        n = i[4:]
        os.chdir(i)
        out_files = glob.glob("*.out*")
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
        freqs, ir_intensity = vibrational_frequencies_gaussian(filename)
        f = open(paths+"vib%s.csv" % n, 'w')
        for i, j in zip(freqs, ir_intensity):
            line = str(i*0.97) + ' ' + str(j) + '\n'
            f.write(line)
        f.close()
        
        if overTones:
            #print(os.getcwd(), paths+"vib%s.csv"% n)
            a = overtones(paths+"vib%s.csv"% n, T)
            a = combine_modes_overtones(paths+"vib%s.csv"% n, a)
            a = trim_data(a, x_range=[50, 4500], y_range=[10, 10000])
            np.savetxt(paths+"vib%s.csv"% n, a, fmt='%.9f')
        

        os.chdir("..")
    os.chdir("..")
if __name__ == '__main__':
    #main()
    for i in range(22, 23):
        a = overtones("../results/vibrational_values/vib%d.csv" % i)
        a = combine_modes_overtones("../results/vibrational_values/vib%d.csv" % i, a)
        a = trim_data(a, x_range=[50, 5000], y_range=[10, 10000])

        print(a)
        np.savetxt('test.csv', a, fmt='%.9f')
