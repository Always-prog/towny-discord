from yaml import safe_load, load as yaml_load
from os import listdir
config = safe_load(open('./config.yaml','r'))
token = config.get('bot_token')