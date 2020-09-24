

import pandas as pd
import sqlite3
import os


def create_site_list():
    """Reades ClimbingAreasInfo excel file.
    Creates a list from each column in the test_sites dataframe
    Returns that list of sites and corresponding information. 

	*********************************
	***This function is deprecated***
	*********************************
    """
    
    sites = pd.read_excel(r'/Users/ep9k/Desktop/Climbing-Weather-App/ClimbingWeatherAppFlask/database/ClimbingAreasInfo.xlsx')

    sites = sites.values.tolist()

    return sites


def create_database():
	"""Creates SQLite database called ClimbingAreasInfo with one table (ClimbingAreasInfo) in the databases folder.
	Then reads in ClimbinAreasInfo.csv to a pandas dataframe, then to the sqlite database """

	#check and see if database already exists
	if os.path.isfile('database/ClimbingAreasInfo.db') == True:
			os.remove('database/ClimbingAreasInfo.db')

	conn = sqlite3.connect('database/ClimbingAreasInfo.db')

	c = conn.cursor()

	c.execute("""CREATE TABLE ClimbingAreasInfo (
			state text,
			city text,
			alias text,
			city_id integer,
			lat real,
			lon real 
			) """)

	#read csv into pandas dataframe, then pandas dataframe into sqlite in just 2 lines!
	df = pd.read_csv(r'/Users/ep9k/Desktop/Climbing-Weather-App/ClimbingWeatherAppFlask/database/ClimbingAreasInfo.csv')
	df.to_sql('ClimbingAreasInfo', conn, if_exists='append', index=False)

	conn.commit()

	conn.close()


	

def create_site_list_sqlite():
	"""This is a sqlite proxy to the above function (create_site_list()).
	This performs an SQL query on the database to return all information from the table ClimbingAreasInfo.
	All data from the table is returned in a list. Each item from the list is structured as follows:
	(state, city, alias, city_id, lat, lon)  real data example: ('HI', 'Kahului', 'Maui', 5847411, 20.807, -156.453) """

	conn = sqlite3.connect('database/ClimbingAreasInfo.db')

	c = conn.cursor()

	c.execute("SELECT * FROM ClimbingAreasInfo")

	data = c.fetchall()

	conn.close()

	modified_data = []

	#this loop rounds lat/lon coordinates to 3 decimal places. For some reason they are very long when returned from SQLite
	for i in data:
		i = list(i)
		i[4] = round(i[4], 3)
		i[5] = round(i[5], 3)
		modified_data.append(i)

	return modified_data


def add_site_to_sqlite_database(state, city, alias, city_id, lat, lon):
	"""This function adds a climbing site to the sqlite database. In order to do that I need to insert the following:
	state, city, alias, city_id (from city.list.json), lat, lon """

	conn = sqlite3.connect('database/ClimbingAreasInfo.db')

	c = conn.cursor()

	c.execute("INSERT INTO ClimbingAreasInfo VALUES (?, ?, ?, ?, ?, ?)", (state, city, alias, city_id, lat, lon))

	conn.commit()


def remove_site_from_sqlite_database(city):
	""" Removes site from SQLite database using the city name """

	conn = sqlite3.connect('database/ClimbingAreasInfo.db')

	c = conn.cursor()

	c.execute("DELETE FROM ClimbingAreasInfo WHERE city=:city", {'city': city})

	conn.commit()






# conn = sqlite3.connect('database/ClimbingAreasInfo.db')
# c = conn.cursor()


#DELETE statement
#remove_site_from_sqlite_database('Vancouver')


#ADD statements
#add_site_to_sqlite_database('BC', 'Vancouver', 'Squamish', 6173331, 49.710849, -123.126449)
#add_site_to_sqlite_database('BC', 'Golden', 'Bugaboos', 6173331, 50.740770, -116.782531)


# c.execute("SELECT * FROM ClimbingAreasInfo WHERE state='NM'")
# print(c.fetchall())





