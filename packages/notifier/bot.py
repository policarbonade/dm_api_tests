from pathlib import Path
from telebot import TeleBot
from vyper import v

config = Path(__file__).resolve().parents[2] / "config"
v.set_config_type("yaml")
v.set_config_name("prod")
v.add_config_path(config)
v.read_in_config()


def send_file() -> None:
    telegram_bot = TeleBot(v.get("telegram.token"))
    file_path = Path(__file__).resolve().parents[2] / "swagger-coverage-dm-api-account.html"
    with open(file_path, 'rb') as document:
        telegram_bot.send_document(
            v.get("telegram.chat_id"),
            document=document,
            caption='coverage'
        )


if __name__ == '__main__':
    send_file()
