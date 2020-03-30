# Celeration

This application's purpose is to analyze data about COVID-19 from [this repo](https://github.com/CSSEGISandData) 

## Workflow
* User must decide chart will contain a single region or comparison of multiple regions
* User must define the region(s) of interest
* User can define the end date or all of the data will be used
* User can decide to make a single chart or use a loop to generate multiple charts
* User must specify the country(s) of interest or choose 'all countries'
* User must have a folder containing the latest COVID-19 data from github (see above)
* The 'load_data' function changes to the COVID-19 folder and reads the appropriate .csv as a dataframe
* The 'get_data' function slices the appropriate dataframe information for the specified region
* The main function 'for loop' goes through a list of all the region of interest.  For each region:
	* The 'count

## Dependencies
* matplotlib (3.0.2)
* numpy (1.18.1)
* scikit-learn (0.19.2)
