import requests
import json
import datetime
import os
from statistics import mean
import historical_weather as hw

def daily_forecast(city_id):
    """city_id is used to create api request to return today's weather forecast for city."""
    
    #key = os.environ.get('OPENWEATHERMAP_API_KEY')
    key = "333de4e909a5ffe9bfa46f0f89cad105"


    request = requests.get(f'http://api.openweathermap.org/data/2.5/group?APPID={key}&id={city_id}&units=imperial')
    
    json_data = json.loads(request.text)
    
#    pprint(json_data) #including this in case you want to see pprint json data for each city in list
    return json_data   



def extended_forecast(city_id):
    """
    Each loop takes the city ID and makes an API request with it.
    This goes into daily_forecast_functions.py and uses state_choice() function
    city_id_list is returned from state_choice and adds them into api request to return weather for city, based on its unique city_id.
    
    This is good for 4 days into the future. Does not include today's forecast'
    """

    # key = os.environ.get('OPENWEATHERMAP_API_KEY')
    key = "333de4e909a5ffe9bfa46f0f89cad105"



    json_data_list = []             #need to create a list to store json data, so we capture all data from each state (and locations within that state) per API request

    # request = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?id=#{city_id}&APPID=333de4e909a5ffe9bfa46f0f89cad105&units=imperial&')
    request = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={key}&units=imperial&')
    #5 day forecast request format
    json_data = json.loads(request.text)
    json_data_list.append(json_data)

    return json_data_list



#############INSERT HISTORICAL WEATHER INFO HERE
#output should look like this: [(7.0, 0.0, (0.0, 0.0), 0.0), (0.0, 0.0, (0.0, 0.0), 0.0)]
# this tuple is (for one day) (daily precip, avg wind, (hi temp, lo temp), humidity)

def historical_forecast(lat, lon):
    """city_id, lat, and lon are used to create api request to return previous 2 days weather forecast for location"""
    
    #gets unix timestamp for each of last two days
    today = datetime.date.today()
    day1 = hw.create_unix_timestamp(today - datetime.timedelta(days=1))
    day2 = hw.create_unix_timestamp(today - datetime.timedelta(days=2))

    days = [day1, day2]

    daily_stats = []

    #make api call and get weather for each day
    for day in days:
    
        API_KEY = '333de4e909a5ffe9bfa46f0f89cad105'
        request = requests.get(f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={day}&appid={API_KEY}&units=imperial')
        
        json_data = json.loads(request.text)
        
        #get high and low temp for one day
        temperatures = []
        for i in json_data['hourly']:
            temperatures.append(i['temp'])
        hi_temp = max(temperatures)
        lo_temp = min(temperatures)
        
        #get rainfall total for one day
        daily_precip = []
        for i in json_data['hourly']:
            try:                            #if hour has rainfall
                daily_precip.append(i['rain']['1h'])
            except:                         #if no rainfall in that hour
                pass
        daily_precip = sum(daily_precip)
        
        #get average wind speed
        wind_speeds = []
        for i in json_data['hourly']:
            wind_speeds.append(i['wind_speed'])
        avg_wind = round(mean(wind_speeds), 2)    #rounded to 2 decimal places
        
        # get average humidity
        humidity = []
        for i in json_data['hourly']:
            humidity.append(i['humidity'])
        avg_humidity = round(mean(humidity), 2)
        
        stats_today = (daily_precip, avg_wind, (hi_temp, lo_temp), avg_humidity)
        daily_stats.append(stats_today)

    return daily_stats

#for Ouray, CO
print('HERE')
print(historical_forecast(38.03, -107.69))


def format_daily_forecast(city_id):
    """ Takes json_data_list from extended_forecast() and breaks it apart, using only the current day's data.
    Then it pulls out today's hi_temp, lo_temp, precipitation, average wind speed, and average humidity"""

    try:
        extended_forecast_data = extended_forecast(city_id)
        todays_data = extended_forecast_data[0]['list']


        current_date = datetime.date.today()
        today = str(current_date)
        
        todays_weather_data = []
        
        for i in todays_data:
            date = i['dt_txt'][:10]
            if date == today:
                todays_weather_data.append(i)
                
        if len(todays_weather_data) > 0:
        #this is for if you check late in the day and there is no more data returned for the current day by the weather provider
                
            daily_hi = []
            daily_lo = []
            daily_precip = []
            daily_wind = []
            daily_humidity = []
            
            for i in todays_weather_data:
                hi_temp = i['main']['temp_max']
                lo_temp = i['main']['temp_min']
                wind_speed = i['wind']['speed']
                humidity = i['main']['humidity']
            
                
                try:                            #this skips over null rain value if its not raining today
                    precip = i['rain']['3h']
                except KeyError:
                    precip = 0.0
                    
                daily_hi.append(hi_temp)
                daily_lo.append(lo_temp)
                daily_precip.append(precip)
                daily_wind.append(wind_speed)
                daily_humidity.append(humidity)
                
            final_daily_stats = []
            
            daily_hi = max(daily_hi)
            daily_lo = min(daily_lo)
            daily_precip = round((sum(daily_precip) * 0.0393701), 2)   #converting mm to in and rounding to two decimal places
            daily_wind = round((sum(daily_wind) / len(daily_wind)), 2)
            daily_humidity = round((sum(daily_humidity) / len(daily_humidity)), 2)
            
            final_daily_stats.append((daily_hi, daily_lo, daily_precip, daily_wind, daily_humidity))
        
            # print(final_daily_stats)
            return final_daily_stats

        else:
            #this is in case there is no data returned for current day because person checks late in the day
            #must use daily_forecast() function instead, which leads to incomplete data but is better than nothing
            
            data_now = daily_forecast(city_id)
            data_now = data_now['list'][0]
            
            final_daily_stats = []
            
            hi_temp = data_now['main']['temp_max']
            lo_temp = data_now['main']['temp_min']
            daily_precip = 0.0  #no current rainfall totals are provided
            daily_wind = data_now['wind']['speed']
            daily_humidity = data_now['main']['humidity']

            final_daily_stats.append((hi_temp, lo_temp, daily_precip, daily_wind, daily_humidity))

            return final_daily_stats

    except Exception:
        
        final_daily_stats = [(0.0, 0.0, 0.0, 0.0, 0.0)]

        return final_daily_stats








def format_extended_forecast(city_id):
    """Takes json_data_list from extended_forecast() and breaks it apart by day.
    Then pulls out daily max_temp, min_temp, precipitation, average wind speed, average humidity"""
    
    extended_forecast_data = extended_forecast(city_id)
    data = extended_forecast_data[0]['list']


    
    current_date = datetime.date.today()
    today = str(current_date)
    five_days_out = current_date + datetime.timedelta(days=5)
    five_days_out = str(five_days_out)
    
    dates = []
    
    for i in data:
        date = i['dt_txt'][:10]
        if date != today and date != five_days_out:  #i don't want current date or 5 days from now date. Only next 4 days
            dates.append(date)
    
    
    #get unique dates and keep order
    unique_dates = []
    
    for date in dates:
        if date not in unique_dates:
            unique_dates.append(date)
            
    #now I want to get daily high and low temp, plus the average humidity for each day
    temps_day_1 = []
    temps_day_2 = []
    temps_day_3 = []
    temps_day_4 = []
    precip_day_1 = []
    precip_day_2 = []
    precip_day_3 = []
    precip_day_4 = []
    wind_day_1 = []
    wind_day_2 = []
    wind_day_3 = []
    wind_day_4 = []
    humidity_day_1 = []
    humidity_day_2 = []
    humidity_day_3 = []
    humidity_day_4 = []
    
    
    
    for i in data:
        date = i['dt_txt'][:10]
        temperature = i['main']['temp']
        wind_speed = i['wind']['speed']
        humidity = i['main']['humidity']
        
        try:                                      #this skips over null values. There is only a rain value if rain is predicted
            i['rain']['3h']
            precip = i['rain']['3h']              #rain volume is in millimeters
        except KeyError:
            precip = 0.0
    
        
        if date == unique_dates[0]:
            temps_day_1.append(temperature)
            precip_day_1.append(precip)
            wind_day_1.append(wind_speed)
            humidity_day_1.append(humidity)
            
        elif date == unique_dates[1]:
            temps_day_2.append(temperature)
            precip_day_2.append(precip)
            wind_day_2.append(precip)
            humidity_day_2.append(humidity)
        
        elif date == unique_dates[2]:
            temps_day_3.append(temperature)
            precip_day_3.append(precip)
            wind_day_3.append(precip)
            humidity_day_3.append(humidity)
            
        elif date == unique_dates[3]:
            temps_day_4.append(temperature)
            precip_day_4.append(precip)
            wind_day_4.append(precip)
            humidity_day_4.append(humidity)
    
            
    #this contains a tuple of (daily_max_temp, daily_min_temp, daily_precip, daily avg_wind, daily avg_humidity)
    final_daily_stats = []
    
    max1 = max(temps_day_1)
    min1 = min(temps_day_1)
    precip1 = round((sum(precip_day_1) * 0.0393701), 2)   #converts mm to inches. rounds to 2 decimal places
    avg_wind_1 = round((sum(wind_day_1) / len(wind_day_1)), 2)
    avg_humidity_1 = round((sum(humidity_day_1) / len(humidity_day_1)), 2)
    final_daily_stats.append((max1, min1, precip1, avg_wind_1, avg_humidity_1))
    
    max2 = max(temps_day_2)
    min2 = min(temps_day_2)
    precip2 = round((sum(precip_day_2) * 0.0393701), 2)  
    avg_wind_2 = round((sum(wind_day_2) / len(wind_day_2)), 2)
    avg_humidity_2 = round((sum(humidity_day_2) / len(humidity_day_2)), 2)
    final_daily_stats.append((max2, min2, precip2, avg_wind_2, avg_humidity_2))
    
    max3 = max(temps_day_3)
    min3 = min(temps_day_3)
    precip3 = round((sum(precip_day_3) * 0.0393701), 2)
    avg_wind_3 = round((sum(wind_day_1) / len(wind_day_1)), 2)
    avg_humidity_3 = round((sum(humidity_day_3) / len(humidity_day_3)), 2)
    final_daily_stats.append((max3, min3, precip3, avg_wind_3, avg_humidity_3))
    
    max4 = max(temps_day_4)
    min4 = min(temps_day_4)
    precip4 = round((sum(precip_day_4) * 0.0393701), 2)
    avg_wind_4 = round((sum(wind_day_4) / len(wind_day_4)), 2)
    avg_humidity_4 = round((sum(humidity_day_4) / len(humidity_day_4)), 2)
    final_daily_stats.append((max4, min4, precip4, avg_wind_4, avg_humidity_4))
    
    # print(final_daily_stats)

    return final_daily_stats




def get_date_range():
    """Creates date range for 7 day period of weather forecast. This includes two days prior to current date through
    4 days beyond current date. (2 previous days + 5 day forecast)"""

    today = datetime.date.today()
    two_days_ago = today - datetime.timedelta(days=2)
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    two_days_from_now = today + datetime.timedelta(days=2)
    three_days_from_now = today + datetime.timedelta(days=3)
    four_days_from_now = today + datetime.timedelta(days=4)
    
    all_dates = [two_days_ago, yesterday, today, tomorrow, two_days_from_now, three_days_from_now, four_days_from_now]
    
    formatted_dates = []
    
    for date in all_dates:
        date = date.strftime('%m-%d-%Y')
        formatted_dates.append(date)
        
    return formatted_dates




def image_choice(lat, lon, city_id):
    """ Ultimately returns the URL for each day, which will be used choose image
    for weather app weather forecast. Images returned are 'hot', 'cold', 'rain',
    'wind', 'sunny'. 
    
    First all the weather forecasts are collected and put into same order:
    (hi_temp, lo_temp, daily_precip, daily_wind, daily_humidity)
    
    Then take that data and put into weather_type object. Then take text of each
    daily weather and return url string for use in object 
    """

    # historical_weather = get_historical_weather(lat, lon)   # this is what is should look like: [(2.0, 0.0, (0.0, 0.0), 0.0), (0.0, 0.0, (0.0, 0.0), 0.0)]
    historical_weather = [(2.0, 0.0, (0.0, 0.0), 0.0), (0.0, 0.0, (0.0, 0.0), 0.0)]

    #this is a reorganized tuple so it matches the format of the daily_forecast and extended_forecast
    historical_weather = [(historical_weather[0][2][1], historical_weather[0][2][0], historical_weather[0][0], historical_weather[0][1], historical_weather[0][3]), (historical_weather[1][2][1], historical_weather[1][2][0], historical_weather[1][0], historical_weather[1][1], historical_weather[1][3])]
    
    todays_weather = format_daily_forecast(city_id)
    #this will be a tuple for each day as follows: (hi_temp, lo_temp, daily_precip, daily_wind, daily_humidity)
    extended_weather = format_extended_forecast(city_id)
    #this will be a tuple for each day as follows: (daily_max_temp, daily_min_temp, daily_precip, daily avg_wind, daily avg_humidity)
    
    all_weather = historical_weather + todays_weather + extended_weather
    
    
    weather_type = []
    
    for day in all_weather:
        
        if day[0] == 0.0:              #this is to handle the case that the historical weather API has timed out and no data is available for the previous two days
            weather_type.append('nodata')
        else:
            if day[0] > 80:
                weather_type.append('hot')
            elif day[0] < 40:
                weather_type.append('cold')
            elif day[2] > .015:
                weather_type.append('rain')
            elif day[3] > 13:
                weather_type.append('wind')
            else:
                weather_type.append('sunny')
            
    
    url_list = []
    
    for weather in weather_type:
        
        if weather == 'hot':
            url_list.append("/static/img/hotandhumid.png")
        elif weather == 'cold':
            url_list.append("/static/img/cold.jpg")
        elif weather == 'rain':
            url_list.append("/static/img/rain.png")
        elif weather == 'wind':
            url_list.append("/static/img/wind.jpg")
        elif weather == 'sunny':
            url_list.append("/static/img/sun.png")
        elif weather == 'nodata':
            url_list.append("/static/img/nodata.png")
        else:
            url_list.append("/static/img/nodata.png")

            
    return url_list


    
            

    





