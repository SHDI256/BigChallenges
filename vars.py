from environs import Env

env = Env()
env.read_env()

HOST = env.str('HOST')
PORT1 = env.int('PORT1')
PORT2 = env.int('PORT2')

WS = env.list('WS')
MEANS = env.list('MEANS')
