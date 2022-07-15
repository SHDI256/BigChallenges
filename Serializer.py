from functools import reduce
from time import time


class Serializer(object):
    class FrameControl:
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
            self.__previous_frame_time = time()
            return 0.0

        def __time_div_count(self):
            while len(self.__tmp) > 0 and time() - self.__tmp[0] > 60:
                self.__tmp.pop()

            if len(self.__tmp) == 0:
                return 0.0

            if len(self.__tmp) == 1:
                return 1.0

            t = time() - self.__tmp[0]
            return (len(self.__tmp) / t) * 60

        def update(self, flag):
            if self.__previous_frame_flag and flag:
                self.__sum_time += self.__count_time_frame()

            if flag and not self.__previous_frame_flag:
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

    def __init__(self):
        self.__nervous_lips = self.FrameControl()
        self.__open_mouth = self.FrameControl()
        self.__hand_with_phone = self.FrameControl()
        self.__hand_of_face = self.FrameControl()
        self.__head_turns = self.FrameControl()
        self.__blinks = self.FrameControl()
        self.__gaze_movements = self.FrameControl()
        self.__clothe_correction = self.FrameControl()
        self.__means = [15, 10, 10, 2, 4, 15, 6, 9]
        self.__before_values = [None] * 8
        self.__ws = [1, 1, 3, 1, 2, 2, 1, 1]

    def __calc(self, x, i):
        if self.__before_values[i]:
            before_values_and_mean = self.__before_values[i] + [self.__means[i]]
        else:
            before_values_and_mean = [self.__means[i]]
        garm_mean = len(before_values_and_mean) / (sum(map(lambda x: 1 / x, before_values_and_mean)))
        pow_mean = (sum(map(lambda x: x ** 2, before_values_and_mean)) / len(before_values_and_mean)) ** 0.5
        if garm_mean <= x <= pow_mean:
            return 0
        elif x > pow_mean:
            return (x / pow_mean - 1) * 100.0 # * self.__ws[i]
        elif x < garm_mean:
            return (x / garm_mean - 1) * -100.0 # * self.__ws[i]

    def __calc3_relu(self, x, i):
        if self.__before_values[i]:
            before_values_and_mean = self.__before_values[i] + [self.__means[i]]
        else:
            before_values_and_mean = [self.__means[i]]
        pow_mean = (sum(map(lambda x: x ** 2, before_values_and_mean)) / len(before_values_and_mean)) ** 0.5
        if x <= pow_mean:
            return 0 # * self.__ws[i]
        elif x > pow_mean:
            return min((x / pow_mean - 1) * 100, 100.0) # * self.__ws[i]

    def __call_parameters(self):
        return [
            self.__calc3_relu(self.__nervous_lips.count_time(), 0),
            self.__calc3_relu(self.__open_mouth.count_time(), 1),
            self.__calc3_relu(self.__hand_with_phone.count_time(), 2),
            self.__calc3_relu(self.__hand_of_face.count_frame(), 3),
            self.__calc(self.__head_turns.count_frame_div_time(), 4),
            self.__calc(self.__blinks.count_frame_div_time(), 5),
            self.__calc(self.__gaze_movements.count_frame_div_time(), 6),
            self.__calc(self.__clothe_correction.count_intersection_over_union(), 7),
        ]

    def get(self):
        return self.nervous_lips_counter() + \
               self.open_mouth_counter() + \
               self.hand_with_phone_counter() + \
               self.hand_of_face_counter() + \
               self.head_turns_counter() + \
               self.blinks_counter() + \
               self.gaze_movements_counter() + \
               self.clothe_correction_counter() + \
               self.__call_parameters()

    def nervous_lips_counter(self):
        return [self.__nervous_lips.count_frame(),
                self.__nervous_lips.count_time(),
                self.__nervous_lips.count_frame_div_time(),
                self.__nervous_lips.count_intersection_over_union()]

    def open_mouth_counter(self):
        return [self.__open_mouth.count_frame(),
                self.__open_mouth.count_time(),
                self.__open_mouth.count_frame_div_time(),
                self.__open_mouth.count_intersection_over_union()]

    def hand_with_phone_counter(self):
        return [self.__hand_with_phone.count_frame(),
                self.__hand_with_phone.count_time(),
                self.__hand_with_phone.count_frame_div_time(),
                self.__hand_with_phone.count_intersection_over_union()]

    def hand_of_face_counter(self):
        return [self.__hand_of_face.count_frame(),
                self.__hand_of_face.count_time(),
                self.__hand_of_face.count_frame_div_time(),
                self.__hand_of_face.count_intersection_over_union()]

    def head_turns_counter(self):
        return [self.__head_turns.count_frame(),
                self.__head_turns.count_time(),
                self.__head_turns.count_frame_div_time(),
                self.__head_turns.count_intersection_over_union()]

    def blinks_counter(self):
        return [self.__blinks.count_frame(),
                self.__blinks.count_time(),
                self.__blinks.count_frame_div_time(),
                self.__blinks.count_intersection_over_union()]

    def gaze_movements_counter(self):
        return [self.__gaze_movements.count_frame(),
                self.__gaze_movements.count_time(),
                self.__gaze_movements.count_frame_div_time(),
                self.__gaze_movements.count_intersection_over_union()]

    def clothe_correction_counter(self):
        return [self.__clothe_correction.count_frame(),
                self.__clothe_correction.count_time(),
                self.__clothe_correction.count_frame_div_time(),
                self.__clothe_correction.count_intersection_over_union()]

    def update(self, data):
        self.__nervous_lips.update(data[0])
        self.__open_mouth.update(data[1])
        self.__hand_with_phone.update(data[2])
        self.__hand_of_face.update(data[3])
        self.__head_turns.update(data[4])
        self.__blinks.update(data[5])
        self.__gaze_movements.update(data[6])
        self.__clothe_correction.update(data[7])
