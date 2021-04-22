import requests
import json
from datetime import datetime, timedelta
import os



def define_dates():
    """
    Uses datetimem odule to get date for historical weather forecasts.
    Gets yesterday's, 2 days ago dates
    Formatted as '2020-05-17' 
    """
    
    two_days_ago_date = ((datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')), (datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')))
    yesterday_date = ((datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')), (datetime.strftime(datetime.now() - timedelta(0), '%Y-%m-%d')))

    return (two_days_ago_date, yesterday_date)




def get_historical_weather(lat, lon):
    """Get's weather forecast for desired historical date at a desired location. I'm gathering weather forecast for 2 day period so I am iterating to 
    gather two days' weather data (yesterday, two days ago). Will be returned in a list object at the end.
    
    precipitation data is measured in inches per hour
    wind speed is measured in miles per hour
    temperature is measures in degrees Fahrenheit"""
    

    key = os.environ.get('CLIMACELL_API_KEY')
    url = "https://api.climacell.co/v3/weather/historical/station"

    dates = define_dates()

    weather_data_by_day = []

    for date in dates:

        querystring = {"lat": lat, "lon": lon, "unit_system": 'us', "start_time": date[0], "end_time": date[1], "fields": "precipitation,wind_gust,temp,humidity", "apikey": key}
        # querystring = {"lat": lat, "lon": lon, "unit_system": 'us', "start_time": date[0], "end_time": date[1], "fields": "humidity", "apikey": key}


        response = requests.request("GET", url, params=querystring)

        daily_data = json.loads(response.text)
    
        weather_data_by_day.append(daily_data)

    return weather_data_by_day






def parse_daily_precip(weather_data):
    """parses precipitation from weather data input.
    Returns precipitation total in inches, for each of the two days."""
    
    try:
        precip_total_by_day = []
        
        for day in weather_data:
    
            precip_total = []
        
            for i in day:
                precip = (i['precipitation']['value'])
                if precip != None:
                    precip_total.append(float(precip))
                elif precip == None:                         #converts None values into 0.0 float values
                    precip = 0.0
                    precip_total.append(precip)
            
            length = len(precip_total)
            
            rounded_to_int = rounding(length)  #rounds # of observations to nearest multiple of 24
            change_needed = rounded_to_int - length   # number needed (+/-) to get to nearest multiple of 24
            
            modified_precip_total = modify_observations_list(change_needed, precip_total)
            
            precip_total = sum(modified_precip_total)
            precip_total = precip_total / rounded_to_int  #divides total daily precipitation by # of multiples of 24
        
            precip_total_by_day.append(precip_total)
            
        return precip_total_by_day

            
    except TypeError:
        
        return "API rate limit probably exceeded"
        
    



def parse_daily_wind(weather_data):
    """Parses daily wind speed from weather data input.
    Returns average wind speed in miles per hour, for each of the two days."""
    
    try:
        
    
        wind_speed_by_day = []
        
        for day in weather_data:
            
            wind_total = []
            
            for i in day:
                
                wind = i['wind_gust']['value']
                if wind != None:
                    wind_total.append(float(wind))
                elif wind == None:                         #converts None values into 0.0 float values
                    wind = 0.0
                    wind_total.append(wind)
                    
            length = len(wind_total)
            
            rounded_to_int = rounding(length)  #rounds # of observations to nearest multiple of 24
            change_needed = rounded_to_int - length  # number needed (+/-) to get to nearest multiple of 24
                
            modified_wind_total = modify_observations_list(change_needed, wind_total)
        
            wind_total = sum(modified_wind_total)
            avg_wind_speed = wind_total / rounded_to_int
            
            wind_speed_by_day.append(avg_wind_speed)
        
        return wind_speed_by_day 
    
    except TypeError:
        
        return "API rate limit probably exceeded"


def parse_daily_temp(weather_data):
    """Parses daily temparature from weather data input.
    Returns high and low temperatures for each day"""
        
    try:
        
        daily_min_and_max_temps = []
            
        for day in weather_data:
                
            temperatures = []
                
            for i in day:
                    
                temp = i['temp']['value']
                temperatures.append(temp)
                    
            min_temp = min(temperatures)
            max_temp = max(temperatures)
                
            daily_min_and_max_temps.append((min_temp, max_temp))
                
        return daily_min_and_max_temps
            
    except TypeError:
            
        return "API rate limit probably exceeded"


def parse_daily_humidity(weather_data):
    """Parses daily humidity from weather data input. 
    Returns average humidity level for each day"""
    
    try:
        
        daily_humidity_average = []
        
        for day in weather_data:
            
            humidity_values = []
            
            for i in day:
                
                humidity = i['humidity']['value']
                humidity_values.append(humidity)

            avg_humidity = round((sum(humidity_values) / len(humidity_values)), 2)
            daily_humidity_average.append(avg_humidity)
            
        return daily_humidity_average

    except TypeError:

        return "API rate limit probably exceeded"                
    
    
    
        

def rounding(length): 
    """rounds precipitation/wind measurements total to nearest multiple of 24.
    We get different numbers of daily measurements form each weather station
    This calculates what is the nearest multiple of 24 to then number of daily measurements"""
    
    # Smaller multiple 
    a = (length // 24) * 24

    # Larger multiple 
    b = a + 24
      
    # Return of closest of two 
    return (b if length - a > b - length else a) 


def modify_observations_list(change_needed, observations_list):
    """modify precip/wind results to make list length a multiple of 24.
    Either fills extra spaces with 0 or removes extra results from list, depending 
    on change_needed"""
    
    if change_needed > 0:
        for _ in range(change_needed):
            observations_list.append(0.0)     #populate list with 0 values at end of list
    elif change_needed < 0:
        observations_list = observations_list[:change_needed]   #removing x number of values from end of list
    else:
        change_needed == 0  #explicitly stating "if number is already multiple of 24, do nothing"

    return observations_list

    
    
###for testing purposes
# weather_data = get_historical_weather("30.26666", "-97.733330")

# result = parse_daily_wind(weather_data)
# result2 = parse_daily_precip(weather_data)
# result3 = parse_daily_temp(weather_data)
# result4 = parse_daily_humidity(weather_data)










    

