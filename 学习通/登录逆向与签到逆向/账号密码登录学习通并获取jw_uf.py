import requests
from requests.utils import dict_from_cookiejar
import execjs
import time
requests.packages.urllib3.disable_warnings()
import re


t=int(time.time()*1000)
js_Code=execjs.compile(open('jm.js', encoding='utf-8').read())
name=js_Code.call('encryptByAES','13383403941')
pwd=js_Code.call('encryptByAES','lll060503')

session = requests.session()
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://passport2.chaoxing.com',
    'Pragma': 'no-cache',
    'Referer': 'https://passport2.chaoxing.com/login?fid=12&refer=http%3A%2F%2Fi.chaoxing.com%2Fbase%3Ft%3D1763341782903%26backUrl%3Dhttps%253A%252F%252Fmh.chaoxing.com%252Fcookie%252Fcname%253Furl%253Dhttp%253A%252F%252Fjwc.scsw.edu.cn%26vflag%3Dtrue%26fid%3D3011%26tid%3D0%26wfworg%3Dtrue&space=2',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'fid': '-1',
    'uname': name,
    'password': pwd,
    'refer': 'http%3A%2F%2Fi.chaoxing.com%2Fbase%3Ft%3D1763341782903%26backUrl%3Dhttps%253A%252F%252Fmh.chaoxing.com%252Fcookie%252Fcname%253Furl%253Dhttp%253A%252F%252Fjwc.scsw.edu.cn%26vflag%3Dtrue%26fid%3D3011%26tid%3D0%26wfworg%3Dtrue',
    't': 'true',
    'forbidotherlogin': '0',
    'validate': '',
    'doubleFactorLogin': '0',
    'independentId': '0',
    'independentNameId': '0',
}

re1=session.post(url='https://passport2.chaoxing.com/fanyalogin',verify=False,data=data,headers=headers)

url=re1.json()['url']

data = {
    'courseType': '1',
    'courseFolderId': '0',
    'query': '',
    'pageHeader': '-1',
    'single': '0',
    'superstarClass': '0',
    'isFirefly': '0',
}

response = session.post(
    'https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courselistdata',
    headers=headers,
    data=data,
    verify=False,
)

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

    return {
        'name': name,
        'political_status': political_status,
        'gender': gender,
        'candidate_number': candidate_number,
        'origin_place': origin_place,
        'exam_score': exam_score,
        'graduated_school': graduated_school,
        'ethnicity': ethnicity,
        'student_id': student_id,
        'id_card': id_card,
    }

xinxi(jw_uf)

