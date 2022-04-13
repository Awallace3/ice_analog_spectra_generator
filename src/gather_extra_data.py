import os
import subprocess


def main():
    fnames = [
            "./data/extra_data/first/first/exc_cam.out",
            "./data/extra_data/first/first/exc.out",
            "./data/extra_data/first/first/exc_wb97xd.out",
            ]
    acquiredStates = ["80", "77", "68"]
    for n, i in enumerate(fnames):
        out = i.split("/")[-1][:-4]
        a = acquiredStates[n]
        cmd = ("""awk '/Excited State/ {print $7, $9}' %s | sed 's/f=//g' | tac | tail -n %s > ./theoretical_data/%s.csv""" % (i, a, out))
        subprocess.call(cmd, shell=True)
    return


if __name__ == "__main__":
    main()
