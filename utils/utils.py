from os import system, name
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
import json
import configparser

# clear console


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def connect_mongo_db(user, pwd, host):
    uri = (f'mongodb://{quote_plus(user)}:{quote_plus(pwd)}@{host}')

    try:
        mcon = MongoClient(uri)
        mdb = mcon.pwdmanager
        return mdb
    except ConnectionFailure:
        return None


def upload_pwd_from_file(file, mdb):
    # TO DO
    # 1 - Check for existing system and confirm update or new
    file_dict = json.load(open(file, 'r'))
    for item in file_dict:
        result = mdb.systems.insert_one(item)
    file_dict.close()


def get_sys_db_params(file):
    config = configparser.ConfigParser()
    config.read(file)

    host = config['DEFAULT']['host']
    user = config[host]['user']
    pwd = config[host]['password']

    return {'host': host, 'user': user, 'pwd': pwd}
