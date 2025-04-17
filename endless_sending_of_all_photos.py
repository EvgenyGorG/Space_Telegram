import argparse
import os
from pathlib import Path
import random
import time

import telegram
from dotenv import load_dotenv

from send_specific_image import send_image


def send_images(tg_bot, tg_chat_id, folder, send_time):
    images_info = list(os.walk(folder))
    images = images_info[0][2]

    while True:
        random.shuffle(images)
        for image in images:
            image_path = Path(folder, image)
            send_image(tg_bot, tg_chat_id, image_path)
            time.sleep(send_time)


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
        type=str,
        help='Frequency of sending images (in seconds)',
        default=14400
    )

    args = parser.parse_args()

    try:
        send_images(tg_bot, tg_chat_id, args.directory, args.send_time)
    except telegram.error.NetworkError:
        time.sleep(10)
        send_images(tg_bot, tg_chat_id, args.directory, args.send_time)


if __name__ == '__main__':
    main()