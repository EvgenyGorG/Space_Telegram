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
    send_time = int(os.environ['SEND_TIME'])

    tg_bot = telegram.Bot(token=tg_bot_token)
    tg_chat_id = '@CosmoPicc'

    folder = 'images'

    send_images(tg_bot, tg_chat_id, folder, send_time)


if __name__ == '__main__':
    main()