import argparse
from pathlib import Path

import requests

from picture_work_instruments import picture_download


def download_spacex_images(images_file_path, launch_id):
    launch_info = 'https://api.spacexdata.com/v5/launches/'

    response = requests.get(f'{launch_info}{launch_id}')
    response.raise_for_status()
    response = response.json()

    picture_links = response['links']['flickr']['original']

    for picture_number, picture_link in enumerate(picture_links):
        picture_name = f'spacex_{picture_number + 1}.jpg'
        picture_download(picture_name, picture_link, images_file_path)


def main():
    images_file_path = 'images'
    Path(images_file_path).mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(
        description='Download images from SpaceX launch'
    )
    parser.add_argument(
        '-id',
        '--launch_id',
        type=str,
        help='Certain SpaceX launch ID',
        default='latest'
    )
    args = parser.parse_args()

    download_spacex_images(images_file_path, args.launch_id)


if __name__ == '__main__':
    main()