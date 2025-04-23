import argparse
from pathlib import Path

import requests

from picture_work_instruments import download_picture


def download_spacex_images(images_file_path, launch_id):
    launch_url = 'https://api.spacexdata.com/v5/launches/'

    response = requests.get(f'{launch_url}{launch_id}')
    response.raise_for_status()
    response = response.json()

    picture_links = response['links']['flickr']['original']

    for picture_number, picture_link in enumerate(picture_links, start=1):
        picture_name = f'spacex_{picture_number}.jpg'
        download_picture(picture_name, picture_link, images_file_path)


def main():
    parser = argparse.ArgumentParser(
        description='Download images from SpaceX launch'
    )

    parser.add_argument(
        '-d',
        '--directory',
        type=str,
        help='In which directory do you want to save the images?',
        default=Path(Path.cwd(), 'images')
    )

    parser.add_argument(
        '-id',
        '--launch_id',
        type=str,
        help='Certain SpaceX launch ID',
        default='latest'
    )

    args = parser.parse_args()

    download_spacex_images(args.directory, args.launch_id)


if __name__ == '__main__':
    main()