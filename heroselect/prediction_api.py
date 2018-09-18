import requests

endpoint = '127.0.0.1'

def predict(radiant, dire):
    p = 0.77


    # 0.75; 0.86; 1; 1.16; 1.33
    if   p < 0.75:msg = 'Serious advantage for dire'
    elif p < 0.86:msg = 'Advantage for dire'
    elif p < 1.16:msg = 'Almost equal picks'
    elif p < 1.33:msg = 'Advantage for radiant'
    else:         msg = 'Serious advantage for radiant'
    return {'probability': p, 'msg': msg}