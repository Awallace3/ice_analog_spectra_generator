import glob
import os
import subprocess
import time
from .job_progression import job_progression


def check_add_methods(add_methods, funct_name):
    ln = len(add_methods["methods"])
    if (
        ln == len(add_methods["basis_set"])
        and ln == len(add_methods["mem_com"])
        and ln == len(add_methods["mem_pbs"])
    ):
        return True
    else:
        print("\nIncorrect input.", "\nTerminating %s before start\n" % funct_name)
        return False


def read_user():
    """
    opens user to read in the string for the user
    """
    with open("user", "r") as fp:
        return fp.read().rstrip()


def add_qsub_dir(qsub_dir, geom_dir, path_qsub_queue="../../qsub_queue.txt"):
    if qsub_dir == "None":
        return 0
    elif qsub_dir == "./":
        qsub_path = geom_dir + "\n"
    else:
        qsub_path = "%s/%s\n" % (geom_dir, qsub_dir)
    # print(os.getcwd(), qsub_path, "../../qsub_queue.txt")
    with open(path_qsub_queue, "a") as fp:
        fp.write(qsub_path)
    return 1


def r_qsub_dir(method_mexc, solvent):
    if method_mexc == "CAM-B3LYP":
        qsub_dir = "mexc"
    else:
        qsub_dir = method_mexc.lower()
    if solvent != "":
        qsub_dir += "_%s" % solvent
    return qsub_dir


def qsub_to_max(max_queue=100, user=""):
    with open("qsub_queue.txt", "r") as fp:
        qsubs = fp.readlines()
    cmd = "qstat -u %s | wc -l > qsub_len" % user
    # for local testing...
    # cmd = "qstat | wc -l > ../qsub_len"
    subprocess.call(cmd, shell=True)
    if os.path.exists("qsub_len"):
        print("qsub_to_max", os.getcwd(), "qsub_len", "qsub_queue.txt")
        with open("qsub_len", "r") as fp:
            current_queue = int(fp.read()) - 5
        os.remove("qsub_len")
    else:
        current_queue = 0
    dif = max_queue - current_queue
    print("dif is", dif)
    if dif > 0:
        cnt = 0
        while cnt < dif and len(qsubs) > 0:
            qsub_path = qsubs.pop(0)
            qsub_path = qsub_path.rstrip().replace("\n", "")
            print("\n", qsub_path, os.getcwd(), "\n")
            qsub(qsub_path)
            cnt += 1
    with open("qsub_queue.txt", "w") as fp:
        for i in qsubs:
            fp.write(i)
    return 1


def qsub(path="."):
    print("qsub dir", path)
    resetDirNum = len(path.split("/"))
    if path != ".":
        os.chdir(path)
    pbs_file = glob.glob("*.pbs")[0]
    cmd = "qsub %s" % pbs_file
    print(os.getcwd(), "cmd", cmd)
    subprocess.call(cmd, shell=True)
    if path != ".":
        for i in range(resetDirNum):
            os.chdir("..")


def jobResubmit_v2(
    monitor_jobs,
    min_delay,
    number_delays,
    method_opt,
    basis_set_opt,
    mem_com_opt,
    mem_pbs_opt,
    method_mexc,
    basis_set_mexc,
    mem_com_mexc,
    mem_pbs_mexc,
    cluster,
    route="results",
    add_methods={
        "methods": [],
        "basis_set": [],
        "solvent": [],
        "mem_com": [],
        "mem_pbs": [],
    },
    max_queue=200,
    results_json="results.json",
    user=read_user(),
    identify_zeros=False,
    create_smiles=True,
):
    """
    Modified from jobResubmit_v2 from
    https://www.github.com/Awallace3/Dyes
    """
    if identify_zeros:
        zeros_lst = []
    if not os.path.exists("qsub_queue.txt"):
        subprocess.call("touch qsub_queue.txt", shell=True)

    if not check_add_methods(add_methods, "jobResubmit_v2"):
        return []

    add_methods_length = len(add_methods["methods"])

    min_delay = min_delay * 60
    # cluster_list = glob.glob("%s/*" % route)
    complete = []
    resubmissions = []
    for i in range(len(monitor_jobs)):
        complete.append(0)
        resubmissions.append(2)
        # resubmissions.append(resubmission_max)
    calculations_complete = False
    # comment change directory below in production
    print(os.getcwd())
    os.chdir(route)

    for i in range(number_delays):
        # time.sleep(min_delay)
        for num, j in enumerate(monitor_jobs):
            os.chdir(j)
            delay = i
            mexc_check = glob.glob("mexc")
            if len(mexc_check) > 0:
                complete[num] = 1
                mexc_check_out = glob.glob("mexc/mexc.o*")
                mexc_check_out_complete = glob.glob("mexc/*_o*")
                if (
                    complete[num] < 2
                    and len(mexc_check_out) > 0
                    and len(mexc_check_out_complete) > 0
                ):
                    complete[num] = 2
            if complete[num] < 1:
                if identify_zeros:
                    zeros_lst.append(j)
                print("directory for", j)
                action, resubmissions, qsub_dir = job_progression(
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
                    cluster,
                    j,
                    xyzSmiles=create_smiles,
                )
                if qsub_dir != "None":
                    add_qsub_dir(qsub_dir.lower(), j)
            if complete[num] <= 2:
                for pos in range(add_methods_length):
                    test_dir = r_qsub_dir(
                        add_methods["methods"][pos], add_methods["solvent"][pos]
                    )
                    if not os.path.exists(test_dir):
                        print("add method", add_methods)
                        (action, resubmissions, qsub_dir) = job_progression(
                            num,
                            method_opt,
                            basis_set_opt,
                            mem_com_opt,
                            mem_pbs_opt,
                            add_methods["methods"][pos],
                            add_methods["basis_set"][pos],
                            add_methods["mem_com"][pos],
                            add_methods["mem_pbs"][pos],
                            resubmissions,
                            delay,
                            cluster,
                            j,
                            xyzSmiles=False,
                            solvent=add_methods["solvent"][pos],
                        )
                        # print(pos, os.getcwd())
                        if qsub_dir != "None":
                            add_qsub_dir(qsub_dir.lower(), j)
                    else:
                        complete[num] += 1

            mexc_check = []
            os.chdir("..")
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            # if stage == len(complete)*2:
            if stage == len(complete) * (add_methods_length + 2):
                calculations_complete = True

        qsub_to_max(max_queue, user)
        # qsub_to_max(max_queue, 'r2652')
        if calculations_complete:
            print(complete)
            print("\nCalculations are complete.")
            print("Took %.2f hours" % (i * min_delay / 60))
            return complete
        print("Completion List\n", complete, "\n")
        print("delay %d" % (i))
        """
        qsub_funct
        """
        if identify_zeros:
            print("identified zeros:", zeros_lst)
        time.sleep(min_delay)
    for i in range(len(resubmissions)):
        if resubmissions[i] < 2:
            print("Not finished %d: %s" % (resubmissions[i], monitor_jobs[i]))
    os.chdir("..")
    return complete


def jobResubmit(
    config={
        "enable": {"exc": True, "vib": False},
        "dataPath": "data/48_1_1_h2o_nh3",
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
    default_dir = os.getcwd()
    dataPath = config["dataPath"]
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
    cluster_list = glob.glob(dataPath + "geom*")
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
                action, resubmissions = job_progression(
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
            # os.chdir("../..")
            os.chdir(default_dir)
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


def qmgr_setup_status_list(jobList):
    """
    Sets up qmgr with a list for looping over
    jobs and keeping track of which step each
    directory is at.
    """
    status = []
    for job in jobList:
        el = [job, []]
        dataPath = job["dataPath"]
        job_dirs = dataPath + "/geom*"
        jobs = glob.glob(job_dirs)
        for i in jobs:
            # insertion = [dataPath, step, resub, numExcJobs, numVibJobs]
            insertion = [i, -1, 2, 0, 0]
            excList = job['excList']
            for excJob in excList:
                insertion[3] += 1
            vibList = job['vibList']
            for vibJob in vibList:
                insertion[4] += 1
            el[1].append(insertion)
        status.append(el)
    if len(status) == 0:
        print("No data directories detected. Check that the dataPath exists.")
    return status


def queue_logic(default_dir, status, delay, enabled):
    """
    determines which step the directory is at in the requested jobs
    and places jobs in the qsub_queue
    """
    job_term = []
    path_qsub_queue = default_dir + '/qsub_queue.txt'
    if not enabled["exc"] and enabled['vib']:
        vib_only = True
    else:
        vib_only = False
    for n, job_group in enumerate(status):
        jobs = job_group[0]
        job_dirs = job_group[1]
        kill_list = []
        for i in range(len(job_dirs)):
            stat = job_dirs[i]
            geomDirName = stat[0].split('/')[-1]
            print('stat', stat)
            job_dir = stat[0]
            lStat = stat[1]
            os.chdir(job_dir)
            try:
                # optimization step
                if lStat == -1 and not vib_only:
                    action, stat, qsub_dir = job_progression(
                            config=jobs,
                            delay=delay,
                            stat=stat,
                            cluster='map',
                            geomDirName=geomDirName,
                            )
                    job_dirs[i] = stat
                    if qsub_dir != "None":
                        add_qsub_dir(
                                qsub_dir.lower(),
                                stat[0],
                                path_qsub_queue
                                )
                elif lStat == -1 and vib_only:
                    action, stat, qsub_dir = job_progression(
                            config=jobs,
                            delay=delay,
                            stat=stat,
                            cluster='map',
                            geomDirName=geomDirName,
                            vib_only=vib_only,
                            spec_type='vibrational'
                            )
                    job_dirs[i] = stat
                    if qsub_dir != "None":
                        add_qsub_dir(
                                qsub_dir.lower(),
                                stat[0],
                                path_qsub_queue
                                )
                # electrobnic excited states
                elif lStat == 0 and enabled["exc"]:
                    for j in range(len(jobs['excList'])):
                        action, stat, qsub_dir = job_progression(
                                config=jobs,
                                delay=delay,
                                stat=stat,
                                cluster='map',
                                geomDirName=geomDirName,
                                )
                        if qsub_dir != "None":
                            add_qsub_dir(
                                    qsub_dir.lower(),
                                    stat[0],
                                    path_qsub_queue
                                    )
                    job_dirs[i] = stat
                # vibrational excited states
                elif (
                        lStat == stat[3] and enabled["vib"]
                        or
                        lStat == 0 and not enabled['exc'] and enabled['vib']
                     ):

                    for j in range(len(jobs['vibList'])):
                        action, stat, qsub_dir = job_progression(
                                config=jobs,
                                delay=delay,
                                stat=stat,
                                cluster='map',
                                geomDirName=geomDirName,
                                spec_type='vibrational',
                                vib_only=vib_only
                                )
                        if qsub_dir != "None":
                            add_qsub_dir(
                                    qsub_dir.lower(),
                                    stat[0],
                                    path_qsub_queue
                                    )
                    job_dirs[i] = stat
                else:
                    print(i, 'added to kill list')
                    kill_list.append(i)
            except:
                print("%%% Need to help", stat[0])
            os.chdir(default_dir)
        for k in reversed(kill_list):
            val = job_dirs.pop(k)
            print('popped', val)
        if len(job_dirs) == 0:
            job_term.append(n)
        else:
            status[n][1] = job_dirs
    for k in reversed(job_term):
        val = status.pop(k)
    return status


def qmgr(
    config={
        "enable": {"exc": True, "vib": False},
        "options": {
            "minDelay": 360, "maxResub": 100,
            "maxQueue": 200, "cluster": "map"
            },
        "jobList": [
            {
                "dataPath": "data/48_1_1_h2o_nh3",
                "optResub": {
                    "optMethod": "B3LYP",
                    "optBasisSet": "6-31G(d)",
                    "memComFile": "1600",
                    "memPBSFile": "15",
                },
                "excList": [
                    {
                        "excMethod": "CAM-B3LYP",
                        "excBasisSet": "6-311G(d,p)",
                        "memComFile": "1600",
                        "memPBSFile": "15",
                        "nStates": 25,
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
                "vibList": [
                    {
                        "excMethod": "CAM-B3LYP",
                        "excBasisSet": "6-31+G(d,p)",
                        "memComFile": "1600",
                        "memPBSFile": "15",
                    }
                ],
            },
            {
                "dataPath": "data/48_1_1_h2o_nh3",
                "optResub": {
                    "optMethod": "B3LYP",
                    "optBasisSet": "6-31G(d)",
                    "memComFile": "1600",
                    "memPBSFile": "15",
                },
                "excList": [
                    {
                        "excMethod": "CAM-B3LYP",
                        "excBasisSet": "6-311G(d,p)",
                        "memComFile": "1600",
                        "memPBSFile": "15",
                        "nStates": 25,
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
                "vibList": [
                    {
                        "excMethod": "CAM-B3LYP",
                        "excBasisSet": "6-31+G(d,p)",
                        "memComFile": "1600",
                        "memPBSFile": "15",
                    }
                ],
            },
        ],
    }
):
    """
    qmgr jobLists submitted to this function will handle
    each cluster's requested calculations in the order of
    geometry optimizations then electronic excited states
    followed by vibrationally excited states.
    The types of excited states can be toggled on and off
    in the qmgr "enable" field.
    """
    default_dir = os.getcwd()
    if not os.path.exists("qsub_queue.txt"):
        subprocess.call("touch qsub_queue.txt", shell=True)
    jobList = config["jobList"]
    status = qmgr_setup_status_list(jobList)
    minDelay = config["options"]['minDelay']
    maxResub = config["options"]['maxResub']
    maxQueue = config["options"]['maxQueue']
    user = read_user()

    enabled = config["enable"]
    delay = False
    # total_time = minDelay * maxResub
    for i in range(maxResub):
        status = queue_logic(default_dir, status, delay, enabled)
        # qsub_to_max(maxQueue, user)
        if not delay:
            delay = True
        if len(status) == 0:
            print("All qmgr jobs are finished.")
            return
        print(
                "\nDelay:", i, 'out of', maxResub, "\n"
                )
        time.sleep(minDelay)

    return
