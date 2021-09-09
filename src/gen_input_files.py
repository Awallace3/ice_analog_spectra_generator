def CFOUR_input_files(
    method, basis_set, 
    mem_ZMAT, mem_pbs, data, dir_name, cluster='map',
    baseName='mexc', 
 ):
    if cluster == 'map':
        with open('%s/ZMAT' % (dir_name), 'w') as fp:
            fp.write("%s\n" % (dir_name))
            fp.write(data)
            fp.write('\n\n')
            fp.write("*CFOUR(CHARGE=0,REFERENCE=RHF,SPHERICAL=ON,BASIS=%s\n" % basis_set)
            fp.write("LINDEP_TOL=7,LINEQ_CONV=7,SCF_CONV=6,SCF_MAXCYC=250\n")
            fp.write("CALC=%s,EXCITE=EOMEE,ESTATE_SYM=5\nESTATE_PROP=EXPECTATION\nCOORDS=CARTESIAN\n" % method) 
            fp.write("FROZEN_CORE=ON,ABCDTYPE=AOBASIS\nCONVERGENCE=7,MEMORY_SIZE=%s,MEM_UNIT=GB)\n" % mem_ZMAT)
        with open('%s/%s.pbs' % (dir_name, baseName), 'w') as fp:
            fp.write("#!/bin/csh\n#\n#PBS -N %s\n" % baseName)
            fp.write("#PBS -S /bin/csh\n#PBS -j oe\n#PBS -W umask=022\n#PBS -l cput=2400:00:00\n#PBS -l mem=%sgb\n#PBS -l nodes=1:ppn=2\n#PBS -q gpu" % mem_pbs)
            fp.write('\n\ncd $PBS_O_WORKDIR\nsetenv NUM $NCPUS\necho "$NUM cores requested in PBS file"\necho " "\nsource /ddn/home1/r1621/.tschrc\n/ddn/home1/r1621/maple/bin/tempQC/bin/c4ext_old.sh 20\n')
    return

def gaussianInputFiles(output_num, method_opt, 
                    basis_set_opt, mem_com_opt, 
                    mem_pbs_opt, cluster, 
                    baseName='mexc', procedure='OPT',
                    data='', dir_name='', solvent='', 
                    outName='mexc_o'
                    ):
    # baseName = baseName.com / baseName.pbs / baseName.out
    # dir_name = directory name 
    output_num = str(output_num)
    if output_num == '0':
        output_num = ''

    if dir_name=='':
        dir_name=baseName
    
    if data == '':
        with open('tmp.txt') as fp:
            data = fp.read()

    # Reading data from file2
    charges = "0 1"

    if cluster == "map":
        with open('%s/%s.com' % (dir_name, baseName), 'w') as fp:
            fp.write("%mem={0}mb\n".format(mem_com_opt))
            fp.write("%nprocs=4\n")
            if solvent == '':
                fp.write("#N %s/%s %s" % (method_opt, basis_set_opt, procedure))
            else:
                fp.write("#N %s/%s %s %s" % (method_opt, basis_set_opt, procedure, solvent))

            fp.write("\n\n")
            fp.write("Name ModRedundant - Minimalist working constrained optimisation\n")
            fp.write("\n")
            fp.write(charges + "\n")
            fp.write(data)
            fp.write("\n")

        with open('%s/%s.pbs' % (dir_name, baseName), 'w') as fp:
            fp.write("#!/bin/sh\n")
            fp.write("#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l " % outName)
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            # r410 node
            fp.write("#PBS -q r410\n")
            fp.write("#PBS -W umask=022\n")
            fp.write(
                "#PBS -l nodes=1:ppn=1\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
            fp.write(
                "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
            fp.write(
                """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n""")
            fp.write("then\n")
            fp.write(
                "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n")
            fp.write(
                """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n""")
            fp.write(
                "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n")
            fp.write("""  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n""")
            fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
            fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
            fp.write("cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 {0}.com {0}.out".format(baseName, baseName) +
                    str(output_num) + "\n\nrm -r $scrdir\n")
    elif cluster == 'seq':
        with open('%s/%s.com' % (dir_name, baseName), 'w') as fp:
            fp.write('%mem=8gb\n')
            if solvent == '':
                fp.write("#N %s/%s %s" % (method_opt, basis_set_opt, procedure))
            else:
                fp.write("#N %s/%s %s %s" % (method_opt, basis_set_opt, procedure, solvent))

            fp.write("\n\n")
            fp.write("Name \n")
            fp.write("\n")
            fp.write(charges + "\n")
            fp.write(data)
            fp.write("\n")

        with open('%s/%s.pbs' % (dir_name, baseName), 'w') as fp:
            fp.write("#!/bin/sh\n")
            fp.write("#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -W umask=022\n#PBS -j oe\n#PBS -m abe\n#PBS -l cput=1000:00:00\n#PBS -l " % outName)
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            fp.write("#PBS -l nodes=1:ppn=2\n#PBS -l file=100gb\n\n")
            fp.write("export g09root=/usr/local/apps/\n. $g09root/g09/bsd/g09.profile\n\n")
            fp.write("scrdir=/tmp/bnp.$PBS_JOBID\n\nmkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
            fp.write("printf 'exec_host = '\nhead -n 1 $PBS_NODEFILE\n\ncd $PBS_O_WORKDIR\n\n")
            fp.write("/usr/local/apps/bin/g09setup %s.com %s.out%s" % (baseName, baseName, output_num))
