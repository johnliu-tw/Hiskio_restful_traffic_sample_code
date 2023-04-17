# From Demo Test
from hashlib import sha1
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
import hmac
from requests import request
from pprint import pprint

import json
import math
import geocoder

app_id = 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
app_key = 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'

class Auth():
    def __init__(self, app_id, app_key):
        # 需教學 id 和 key 的關係，並可做修改
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        # 教學 auth 內部核可流程
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()
        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


if __name__ == '__main__':
    # a = Auth(app_id, app_key)
    # print(a.get_auth_header())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    response = request('get', 'https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/Station?$format=JSON', headers= headers)
    data = json.loads(response.text)
    # 示範 pprint 好處( 結構化 )
    # pprint(data)
    location = geocoder.ip('me').latlng
    my_lat = location[0]
    my_lon = location[1]
    min_result = 9999.0
    result_name = '台北'
    for station in data['Stations']:
        lat = station['StationPosition']['PositionLat']
        lon = station['StationPosition']['PositionLon']
        result = math.sqrt(math.pow( (lat - my_lat), 2) + math.pow( (lon - my_lon), 2))
        if station['StationName']['Zh_tw'] not in '正義':
            # pprint(station)
            pass
        if min_result > result:
            min_result = result
            result_name = station['StationName']['Zh_tw']

    print(result_name)