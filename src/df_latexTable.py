import pandas as pd
import re 

def df_latexTable (path, df, rounding=2):
    # Latex package \usepackage{booktabs}
    with open(path, 'w') as fp:
        #fp.write(df.to_latex(index=False)) # works but not what i entirely want

        cols = len(df.columns.values)
        cs = ''
        for i in range(cols):
            cs += ' c'
        cs += " "
        fp.write('\\begin{center}\n\\begin{tabular}{ %s }\n\t\\toprule\n' % cs)
        header_line = '\t'
        for i in df.columns.values:
            header_line += "%s & " % (i)
        header_line = header_line[:-2]
        header_line += '\\\\\n\t\\midrule\n'
        fp.write(header_line)
        for index, row in df.iterrows():
            line = '\t'
            for num, i in enumerate(df.columns.values):
                #print(index, row[i])
                cell = row[i]
                if isinstance(cell, float):
                    #significant_digits = rounding[num][0]
                    #cell = round(cell, significant_digits - int(math.floor(math.log10(abs(cell)))) - 1)
                    if rounding == 2:
                        line += '%.2f & ' % cell
                    elif rounding == 1:
                        line += '%.1f & ' % cell
                    else:
                        line += '%.4f & ' % cell
                else:
                    line +=  '%s & ' % cell
            line = line[:-2]
            line += '\\\\\n'
            fp.write(line)
        
        fp.write('\t\\bottomrule\n\\end{tabular}\n\\end{center}')
        
def latexTable_df (path, headers):
	header_dict = {}
	for i in headers:
		header_dict[i] = []
	df = pd.DataFrame(header_dict)
	with open(path, 'r') as fp:
		data = fp.read()
		data = data.replace('\\bottomrule', '\\midrule').split('\\midrule')
		data = (data[1].rstrip().split("\\\\"))[:-1]
		for i in range(len(data)):
			row = (data[i].replace("\n", '').replace('\t', '')).split(" & ")
			df.loc[len(df.index)] = row
	return df



"""
headers = ['Method', 'Basis Set', 'Excitation (eV)',
 '\\vtop{\\hbox{\\strut Oscillator Strength}\\hbox{\\strut (Normalized)}}']
df = latexTable_df('latex_df_6-311++G(2d,2p).tex', headers)
print(df)
"""
