import os
import glob
import numpy as np

def Convert(string):
	li = list(string.split(" "))
	return li

def cleanLine(line):
	aList = []
	cropped_line = line.rstrip()
	for i in range(2,10):
		k = ' ' * i
		cropped_line = cropped_line.replace(k, " ")
	cropped_line = cropped_line.split(" ")
	for i in cropped_line:
		if i == '':
			continue
		else: 
			aList.append(float(i))
	return aList

def conv_num(string):
	li = list(string.split(" "))
	return li


def clean_many_txt(geomDirName, xyzSmiles=True, numbered=True):
	""" This will replace the numerical forms of the elements as their letters numbered in order """

	f = open('tmp.txt', 'r')
	"""
	a = ['14.0 ','30.0 ' ,
			'16.0 ', '6.0 ', 
			'8.0 ', '1.0 ', 
			'7.0 ' 
		]
	table = {
		'6.0 ': 'C', '8.0 ': 'O', 
		'1.0 ': 'H', '7.0 ': 'N', 
		'16.0 ': 'S', '30.0 ': 'Zn', 
		'14.0 ': 'Si'
	}
	"""
	a = ['14.000000 ','30.000000 ' ,
			'16.000000 ', '6.000000 ',
			'8.000000 ', '1.000000 ',
			'7.000000 '
		]
	table = {
		'6.000000 ': 'C', '8.000000 ': 'O',
		'1.000000 ': 'H', '7.000000 ': 'N',
		'16.000000 ': 'S', '30.000000 ': 'Zn',
		'14.000000 ': 'Si'
	}


	xyzToMolLst = []
	lst = []
	cnt2 = 0
	for line in f:
		cnt2 += 1
		for word in a:
			if word in line:
				convert_wrd = table[word]
				line2 = line.replace(word, convert_wrd + " ")
				if numbered:
					line = line.replace(word, convert_wrd + str(cnt2) + " ")
				else:
					line = line.replace(word, convert_wrd + " ")

				

		lst.append(line)
		xyzToMolLst.append(line2)
	f.close()
	f = open('tmp.txt', 'w')
	length = 0
	for line in lst:
		f.write(line)
		length += 1
	f.close()
	#if xyzSmiles:
	#	xyzToSmiles(length, xyzToMolLst, geomDirName)

def find_geom(lines, error, filename, imaginary, geomDirName,
    xyzSmiles=False, numberedClean=True
):
	word_error = "Error"
	geom_start = "Standard orientation:"

	geom_end = " Standard basis:"
	standards = []
	orientation = []
	found = False
	geom_size = 0
	geom_list = []
	with open(filename) as search:
		for num, line in enumerate(search, 1):
			if " Charge =  0 Multiplicity = 1" in line:
				geom_size = num + 1
				found = True
			elif found == True and num < geom_size + 200:
				geom_list.append(line)
			elif found == True and line == ' \n':
				break
	clean_geom_size = []
	for i in geom_list:
		if not " \n" == i:
			clean_geom_size.append(i)
		elif i == ' \n':
			break
	geom_size = len(clean_geom_size)
	if error == True:
		pop_2 = "Population analysis using the SCF Density."
		pops = []
		pop_2_test = False
		with open(filename) as search:
			for line in search:
				if pop_2 in line:
					pops.append(1)
				if len(pops) == 2:
					pop_2_test = True
		if pop_2_test == True:
			with open(filename) as search:
				for num, line in enumerate(search, 1):
					if geom_start in line:
						standards.append(num + 5)

			geom_end_pops = " Rotational constants (GHZ):"
			with open(filename) as search:
				for num, line in enumerate(search, 1):
					if geom_end_pops in line:
						orientation.append(num - 1)
		else:
			with open(filename) as search:
				for num, line in enumerate(search, 1):
					if geom_start in line:
						standards.append(num + 5)
						
			with open(filename) as search:
				for num, line in enumerate(search, 1):
					if geom_end in line:
						orientation.append(num - 2)
	else:

		with open(filename) as search:
			for num, line in enumerate(search, 1):
				if geom_start in line:
					standards.append(num + 5)

		with open(filename) as search:
			for num, line in enumerate(search, 1):
				if geom_end in line:
					orientation.append(num - 2)
	if len(orientation) < 6:
		orien = len(orientation)
	else:
		orien = 5
	if len(standards) < 6:
		stand = len(standards)
	else:
		stand = 5
	for i in range(-1, -orien, -1):
		for j in range(-1, -stand, -1):
			length = orientation[i] - standards[j]
			if length == geom_size:
				orien = i
				stand = j
				break
	if stand == 5:
		stand = -1
	del lines[standards[stand] - 1 + length:]
	del lines[:standards[stand] - 1]

	cleaned_lines = []
	for i in range(len(lines)):
		clean = cleanLine(lines[i])
		cleaned_lines.append(clean)

	start_array = np.array(cleaned_lines)
	new_geom = np.zeros(((int(len(start_array[:, 3]))), 4))
	new_geom[:, 0] = start_array[:, 1]
	new_geom[:, 1] = start_array[:, 3]
	new_geom[:, 2] = start_array[:, 4]
	new_geom[:, 3] = start_array[:, 5]

	out_file = "tmp.txt"
	np.savetxt(out_file, new_geom,
				fmt="%f")

	if not imaginary:
		clean_many_txt(geomDirName, xyzSmiles, numberedClean)
	elif error:
		clean_many_txt(geomDirName, xyzSmiles, numberedClean)
