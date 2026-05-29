import requests
from dns.message import make_response
from requests.utils import dict_from_cookiejar
from flask import flash,make_response
import execjs
import time
requests.packages.urllib3.disable_warnings()
import re
session = requests.session()

cookies = {
    'fid': '3011',
    'JSESSIONID': 'F2C0459B3EBF4DB8C9162C75A052A98E',
    'route': '52ffa9af7a380e114204ed76732d509c',
    'retainlogin': '2',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://passport2.chaoxing.com/login?fid=12&refer=http%3A%2F%2Fi.chaoxing.com%2Fbase%3Ft%3D1763341782903%26backUrl%3Dhttps%253A%252F%252Fmh.chaoxing.com%252Fcookie%252Fcname%253Furl%253Dhttp%253A%252F%252Fjwc.scsw.edu.cn%26vflag%3Dtrue%26fid%3D3011%26tid%3D0%26wfworg%3Dtrue&space=2',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'fid': '12',
    'refer': 'http://i.chaoxing.com/base?t=1763341782903&backUrl=https%3A%2F%2Fmh.chaoxing.com%2Fcookie%2Fcname%3Furl%3Dhttp%3A%2F%2Fjwc.scsw.edu.cn&vflag=true&fid=3011&tid=0&wfworg=true',
    'space': '2',
}

response = session.get('https://passport2.chaoxing.com/login', params=params, cookies=cookies, headers=headers)

text = response.text
enc=re.findall(r'<input type="hidden" value="(.*?)" id="enc"/>',text)[0]
uuid=re.findall(r'<input type="hidden" value="(.*?)" id="uuid"/>',text)[0]
print('enc:'+enc+'\n'+'uuid:'+uuid)

params = {
    'uuid': uuid,
    'fid': '-1',
}
response = session.get('https://passport2.chaoxing.com/createqr', params=params, cookies=cookies, headers=headers)
open('qr.png', 'wb').write(response.content)
data = {
    'enc': enc,
    'uuid':uuid,
    'doubleFactorLogin': '0',
    'forbidotherlogin': '0',
}

while True:
    response = session.post('https://passport2.chaoxing.com/getauthstatus/v2', cookies=cookies, headers=headers,data=data)
    print(response.text)
    if response.json()['mes'] == '已扫描':
        uid=response.json()['uid']
        tx = session.get(f'https://photo.chaoxing.com/p/{uid}_160', headers=headers)
        open('tx.png', 'wb').write(tx.content)
    if response.json()['mes'] == '验证通过':
        break
    time.sleep(1)
session.get('http://i.chaoxing.com/base?t=1763341782903&backUrl=https%3A%2F%2Fmh.chaoxing.com%2Fcookie%2Fcname%3Furl%3Dhttp%3A%2F%2Fjwc.scsw.edu.cn&vflag=true&fid=3011&tid=0&wfworg=true',headers=headers)

uid=session.cookies.get('_uid')
vc3=session.cookies.get('vc3')
uf=session.cookies.get('uf')
_d=session.cookies.get('_d')

jw_cookie = {
    '_d': _d,
    'UID': uid,
    'vc3': vc3,
    'uf': uf,
}


params = ''

session.get(
    'https://jwc.scsw.edu.cn/jw/admin/scanLogin',
    params=params,
    cookies=jw_cookie,
    headers=headers,
    verify=False,  # 新增：忽略SSL证书校验（必加，否则可能报错）
    allow_redirects=False  # 新增：禁止重定向，避免Cookie被覆盖
)

cookie_dict = dict_from_cookiejar(session.cookies)
# 直接提取jw_uf的值（不存在则返回None/自定义默认值）
jw_uf = cookie_dict.get('jw_uf')
print(jw_uf)


def xinxi(jw_uf):
    cookies = {
        'jw_uf': jw_uf,
    }

    response = requests.get('https://jwc.scsw.edu.cn/jw/admin/xsd/xsjbxx/xskpxgview', cookies=cookies)

    # 使用正则表达式提取各项信息
    def extract_field_by_label(html_text, field_label):
        """根据标签文本提取对应字段值"""
        escaped_label = re.escape(field_label)

        # 通用模式：匹配标签文本并提取内容区域的label值
        pattern = rf'<div class="item-label">[^<]*<label[^>]*>[^<]*{escaped_label}[^<]*</label>[^<]*</div>[^<]*<div class="item-content">[^<]*<label[^>]*>([^<]+)</label>'
        match = re.search(pattern, html_text, re.DOTALL)
        if match:
            return match.group(1).strip()

        return None

    # 提取各项信息
    name = extract_field_by_label(response.text, '姓名:')
    political_status = extract_field_by_label(response.text, '政治面貌:')
    gender = extract_field_by_label(response.text, '性别:')
    candidate_number = extract_field_by_label(response.text, '考生号:')
    origin_place = extract_field_by_label(response.text, '生源地:')
    exam_score = extract_field_by_label(response.text, '高考成绩:')
    graduated_school = extract_field_by_label(response.text, '毕业中学:')
    ethnicity = extract_field_by_label(response.text, '民族:')  # 添加民族信息

    student_id = ''
    # 单独提取学号，使用专门的正则表达式
    student_id_match = re.search(
        r'<label><font[^>]*>\*</font>学号:</label>[^<]*</div>[^<]*<div class="item-content">[^<]*<input[^>]*>[^<]*<label>([^<]+)</label>',
        response.text, re.DOTALL)
    if student_id_match:
        student_id = student_id_match.group(1).strip()

    # 提取身份证号
    id_card = extract_field_by_label(response.text, '身份证件号:')

    # 输出结果
    print(f"姓名: {name}")
    print(f"身份证号: {id_card}")
    print(f"政治面貌: {political_status}")
    print(f"性别: {gender}")
    print(f"考生号: {candidate_number}")
    print(f"生源地: {origin_place}")
    print(f"高考成绩: {exam_score}")
    print(f"毕业中学: {graduated_school}")
    print(f"民族: {ethnicity}")  # 输出民族信息
    print(f"学号: {student_id}")  # 输出学号信息

xinxi(jw_uf)