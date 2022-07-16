import pandas
from matplotlib import pyplot as plt
import math

dt = pandas.read_excel('Stress.xlsx')
print(dt.columns)
gender = list(dt['Ваш пол'])
print(set(gender))
ages = list(dt['Сколько вам лет?'])
print(set(ages))
blinks = list(dt['Замечаете ли вы, что когда нервничаете, чаще моргаете?'])
print(set(blinks))
nervous_g = list(dt['Замечаете ли вы, что когда нервничаете, сжимаете/"кусаете" губы?'])
print(set(nervous_g))
breath = list(dt['Замечаете ли вы, что когда нервничаете, появляется учащённое дыхание?'])
print(set(breath))
hand_with_face = list(dt['Замечаете ли вы, что когда нервничаете, начинаете касаться лица руками (чаще)?'])
print(set(hand_with_face))
movement_g = list(dt['Замечаете ли вы, что когда нервничаете, часто переводите взгляд?'])
print(set(movement_g))
get_red = list(dt['Замечаете ли вы, что когда нервничаете, краснеете?'])
print(set(get_red))
tremor = list(dt['Замечаете ли вы, что когда нервничаете, начинают слегка дрожать руки'])
print(set(tremor))
clother_correction = list(dt['Замечаете ли вы, что когда нервничаете, начинаете "теребить" одежду? ( галстук, бабочку, рубашку )'])
print(set(clother_correction))
more = list(dt['Какие ещё признаки стресса вы замечали? Будем премного благодарны вам за идеи. Заранее спасибо :3'])
print(set(more))


# TODO
def gender4(x):
    if type(x) is float:
        return 0
    elif x == 'Мужской':
        return 1
    elif x == 'Женский':
        return -1
gender = list(map(gender4, gender))
print('Gender')
plt.stem(['Мужской', 'Женский', 'IT'], [gender.count(1), gender.count(-1), gender.count(0)])
plt.show()


def ages4(x):
    if math.isnan(x):
        return 0
    return int(x)
ages = list(map(ages4, ages))
print('Ages')
plt.stem(list(range(0, 100)), list(ages.count(i) for i in range(0, 100)))
plt.show()


blinks = list(map(str, blinks))
unique_blinks = list(set(blinks))
print('Blinks')
plt.stem(unique_blinks, list(blinks.count(i) for i in unique_blinks))
plt.show()


nervous_g = list(map(str, nervous_g))
unique_nervous_g = list(set(nervous_g))
print('Nervous g')
plt.stem(unique_nervous_g, list(nervous_g.count(i) for i in unique_nervous_g))
plt.show()


breath = list(map(str, breath))
unique_breath = list(set(breath))
print('Breath')
plt.stem(unique_breath, list(breath.count(i) for i in unique_breath))
plt.show()


hand_with_face = list(map(str, hand_with_face))
unique_hand_with_face = list(set(hand_with_face))
print('Hand with face')
plt.stem(unique_hand_with_face, list(hand_with_face.count(i) for i in unique_hand_with_face))
plt.show()


movement_g = list(map(str, movement_g))
unique_movement_g = list(set(movement_g))
print('Movement gaze')
plt.stem(unique_movement_g, list(movement_g.count(i) for i in unique_movement_g))
plt.show()


get_red = list(map(str, get_red))
unique_get_red = list(set(get_red))
print('Get red')
plt.stem(unique_get_red, list(get_red.count(i) for i in unique_get_red))
plt.show()


tremor = list(map(str, tremor))
unique_tremor = list(set(tremor))
print('Tremor')
plt.stem(unique_tremor, list(tremor.count(i) for i in unique_tremor))
plt.show()


clother_correction = list(map(str, clother_correction))
unique_clother_correction = list(set(clother_correction))
print('Clother')
plt.stem(unique_clother_correction, list(clother_correction.count(i) for i in unique_clother_correction))
plt.show()

# plt.imshow()
