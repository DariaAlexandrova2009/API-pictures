import requests
import os
import urllib.request
import urllib.parse
import datetime

DIRECTORY = 'images'
filename = 'hubble.jpeg'
url = "https://dvmn.org/media/HST-SM4.jpeg"

response = requests.get(url)
response.raise_for_status()

if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)


def download_file(url, params, path):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    lounch_id = '5eb87d47ffd86e000604b38a'
    response = requests.get(f'https://api.spacexdata.com/v5/launches/{lounch_id}')
    response.raise_for_status()
    photos_urls = response.json()['links']['flickr']['original']
    for photo_number, photo_url in enumerate(photos_urls):
        path = os.path.join(DIRECTORY, f"image_{photo_number}.jpg")
        download_file(photo_url, {}, path)


def get_file_extension(file_url):
    encoded_string = urllib.parse.unquote(file_url)
    url_parts = urllib.parse.urlsplit(encoded_string)
    path = url_parts.path
    file_path, file_extension = os.path.splitext(path)
    return file_extension


def get_apod():
    params = {
        'api_key': 'IEKC6O21b3ZkKyQ3oELkKykpbRY6N1MZo5Sbl4VT', 
        'count': 30
    }
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()
    launches = response.json()
    for photo_number, photo in enumerate(launches):
        if photo['media_type'] == 'image':
            extension = get_file_extension(photo['url'])
            path = os.path.join(
                DIRECTORY,
                f"image_nasa_{photo_number}{extension}")
            
            download_file(photo["url"], params, path)


def get_epicphoto():
    nasa_token = "IEKC6O21b3ZkKyQ3oELkKykpbRY6N1MZo5Sbl4VT"
    payload = {'api_key': nasa_token}
    response = requests.get('https://api.nasa.gov/EPIC/api/natural/images',params=payload)
    response.raise_for_status()
    images = response.json()
    for image_number, image in enumerate(images):
        url = 'https://api.nasa.gov/EPIC/archive/natural'
        date = datetime.datetime.fromisoformat(image['date'])
        date = date.strftime("%Y/%m/%d")
        image_name = image['image']
        path = os.path.join(DIRECTORY, f'epic_photo_{image_number}.png')
        download_file(f'{url}/{date}/png/{image_name}.png', payload, path)



fetch_spacex_last_launch()
get_epicphoto()
get_apod()
        
