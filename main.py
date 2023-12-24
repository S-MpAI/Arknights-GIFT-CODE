import os

do = os.getcwd()
debugVal = False

import requests
import ast
import subprocess
import time
import logging
from datetime import datetime, timedelta

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
violet = "\033[35m"
turquoise = "\033[36m"
white = "\033[37m"
st = "\033[37"

if str(os.name) == "nt":
  dir_pref = "\\"
else:
  dir_pref = "/"


def cls():
  try:
    subprocess.call("clear")  # linux/mac
  except:
    subprocess.call("cls", shell=True)

gift_code = input('Введите подарочный код >>> ')

def debDEF(text, debugVal, py_logger, py_log_num, exc_info=False):
  """
    Отладочная функция для вывода информации в консоль и лог-файл.

    Параметры:
    - text (строка): Текст для отладочного вывода.
    - debugVal (булево): Флаг отладочного вывода.
    - py_logger (Logger): Объект логгера.
    - py_log_num (целое число): Номер логгирования (1 - info, 2 - warning, 3 - error, 4 - critical).
    - exc_info (булево): Флаг вывода информации об исключении (по умолчанию False).
  """
  if debugVal == True:
    print('\r', end='')
    print(f'{yellow}[DEBUG] {blue}{text}{white}')

  if py_log_num == 1: py_logger.info(text)
  elif py_log_num == 2: py_logger.warning(text)
  elif py_log_num == 3: py_logger.error(text)
  elif py_log_num == 4: py_logger.critical(text)
  else: py_logger.debug(text)


starting_script_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
starting_script_time2 = starting_script_time.replace('-', '_').replace(
    ' ', '_').replace(':', '_')


def set_logger_settings():
  """
    Функция для создания и настройки объекта логгера.

    Возвращаемое значение:
    - Кортеж, содержащий объект логгера и строку с временем запуска скрипта.
  """
  py_logger = logging.getLogger(__name__)
  py_logger.setLevel(logging.INFO)

  py_handler = logging.FileHandler(f"{starting_script_time2}.log", mode="w")
  py_handler.setFormatter(
      logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
  py_logger.addHandler(py_handler)
  os.chdir(do)
  starting_script_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
  debDEF(f"{'='*15}- STARTing script in [{starting_script_time}] -{'='*15}",
         debugVal, py_logger, 1)

  return py_logger, starting_script_time


try:
  os.mkdir("logging")
  os.chdir(f'{do + dir_pref + "logging"}')
  py_logger, starting_script_time = set_logger_settings()
except FileExistsError:
  os.chdir(f'{do + dir_pref + "logging"}')
  py_logger, starting_script_time = set_logger_settings()
  pass
except PermissionError:
  py_logger, starting_script_time = set_logger_settings()
  pass

ch = 'Y'

while ch != 'N':

  cls()

  debDEF(f'{"-"*11} New session started {"-"*11}', debugVal, py_logger, 1)
  UID = int(input('Enter UID from the main menu >>> '))
  debDEF(f"[INPT] ID ({UID}) has been entered.", debugVal, py_logger, 1)

  try:
    r = requests.get(f'https://arknights.global/api/gift/playerinfo?uid={UID}')

    cont = r.text.replace(':false', ':False').replace(':true', ':True')
    cont = ast.literal_eval(cont)
    err_ = None

  except requests.exceptions.ConnectionError as err_code:
    if "[Errno 11001]" in str(err_code):
      err_ = 'You are not connected to the Internet'
    cont = err_code
  except Exception as err:
    cont = err
    err_ = err

  pr = ''
  pr = pr + f'''┌{"-"*10} Requests \n╎'''
  if err_ == None:
    pr = pr + f'\n╎ Status: Requests - {green}OK{white}\n'
    debDEF(f"[Main] REQUEST Status - OK", debugVal, py_logger, 1)
  else:
    pr = pr + f'\n╎ Status: Requests - {red}Error{white}\n'
    debDEF(f"[Error] REQUEST Status - Error", debugVal, py_logger, 3)

  if err_ == None:
    v = cont["meta"]["v"]
    pr = pr + f'╎\n├{"-"*10} Version: \n╎'
    pr = pr + f'\n╎ Version API: {green}{v}{white}\n'
    debDEF(f"[Main] REQUEST VersionAPI - {v}", debugVal, py_logger, 1)

  pr = pr + f'╎\n├{"-"*10} Info: \n╎'

  if err_ == None:
    if cont['meta']['ok'] == True:

      UID = cont['data']['uid']
      LVL = cont['data']['level']
      NICKNAME = cont['data']['nickname']

      pr = pr + f'\n╎ NickName: {green}{NICKNAME}{white}'
      pr = pr + f'\n╎ Level: {green}{LVL}{white}'
      pr = pr + f'\n╎ UserID: {green}{UID}{white}'
      debDEF(f"[Main] DATA User information", debugVal, py_logger, 1)
      debDEF(f"[Data] NickName - {NICKNAME}", debugVal, py_logger, 1)
      debDEF(f"[Data] Level - {LVL}", debugVal, py_logger, 1)
      debDEF(f"[Data] UserID - {UID}", debugVal, py_logger, 1)

    else:
      err_code = cont['meta']['err']['code']
      msg = cont['meta']['err']['msg']
      pr = pr + f'\n╎ Code:  {red}{err_code}{white}'
      pr = pr + f'\n╎ Error: {red}{msg}{white}'
      debDEF(f"[Main] DATA User information", debugVal, py_logger, 1)
      debDEF(f"[Error] Code - {err_code}", debugVal, py_logger, 1)
      debDEF(f"[Error] Error - {msg}", debugVal, py_logger, 1)

  else:
    pr = pr + f'\n╎ Error: Message - {red}{err_}{white}'
    debDEF(f"[Error] Error: {err_}", debugVal, py_logger, 3)

  print(pr)

  # ch = input(f'''╎\n└{"-"*10} Continue? (Y/N) >>> ''')

  if err_ == None:
    if err_ != "You've already got the pack, save that for someone else!!!":
      if input(f'╎\n├ Activate gift code {gift_code} ? (Y/N) >>> ') == 'Y':

        try:
          r = requests.post('https://arknights.global/api/gift/exchange',
                            data={
                                "code": gift_code,
                                "uid": UID
                            }).text.replace(':false', ':False').replace(
                                ':true', ':True')
          #print(r)
          cont = ast.literal_eval(r)
          err_ = None
        except requests.exceptions.ConnectionError as err_code:
          if "[Errno 11001]" in str(err_code):
            err_ = 'You are not connected to the Internet'
          cont = err_code
        except Exception as err:
          cont = err
          err_ = err

        pr = ''
        pr = pr + f'╎\n├{"-"*10} Gifs: \n╎'
        if err_ == None:
          if cont['meta']['ok'] == True:
            
            giftName = cont['data']['giftName']

            pr = pr + f'\n╎ Status: {green}SUCCESS{white}'
            pr = pr + f'\n╎ NickName: {green}{NICKNAME}{white}'
            pr = pr + f'\n╎ GiftName: {green}{giftName}{white}'
            pr = pr + f'\n╎ UserID: {green}{UID}{white}'
            debDEF(f"[Main] GIFT User information", debugVal, py_logger, 1)
            debDEF(f"[GIFT] NickName - {NICKNAME}", debugVal, py_logger, 1)
            debDEF(f"[GIFT] Level - {LVL}", debugVal, py_logger, 1)
            debDEF(f"[GIFT] UserID - {UID}", debugVal, py_logger, 1)

          else:
            err_code = cont['meta']['err']['code']
            msg = cont['meta']['err']['msg']
            pr = pr + f'\n╎ Status: {red}ERROR{white}'
            pr = pr + f'\n╎ Code:  {red}{err_code}{white}'
            pr = pr + f'\n╎ Error: {red}{msg}{white}'
            debDEF(f"[Main] GIFT User information", debugVal, py_logger, 1)
            debDEF(f"[Error] Code - {err_code}", debugVal, py_logger, 1)
            debDEF(f"[Error] Error - {msg}", debugVal, py_logger, 1)
        else:
          pr = pr + f'\n╎ Error: Message - {red}{err_}{white}'
          debDEF(f"[Error] Error: {err_}", debugVal, py_logger, 3)
        print(pr)
  else:
    debDEF(f'The user survey was not displayed due to an error.', debugVal,
           py_logger, 1)

  debDEF(f'{"-"*11} The session was closed {"-"*11}', debugVal, py_logger, 1)
  ch = input(f'╎\n├{"-"*10} Continue? \n╎ (Y/N) >>> ')

debDEF(
    f"""The script has been completed in [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]""",
    debugVal, py_logger, 1)
