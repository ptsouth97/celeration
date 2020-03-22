#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter
import numpy as np
import datetime
import os
from sklearn.linear_model import LinearRegression
import math


def main():
	''' main function'''

	# define region
	countries = ['Singapore']

	# get a list of the countries
	'''countries = load_data('Confirmed')
	countries = countries['Country/Region']
	countries = countries.drop_duplicates()
	countries = countries.tolist()'''
	
	for country in countries:

		print('Now processing {}...'.format(country))

		# define data type  (Confirmed, Deaths, Recovered)
		data_types = ['Confirmed', 'Deaths']

		# initialize blank DataFrame
		df = pd.DataFrame()

		for data in data_types:

			# load data
			confirmed = load_data(data)
	
			# slice regional data only
			region_df = get_data(confirmed, country)
	
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
		plot_data(df, country)


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

	sums = df.apply(np.sum, axis=0)
	sums.columns = ['Cumulative']
	
	return sums


def calc_daily_count(df):
	''' calculates the daily count from the cumulative count'''

	df = df.diff()
	df.columns = ['Daily']

	return df


def regression(df):
	''' performs curve fit'''

	# filter out row where cumulative cases is greater than 30
	greater_30 = df['Cumulative cases']>30
	df = df[greater_30]
	
	# replace 0's in data frame with 1's to prevent errors
	df = df.replace(to_replace=0, value=1)

	# find number of days between end of chart and start date
	start = df.index[0]
	end = datetime.datetime(2020, 5, 17)
	days = (end - start).days
	shift = 140 - days

	# Create X and Y prediction spaces
	num = len(df)
	X = np.arange(1, num+1).reshape(-1, 1)
	Y = df['Daily cases'].values.reshape(-1, 1)
	
	# Perform regression	
	linear_regressor = LinearRegression()
	linear_regressor.fit(X, np.log(Y))

	# Get linear regression parameters
	m = linear_regressor.coef_
	b = linear_regressor.intercept_

	# Initialize and fill data frame for regression results
	values = []
	
	for value in range(1, 140): #days+1):   # changed 'begin' from '1'
		values.append(math.exp(m*(value-shift) + b))

	# Create a date frame the size of the celeration chart and fill it with the calculated values
	predictions = pd.DataFrame(index=[np.arange(1, 140)], data=values)

	# Create a data frame to join with the predictions that matches the size of the celeration chart
	total_days = 140
	early_days = 140 - days
	early_predictions = pd.DataFrame(np.zeros((early_days, 1)))

	predictions = predictions.append(early_predictions)
	predictions.reset_index(inplace=True)
	predictions.drop(['index'], axis=1, inplace=True)


	# Convert index back to dates
	dates = predictions.index.values
	dates = dates.tolist()
	
	dates = [ datetime.datetime(2019, 12, 29) + datetime.timedelta(days=date) for date in dates ]

	predictions['dates'] = dates
	predictions.set_index('dates', inplace=True)
	predictions = predictions.rename(columns={0: 'celeration curve'})
	predictions.replace(to_replace=0, value=np.nan, inplace=True)
	

	# Calculate the celeration value
	week1 = float(predictions.iloc[78])
	week0 = float(predictions.iloc[71])
	celeration = week1 / week0
	
	return predictions, celeration


def state_data(df, area):
	''' plots data'''

	is_sc = df['Province/State']=='South Carolina'
	df = df[is_sc]
	df.reset_index(drop=True, inplace=True)
	df.drop(['Province/State', 'Country/Region'], axis=1, inplace=True)
	df = df.T
	print(df.iloc[0])
	df.set_index(df.iloc[0], inplace=True)

	return


def plot_data(df, area):
	''' plots data'''

	# get the current date
	date = df.index[-1]
	
	# replace date slashes with dashes
	date = date.replace('/', '-')

	# replace NaN values with 0
	df = df.fillna(0)

	# change index to datetime
	df.index = pd.to_datetime(df.index, infer_datetime_format=True) #format='%m/%-d/%y')
	
	Y_pred, celeration = regression(df)

	# Add predictions to dataframe
	df = pd.concat([df, Y_pred], axis=1)

	# Build plot
	fig = plt.figure()
	fig.set_size_inches(11, 8.5)

	ax = df['Cumulative cases'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['Daily cases'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	#ax = df['Cumulative deaths'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	#ax = df['Daily deaths'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
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
	fig.text(0.8, 0.2, 'Celeration = x{:.1f} per week'.format(celeration), \
			horizontalalignment='center', \
			verticalalignment='center', \
			bbox=dict(facecolor='white', alpha=1.0))

	fig.text(0.025, 0.025, 'Source: Johns Hopkins', bbox=dict(facecolor='white', alpha=1.0))
	fig.text(0.12, 0.96, '29-Dec-2019', rotation=45)

	# label chart
	plt.title('2019 nCoV in {} as of {}'.format(area, date))
	plt.xlabel('Days')
	plt.ylabel('Counts of Cases and Deaths')
	
	# change to appropriate directory to save chart
	os.chdir('./charts')

	if not os.path.exists('./' + date):
		os.mkdir(date)
	
	os.chdir('./' + date)
	
	# save chart
	plt.savefig(area + '.png')
	
	# change back to original working directory
	os.chdir('../..')

	# display the chart
	plt.show()
	

	return df


if __name__ == '__main__':
	main()
