from environs import Env

env = Env()
env.read_env()

HOST = env.str('HOST')
PORT = env.str('PORT')
