import os
from pathlib import Path

from dotenv import load_dotenv
import requests

from picture_work_instruments import picture_download, get_file_expansion


def download_apod_images(api_key, images_file_path):
    apod_image_info = 'https://api.nasa.gov/planetary/apod'

    payload = {
        'count': 30,
        'api_key': api_key
    }

    images_info = requests.get(apod_image_info, params=payload)
    images_info.raise_for_status()
    images_info = images_info.json()

    for page_number, page in enumerate(images_info):
        image_url = images_info[page_number]['url']
        image_expansion = get_file_expansion(image_url)
        image_name = f'nasa_apod_{page_number + 1}{image_expansion}'
        picture_download(image_name, image_url, images_file_path)


def main():
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']

    images_file_path = 'images'
    Path(images_file_path).mkdir(parents=True, exist_ok=True)

    download_apod_images(nasa_api_key, images_file_path)


if __name__ == '__main__':
    main()