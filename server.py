from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from thrift_api.data_transfer import DataTransfer

from Serializer import Serializer
from processing.image_processing import numpy_to_img, numpy_to_bytes, bytes_to_numpy

from multiprocessing import Process

from keyboard import is_pressed


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
        print(data)

    def data_transfer_bool(self, data):
        self.cmp.update(data)
        print(data)

    def request_image_transfer(self):
        return numpy_to_bytes(self.img)

    def request_data_transfer_double(self):
        print(self.cmp.get())
        return self.cmp.get()

    def request_predict_transfer(self, predict):
        pass

    def data_transfer_verdict(self, verdict):
        print(verdict)


handler = TransferHandler()
processor = DataTransfer.Processor(handler)
transport = TSocket.TServerSocket(host='192.168.1.119', port=8080)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

#
# def main(server):
#     server.serve()
#
#
# def reboot():
#     while 1:
#         if is_pressed('ctrl'): handler.cmp = Serializer()
#
#
# if __name__ == '__main__':
#
#     server_proc = Process(target=main, args=(server,))
#     reboot_proc = Process(target=reboot)
#
#     server_proc.start()
#     reboot_proc.start()

server.serve()