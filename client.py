# from vars import HOST, PORT

from client_api import Transfer

from vars import HOST, PORT

transfer = Transfer(HOST)
transfer.open()
transfer.request_transfer_image()
transfer.close()