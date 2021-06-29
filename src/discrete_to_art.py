import numpy as np
import numpy as np
import os
import glob
import subprocess

def unit_conversion(data, x_units=['nm', 'eV']):
	if x_units[0]=='nm' and x_units[1]=='eV':
		h = 6.62607004E-34
		c = 3E17
		Joules_to_eV = 1.602E-19
		for i in range(len(data[:,0])):
			data[i,0] = h*c/(data[i,0]*Joules_to_eV)
		return data
	else:
		print("Unit conversion is not supported yet.")



def discrete_to_art(path, x_units=['nm', 'eV'], x_range=[100, 320], broadening=2.0):
	location = os.getcwd().split("/")[-1]
	path_src = ''
	if location == 'src':
		pass
	else:
		path_src += 'src/'

	data = np.genfromtxt(path)
	np.savetxt('data', data, delimiter=' ')
	cmd = 'perl %sspecsim_args.pl %.2f %.2f %.2f' % (path_src, x_range[0], x_range[1], broadening) 
	subprocess.call(cmd, shell=True)
	data = np.genfromtxt('spec')
	os.remove('data')
	os.remove('spec')
	data = unit_conversion(data, x_units)
	return data

if __name__ == '__main__':
	discrete_to_art('../../ribbon/8rib_cam.dat', x_units=['nm', 'eV'])