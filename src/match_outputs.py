import glob
import os
import subprocess

os.chdir("../calc_zone")
directories = glob.glob("geom*")
for i in directories:
    os.chdir(i)
    out_files = glob.glob("*.out*")
    out_completion = glob.glob("mex_o.*")
    for i in range(len(out_completion)-len(out_files)):
        del_o = out_completion.pop()
        subprocess.call("echo " + del_o, shell=True)
    os.chdir("..")