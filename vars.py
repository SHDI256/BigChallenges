from environs import Env

env = Env()
env.read_env()

HOST = env.str('HOST')
PORT1 = env.str('PORT1')
PORT2 = env.str('PORT2')
