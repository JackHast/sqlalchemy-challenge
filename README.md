# sqlalchemy-challenge

# Contents of Repository
The following repository has a jupyter notebook 'climate_analysis.ipynb' and a python file 'app.py' along with a resources folder with sqllite file 'hawaii_sqllite' containing data used in both 'climate_analysis.ipynb' and 'app.py'

Note, in order for both python files to run the libraries sqlalchemy and flask must be installed. 

# Summary

Firstly, in 'climate_analysis.ipynb', sqlalchemy is used to query data from the 'hawaii_sqllite' database, specifically temperature and precipitation readings from 9 separate weather stations from 1/1/2010 to 8/23/2017. From this data the most active station is found and a histogram of temperatures is plotted from this station for the past year. 

In the python script 'app.py', flask is used to create a webpage with 3 static routes, /api/v1.0/precipitation which returns a jsonified dictionary of precipitation data from the past year with dates as keys, /api/v1.0/stations which returns the 9 stations and /api/v1.0/tobs which returns jsonified dictionary of temperatures for the most active station from the past year. Finally, two dynamic routes are created, /api/v1.0/<start> which returns min, max and mean temperatures from start date and /api/v1.0/<start>/<end> which returns min, max and mean temperatures between start and end dates that are specified. 

