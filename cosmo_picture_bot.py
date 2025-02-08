import os

import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    tg_bot_token = os.environ['TELEGRAM_BOT_TOKEN']

    tg_bot = telegram.Bot(token=tg_bot_token)
    tg_chat_id = '@CosmoPicc'

    tg_bot.send_message(chat_id=tg_chat_id, text="Hello people.")


if __name__ == '__main__':
    main()
