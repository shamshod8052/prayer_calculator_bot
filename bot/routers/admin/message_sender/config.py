from environs import Env

env = Env()
env.read_env()

SLEEP_TIME = env.float('SLEEP_TIME')
MAX_CONCURRENT = env.int('MAX_CONCURRENT')
