#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter
import numpy as np
import datetime
import os


def main():
	''' main function'''

	# define region
	region = 'Italy'

	# define data type  (Confirmed, Deaths, Recovered)
	data_types = ['Confirmed', 'Deaths']

	# initialize blank DataFrame
	df = pd.DataFrame()

	for data in data_types:

		# load data
		confirmed = load_data(data)
	
		# slice regional data only
		region_df = get_data(confirmed, region)
	
		# sum cumulative values for each day
		cumulative = count_data(region_df)

		# calculate daily counts
		daily = calc_daily_count(cumulative)

		# combine 2 series
		addition = pd.concat([cumulative, daily], axis=1)

		# add to dataframe
		df = pd.concat([df, addition], axis=1)

	df.columns=(['Cumulative cases', 'Daily cases', 'Cumulative deaths', 'Daily deaths'])

	# plot data
	plot_data(df, region)


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
	''' returns df with selected regional cases only'''

	is_place = df['Country/Region'] == place	
	df = df[is_place]
	df.reset_index(drop=True, inplace=True)
	df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1, inplace=True)

	return df


def count_data(df):
	''' counts cumulative cases each day'''

	#df['delta'] = df['3/18/20'] - df['3/17/20']
	#daily = df['delta'].sum()
	#print('The US daily new cases is {}'.format(str(daily)))

	sums = df.apply(np.sum, axis=0)
	sums.columns = ['Cumulative']
	
	return sums


def calc_daily_count(df):
	''' calculates the daily count from the cumulative count'''

	df = df.diff()
	df.columns = ['Daily']

	return df


def plot_data(df, area):
	''' plots data'''

	#is_sc = df['Province/State']=='South Carolina'
	#df = df[is_sc]
	#df.reset_index(drop=True, inplace=True)
	#df.drop(['Province/State', 'Country/Region'], axis=1, inplace=True)
	#df = df.T
	#print(df.iloc[0])
	#df.set_index(df.iloc[0], inplace=True)

	# Combine 2 series into dataframe
	# df = pd.concat([s1, s2], axis=1)

	# change index to datetime
	df.index = pd.to_datetime(df.index, infer_datetime_format=True) #format='%m/%-d/%y')
	print(df)

	
	# change series back to df
	#df = pd.DataFrame(df)

	# assign column name
	#df.columns = ['Cumulative', 'Daily']

	# plot df
	ax = df.plot(marker='o', markersize=3, linewidth=1, logy=True, legend=True)

	# set the range for the y axis
	ax.set_ylim([1, 1000000])

	# turn on major and minor grid lines for y axis 
	ax.yaxis.grid(True, which='minor', linestyle='-', alpha=0.5)
	ax.yaxis.grid(True, which='major', linestyle='-', alpha=0.8)
	
	# move x-axis labels to the top
	# ax.xaxis.set_ticks_position('top')

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

	# label chart
	plt.title('COVID-19 in ' + area)
	plt.xlabel('Days')
	plt.ylabel('Counts of Cases and Deaths')
	
	# change to appropriate directory to save chart
	os.chdir('./charts')
	
	# save chart
	plt.savefig(area + '.png')
	
	# change back to original working directory
	os.chdir('..')

	# display the chart
	plt.show()
	

	return df


if __name__ == '__main__':
	main()
