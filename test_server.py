from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from thrift_api.data_transfer import DataTransfer
from thrift_api.data_transfer import DataRegistration

from processing.data_processing import Serializer
from processing.image_processing import numpy_to_bytes, bytes_to_numpy

from multiprocessing import Process

# from keyboard import is_pressed


class TransferHandler:
    def __init__(self):
        self.log = {}
        self.image_counter = 0
        self.cmp = Serializer()
        self.img = None

    def data_transfer_image(self, img):
        self.img = bytes_to_numpy(img)
        self.image_counter += 1

    def data_transfer_int(self, data):
        pass

    def data_transfer_bool(self, data):
        self.cmp.update_parameters(data)
        print(data)

    def request_image_transfer(self):
        return numpy_to_bytes(self.img)

    def request_data_transfer_double(self):
        print(self.cmp.get_user_parameters())
        return self.cmp.get_user_parameters()

    def request_predict_transfer(self, predict):
        pass

    def data_transfer_verdict(self, verdict):
        print(verdict)

    def data_transfer_double(self, data):
        self.cmp.update_face(data)
        print(self.cmp.update_face(data))
        return data

    def reboot(self):
        if is_pressed('ctrl'):
            print(1)
            self.cmp = Serializer()


class RegistrationHandler:
    def __init__(self):
        self.cmp = Serializer()
        self.photo = None
        self.full_name = None
        self.sex = None
        self.age = None

    def data_transfer_photo(self, img):
        self.photo = bytes_to_numpy(img)
        print(self.photo)
        self.cmp.add_user(self.full_name, self.sex, self.age, self.photo)

    def data_transfer_full_name(self, full_name):
        self.full_name = ' '.join(full_name)

    def data_transfer_sex(self, sex):
        self.sex = int(sex)

    def data_transfer_age(self, age):
        self.age = age


transfer_handler = TransferHandler()
registration_handler = RegistrationHandler()

transfer_processor = DataTransfer.Processor(transfer_handler)
registration_processor = DataRegistration.Processor(registration_handler)

transfer_transport = TSocket.TServerSocket(host='192.168.1.183', port=8080)
registration_transport = TSocket.TServerSocket(host='192.168.1.183', port=9090)

transfer_tfactory = TTransport.TBufferedTransportFactory()
registration_tfactory = TTransport.TBufferedTransportFactory()

transfer_pfactory = TBinaryProtocol.TBinaryProtocolFactory()
registration_pfactory = TBinaryProtocol.TBinaryProtocolFactory()

transfer_server = TServer.TSimpleServer(transfer_processor, transfer_transport, transfer_tfactory, transfer_pfactory)
registration_server = TServer.TSimpleServer(registration_processor, registration_transport, registration_tfactory, registration_pfactory)


def main(server):
    server.serve()


# def reboot():
#     while 1:
#         transfer_handler.reboot()


if __name__ == '__main__':

    transfer_server_proc = Process(target=main, args=(transfer_server,))
    registration_server_proc = Process(target=main, args=(registration_server,))

    # reboot_proc = Process(target=reboot)

    transfer_server_proc.start()
    registration_server_proc.start()
    # reboot_proc.start()
