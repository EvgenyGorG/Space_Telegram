import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
import requests

from picture_work_instruments import download_picture, get_file_expansion


def download_apod_images(api_key, images_file_path, count):
    apod_image_url = 'https://api.nasa.gov/planetary/apod'

    payload = {
        'count': count,
        'api_key': api_key
    }

    images_info = requests.get(apod_image_url, params=payload)
    images_info.raise_for_status()
    images_info = images_info.json()

    for page_number, page in enumerate(images_info, start=1):
        if page['media_type'] == 'image':
            image_url = page['url']
            image_expansion = get_file_expansion(image_url)
            image_name = f'nasa_apod_{page_number}{image_expansion}'
            download_picture(image_name, image_url, images_file_path)


def main():
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']

    parser = argparse.ArgumentParser(
        description='Download APOD NASA images'
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
        type=int,
        help='How many photos should upload?',
        default=5
    )

    args = parser.parse_args()

    download_apod_images(nasa_api_key, args.directory, args.number_of_images)


if __name__ == '__main__':
    main()