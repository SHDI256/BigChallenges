from client_api import Transfer
from vars import HOST
from datetime import datetime
from time import sleep
import cv2
from random import randint

from vars import PORT1


def generator():
    transfer = Transfer(HOST)
    while True:
        transfer.open()
        yield transfer.request_transfer_image()
        transfer.close()


def tgenerator():
    i = 1
    transfer = Transfer(HOST)
    while True:
        transfer.open()
        p1, p2, p3, p4, p5, p6, p7, p8 = transfer.request_data_transfer_double()
        photo = [f'Имя: {i}', f'Возраст: {i}', f'Пол: {i}', f'Частота моргания: {p6}', f'Частота перевода взгляда: {p7}',
                 f'Повороты головы: {p5}', f'Рука у лица: {p4}', f'Рука с телефоном: {p3}', f'Открытый рот: {p2}',
                 f'Нервные губы: {p1}', f'Поправление одежды: {p8}']
        yield photo
        i += 1
        transfer.close()
        sleep(1)


def v2ch(x):
    if x > 0:
        return f'+{x:.0f}'
    return f'{x:.0f}'


def nandx(n, x):
    return v2ch((x / n - 1) * 100)


def otrnandx(nmn, nmx, x):
    if x > nmx:
        return nandx(nmx, x)
    elif x < nmn:
        return nandx(nmn, x)
    return nandx(x, x)


def calc(x, mean, before_values=None, w=1):
    from functools import reduce
    if before_values:
        before_values_and_mean = before_values + [mean]
    else:
        before_values_and_mean = [mean]
    garm_mean = len(before_values_and_mean) / (sum(map(lambda x: 1/x, before_values_and_mean)))
    geom_mean = reduce((lambda x, y: x * y), before_values_and_mean) ** (1 / len(before_values_and_mean))
    arif_mean = sum(before_values_and_mean) / len(before_values_and_mean)
    max_mean = (sum(map(lambda x: x ** 2, before_values_and_mean)) / len(before_values_and_mean)) ** 0.5
    vector = [x / garm_mean - 1, x / geom_mean - 1, x / arif_mean - 1, x / max_mean - 1]
    return min(map(abs, vector)) * 100 * w


def calc_high_low(x, mean, before_values=None, w=1):
    if before_values:
        before_values_and_mean = before_values + [mean]
    else:
        before_values_and_mean = [mean]
    garm_mean = len(before_values_and_mean) / (sum(map(lambda x: 1/x, before_values_and_mean)))
    pow_mean = (sum(map(lambda x: x ** 2, before_values_and_mean)) / len(before_values_and_mean)) ** 0.5
    if garm_mean <= x <= pow_mean:
        return 0 * w
    elif x > pow_mean:
        return (x / pow_mean - 1) * 100 * w
    elif x < garm_mean:
        return -(x / garm_mean - 1) * 100 * w


def calc_low_relu(x, mean, before_values=None, w=1):
    if before_values:
        before_values_and_mean = before_values + [mean]
    else:
        before_values_and_mean = [mean]
    pow_mean = (sum(map(lambda x: x ** 2, before_values_and_mean)) / len(before_values_and_mean)) ** 0.5
    if x <= pow_mean:
        return 0 * w
    elif x > pow_mean:
        return (x / pow_mean - 1) * 100 * w


def calc_high_relu(x, mean, before_values=None, w=1):
    if before_values:
        before_values_and_mean = before_values + [mean]
    else:
        before_values_and_mean = [mean]
    garm_mean = len(before_values_and_mean) / (sum(map(lambda x: 1/x, before_values_and_mean)))
    if garm_mean <= x:
        return 0 * w
    elif x < garm_mean:
        return -(x / garm_mean - 1) * 100 * w


def generator2():
    i = 1
    transfer = Transfer(HOST, PORT1)
    # interest = [randint(0, 10) for _ in range(8)]
    while True:
        transfer.open()
        # p1, p2, p3, p4, p5, p6, p7, p8, *_ = transfer.request_data_transfer_double()
        spisok = transfer.request_data_transfer_double()
        # print(spisok)
        nervous_g = spisok[:4]
        opened_mouth = spisok[4:8]
        hand_with_phone = spisok[8:12]
        hand_with_face = spisok[12:16]
        head_rotation = spisok[16:20]
        blinks = spisok[20:24]
        gaze_movement = spisok[24:28]
        clother_correction = spisok[28:32]
        interest = spisok[32:40]
        # print(len(spisok))
        photo = transfer.request_transfer_image()
        # for i in range(8):
            # interest[i] += randint(-3, 2)
            # interest[i] = max(0, interest[i])
        vector = [f'Имя: {i}', f'Возраст: {i}', f'Пол: {i}', f'Нервные губы: {nervous_g[0]:.0f} times | {nervous_g[1]:.0f} sec | {nervous_g[2]:.0f} cpm | {nervous_g[3]:.0f}% | Δ{interest[0]:,.0f}%',
                  f'Открытый рот: {opened_mouth[0]:.0f} times | {opened_mouth[1]:.0f} sec | {opened_mouth[2]:.0f} cpm | {opened_mouth[3]:.0f}% | Δ{interest[1]:,.0f}%',
                  f'Рука с телефоном: {hand_with_phone[0]:.0f} times | {hand_with_phone[1]:.0f} sec | {hand_with_phone[2]:.0f} cpm | {hand_with_phone[3]:.0f}% | Δ{interest[2]:,.0f}%',
                  f'Рука у лица: {hand_with_face[0]:.0f} times | {hand_with_face[1]:.0f} sec | {hand_with_face[2]:.0f} cpm | {hand_with_face[3]:.0f}% | Δ{interest[3]:,.0f}%',
                  f'Повороты головы: {head_rotation[0]:.0f} times | {head_rotation[1]:.0f} sec | {head_rotation[2]:.0f} cpm | {head_rotation[3]:.0f}% | Δ{interest[4]:,.0f}%',
                  f'Моргания: {blinks[0]:.0f} times | {blinks[1]:.0f} sec | {blinks[2]:.0f} cpm | {blinks[3]:.0f}% | Δ{interest[5]:,.0f}%',
                  f'Переводы взгляда: {gaze_movement[0]:.0f} times | {gaze_movement[1]:.0f} sec | {gaze_movement[2]:.0f} cpm | {gaze_movement[3]:.0f}% | Δ{interest[6]:,.0f}%',
                  f'Поправление одежды: {clother_correction[0]:.0f} times | {clother_correction[1]:.0f} sec | {clother_correction[2]:.0f} cpm | {clother_correction[3]:.0f}% | Δ{interest[7]:,.0f}%',
                  interest
                  ]

        yield vector, photo
        i += 1
        transfer.close()


# for i in tgenerator():
#     print(i)

# for i in generator():
#     # print(i.shape)
#     i = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
#     cv2.imshow('frame', i)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
#     # closing all open windows
# cv2.destroyAllWindows()
