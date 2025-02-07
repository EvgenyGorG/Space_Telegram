from os.path import split, splitext
import os
from pathlib import Path
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
import requests


def get_file_expansion(url):
    url_parts = urlparse(url)
    url_address = url_parts[2]
    url_name = unquote(split(url_address)[1])
    file_expansion = splitext(url_name)[1]

    return file_expansion


def download_APOD_images(api_key, images_file_path):
    APOD_API_method = 'https://api.nasa.gov/planetary/apod'

    payload = {
        'count': 30,
        'api_key': api_key
    }

    images_info = requests.get(APOD_API_method, params=payload)
    images_info.raise_for_status()
    images_info = images_info.json()

    for page_number, page in enumerate(images_info):
        image_name = f'nasa_apod_{page_number + 1}.jpg'
        image_url = images_info[page_number]['url']
        image = requests.get(image_url)
        image.raise_for_status()

        with open(images_file_path + '\\' + image_name, 'wb') as picture:
            picture.write(image.content)


def download_NASA_EPIC_images(api_key, images_file_path):
    NASA_EPIC_images_info_method = 'https://api.nasa.gov/EPIC/api/natural/images'

    payload = {
        'api_key': api_key
    }

    NASA_EPIC_images_info_response = requests.get(NASA_EPIC_images_info_method, params=payload)
    NASA_EPIC_images_info_response.raise_for_status()
    NASA_EPIC_images_info_response = NASA_EPIC_images_info_response.json()

    for page_number in range(5):
        file_name = NASA_EPIC_images_info_response[page_number]['image']
        image_name = f'nasa_epic_{page_number + 1}.jpg'
        image_date = NASA_EPIC_images_info_response[page_number]['date'].split(' ')[0].replace('-', '/')
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{file_name}.png?api_key={api_key}'
        image = requests.get(image_url)
        image.raise_for_status()

        with open(images_file_path + '\\' + image_name, 'wb') as picture:
            picture.write(image.content)


def main():
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']

    images_file_path = r'D:\Devman\Space_Telegram\images'
    Path(images_file_path).mkdir(parents=True, exist_ok=True)

    picture_url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    picture_name = 'hubble.jpeg'

    download_APOD_images(nasa_api_key, images_file_path)

    download_NASA_EPIC_images(nasa_api_key, images_file_path)


if __name__ == '__main__':
    main()