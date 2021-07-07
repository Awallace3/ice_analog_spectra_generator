import subprocess
import numpy as np
import os

import sys

from numpy.ma import nomask
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
	
def data_to_specsim(data, x_range=[6, 12], deltaG=1):
	np.savetxt('data', data, delimiter=" ")
	cmd = 'perl specsim_args.pl %.2f %.2f %.2f' % (x_range[0], x_range[1], deltaG)
	subprocess.call(cmd, shell=True)
	data = np.genfromtxt('spec')
	os.remove('data')
	os.remove('spec')
	return data

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

def read_data(path, delim=','):
	return np.genfromtxt(path)

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

def discrete_pre_specsim():
	method = 'CAM-B3LYP'
	basis_set_mexc = '6-311++G(2d,2p)'
	nStates = '50'
	acquiredStates = '45'
	T = 457.088     # co2

	gather_exc_energies(method, basis_set_mexc, nStates, acquiredStates, T)
	data = read_specsim_data_eV("results/final/data/data")
	display_discrete_plot(data)

def plot_data(data_lst_comp, data_lst_exp,
			mol='h2o',
			title='',
			x_label='Energy (eV)', 
			y_label='Oscillator Strength',
			x_range=[6, 10.5],
			y_range=[0,1.2]
			):
	fig, ax1 = plt.subplots(dpi=200)
	for i in data_lst_comp:
		ax1.plot(i[0][:,0], i[0][:,1], i[2], label=i[1])

	for i in data_lst_exp:
		ax1.plot(i[0][:,0], i[0][:,1], i[2], label=i[1])
	#ax1.set_title("CAM-B3LYP/6-311G(d,p)")
	ax1.set_title(title)
	ax1.set_ylabel(y_label)
	ax1.set_ylim(y_range)
	ax1.set_xlabel(x_label)
	ax1.set_xlim(x_range)
	ax1.legend(loc='best')

	plt.savefig("../../gas_solid/gas_solid_%s.png"%mol)	

def energy_cut_off(data, value, above=True):
	data = data[data[:, 0].argsort()]
	pos = -1
	for i in range(len(data[:,0])):
		if above:
			if data[i,0] < value:
				pos = i
				break
		else:
			if data[i,0] > value:
				pos = i
				break
	end=len(data[:,0])
	if above:
		data = np.delete(data, np.s_[0:pos], axis=0)
	else:
		data = np.delete(data, np.s_[pos:end], axis=0)
	#rint(data)
	return data

def normalize(data):
	maxy = np.max(data[:,1], axis=0)
	for i in range(len(data[:,1])):
		data[i, 1] = data[i,1] / maxy
	return data

def conv_nm_to_eV(data):
	h=6.6261E-34
	c=2.998E17
	J_eV = 1.602E-19
	for i in range(len(data[:,0])):
		data[i,0] = h*c/(data[i,0]*J_eV)
	data = data[data[:,0].argsort()]	
	return data

def gas_solid_plot_h2o():
	mol = 'h2o'
	exp_solid = np.genfromtxt('../../../exp_data/%s_solid.csv'% mol, delimiter=', ')
	exp_gas = np.genfromtxt('../../../exp_data/%s_gas.csv'% mol, delimiter=', ')
	mon = read_data('../../gas_solid/mon_ev_osc.txt', delim=' ')
	mon = data_to_specsim(mon, [6,11], 0.10)

	#rand8 = conv_nm_to_eV(read_data('../../8_rand_ice/results/final/data/spec', delim=' '))

	rand32 = conv_nm_to_eV(read_data('../results/final/data/spec', delim=' '))

	data_lst_comp = [[mon, 'Monomer', '-'], [rand32, '32 Randomized Clusters', '-']]
	data_lst_exp = [[exp_gas, 'Exp. Gas', '--'], [exp_solid, 'Exp. Solid', '--']] 
	for n, i in enumerate(data_lst_comp):
		data_lst_comp[n][0] = normalize(energy_cut_off(i[0], 11, False))
	for n, i in enumerate(data_lst_exp):
		data_lst_exp[n][0] = normalize(i[0])
	
	
	plot_data(data_lst_comp, data_lst_exp, title='CAM-B3LYP/6-311G(d,p)')

if __name__ == '__main__':
	gas_solid_plot_h2o()
	




