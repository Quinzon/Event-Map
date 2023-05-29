import keys
import requests
from urllib.parse import quote


def geocode_address(address, api_key=keys.Keys.Yandex_API):
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&format=json&geocode={quote(address)}'
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        if json_response['response']['GeoObjectCollection']['featureMember']:
            coordinates_str = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            return ', '.join(reversed([x for x in coordinates_str.split()]))
        else:
            return None
    else:
        raise Exception(f'Error geocoding address: {response.text}')
