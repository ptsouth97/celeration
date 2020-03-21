#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def main():
	''' main function'''

	# define country
	country = 'Italy'

	# define data type  (Confirmed, Deaths, Recovered)
	which_data = 'Confirmed.csv'

	# load data
	confirmed = load_data(which_data)

	# slice data
	country_df = get_data(confirmed, country)
	# print(country_df)
	
	# count data
	count = count_data(country_df)
	print(count)

	# plot data
	#plot_data(count)


def load_data(data):
	''' loads csv file into pandas df'''

	os.chdir('./csse_covid_19_data/csse_covid_19_time_series')

	filename = 'time_series_19-covid-' + data
	df = pd.read_csv(filename)
	
	return df


def get_data(df, place):
	''' returns df with us cases only'''

	is_place = df['Country/Region'] == place	
	df = df[is_place]
	df.reset_index(drop=True, inplace=True)
	df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1, inplace=True)

	df.plot(marker='o', legend=None)
	#plt.show()

	return df


def count_data(df):
	''' counts new cases each day'''

	#df['delta'] = df['3/18/20'] - df['3/17/20']
	#daily = df['delta'].sum()
	#print('The US daily new cases is {}'.format(str(daily)))

	sums = df.apply(np.sum, axis=0)
	
	return sums


def plot_data(df):
	''' plots data'''

	#is_sc = df['Province/State']=='South Carolina'
	#df = df[is_sc]
	#df.reset_index(drop=True, inplace=True)
	#df.drop(['Province/State', 'Country/Region'], axis=1, inplace=True)
	#df = df.T
	#print(df.iloc[0])
	#df.set_index(df.iloc[0], inplace=True)

	print(df.shape)
	df.plot(marker='o', legend=None)
	plt.title('Cumulative Cases of COVID-19 in South Carolina')
	plt.xlabel('Days')
	plt.ylabel('Cases')
	plt.show()

	return df


if __name__ == '__main__':
	main()
