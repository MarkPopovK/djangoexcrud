import requests, json

endpoint = 'http://91909711.ngrok.io/'

def predict(radiant, dire):
    get_args = '?'
    for hero in radiant:
        get_args += f'r={hero}&'
    for hero in dire:
        get_args += f'd={hero}&'

    data = requests.get(endpoint+get_args)
    try:
        json_data = json.loads(data.text)
        p = json_data['p'][0]
    except Exception as e:
        print(e)
        p = 1


    # 0.75; 0.86; 1; 1.16; 1.33
    if   p < 0.66:msg = 'Serious advantage for dire'
    elif p < 0.75:msg = 'Advantage for dire'
    elif p < 1.33:msg = 'Almost equal picks (within error margin)'
    elif p < 1.52:msg = 'Advantage for radiant'
    else:         msg = 'Serious advantage for radiant'
    return {'probability': p, 'msg': msg}

