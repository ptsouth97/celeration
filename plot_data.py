#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression


def main():
	''' main function for testing'''
	
	df = pd.read_csv('test.csv')
	lunar_plot(df)
	temp_plot(df)
	stand_plot(df)
	stand_time_histogram(df)
	hogs_stand_plot(df)
	hogs_stand_time_histogram(df)


def show_all(df):
	''' all in one plot'''
	
	# Lunar
	plt.figure(1)
	plt.subplot(221)
	lunar = df.groupby('moon').day_deer.sum()
	lunar.plot(kind='bar', rot=45, color='green')
	plt.xlabel('Moon phase')
	plt.ylabel('Number of deer')
	plt.title('Legal shooting deer by moon phase')
	plt.tight_layout()

	# Temperature
	plt.subplot(222)
	# plt.scatter(df['temp'], df['deer'], color='red')
	plt.hist(df['temp'], bins=10)
	plt.xlabel('Temp (F)')
	plt.ylabel('Number of deer')
	plt.gca().ticklabel_format(useOffset=False)
	plt.title('Number of deer by temperature')
	plt.tight_layout()
	

	# Total Deer by Stand
	plt.subplot(223)
	#location = df.groupby('stand').deer.sum()
	#location.plot(kind='bar', rot=45, color='orange')
	
	sns.boxplot(x='stand', y='deer', data=df)
	plt.xlabel('Stand')
	plt.ylabel('Number of deer')
	plt.title('Total deer by stand')
	plt.tight_layout()

	# Day Deer by Stand
	plt.subplot(224)
	# loc = df.groupby('stand').day_deer.sum()
	# loc.plot(kind='bar', rot=45)

	sns.violinplot(x='stand', y='day_deer', data=df)
	plt.xlabel('Stand')
	plt.ylabel('Number of deer')
	plt.title('Legal shooting deer by stand')
	plt.tight_layout()
	plt.savefig('Bampfield Stats.png')

	plt.show()

	# Heatmap
	num_df = df._get_numeric_data()
	sns.heatmap(num_df, linewidth=0.5, cmap='Blues_r')
	plt.title('Covariance plot')
	plt.show()


def plot_all_stands(df, animal, lastXdays):
	''' plots total number of observations for each stand'''

	if animal == 'deer':
		total = df.groupby('stand').deer.sum()

	if animal == 'hogs':
		total = df.groupby('stand').hogs.sum()

	total.plot(kind='bar', rot=45)
	plt.xlabel('Stand')
	plt.ylabel('Total photographic observations')
	title = 'Total number of ' +animal+ ' observations by stand for ' +str(lastXdays)+ ' days'
	plt.title(title)
	plt.tight_layout()
	plt.show()


def lunar_plot(df):
	''' Plots number of deer photographed during daylight hours by moon phase'''

	lunar = df.groupby('moon').day_deer.sum()
	lunar.plot(kind='bar', rot=45)
	plt.xlabel('Moon phase')
	plt.ylabel('Number of deer photographed during daylight')
	plt.title('Legal shooting deer by moon phase')
	plt.tight_layout()
	plt.show()

	return

def temp_plot(df, animal):
	''' Plots number of animals photographed vs temperature'''
	
	# get the appropriate columns from df and turn into numpy arrays	
	X = np.array(df['temp']).reshape(-1,1)
	y = np.array(df[animal]).reshape(-1,1)

	# create the regressor
	reg = LinearRegression()

	# create the prediction space
	prediction_space = np.linspace(min(X), max(X)).reshape(-1,1)

	# fit the model to the data
	reg.fit(X, y)

	# compute predictions over the prediction space
	y_pred = reg.predict(prediction_space)

	# print R^2
	score = reg.score(X, y)
	r2 = 'R^2 = ' + str(score)

	# plot the regression line and raw data points
	plt.plot(prediction_space, y_pred, color='black', linewidth=3)
	plt.scatter(X, y)
	plt.xlabel('Temp (F)')
	plt.ylabel('Number of photographic observations')
	plt.gca().ticklabel_format(useOffset=False)
	title = 'Number of ' +animal+ ' by temperature'
	plt.title(title)
	plt.annotate(s=r2, xy=(10,10), xycoords='figure points')
	plt.tight_layout()
	plt.show()

	return


def stand_plot(df):
	''' Plots number of deer photographed by stand'''

	location = df.groupby('stand').deer.sum()
	location.plot(kind='bar', rot=45)
	plt.xlabel('Stand')
	plt.ylabel('Number of deer photographed')
	plt.title('Number of deer by stand')
	plt.tight_layout()
	plt.show()

	return


def stand_time_histogram(df, animal, stand):
	''' Plots histogram of animal observation times for a given stand'''

	df_animal = df[(df[animal] > 0)]
	datetimes = df_animal.loc[:, ['obs_time', animal]]
	dt_list = datetimes['obs_time'].apply(lambda x: x.split(' '))
	times = dt_list.apply(lambda x: x.pop(1))
	data = times.apply(lambda x: pd.to_datetime(x, format='%H:%M:%S'))
	hours = data.apply(lambda x: x.hour)
	hours_column = pd.Series(hours)
	datetimes['time_hour'] = hours_column.values
	grouped_hours = datetimes.groupby('time_hour')
	animals_by_hour = grouped_hours[animal].sum()
	animals_by_hour.plot(kind='bar', rot=45)
	title = stand+ ': Number of ' +animal+ ' observed by hour'
	plt.xlabel('Hour')
	plt.ylabel('Number of observations')
	plt.title(title)
	plt.tight_layout()
	plt.show()


if __name__ == '__main__':
	main()
