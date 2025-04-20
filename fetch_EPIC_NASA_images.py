import argparse
from datetime import datetime
import os
from pathlib import Path

from dotenv import load_dotenv
import requests

from picture_work_instruments import download_picture, get_file_expansion


def download_nasa_epic_images(api_key, images_file_path, number_of_images):
    epic_images_info = 'https://api.nasa.gov/EPIC/api/natural/images'

    payload = {
        'api_key': api_key
    }

    images_info_response = requests.get(epic_images_info, params=payload)
    images_info_response.raise_for_status()
    images_info_response = images_info_response.json()

    images_info = images_info_response[:number_of_images]

    for page_number, page in enumerate(images_info, start=1):
        file_name = page['image']

        image_date_time = page['date']
        iso_image_date_time = datetime.fromisoformat(image_date_time)
        formatted_image_date = iso_image_date_time.strftime("%Y/%m/%d")

        response = requests.get(f'https://api.nasa.gov/EPIC/archive/natural/{formatted_image_date}/png/{file_name}.png', params=payload)
        image_url = response.url

        image_expansion = get_file_expansion(image_url)
        image_name = f'nasa_epic_{page_number}{image_expansion}'

        download_picture(image_name, image_url, images_file_path)


def main():
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']

    parser = argparse.ArgumentParser(
        description='Download EPIC NASA images'
    )

    parser.add_argument(
        '-d',
        '--directory',
        type=str,
        help='In which directory do you want to save the images?',
        default=Path(Path.cwd(), 'images')
    )

    parser.add_argument(
        '-n',
        '--number_of_images',
        type=str,
        help='How many photos should upload?',
        default=5
    )

    args = parser.parse_args()

    download_nasa_epic_images(nasa_api_key, args.directory, args.number_of_images)


if __name__ == '__main__':
    main()