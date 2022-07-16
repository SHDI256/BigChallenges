import numpy as np
from time import sleep


def tgenerator():
    i = 1
    while True:
        photo = [f'Имя: {i}', f'Возраст: {i}', f'Пол: {i}', f'Частота моргания: {i}', f'Частота перевода взгляда: {i}', f'Повороты головы: {i}', f'Рука у лица: {i}', f'Рука с телефоном: {i}', f'Открытый рот: {i}', f'Нервные губы: {i}']
        yield photo
        i += 1
        sleep(1/5)
