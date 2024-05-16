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


    longitude = request.data["longitude"]
    latitude = request.data["latitude"]

    if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
        return Response(request.data, status.HTTP_400_BAD_REQUEST)

    url = f'https://api.open-meteo.com/v1/forecast?latitude={longitude}2&longitude={longitude}&daily=weather_code,temperature_2m_max,temperature_2m_min,sunshine_duration'
    response = requests.get(url)

    if not response.ok:
        return Response(request.data, status.HTTP_500_INTERNAL_SERVER_ERROR)

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
