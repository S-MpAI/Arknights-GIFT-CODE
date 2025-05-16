import os
import requests
import json
import time
import logging
from pathlib import Path
from datetime import datetime

from typing import Tuple, Optional

COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "violet": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
}

DEBUG = False
BASE_DIR = Path.cwd()
LOG_DIR = BASE_DIR / "logging"

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def debug_log(message: str, level: int, logger: logging.Logger):
    if DEBUG:
        print(f"{COLORS['yellow']}[DEBUG]{COLORS['blue']} {message}{COLORS['white']}")
    log_funcs = [logger.debug, logger.info, logger.warning, logger.error, logger.critical]
    log_funcs[min(level, 4)](message)

def setup_logger() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    log_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".log"
    log_path = LOG_DIR / log_name

    logger = logging.getLogger("gift_code_checker")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_path)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)

    debug_log("Logger initialized.", 1, logger)
    return logger

def fetch_user_info(uid: int, logger: logging.Logger) -> Tuple[Optional[dict], Optional[str]]:
    try:
        resp = requests.get(f"https://arknights.global/api/gift/playerinfo?uid={uid}")
        data = resp.json()
        return data, None
    except requests.exceptions.RequestException as e:
        debug_log(f"Request failed: {e}", 3, logger)
        return None, str(e)
    except json.JSONDecodeError:
        return None, "Invalid JSON received."

def redeem_gift(uid: int, code: str, logger: logging.Logger) -> Tuple[Optional[dict], Optional[str]]:
    try:
        resp = requests.post("https://arknights.global/api/gift/exchange", data={"uid": uid, "code": code})
        data = resp.json()
        return data, None
    except requests.exceptions.RequestException as e:
        debug_log(f"POST request failed: {e}", 3, logger)
        return None, str(e)
    except json.JSONDecodeError:
        return None, "Invalid JSON received."

def main():
    logger = setup_logger()
    gift_code = input("Введите подарочный код >>> ").strip()

    while True:
        cls()
        debug_log("Новая сессия", 1, logger)

        try:
            uid = int(input("Введите UID >>> "))
        except ValueError:
            print(f"{COLORS['red']}Неверный UID!{COLORS['reset']}")
            continue

        user_data, error = fetch_user_info(uid, logger)
        if error:
            print(f"{COLORS['red']}Ошибка запроса: {error}{COLORS['reset']}")
        elif user_data and user_data.get("meta", {}).get("ok"):
            info = user_data["data"]
            print(f"""
╔═[ Игрок найден ]
║ Ник: {COLORS['green']}{info['nickname']}{COLORS['reset']}
║ Уровень: {COLORS['green']}{info['level']}{COLORS['reset']}
║ UID: {COLORS['green']}{info['uid']}{COLORS['reset']}
╚══════════════════
""")
            if input("Активировать подарок? (Y/N) >>> ").strip().upper() == 'Y':
                gift_result, gift_error = redeem_gift(uid, gift_code, logger)
                if gift_error:
                    print(f"{COLORS['red']}Ошибка при активации: {gift_error}{COLORS['reset']}")
                elif gift_result and gift_result.get("meta", {}).get("ok"):
                    gift = gift_result["data"]
                    print(f"{COLORS['green']}Успешно! Получен подарок: {gift['giftName']}{COLORS['reset']}")
                else:
                    msg = gift_result["meta"]["err"]["msg"]
                    print(f"{COLORS['red']}Ошибка: {msg}{COLORS['reset']}")
        else:
            msg = user_data["meta"]["err"]["msg"] if user_data else "Неизвестная ошибка"
            print(f"{COLORS['red']}Ошибка: {msg}{COLORS['reset']}")

        if input("Продолжить? (Y/N) >>> ").strip().upper() != "Y":
            break

    debug_log("Скрипт завершён.", 1, logger)

if __name__ == "__main__":
    main()
