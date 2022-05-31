import glob
import os
import subprocess
import random


def fix_mex(path: str):
    print("Starting... %s" % path)
    directories = glob.glob("%s/geom*" % path)
    for i in directories:
        print(i)
        out_files = glob.glob("%s/*.out*" % i)
        out_completion = glob.glob("%s/mex_o.*" % i)
        len_file = len(out_files)
        len_complete = len(out_completion)
        #print("len_complete", len(out_completion), "len_outfiles", len(out_files))
        if len_complete > len_file:
            for i in range(len_complete - len_file):
                del_o = out_completion.pop()
                print('rm %s' % del_o)
                subprocess.call("rm " + del_o, shell=True)
        elif len_complete < len_file:
            for i in range((len_file - len_complete)):
                create_o = "%s/mex_o.o%s0000" % (
                    i, str(random.randint(100000, 999999)))
                print('touch %s' % create_o)
                subprocess.call("touch " + create_o, shell=True)


def fix_mexc():
    os.chdir("../calc_zone")
    directories = glob.glob("geom*")
    for i in directories:
        print(i)
        os.chdir(i + "/mexc")

        out_files = glob.glob("*.out*")
        out_completion = glob.glob("mexc_o.*")
        len_file = len(out_files)
        len_complete = len(out_completion)
        #print("len_complete", len(out_completion), "len_outfiles", len(out_files))
        if len_complete > len_file:
            for i in range(len_complete - len_file):
                del_o = out_completion.pop()
                #subprocess.call("echo " + del_o, shell=True)
                print('rm %s' % del_o)
                subprocess.call("rm " + del_o, shell=True)
        elif len_complete < len_file:
            for i in range((len_file - len_complete)):
                create_o = "mexc_o.o%s0000" % str(i + 15)
                print('touch %s' % create_o)
                #subprocess.call("echo " + create_o, shell=True)
                subprocess.call("touch " + create_o, shell=True)
        os.chdir("../..")


def main():
    #fix_mex()
    fix_mexc()


# main()
