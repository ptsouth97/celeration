#!/usr/bin/python3

import pandas as pd
import os


def main():
	''' Main function'''

	path = './celerations'
	filelist = os.listdir(path)
	filelist.sort()
	print(filelist)
	filelist = filelist[-2:]
	date = filelist[-1]

	os.chdir(path)

	results = pd.DataFrame()

	for a_file in filelist:

		df = pd.read_csv(a_file, index_col=0) #, columns=['country', 'celeration'])
		results = results.merge(df, how='outer', left_index=True, right_index=True)
		
		

	results['delta'] = results['1_y'] - results['1_x']

	print(results)

	os.chdir('../old_celerations')

	results.to_csv(date+'-results.csv')
	#print(df.index)


if __name__ == '__main__':
	main()
