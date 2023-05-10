import requests
import psycopg2
from psycopg2 import sql
from datetime import datetime


def get_events_from_timepad_api(token, params=None):
    if params is None:
        params = {}

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    url = 'https://api.timepad.ru/v1/events'

    # Начинаем с первой страницы
    page = 1
    limit = 50
    events = []

    max_pages = 100  # ограничиваем количество страниц, чтобы получить 1000 мероприятий

    while page <= max_pages:
        params.update({
            'skip': (page - 1) * limit,
            'limit': limit
        })

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f'Error loading events: {response.json()}')

        new_events = response.json()['values']
        events.extend(new_events)

        # Если мы получили меньше мероприятий, чем лимит, значит, мы достигли последней страницы
        if len(new_events) < limit:
            break

        print((limit * page) / (limit * max_pages) * 100)
        page += 1
    print(events)
    return events


def save_events_to_db(events, db_config):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    for event in events:
        if 'location' in event and 'city' in event['location']:
            location = event['location']['city']
        else:
            location = None

        if 'poster_image' in event and 'default_url' in event['poster_image']:
            image_url = event['poster_image']['default_url']
        else:
            image_url = None

        date = datetime.strptime(event['starts_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S')

        event_data = (
            event['id'],
            event['name'],
            event.get('description_short', ''),
            location,
            date,
            event['url'],
            image_url
        )

        insert_query = sql.SQL("""
            INSERT INTO map_event (id, title, description, location, date, link, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET title = EXCLUDED.title,
                description = EXCLUDED.description,
                location = EXCLUDED.location,
                date = EXCLUDED.date,
                link = EXCLUDED.link,
                image = EXCLUDED.image;
        """)
        print(event_data)
        cursor.execute(insert_query, event_data)

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    api_key = 'bc140ac6cf042dbe9f64de8827fb67786217e45b'
    events = get_events_from_timepad_api(api_key)

    db_config = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'Ckjy9088',
        'host': 'localhost',
        'port': '5432'
    }

    save_events_to_db(events, db_config)
