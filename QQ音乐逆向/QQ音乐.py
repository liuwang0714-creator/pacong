import requests
import execjs
import json

cookies = {
    '_qimei_uuid42': '19c1c0d2f331003979aece0e024aec4657be71bd77',
    'yybsdk-webId': '746a31300000019b637fbbc70000148e',
    '_qimei_i_3': '64ed7181c65f53d3c5c5aa630dd176b4ffeff5a2475956d4b78e2e0a77c6256f373764943989e2d49393',
    '_qimei_q36': '',
    '_qimei_h38': '',
    '_qimei_q32': '',
    'RK': 'XquNccvOFr',
    'ptcz': '1c5b38514b5ba56a901f294cdd0d0047e6915e5dc99c12da59c4290484fbf9e1',
    'pgv_pvid': '3201238304',
    'qq_domain_video_guid_verify': 'b0b354a148d841e0',
    '_qimei_fingerprint': '9e6d26f550d63e7ed004cfe87f5f5b14',
    '_qimei_i_2': '5dcd69c3c90c',
    '_qimei_i_1': '76cd73e5f313',
    '_clck': '6tmetb|1|g48|0',
    'eas_sid': 'M1Z727W3y2j059J7d783u311F6',
    'fqm_pvqid': 'c1a18362-ef69-4097-9c4b-71576deb36a7',
    'ts_refer': 'cn.bing.com/',
    'ts_uid': '1925173676',
    'fqm_sessionid': '7500e703-abb1-4d49-9252-06550aa841e4',
    'pgv_info': 'ssid=s591321843',
    '_qpsvr_localtk': '0.28128193848127203',
    'login_type': '1',
    'qqmusic_key': 'Q_H_L_63k3NRAuypf12xSOT_AFfaYbtQW7tQyRbzbCqukIMfRnsOPIL52UyG-kY4VrAIoIU8x9Ulz5CDkvGmhGwWVS67X5f',
    'qm_keyst': 'Q_H_L_63k3NRAuypf12xSOT_AFfaYbtQW7tQyRbzbCqukIMfRnsOPIL52UyG-kY4VrAIoIU8x9Ulz5CDkvGmhGwWVS67X5f',
    'psrf_qqaccess_token': 'CCCDFDFD9FCF7028FB60A31BB4595245',
    'psrf_musickey_createtime': '1777436362',
    'wxopenid': '',
    'tmeLoginType': '2',
    'uin': '1989811470',
    'psrf_qqopenid': '1C8EDF5C09CFE89F0FB8ADE03C4112C4',
    'euin': 'oKEFNKc5oKvlon**',
    'wxrefresh_token': '',
    'music_ignore_pskey': '202306271436Hn@vBj',
    'psrf_qqunionid': '50818B3E5E94E74D1A60EF3140860A2A',
    'psrf_access_token_expiresAt': '1782620362',
    'psrf_qqrefresh_token': 'EDFC414FF583B2E0B61B405AAEAB2EA6',
    'wxunionid': '',
    'ts_last': 'y.qq.com/',
}

headers = {
    'accept': 'application/octet-stream',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'content-type': 'text/plain',
    'origin': 'https://y.qq.com',
    'priority': 'u=1, i',
    'referer': 'https://y.qq.com/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '_qimei_uuid42=19c1c0d2f331003979aece0e024aec4657be71bd77; yybsdk-webId=746a31300000019b637fbbc70000148e; _qimei_i_3=64ed7181c65f53d3c5c5aa630dd176b4ffeff5a2475956d4b78e2e0a77c6256f373764943989e2d49393; _qimei_q36=; _qimei_h38=; _qimei_q32=; RK=XquNccvOFr; ptcz=1c5b38514b5ba56a901f294cdd0d0047e6915e5dc99c12da59c4290484fbf9e1; pgv_pvid=3201238304; qq_domain_video_guid_verify=b0b354a148d841e0; _qimei_fingerprint=9e6d26f550d63e7ed004cfe87f5f5b14; _qimei_i_2=5dcd69c3c90c; _qimei_i_1=76cd73e5f313; _clck=6tmetb|1|g48|0; eas_sid=M1Z727W3y2j059J7d783u311F6; fqm_pvqid=c1a18362-ef69-4097-9c4b-71576deb36a7; ts_refer=cn.bing.com/; ts_uid=1925173676; fqm_sessionid=7500e703-abb1-4d49-9252-06550aa841e4; pgv_info=ssid=s591321843; _qpsvr_localtk=0.28128193848127203; login_type=1; qqmusic_key=Q_H_L_63k3NRAuypf12xSOT_AFfaYbtQW7tQyRbzbCqukIMfRnsOPIL52UyG-kY4VrAIoIU8x9Ulz5CDkvGmhGwWVS67X5f; qm_keyst=Q_H_L_63k3NRAuypf12xSOT_AFfaYbtQW7tQyRbzbCqukIMfRnsOPIL52UyG-kY4VrAIoIU8x9Ulz5CDkvGmhGwWVS67X5f; psrf_qqaccess_token=CCCDFDFD9FCF7028FB60A31BB4595245; psrf_musickey_createtime=1777436362; wxopenid=; tmeLoginType=2; uin=1989811470; psrf_qqopenid=1C8EDF5C09CFE89F0FB8ADE03C4112C4; euin=oKEFNKc5oKvlon**; wxrefresh_token=; music_ignore_pskey=202306271436Hn@vBj; psrf_qqunionid=50818B3E5E94E74D1A60EF3140860A2A; psrf_access_token_expiresAt=1782620362; psrf_qqrefresh_token=EDFC414FF583B2E0B61B405AAEAB2EA6; wxunionid=; ts_last=y.qq.com/',
}
def maindef(name):
    rs2 = requests.post("http://127.0.0.1:8676/ie",
        data=json.dumps({
            "name": name
            }),
            headers={"Content-Type": "application/json"})


    params = {
        '_': '1777436782282',
        'encoding': 'ag-1',
        'sign': rs2.text,
    }
    rs1 = requests.post("http://127.0.0.1:8676/toparams",
                        data=json.dumps({
                            "name": name
                        }),
                        headers={"Content-Type": "application/json"})
    data = rs1.text
    response = requests.post('https://u6.y.qq.com/cgi-bin/musics.fcg', params=params, cookies=cookies, headers=headers,
                             data=data)
    jsonarr = json.dumps(list(response.content))


    res = requests.post(
        "http://127.0.0.1:8676/encrypt",
        data=jsonarr,
        headers={"Content-Type": "application/json"}
    )

    print(res.json())

maindef("最好的安排")