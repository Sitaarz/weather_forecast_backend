# Project hosted under link:
https://weather-forecast-frontend-f4sh.onrender.com/

# weather_forecast_backend

## REST API utilizes https://api.open-meteo.com/ API

## REST API Endpoints
Current Weather:

Endpoint: /weather_forcast_api/
Method: POST
Parameters: latitude (lat), longitude (lon)
Return Value: {'date': dates_list, 'weather_code': wheather_code_list, 'max_temperature': temperature_2m_max_list,
                     'min_temperature': temperature_2m_min_list, 'energy': sunshine_duration_list}
