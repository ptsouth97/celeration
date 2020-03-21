#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter
import numpy as np
import datetime
import os
from sklearn.linear_model import LinearRegression


def main():
	''' main function'''

	# define region
	countries = ['Italy']

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


def regression(df):
	''' performs curve fit'''

	df = df.replace(to_replace=0, value=1)
	start_date = df.index[0]
	
	num = len(df)
	X = np.arange(1, num+1).reshape(-1, 1)
	Y = df.iloc[:, 1].values.reshape(-1, 1)
	
	linear_regressor = LinearRegression()
	linear_regressor.fit(X, np.log(Y))
	Y_pred = linear_regressor.predict(X)

	predictions = pd.DataFrame(Y_pred, index=df.index)
	predictions = predictions.apply(np.exp, axis=0)

	return predictions


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
	
	Y_pred = regression(df)

	# Add predictions to dataframe
	df = pd.concat([df, Y_pred], axis=1)
	df = df.rename(columns={0: 'model'})
	print(df)	

	#ax = plt.plot(df['Daily cases'])
	ax = df['Cumulative cases'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['Daily cases'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['Cumulative deaths'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['Daily deaths'].plot(kind='line', marker='.', linewidth=1, logy=True, legend=True)
	ax = df['model'].plot(kind='line', marker=None, linewidth=1, logy=True, legend=True)
	
	# set the range for the y axis
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

	# label chart
	plt.title('2019 nCoV in ' + area + ' as of ' + date)
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
