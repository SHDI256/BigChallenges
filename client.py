from client_api import Transfer

from vars import HOST


transfer = Transfer(HOST)

transfer.open()
transfer.trans_data_bool([False] * 8)
transfer.close()