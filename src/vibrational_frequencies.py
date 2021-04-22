import numpy as np
import os
import glob
import subprocess


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


def main():
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
        os.chdir("..")
    os.chdir("..")

main()