import argparse
import os
from pathlib import Path
import random

import telegram
from dotenv import load_dotenv


def get_random_image(image_path):
    images = os.listdir(image_path)
    image = random.choice(images)
    return Path(image_path, image)


def send_image(tg_bot, tg_chat_id, image_path):
    if not image_path.suffix:
        image_path = get_random_image(image_path)

    with open(Path(image_path), 'rb') as file:
        tg_bot.send_document(
            chat_id=tg_chat_id,
            document=file
        )


def main():
    load_dotenv()
    tg_bot_token = os.environ['TELEGRAM_BOT_TOKEN']

    tg_bot = telegram.Bot(token=tg_bot_token)
    tg_chat_id = os.environ['TG_CHAT_ID']

    parser = argparse.ArgumentParser(
        description='Send image in chat'
    )

    parser.add_argument(
        'image_path',
        type=str,
        help='Image path in C:/folder/ format or C:/folder/image.(exp) if you want to send specific image'
    )

    args = parser.parse_args()

    send_image(tg_bot, tg_chat_id, Path(args.image_path))


if __name__ == '__main__':
    main()
