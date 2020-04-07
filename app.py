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
	while True:

		mode = input("Chart mode: 'solo' or 'comparision' ").strip()
		mode_list = ['solo', 'comparison']

		if mode in mode_list:
			break

		else:
			print('Sorry, that is not a valid option. Please try again.')
			print('')


	# define region of interest -- 'state', 'country', 'all countries', or 'all states'
	while True:
	
		region = input("What regions? 'state', 'country', 'all countries', or 'all states' ").lstrip().rstrip()
		region_list = ['state', 'country', 'all countries', 'all states']

		if region in region_list:
			break
		else:
			print('Sorry, that is not a valid option. Please try again.')
			print('')

	# Define multiple trends within one chart?
	multi_trend = input("Do you want to define multiple trends for single charts? (True/False) ").lstrip().rstrip()

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

	elif region == 'state':
		countries = 'US'
		state = 'South Carolina'

	elif region == 'country':
		countries = input('Enter the countries to analyze separated by a comma: ').split(',')
	
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
			
			if state != None:

				# Get state data
				region_df = state_data(region_df, state)

			else:
				# Drop unnecessary columns
				region_df = region_df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1)
						
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

		if check == True:
			continue

		#df.to_csv('China_regression_test_data.csv')

		# Prep data for regression
		df, date = fit_curve.prep_data(df, stop_date)

		# Regression
		df, celeration = fit_curve.regression(df, date, multi_trend)
		
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
		charting.plot_data(df, country, state, celeration, date, region, multi_trend)
	
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


if __name__ == '__main__':
	main()
