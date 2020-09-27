# isitdry
Climbing Weather App - Python Flask application


Climbing Weather Forecast application I built in order to learn the python flask web framework. It is pretty simple, but actually does tell the weather at various climbing destinations internationally. There are over 200 locations in the US and 300 internationally. 

***To deploy locally***

-clone repository
-start virtual environment using the following:

        ` python -m venv env  ` 
        
        - This will create a new 'env' environment folder in your directory
        
        - Build your dependencies from requirements.txt file:
        
            - ` pip3 install -r requirements.txt`
            
        - To start this virtual environment, run:
        
            - `source env/bin/activate`

-set environment variables locally (available in Heroku dashboard)
    - to run your own local instance, you'll need three API keys. All are free
        - Google Maps Javascript API: https://developers.google.com/maps/documentation/javascript/overview (to render Google basemap)
        - Open Weather Map: https://openweathermap.org/api (for weather forecast data)
        - Climacell: https://www.climacell.co/ (for historical weather data)
        
    
