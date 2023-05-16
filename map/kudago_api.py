import requests
import psycopg2
from psycopg2 import sql
from datetime import datetime, timezone
from urllib.parse import quote
import keys


def get_events_from_kudago_api(api_key, params=None):
    if params is None:
        params = {}

    headers = {
        'Authorization': f'Token {api_key}',
        'Content-Type': 'application/json',
    }

    url = 'https://kudago.com/public-api/v1.4/events/'

    page = 1
    limit = 200
    events = []
    max_pages = 1000

    while page <= max_pages:
        params.update({
            'page': page,
            'page_size': limit,
            'fields': 'id,title,description,location,dates,images,site_url,place,body_text',
            'expand': 'location,place,dates'
        })

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            page += 1
            continue

        new_events = response.json()['results']
        events.extend(new_events)

        if len(new_events) < limit:
            break

        print(f'KudaGO API {round((limit * page) / (limit * max_pages) * 100, 3)}%')

        page += 1
    return events


def save_events_to_db(events, db_config):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    current_datetime = datetime.now(timezone.utc)
    count = 0
    max_count = len(events)
    for event in events:
        count += 1

        date = None
        if event.get('dates', []) and event['dates'][0].get('start_date', None):
            date = datetime.strptime(event['dates'][0]['start_date'], '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        if date and datetime.strptime(date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc) < current_datetime:
            continue

        # cursor.execute("SELECT id FROM map_eventapi WHERE id = %s", (event['id'],))
        # if cursor.fetchone():
        #     continue

        if event.get('place', None) and event.get('location', None):
            address = event['location']['name'] + ' ' + event['place']['address']
        else:
            address = None

        location = None
        cursor.execute("SELECT location FROM map_eventapi WHERE id = %s", (event['id'],))
        result = cursor.fetchone()
        if result and result[0]:
            location = result[0]
        else:
            if address:
                geocoded = geocode_address(address)
                if geocoded:
                    location = ', '.join(map(str, reversed(geocoded)))

        image_url = event.get('images', [])[0]['image'] if event.get('images', []) else None

        description = event.get('description', '')

        full_description = event.get('body_text', '')

        event_data = (
            event['id'],
            event['title'],
            description,
            address,
            location,
            date,
            event.get('site_url', None),
            image_url,
            full_description
        )

        insert_query = sql.SQL("""
            INSERT INTO map_eventapi (id, title, description, address, location, date, link, image, full_description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET title = EXCLUDED.title,
                description = EXCLUDED.description,
                address = EXCLUDED.address,
                location = EXCLUDED.location,
                date = EXCLUDED.date,
                link = EXCLUDED.link,
                image = EXCLUDED.image,
                full_description = EXCLUDED.full_description;
        """)
        cursor.execute(insert_query, event_data)

        print(f'Yandex API { round(count / max_count * 100, 4)}%')

    print('Yandex API 100%')
    conn.commit()
    cursor.close()
    conn.close()


def geocode_address(address, api_key=keys.Keys.Yandex_API):
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&format=json&geocode={quote(address)}'
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        if json_response['response']['GeoObjectCollection']['featureMember']:
            coordinates_str = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            return [float(x) for x in coordinates_str.split()]
        else:
            return None
    else:
        raise Exception(f'Error geocoding address: {response.text}')


if __name__ == '__main__':
    api_key = 'public-api'
    events = get_events_from_kudago_api(api_key)

    db_config = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': keys.Keys.DB_PASSWORD,
        'host': 'localhost',
        'port': '5432'
    }

    save_events_to_db(events, db_config)
