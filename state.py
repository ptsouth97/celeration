#!/usr/bin/python3

import pandas as pd
import os


def main():
	''' main function'''

	os.chdir('../COVID-19/csse_covid_19_data/csse_covid_19_time_series')

	df = pd.read_csv('time_series_covid19_confirmed_US.csv')

	state = 'South Carolina'

	is_state = df['Province_State'] == state
	df = df[is_state]

	df.reset_index(drop=True, inplace=True)
	df.drop(['iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State', 'Lat', 'Long_'], axis=1, inplace=True)

	print(df)


if __name__ == '__main__':
	main()
