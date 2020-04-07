#!/usr/bin/python3

import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression
import math
import matplotlib.pyplot as plt
import charting


def main():
	''' main function'''

	# Load test data
	df = pd.read_csv('China_regression_test_data.csv', index_col=0)

	stop_date = None

	# Prep data
	df, date = prep_data(df, stop_date)

	# Regression
	df, celeration = regression(df, date, True)

	return


def moving_average(x, y):
	''' creates a moving average'''

	df = pd.DataFrame(data=y, index=x)
	
	rolling = df[0].rolling(window=6)
	rolling_median = rolling.median()

	plt.plot(x, y, marker='.')
	plt.yscale('log')
	rolling_median.plot(color='red')
	#plt.show()

	
	return


def prep_data(original_df, stop_date):
	''' prepares data for regression'''

	df = original_df

	# Get the current date, or use supplied stop date
	if stop_date == None:
		date = df.index[-1]

	else:
		date = stop_date

	# Replace date slashed with dashed
	date = date.replace('/', '-')

	# Replace NaN with zeros
	df = df.fillna(0)

	# Change index to datetime
	df.index = pd.to_datetime(df.index, infer_datetime_format=True) #format='%m/%-d/%y')

	num = len(df)

	if df.iloc[num-1, 0] >= 30:

		# filter out row where cumulative cases is greater than 30
		greater_30 = df['Cumulative cases']>30
		df = df[greater_30]

	# Check if df is now empty
	if df.empty == True:
		return 'no_df', 'no_celeration', 'no_date'

	# replace 0's in data frame with 1's to prevent errors
	df = df.replace(to_replace=0, value=1)

	# Get rid of any negative numbers with absolute value
	df = df.apply(abs)

	# Filter dates, if requested
	if stop_date != None:
		mask = df.index <= stop_date
		df = df.loc[mask]
		num = len(df)
	#print(df)

	return df, date


def regression(df, date, multi_trend):
	''' performs linear regression'''

	while True:
	
		if multi_trend == True:
			trends = int(input('How many trends? '))

		else:
			trends = 1

		for trend in range(0, trends):

			# find number of days between end of chart and start date
			if multi_trend == False:
				start = df.index[0]

			else:
				year = int(input('What is the start date year? '))
				mon = int(input('What is the start date month? '))
				day = int(input('What is the start date day? '))

				start = datetime.datetime(year, mon, day)
	
			end = datetime.datetime(2020, 5, 17)
			days = (end - start).days
			shift = 140 - days

			# Create X and Y prediction spaces
			num = len(df)
			X = np.arange(1, num+1).reshape(-1, 1)
			Y = df.iloc[0:num, 1].values.reshape(-1, 1)

			# Get the moving averages
			# ma = moving_average(X, Y)

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

			original_df = pd.concat([df, predictions], axis=1)

			if multi_trend == True:
				print(original_df)
				charting.plot_data(original_df, 'China', None, celeration, date, 'solo', multi_trend)
		
		if multi_trend == True:
			satisfied = input("Are you satisfied with the result? ")
				
			if satisfied == "Yes":
				break

		else:
			break

	return original_df, celeration


if __name__ == '__main__':
	main()
