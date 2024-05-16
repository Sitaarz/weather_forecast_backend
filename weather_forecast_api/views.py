from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from jsonschema import validate, ValidationError
from rest_framework import status
import requests
from datetime import datetime

schema = {
    "type": "object",
    "properties": {
        "latitude": {"type": "number"},
        "longitude": {"type": "number"},
    },
    "required": ["latitude", "longitude"],
}

@api_view(['POST'])
def weather_api_post_method(request):
    try:
        validate(instance=request.data, schema=schema)
    except ValidationError:
        return Response(request.data, status.HTTP_400_BAD_REQUEST)
    print(request.data)
    longitude = request.data["longitude"]
    latitude = request.data["latitude"]

    url = f'https://api.open-meteo.com/v1/forecast?latitude={longitude}2&longitude={longitude}&daily=weather_code,temperature_2m_max,temperature_2m_min,sunshine_duration'
    response = requests.get(url)
    data = response.json()
    dates_list = data["daily"]["time"]
    wheather_code_list = data["daily"]["weather_code"]
    temperature_2m_max_list = data["daily"]["temperature_2m_max"]
    temperature_2m_min_list = data["daily"]["temperature_2m_min"]
    sunshine_duration_list = data["daily"]["sunshine_duration"]

    sunshine_duration_list = map(lambda x: round((float(x) / 3600) * 2.5 * 0.2, 2),sunshine_duration_list)
    dates_list = map(lambda x: datetime.strptime(x,'%Y-%m-%d').strftime('%d/%m/%Y'),dates_list)
    return Response({'date': dates_list, 'weather_code': wheather_code_list, 'max_temperature': temperature_2m_max_list,
                     'min_temperature': temperature_2m_min_list, 'energy': sunshine_duration_list})
