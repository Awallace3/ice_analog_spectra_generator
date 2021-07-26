import glob
import os
import subprocess
from gen_input_files import gaussianInputFiles
import gather_energies
import numpy as np
import find_geom
import gen_input_files
"""
path = '%s' % baseName
qsub(path)
baseName = 'mo'
os.mkdir(baseName)
procedure = 'SP GFINPUT POP=FULL'
output_num = 0
"""

def qsub(path='.'):
    resetDirNum = len(path.split("/"))
    if path != '.':
        os.chdir(path)
    pbs_file = glob.glob("*.pbs")[0]
    cmd = 'qsub %s' % pbs_file
    print(os.getcwd(), "cmd", cmd)
    failure = subprocess.call(cmd, shell=True)
    if path != '.':
        for i in range(resetDirNum):
            os.chdir("..")

def discern_base_dir_name(
	method_mexc='CAM-B3LYP',
	basis_set_mexc='6-311G(d,p)',
	nStates='25'
	):
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
	return path_mexc

def gen_mo_files(
		method_basisSet = [['CAM-B3LYP', '6-311G(d,p)']], 
		num_lowest_energy_clusters=2,
		cluster='map',
		mem_com_mexc=1600, 
		mem_pbs_mexc=10,
		nStates='25'
	):
	gather_energies.main()	
	energies = np.genfromtxt('results/energies/energy_all.csv', delimiter=',')
	energies = energies[energies[:,1].argsort()]
	investigate = energies[:num_lowest_energy_clusters, 0].astype('int')
	print(investigate)
	os.chdir("calc_zone")
	for num in investigate:
		print('geom%d'%num)
		os.chdir("geom%d"%num)

		out_files = glob.glob("*.out*")
		if len(out_files) == 0:
			print("NO OUT FILE")
			return

		last_out = out_files[0]
		highest = 1
		for i in range(len(out_files)):
			t = out_files[i][-1]
			if t =='t':
				t = 1
			else:
				t = int(t)
			if t > highest:
				t = highest
				last_out = out_files[i]
		with open(last_out, 'r') as fp:
			lines = fp.readlines()
		find_geom.find_geom(lines, error=False, filename=last_out,
									imaginary=False, geomDirName=i
		)
		with open('tmp.txt', 'r') as fp:
			data = fp.read()
		#print(data)
		os.remove('tmp.txt')

		for i in method_basisSet:
			
			path_mexc = discern_base_dir_name(i[0], i[1], nStates)
			print(path_mexc)
			os.chdir(path_mexc)

			baseName = 'mo'
			os.mkdir(baseName)
			procedure = 'SP GFINPUT POP=FULL'
			output_num = 0
			gen_input_files.gaussianInputFiles(
				output_num, i[0], 
				i[1], mem_com_mexc, 
				mem_pbs_mexc, cluster,
				baseName, procedure,
				data=data,
			)
			path = '%s' % baseName
			qsub(path)

			os.chdir("..")
		os.chdir("..")




if __name__ == "__main__":
	gen_mo_files()