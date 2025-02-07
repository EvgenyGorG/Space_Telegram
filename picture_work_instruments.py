import requests


def picture_download(picture_name, picture_url, images_file_path):
    response = requests.get(picture_url)
    response.raise_for_status()

    with open(images_file_path + '\\' + picture_name, 'wb') as picture:
        picture.write(response.content)
