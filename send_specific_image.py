import argparse
import os
import random

import telegram
from dotenv import load_dotenv


def send_image(tg_bot, tg_chat_id, image_path):
    if not image_path:
        folder = 'images'
        images = os.listdir(folder)
        image = random.choice(images)
        image_path = folder + '/' + image

    tg_bot.send_document(
        chat_id=tg_chat_id,
        document=open(image_path, 'rb')
    )


def main():
    load_dotenv()
    tg_bot_token = os.environ['TELEGRAM_BOT_TOKEN']

    tg_bot = telegram.Bot(token=tg_bot_token)
    tg_chat_id = '@CosmoPicc'

    parser = argparse.ArgumentParser(
        description='Send image in chat'
    )
    parser.add_argument(
        '-i',
        '--image_path',
        type=str,
        help='Image path in folder/image.(expansion) format',
        default=''
    )
    args = parser.parse_args()

    send_image(tg_bot, tg_chat_id, args.image_path)


if __name__ == '__main__':
    main()
