from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from thrift_api.data_transfer import DataTransfer

from image.image_processing import numpy_to_bytes


class Transfer:
    def __init__(self, host, port=8080, func=DataTransfer):
        self.transport = TTransport.TBufferedTransport(TSocket.TSocket(host=host, port=port))
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = DataTransfer.Client(self.protocol)
        self.func = func

    def open(self):
        self.transport.open()

    def close(self):
        self.transport.close()

    def trans_img(self, np_bytes):
        img = numpy_to_bytes(np_bytes)
        self.client.data_transfer_image(img)

    def trans_data_int(self, data):
        self.client.data_transfer_int(data)

    def trans_data_bool(self, data):
        self.client.data_transfer_bool(data)
