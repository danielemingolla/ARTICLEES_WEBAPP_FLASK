import json

# JSON with credential
PATH_JSON = 'articlee/credentials.txt'

# Read from json


def read_json(*args):
    for arg in args:
        if not isinstance(arg, str):
            raise Exception('TUTTI campi devono essere stringhe!')
    result = []
    with open(PATH_JSON) as json_file:
        data = json.load(json_file)
        for arg in args:
            try:
                result.append(data[arg])
            except:
                raise Exception(
                    'Errore: ALMENO una credenziale non esistente!')
        return result


class Config:
    SECRET_KEY, SQLALCHEMY_DATABASE_URI, MAIL_USERNAME, MAIL_PASSWORD = read_json(
        'SECRET_KEY', 'SQLALCHEMY_DATABASE_URI', 'MAIL_USERNAME', 'MAIL_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    DEBUG= True
    TESTING = False
    
