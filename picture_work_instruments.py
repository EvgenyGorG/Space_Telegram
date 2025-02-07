from os.path import split, splitext
from urllib.parse import urlparse, unquote

import requests


def picture_download(picture_name, picture_url, images_file_path):
    response = requests.get(picture_url)
    response.raise_for_status()

    with open(images_file_path + '\\' + picture_name, 'wb') as picture:
        picture.write(response.content)


def get_file_expansion(url):
    url_parts = urlparse(url)
    url_address = url_parts[2]
    url_name = unquote(split(url_address)[1])
    file_expansion = splitext(url_name)[1]

    return file_expansion
