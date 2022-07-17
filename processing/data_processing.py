from processing.db_processing import update_before_values_user, search_by_id
from processing.face_processing import face_find, face_add
from time import time
from vars import WS, MEANS


class Serializer:
    class Calc:

        def __init__(self, before_values, ws):
            self.before_values = before_values
            self.ws = ws

        def calc(self, x, i):
            garm_mean = len(self.before_values[i]) / (sum(map(lambda x: 1 / x, self.before_values[i])))
            pow_mean = (sum(map(lambda x: x ** 2, self.before_values[i])) / len(self.before_values[i])) ** 0.5
            if garm_mean <= x <= pow_mean:
                return 0
            elif x > pow_mean:
                return min((x / pow_mean - 1) * 100.0 * self.ws[i], 100.0)
            elif x < garm_mean:
                return min((x / garm_mean - 1) * -100.0 * self.ws[i], 100.0)

        def calc3_relu(self, x, i):
            pow_mean = (sum(map(lambda x: x ** 2, self.before_values[i])) / len(self.before_values[i])) ** 0.5
            if x <= pow_mean:
                return 0
            elif x > pow_mean:
                return min((x / pow_mean - 1) * 100 * -100.0 * self.ws[i], 100.0)

    class User:
        class __FrameControl:
            def __init__(self):
                self.__previous_frame_flag = False
                self.__previous_frame_time = None
                self.__start_time = time()
                self.__frame_counter = 0
                self.__sum_time = 0.0
                self.__tmp = []

            def __count_time_frame(self):
                if self.__previous_frame_time:
                    return time() - self.__previous_frame_time
                return 0.0

            def __time_div_count(self):
                return (len(self.__tmp) / (time() - self.__start_time)) * 60.0

            def update(self, flag):
                if flag:
                    if self.__previous_frame_flag:
                        self.__sum_time += self.__count_time_frame()
                    else:
                        self.__frame_counter += 1
                        self.__tmp.append(time())

                self.__previous_frame_time = time()
                self.__previous_frame_flag = flag

            def count_frame(self):
                return self.__frame_counter

            def count_time(self):
                return self.__sum_time

            def count_intersection_over_union(self):
                return self.__sum_time / (time() - self.__start_time)

            def count_frame_div_time(self):
                return self.__time_div_count()

        def __init__(self, id):
            self.id = id
            self.username, self.sex, self.age, self.before_values = search_by_id(self.id)[1:5]
            self.before_values = map(int, self.before_values[1:-1].split(', '))
            self.Calc = Serializer.Calc(self.before_values, WS)
            self.__nervous_lips = self.__FrameControl()
            self.__open_mouth = self.__FrameControl()
            self.__hand_with_phone = self.__FrameControl()
            self.__hand_of_face = self.__FrameControl()
            self.__head_turns = self.__FrameControl()
            self.__blinks = self.__FrameControl()
            self.__gaze_movements = self.__FrameControl()
            self.__clothe_correction = self.__FrameControl()

        def __call_parameters(self):
            return [
                self.Calc.calc3_relu(self.__nervous_lips.count_time(), 0),
                self.Calc.calc3_relu(self.__open_mouth.count_time(), 1),
                self.Calc.calc3_relu(self.__hand_with_phone.count_time(), 2),
                self.Calc.calc3_relu(self.__hand_of_face.count_frame(), 3),
                self.Calc.calc(self.__head_turns.count_frame_div_time(), 4),
                self.Calc.calc(self.__blinks.count_frame_div_time(), 5),
                self.Calc.calc(self.__gaze_movements.count_frame_div_time(), 6),
                self.Calc.calc(self.__clothe_correction.count_intersection_over_union(), 7)]

        def get(self):
            return [self.__nervous_lips.count_frame(),
                    self.__nervous_lips.count_time(),
                    self.__nervous_lips.count_frame_div_time(),
                    self.__nervous_lips.count_intersection_over_union()] + \
                   [self.__open_mouth.count_frame(),
                    self.__open_mouth.count_time(),
                    self.__open_mouth.count_frame_div_time(),
                    self.__open_mouth.count_intersection_over_union()] + \
                   [self.__hand_with_phone.count_frame(),
                    self.__hand_with_phone.count_time(),
                    self.__hand_with_phone.count_frame_div_time(),
                    self.__hand_with_phone.count_intersection_over_union()] + \
                   [self.__hand_of_face.count_frame(),
                    self.__hand_of_face.count_time(),
                    self.__hand_of_face.count_frame_div_time(),
                    self.__hand_of_face.count_intersection_over_union()] + \
                   [self.__head_turns.count_frame(),
                    self.__head_turns.count_time(),
                    self.__head_turns.count_frame_div_time(),
                    self.__head_turns.count_intersection_over_union()] + \
                   [self.__blinks.count_frame(),
                    self.__blinks.count_time(),
                    self.__blinks.count_frame_div_time(),
                    self.__blinks.count_intersection_over_union()] + \
                   [self.__gaze_movements.count_frame(),
                    self.__gaze_movements.count_time(),
                    self.__gaze_movements.count_frame_div_time(),
                    self.__gaze_movements.count_intersection_over_union()] + \
                   [self.__clothe_correction.count_frame(),
                    self.__clothe_correction.count_time(),
                    self.__clothe_correction.count_frame_div_time(),
                    self.__clothe_correction.count_intersection_over_union()] + \
                   self.__call_parameters()

        def update(self, data):
            self.__nervous_lips.update(data[0])
            self.__open_mouth.update(data[1])
            self.__hand_with_phone.update(data[2])
            self.__hand_of_face.update(data[3])
            self.__head_turns.update(data[4])
            self.__blinks.update(data[5])
            self.__gaze_movements.update(data[6])
            self.__clothe_correction.update(data[7])

        def save_before_values(self):
            update_before_values_user(id, self.before_values + self.__call_parameters())

    def __init__(self):
        self.user = None

    def update_face(self, face):
        if len(face) == 128:
            sol = face_find(face)[0]
            if not self.user or self.user.id != sol:
                self.user = self.User(sol)
                print(f'New user {sol}')
            else:
                print('Disconnect user')
        else:
            print('Disconnect user')

    def update_parameters(self, tmp):
        if self.user:
            self.user.update(tmp)

    def get_user_parameters(self):
        return self.user.get()

    def add_user(self, full_name, sex, age, img):
        before_values = MEANS
        face_add(full_name, sex, age, img, before_values)
