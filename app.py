
from flask import Flask, render_template

import database as db    
import weather_forecast as wf
import os

app = Flask(__name__)


app.config['GOOGLE_MAPS_JS_API_KEY'] = os.getenv('GOOGLE_MAPS_JS_API_KEY')
app.config['CLIMACELL_API_KEY'] = os.getenv('CLIMACELL_API_KEY')
app.config['OPENWEATHERMAP_API_KEY'] = os.getenv('OPENWEATHERMAP_API_KEY')



@app.route("/")
@app.route("/home")
def home():

    sites = db.create_site_list_sqlite()

    return render_template('home.html',  
                           sites=sites)


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/weather_forecast/<climbing_area>/<city_id>/<lat>/<lon>/<weather_site>")    #creates url using climbing area name, city id, lat, lon, and location of weather site
def weather_forecast(climbing_area, city_id, lat, lon, weather_site):

    sites = db.create_site_list_sqlite()
    daily_forecast = wf.format_daily_forecast(city_id)
    extended_forecast = wf.format_extended_forecast(city_id)
    historical_forecast = wf.get_historical_weather(lat, lon)
    dates = wf.get_date_range()


    return render_template('weather_forecast.html', 
                           climbing_area=climbing_area, 
                           city_id=city_id, 
                           daily_forecast=daily_forecast, 
                           extended_forecast=extended_forecast, 
                           historical_forecast=historical_forecast,
                           dates=dates,
                           lat=lat,
                           lon=lon,
                           weather_site=weather_site,
                           sites=sites,
                           wf=wf)


if __name__ == "__main__":
    app.run(debug=True)    

