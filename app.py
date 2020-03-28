#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter
import numpy as np
import datetime
import os
from sklearn.linear_model import LinearRegression
import math
import get_states
import fit_curve
import charting


def main():
	''' main function'''

	# select mode for charting -- 'solo' or 'comparison'
	mode = 'solo'

	# define region of interest -- 'state', 'country', 'all countries', or 'all states'
	region = 'all countries'

	state = None

	stop_date = None

	if region == 'all countries':		
		# get a list of the all the countries
		countries = load_data('confirmed')
		countries = countries['Country/Region']
		countries = countries.drop_duplicates()
		countries = countries.tolist()

	elif region == 'all states':
		countries = get_states.state_list()
		#countries = load_data('Confirmed')
		#countries = get_data(countries, 'US', 'US')
		#countries = countries['Province/State']
		#countries = countries.drop_duplicates()
		#countries = countries.tolist()

	elif region == 'state':
		countries = 'US'
		state = 'South Carolina'

	elif region == 'country':
		countries = ['Korea, South']
	
	results = pd.DataFrame()	

	# Track celeration?
	track_celeration = 'Yes'

	if track_celeration == 'Yes':
		celerations = pd.DataFrame()

	for country in countries:

		print('NOW PROCESSING {}...'.format(country))
		print('')

		# define data type  (Confirmed, Deaths, Recovered)
		data_types = ['confirmed', 'deaths']

		# initialize blank DataFrame
		df = pd.DataFrame()

		for data in data_types:

			# Load data
			confirmed = load_data(data)
				
			# Slice regional data only
			region_df = get_data(confirmed, country, region)	
			print("four")
			if state != None:

				# Get state data
				region_df = state_data(region_df, state)

			else:
				# Drop unnecessary columns
				region_df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1, inplace=True)
			
			# Sum cumulative values for each day
			cumulative = count_data(region_df)

			# Calculate daily counts
			daily = calc_daily_count(cumulative)

			# Combine 2 series
			addition = pd.concat([cumulative, daily], axis=1)

			# Add to dataframe
			df = pd.concat([df, addition], axis=1)

		df.columns=(['Cumulative cases', 'Daily cases', 'Cumulative deaths', 'Daily deaths'])
		
		# Check if data frame is empty and skip to next country if true
		
		check = df.empty
		print(check)
		print('')

		if check == True:
			continue

		df.to_csv('China_regression_test_data.csv')

		# Regression
		df, celeration, date = fit_curve.regression(df, stop_date)
		
		# Check again if df is empty
		if  celeration == 'no_celeration':
			continue

		# Decide whether to update celeration results
		if track_celeration == 'Yes':

			# Update celeration results
			new_line = pd.Series([country, celeration])

			#celerations = celerations.append(pd.DataFrame(new_line), axis=0, ignore_index=True)	
			celerations = celerations.append(new_line, ignore_index=True)

		if mode == 'Comparison':
			# Build dataset by looping over several regions before plotting
			results = pd.concat([results, df[country + ' Daily cases']], axis=1)

		# Plot data
		charting.plot_data(df, country, state, celeration, date, region)
	
	if track_celeration == 'Yes':
		os.chdir('./celerations')
		print(celerations)
		celerations.to_csv(date+'-celerations.csv', index=False)

	print('Good bye!')
	
	return


def load_data(data):
	''' loads csv file into pandas df'''

	# change to directory for data
	os.chdir('../COVID-19/csse_covid_19_data/csse_covid_19_time_series')

	# create appropriate file name
	filename = 'time_series_covid19_' + data + '_global.csv'
	#filename = 'time_series_19-covid-' + data + '.csv'

	# read the csv into a dataframe
	df = pd.read_csv(filename)

	# return to working directory
	os.chdir('../../../celeration')
	
	return df


def get_data(df, place, region):
	''' returns df with selected regional cases only'''

	if region == 'all states':
		is_place = df['Province/State'] == place

	else:
		is_place = df['Country/Region'] == place	

	df = df[is_place]
	df.reset_index(drop=True, inplace=True)

	return df


def count_data(df):
	''' counts cumulative cases each day'''

	sums = df.apply(np.sum, axis=0)
	sums.columns = ['Cumulative']
	
	return sums


def calc_daily_count(df):
	''' calculates the daily count from the cumulative count'''

	df = df.diff()
	df.columns = ['Daily']

	return df


def state_data(df, state):
	''' plots data'''

	is_state = df['Province/State'] == state
	df = df[is_state]
	
	df.reset_index(drop=True, inplace=True)
	df.drop(['Country/Region', 'Province/State', 'Lat', 'Long'], axis=1, inplace=True)

	return df


def plot_data(df, area, state, celeration, date, mode):
	''' plots data'''

	# Build plot
	fig  = plt.figure()
	fig.set_size_inches(11, 8.5)

	#ax = df.plot(kind='line', logy=True, legend=True, marker='.', linewidth=1)

	ax = df['Cumulative cases'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['Daily cases'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['Cumulative deaths'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['Daily deaths'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['celeration curve'].plot(kind='line', marker=None, linewidth=1, logy=True, legend=True) #, color='k')	

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
	fig.text(0.6, 0.03, 'Celeration = x{:.1f} per week (not counting data points before cumulative cases reached 30, if possible)'.format(celeration),\
			horizontalalignment='left', \
			verticalalignment='center', \
			bbox=dict(facecolor='white', alpha=1.0), \
			wrap=True)
	
	fig.text(0.025, 0.025, 'Source: Johns Hopkins, https://github.com/CSSEGISandData', bbox=dict(facecolor='white', alpha=1.0))
	fig.text(0.12, 0.96, '29-Dec-2019', rotation=45)

	# label chart

	if state == None:
		plt.title('2019 nCoV in {} as of {}'.format(area, date))

	else:
		plt.title('2019 nCoV in {} as of {}'.format(state, date))

	plt.xlabel('Days')
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
	#plt.show()
	plt.close()	

	return 


if __name__ == '__main__':
	main()
