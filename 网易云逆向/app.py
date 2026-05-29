import requests
import execjs
from flask import Flask, Response, request
from flask_cors import CORS

js = execjs.compile(open('js.js', encoding='utf-8').read())
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"], "supports_credentials": True}})
cookies = {
    '_iuqxldmzr_': '32',
    'NMTID': '00ONfH8el93zGJjcE2YmgLftWxew3kAAAGcX9VpgQ',
    'WEVNSM': '1.0.0',
    'WNMCID': 'albbau.1771134346111.01.0',
    'WM_TID': 'MrtB3LDcOVlABEFEUEeS3VHe62QbfelS',
    'ntes_utid': 'tid._.itbtIyOqPilAAkERAFOWmSKGk7zO47Vy._.0',
    'sDeviceId': 'YD-dBoXAKNGlIVAUkVRFAOXnXeD0rzLorR3',
    '__snaker__id': 'Emw6Ka1BuqFbbv4b',
    'ntes_kaola_ad': '1',
    '__root_domain_v': '.163.com',
    '_qddaz': 'QD.395674249592076',
    '__csrf': '69e266420ffa34c0760a1d9f4b98c052',
    'JSESSIONID-WYYY': 'a6Rwkjrlq1na0m00xGBh6v6B6JTcdCo5b2qk5zbiqWij8DY7KEB3JU2WsKZSjvrSkRw%2FBSZlgkowumxe9OXlEkXdd%2F67R438XZa72dYM27p8btq%5CZI7xCCdtEyguIm2acOwZaf1UM2RFAC1slnvu0qswPqHBBdvI9RlyiwKm5zSU1D0u%3A1777186691641',
    'WM_NI': '5f7N%2BfCWkFSekLoIUHrHbeVLmeCNpYhEecFfGPufnZWmrnXRU4tjVmuTdc2onzUXhEZhxylBtoqpnqx4pLV6cW7cTv26oF3987n8Z3dA4fzt6nLFdwXwjmmyCgBGZ4bfbUY%3D',
    'WM_NIKE': '9ca17ae2e6ffcda170e2e6ee88f37caee9f894fb6aaceb8fa7d54b879e9bb1c679f58c8e86ee70b8ada2b4f52af0fea7c3b92af7baf9afaa6e8189a5a7d26fa994a1aad844b298ae86d548afbb8daff353ac9bab84c56e8590bb87ed5295b3be8fdb5a97ecbc8bd567b78cac84b165aea69bb9eb4f9ab8b89aef4ab8b1bf91ed7bbcecc0add53ea189f984d77ef2eaa1a7b233fce9a2d9d939a89ffc87f980f6b284a7e77d9ca9a68ef07381b98ea8d940a2baaeb6dc37e2a3',
    'gdxidpyhxdE': 'OvO0YOQBj62PhULjxYnauR%2FdGqHijbdpQNW4RMfAKx6oYA4MY0Het%5CeQya8%2B%5C2P74AjggOvdh%5Cc359i%2FmtR%5CWIMZv8Ebhh3bwk8%2B6cm3IszZu5I6JC2U4NQgCYObETJRAgnVztw%2FkSh54ZiM%5CjzfCva74%2FbvCIGo5Koan8Ugwo1dHQ6Q%3A1777185799920',
    'NTES_YD_SESS': 'AU5iWBOVu9GVdcDqU_xqudmwarD_5ysOadQXGW5laQWhBlf2BpU6Vj7EJ94GFfLsPBFtDtPG369ICAKR338hSr_RRSMQ4zpbyUF.1b8CJfwTo8rWgu1wQPSPvzx3XrFWZOaVbslV6kce0GHLOqWO3kLfRhDCHYd9_OsmR84xdLYpDDSYL7cAkAbwOIhRw5YJl7KDylTtyT6wrZl7ESHz41dVcMOBTB3X1Mez0oecNQrWC',
    'S_INFO': '1777184945|0|0&60##|19255871546',
    'P_INFO': '19255871546|1777184945|1|music|00&99|null&null&null#bej&null#10#0|&0||19255871546',
    '__csrf': 'c37feaa181add6b52ecd2efad23ab4cc',
    'MUSIC_U': '000C37563AFA4652B90F705FF6A75892937CC518B5930750B6EACC388B1807E36D33745935390D91C488CD08BD3F607B9D8157DBBBE46B281904350EF4497C6806AF4695C2A734B9C84C1F937E9BCD91F838DFB0758BF7E0ADC066D909CFF82017BEDC7C2BE15E65DC1ADA91DB17EB887F7DEF143E265AC432A86DE3A03155C300076DEC2BCD3F0843A9B93607FE0561FB6895E5A6D835CCC23C901BBE2C8410601AFCCBAA50DA05A32E24EDAD55AEE4BEA54C2FC78C5229C3B66DF2F05E4EF6A6E9AF1821E955AFCA0D7DD20DCB7D0DBB9358E69B0BDF4E030D3AE3879A9C1DC13635D0DC5BEF689649E9B90973960475BF729D39F7944EDC205476BCBD7AA393209C5B3CC4FD2C57D9C06BA71140460D091DDA0559663DA158E0D6D7BC5F93DC32ACB7D6A82CA638F6B835493E15980120FB2969B8B8BD236C7EF482C8F0E97B23E9B175A07DFBF858F79E0CE6F49261028037C845AFB8DEA9103F1137ACE8E7ED9F92D970B858B70B45168B8D8C56983F82BE0E859C95C5D701ABB9CCE5636A0A9D95CBA9851BD7292DC6EFC865144E',
    'playerid': '40191758',
}
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'nm-gcore-status': '1',
    'origin': 'https://music.163.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://music.163.com/search/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}
def song(name):
    data = {
        "s": name,
        "type": 1,
        "limit": 30,
        "offset": 0,
        "total": 'true',
        "csrf_token": "69e266420ffa34c0760a1d9f4b98c052"
    };

    ret = js.call("encrypt", name, data)

    params = ret["encText"]
    encSecKey = ret["encSecKey"]
    # 搜索接口
    url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token=69e266420ffa34c0760a1d9f4b98c052'


    data = {
        "params": params,
        "encSecKey": encSecKey
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    json_list = response.json()["result"]["songs"]
    list=[]
    for index, item in enumerate(json_list):
        list.append(
            {
                "id": str(index+1),
                "rname":item['ar'][0]['name'],
                "sname":item["name"],
                "songid":item["privilege"]["id"],
                "picUrl":item['al']["picUrl"],
            }
        )
    return list
def songurl(id):
    sgin_data={
        "ids": f"[{id}]",
        "level": "standard",
        "encodeType": "aac",
        "csrf_token": "69e266420ffa34c0760a1d9f4b98c052"
    }
    ret = js.call("encrypt", id,sgin_data)

    sgin_params = ret["encText"]
    sgin_encSecKey = ret["encSecKey"]

    params = {
        'csrf_token': '69e266420ffa34c0760a1d9f4b98c052',
    }
    data = {
        "params": sgin_params,
        "encSecKey": sgin_encSecKey
    }
    response = requests.post(
        'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=69e266420ffa34c0760a1d9f4b98c052',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    return response.json()['data'][0]['url']

def xunfei():
    return

@app.route("/encrypt", methods=["POST"])
def encrypt():
    name = request.json.get('name')
    return song(name)

@app.route("/play/<song_id>", methods=["GET"])
def play_music(song_id):
    real_url = songurl(song_id)

    headers = {}
    range_header = request.headers.get('Range', None)
    if range_header:
        headers['Range'] = range_header

    resp = requests.get(real_url, stream=True, headers=headers)
    content_length = resp.headers.get('Content-Length')
    status = 200 if not range_header else 206

    return Response(
        resp.iter_content(chunk_size=1024 * 1024),
        status=status,
        mimetype="audio/m4a",
        headers={
            "Content-Type": "audio/m4a",
            "Content-Length": content_length,
            "Accept-Ranges": "bytes",
            "Content-Range": resp.headers.get("Content-Range", "")
        }
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)