import numpy as np
import os

import sys
sys.path.insert(1, '..') # this adds src to python path at runtime for modules
from ice_manager import boltzmannAnalysisSetup
from ice_manager import boltzmannAnalysis
from gather_energies import main as gather_energies
import glob
import matplotlib.pyplot as plt

def gather_exc_energies(method, basis_set_mexc, nStates, acquiredStates, T):
	assume_complete = []
	for i in range(len(glob.glob("calc_zone/geom*"))):
		assume_complete.append(2)
	
	#os.chdir('../calc_zone')
	boltzmannAnalysisSetup(assume_complete, method, basis_set_mexc, nStates, acquiredStates)
	boltzmannAnalysis(T)
	print(os.getcwd())
	#os.chdir("../src")
	

def read_specsim_data_eV(path):
	data = np.genfromtxt(path, delimiter=' ')
	h=6.6261E-34
	c=2.998E17
	J_eV = 1.602E-19
	eV_nm = 1239.8 # eV/nm
	for i in range(len(data[:, 0])):
		data[i, 0] =  h*c/data[i, 0] / J_eV
		#data[i, 0] =  eV_nm/data[i, 0]
	data[data[i,0].argsort()]
	#print(data)
	return data



def display_discrete_plot(data): # 2d np.array
	xs = []
	ys = []
	
	for i in range(len(data[:, 0])):
		for j in range(3):
			xs.append(data[i,0])
			if j == 0 or j ==2:
				ys.append(0)
			elif j == 1:
				ys.append(data[i,1])
	fig, ax1 = plt.subplots(dpi=200)
	ax1.plot(xs, ys, linewidth=0.1)
	#print(xs, ys)
	#ax1.set_xlim(6,12)
	#plt.show() 
	plt.savefig('results/testing/pre_specsim.png')


if __name__ == '__main__':
	#print(os.getcwd())
	method = 'CAM-B3LYP'
	basis_set_mexc = '6-311++G(2d,2p)'
	nStates = '50'
	acquiredStates = '45'
	T = 457.088     # co2
	gather_exc_energies(method, basis_set_mexc, nStates, acquiredStates, T)

	data = read_specsim_data_eV("results/final/data/data")
	display_discrete_plot(data)

