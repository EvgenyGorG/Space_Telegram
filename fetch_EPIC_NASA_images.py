import os
from pathlib import Path

from dotenv import load_dotenv
import requests

from picture_work_instruments import picture_download, get_file_expansion


def download_nasa_epic_images(api_key, images_file_path):
    epic_images_info = 'https://api.nasa.gov/EPIC/api/natural/images'

    payload = {
        'api_key': api_key
    }

    images_info_response = requests.get(epic_images_info, params=payload)
    images_info_response.raise_for_status()
    images_info_response = images_info_response.json()

    for page_number in range(10):
        file_name = images_info_response[page_number]['image']
        image_date = images_info_response[page_number]['date'].split(' ')[0].replace('-', '/')
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{file_name}.png?api_key={api_key}'
        image_expansion = get_file_expansion(image_url)
        image_name = f'nasa_epic_{page_number + 1}{image_expansion}'
        picture_download(image_name, image_url, images_file_path)


def main():
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']

    images_file_path = 'images'
    Path(images_file_path).mkdir(parents=True, exist_ok=True)

    download_nasa_epic_images(nasa_api_key, images_file_path)


if __name__ == '__main__':
    main()