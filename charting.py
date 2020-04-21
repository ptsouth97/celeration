#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter
import numpy as np
import datetime
import os


def main():
	''' main function'''
	
	pass
	
	return


def plot_data(df, area, state, celeration, date, mode, multi):
	''' plots data'''

	# Build plot
	fig  = plt.figure()
	fig.set_size_inches(11, 8.5)

	#ax = df.plot(kind='line', logy=True, legend=True, marker='.', linewidth=1)

	ax = df['Cumulative cases'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['Daily cases'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['Cumulative deaths'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['Daily deaths'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	#ax = df['celeration curve'].plot(kind='line', marker=None, linewidth=1, logy=True, legend=True) #, color='k')	
	

	# Add any necessary vertical lines
	#plt.axvline(x=datetime.datetime(2020, 3, 17), color='yellow', linewidth=1)
	#plt.axhline(y=1000, color='red', linewidth=1, linestyle='--')	
	
	# Set the range for the y axis
	ax.set_ylim([1, 1000000])

	# turn on major and minor grid lines for y axis 
	ax.yaxis.grid(True, which='minor', linestyle='-', alpha=0.5)
	ax.yaxis.grid(True, which='major', linestyle='-', alpha=0.8)
	
	# set the range for the x axis
	ax.set_xlim([datetime.date(2019, 12,29), datetime.date(2020, 5, 17)])

	# set the location for the x axis ticks
	ax.xaxis.set_minor_locator(MultipleLocator(1))
	ax.xaxis.set_major_locator(MultipleLocator(7))

	# turn on the major and minor grid lines for x axis
	ax.xaxis.grid(True, which='minor', linestyle='-', alpha=0.5)
	ax.xaxis.grid(True, which='major', linestyle='-', alpha=0.8)

	# set x labels
	ax.set_xticklabels(np.arange(0, 141, 7))
	
	
	# Create text box
	'''fig.text(0.6, 0.028, 'Celeration = x{:.1f} per week (not counting data points before cumulative cases reached 30, if possible)'.format(celeration),\
			horizontalalignment='left', \
			verticalalignment='center', \
			bbox=dict(facecolor='white', alpha=1.0), \
			wrap=True)'''
	
	fig.text(0.025, 0.013, 'Source: Johns Hopkins, https://github.com/CSSEGISandData' + '\n' \
			+ 'Charter: Blake Crosby, https://github.com/ptsouth97/celeration', bbox=dict(facecolor='white', alpha=1.0))

	#fig.text(0.025, 0.015, 'Charter: Blake Crosby, https://github.com/ptsouth97/celeration')
	fig.text(0.12, 0.96, '29-Dec-2019', rotation=45)

	# label chart

	if state == None:
		plt.title('2019 nCoV in {} as of {}'.format(area, date))

	else:
		plt.title('2019 nCoV in {} as of {}'.format(state, date))

	plt.xlabel('Successive Calendar Days')
	plt.ylabel('Counts of Cases and Deaths')
	
	# change to appropriate directory to save chart
	os.chdir('./charts')

	if 'state' in mode:
		folder = 'states'

	else:
		folder = 'countries'

	if not os.path.exists('./' + date + '/' + folder):
		os.makedirs('./'+date+'/'+folder)
	

	os.chdir('./'+date+'/'+folder)
		
	# save chart
	if state == None:
		plt.savefig(date+'-'+area+'.png')

	else:
		plt.savefig(date+'-'+state + '.png')
	
	# change back to original working directory
	os.chdir('../../..')

	# display the chart
	if multi == True:
		plt.show()

	plt.close()	

	return 


if __name__ == '__main__':
	main()
