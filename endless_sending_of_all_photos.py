import argparse
import os
from pathlib import Path
import random
import time

import telegram
from dotenv import load_dotenv

from send_specific_image import send_image


def get_images_from_directory(folder):
    images_info = list(os.walk(folder))
    return images_info[0][2]


def send_images(tg_bot, tg_chat_id, folder, images, send_time):
    first_check = True

    while True:
        random.shuffle(images)
        try:
            for image in images:
                image_path = Path(folder, image)
                send_image(tg_bot, tg_chat_id, image_path)
                time.sleep(send_time)
                first_check = True

        except telegram.error.NetworkError:
            if first_check:
                first_check = False
                time.sleep(5)
            else:
                time.sleep(30)


def main():
    load_dotenv()
    tg_bot_token = os.environ['TELEGRAM_BOT_TOKEN']

    tg_bot = telegram.Bot(token=tg_bot_token)
    tg_chat_id = os.environ['TG_CHAT_ID']

    parser = argparse.ArgumentParser(
        description='Automatic photo sending'
    )

    parser.add_argument(
        '-d',
        '--directory',
        type=str,
        help='Which directory do you want to send images from?',
        default=Path(Path.cwd(), 'images')
    )

    parser.add_argument(
        '-s',
        '--send_time',
        type=int,
        help='Frequency of sending images (in seconds)',
        default=14400
    )

    args = parser.parse_args()

    images = get_images_from_directory(args.directory)
    send_images(tg_bot, tg_chat_id, args.directory, images, args.send_time)


if __name__ == '__main__':
    main()