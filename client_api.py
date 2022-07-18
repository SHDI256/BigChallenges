from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from thrift_api.data_transfer import DataTransfer, DataRegistration

from image.image_processing import bytes_to_numpy


class Transfer:
    def __init__(self, host, port, func=DataTransfer):
        self.transport = TTransport.TBufferedTransport(TSocket.TSocket(host=host, port=port))
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = DataTransfer.Client(self.protocol)
        self.func = func

    def open(self):
        self.transport.open()

    def close(self):
        self.transport.close()

    def request_transfer_image(self):
        return bytes_to_numpy(self.client.request_image_transfer())

    def request_data_transfer_double(self):
        return self.client.request_data_transfer_double()

    def data_transfer_verdict(self, verdict):
        self.client.data_transfer_verdict(verdict)


class Registration:
    def __init__(self, host, port):
        self.transport = TTransport.TBufferedTransport(TSocket.TSocket(host=host, port=port))
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = DataRegistration.Client(self.protocol)

    def open(self):
        self.transport.open()

    def close(self):
        self.transport.close()

    def data_transfer_photo(self, img):
        self.client.data_transfer_photo(img)

    def data_transfer_full_name(self, full_name):
        self.client.data_transfer_full_name(full_name)

    def data_transfer_sex(self, sex):
        self.client.data_transfer_sex(sex)

    def data_transfer_age(self, age):
        self.client.data_transfer_age(age)

    def data_transfer_int(self, data):
        self.client.data_transfer_int(data)

    def data_transfer_double(self, data):
        self.client.data_transfer_double(data)
