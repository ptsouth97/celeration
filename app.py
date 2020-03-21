#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np
import datetime
import os


def main():
	''' main function'''

	# define region
	region = 'Italy'

	# define data type  (Confirmed, Deaths, Recovered)
	which_data = 'Confirmed'

	# load data
	confirmed = load_data(which_data)

	# slice data
	region_df = get_data(confirmed, region)
	# print(country_df)
	
	# count data
	count = count_data(region_df)
	#print(count)

	# plot data
	plot_data(count, region, which_data)


def load_data(data):
	''' loads csv file into pandas df'''

	# change to directory for data
	os.chdir('../COVID-19/csse_covid_19_data/csse_covid_19_time_series')

	# create appropriate file name
	filename = 'time_series_19-covid-' + data + '.csv'

	# read the csv into a dataframe
	df = pd.read_csv(filename)

	# return to working directory
	os.chdir('../../../celeration')
	
	return df


def get_data(df, place):
	''' returns df with us cases only'''

	is_place = df['Country/Region'] == place	
	df = df[is_place]
	df.reset_index(drop=True, inplace=True)
	df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1, inplace=True)

	return df


def count_data(df):
	''' counts new cases each day'''

	#df['delta'] = df['3/18/20'] - df['3/17/20']
	#daily = df['delta'].sum()
	#print('The US daily new cases is {}'.format(str(daily)))

	sums = df.apply(np.sum, axis=0)
	
	return sums


def plot_data(df, area, data):
	''' plots data'''

	#is_sc = df['Province/State']=='South Carolina'
	#df = df[is_sc]
	#df.reset_index(drop=True, inplace=True)
	#df.drop(['Province/State', 'Country/Region'], axis=1, inplace=True)
	#df = df.T
	#print(df.iloc[0])
	#df.set_index(df.iloc[0], inplace=True)

	# change index to datetime
	df.index = pd.to_datetime(df.index, infer_datetime_format=True) #format='%m/%-d/%y')

	# change series back to df
	df = pd.DataFrame(df)

	# assign column name
	df.columns = [area]

	# plot df
	ax = df.plot(marker='o', \
			logy=True, \
			legend=True, \
			use_index=True, \
			ylim=(0, 1000000))


	# change major and minor gridline locations
	#major_ticks = np.arange(0, 141, 20)
	#ax.set_xticks(major_ticks)
	#ax.grid(True, which='major', alpha=0.5)

	#minor_ticks = np.arange(0, 141, 140)
	#ax.set_xticks(minor_ticks, minor=True)
	#ax.grid(True, which='minor', alpha=0.2)

	#ax.grid(which='both')

	# draw gridlines on the y axis
	ax.yaxis.grid(True, which='minor', linestyle='-', alpha=0.5)
	ax.yaxis.grid(True, which='major', linestyle='-', alpha=0.8)
	
	#ax.xaxis.grid(True, which='minor', linestyle='-')
			
	# move x-axis labels to the top
	# ax.xaxis.set_ticks_position('top')

	# draw gridlines on the x axis
	ax.set_xlim([datetime.date(2019, 12,29), datetime.date(2020, 5, 17)])

	ax.xaxis.set_minor_locator(MultipleLocator(1))
	ax.xaxis.set_major_locator(MultipleLocator(7))

	ax.xaxis.grid(True, which='minor', linestyle='-', alpha=0.5)
	ax.xaxis.grid(True, which='major', linestyle='-', alpha=0.8)

	# label chart
	plt.title('COVID-19 in ' + area)
	plt.xlabel('Days')
	plt.ylabel(data + ' Cases')
	
	plt.savefig('test.png')
	plt.show()

	return df


if __name__ == '__main__':
	main()
