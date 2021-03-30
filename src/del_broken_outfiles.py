import subprocess
import os
import glob

def conv_out_num(name):
    if name[-1] == t:
        val = 1
    elif name[-1].isnumeric():
        val = int(name[-1])
    else:
        val = 0
    return val

def len_outfile(filename):
    with open(filename) as fp:
        lines = fp.readlines()
    return len(lines)

def match_outputs():
    out_files = glob.glob("*.out*")
    out_completion = glob.glob("mex_o.*")
    for i in range(len(out_completion)-len(out_files)):
        del_o = out_completion.pop()
        subprocess.call("echo " + del_o, shell=True)
    

def del_broken_outfiles(path):
    os.chdir(path)
    out_files = glob.glob('*.out*')
    max_out = out_files[0]
    val = conv_out_num(max_out)
    for i in out_files:
        if conv_out_num(i) > val:
            max_out = i
    
    if len_outfile(max_out) < 200:
        subprocess.call("echo " + max_out)
        match_outputs()
    os.chdir("..")


def main():
    os.chdir("../calc_zone")
    directories = glob.glob("*")
    for i in directories:
        del_broken_outfiles(i)
main()
        
            
        
