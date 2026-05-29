import requests
from flask import Flask, request, jsonify, Response, stream_with_context
import re
from flask_cors import CORS
import execjs
requests.packages.urllib3.disable_warnings()
from requests.utils import dict_from_cookiejar
from flask import Flask, jsonify, request, send_file, session as flask_session
import requests, re, time, io

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
app = Flask(__name__)
CORS(app, resources=r'/*')

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

cookies = {
    'fid': '3011',
    'JSESSIONID': 'F2C0459B3EBF4DB8C9162C75A052A98E',
    'route': '52ffa9af7a380e114204ed76732d509c',
    'retainlogin': '2',
}
t=int(time.time()*1000)
js_Code=execjs.compile(open('jm.js', encoding='utf-8').read())
uuid=''
enc=''

@app.route('/user_login',methods=['POST'])
def user_login():
    session = requests.session()
    data = request.get_json()
    name, pwd = data.get('name'), data.get('pwd')
    name = js_Code.call('encryptByAES', name)
    pwd = js_Code.call('encryptByAES', pwd)
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
    re1 = session.post(url='https://passport2.chaoxing.com/fanyalogin', verify=False, data=data, headers=headers)
    if re1.json()['status']==False:
        session.close()
        return {
            "msg":"账号密码错误",
            "code":"503",
        },503

    data = {
        'courseType': '1',
        'courseFolderId': '0',
        'query': '',
        'pageHeader': '-1',
        'single': '0',
        'superstarClass': '0',
        'isFirefly': '0',
    }
    session.post(
        'https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courselistdata',
        headers=headers,
        data=data,
        verify=False,
    )
    uid = session.cookies.get('_uid')
    vc3 = session.cookies.get('vc3')
    uf = session.cookies.get('uf')
    _d = session.cookies.get('_d')
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
        verify=False,
        allow_redirects=False
    )
    cookie_dict = dict_from_cookiejar(session.cookies)
    jw_uf = cookie_dict.get('jw_uf')
    us_xinxi=xinxi(jw_uf)
    session.close()
    return {
        "msg":"登录成功",
        "code":"200",
        "data":{
            "jw_uf":jw_uf,
            "name":us_xinxi["name"],
            "gender":us_xinxi["gender"],
            "address":us_xinxi["origin_place"],
            "student_id":us_xinxi["student_id"],
            "id_card":us_xinxi["id_card"],
            "chengji":us_xinxi["exam_score"],
        }
    },200


@app.route('/get_qr', methods=['GET'])
def get_qr():
    global enc,uuid
    # 1. 初始化会话
    s = requests.Session()
    params = {
        'fid': '12',
        'refer': 'http://i.chaoxing.com/base...',
        'space': '2',
    }
    # 2. 获取页面中的隐藏参数
    resp = s.get('https://passport2.chaoxing.com/login', params=params, headers=headers)

    def extract_value(html_text, target_id):
        """
        从HTML文本中提取指定id对应的value值，兼容两种属性顺序
        :param html_text: 网页HTML文本
        :param target_id: 要提取的id名称（如enc、uuid）
        :return: 提取到的value值，若未找到则返回None
        """
        # 模式1：id="xxx" value="值"
        pattern1 = re.compile(r'id="{}" value="(.*?)"'.format(re.escape(target_id)))
        # 模式2：value="值" id="xxx"
        pattern2 = re.compile(r'value="(.*?)" id="{}"'.format(re.escape(target_id)))

        # 先尝试模式1，找不到再试模式2
        result1 = pattern1.findall(html_text)
        if result1:
            return result1[0]

        result2 = pattern2.findall(html_text)
        if result2:
            return result2[0]

        # 都没找到时返回None，避免索引越界报错
        return None
    enc = extract_value(resp.text, "enc")
    # 提取uuid值
    uuid = extract_value(resp.text, "uuid")

    params = {
        'uuid': uuid,
        'fid': '-1',
    }
    qr_resp = s.get('https://passport2.chaoxing.com/createqr', params=params, cookies=cookies, headers=headers)
    # 5. 直接返回图片给前端显示
    return send_file(io.BytesIO(qr_resp.content), mimetype='image/png')


@app.route('/check_status', methods=['GET'])
def check_status():
    data = {
        'enc': enc,
        'uuid': uuid,
        'doubleFactorLogin': '0',
        'forbidotherlogin': '0',
    }
    # 调用超星接口检查状态
    s = requests.Session()
    resp = s.post(
        'https://passport2.chaoxing.com/getauthstatus/v2',
        data=data,
        cookies=cookies,
        headers=headers
    )
    res_json = resp.json()
    if res_json['mes']=='已扫描':
        return {
            "code":"201",
            "msg":"已扫描",
            "uid":res_json['uid'],
        }
    if res_json['mes']=="验证通过":
        params = {
            't': '1763341782903',
            'backUrl': 'https://mh.chaoxing.com/cookie/cname?url=http://jwc.scsw.edu.cn',
            'vflag': 'true',
            'fid': '3011',
            'tid': '0',
            'wfworg': 'true',
        }

        s.get('http://i.chaoxing.com/base', params=params, headers=headers, verify=False)
        uid = s.cookies.get('_uid')
        vc3 = s.cookies.get('vc3')
        uf = s.cookies.get('uf')
        _d = s.cookies.get('_d')
        jw_cookie = {
            '_d': _d,
            'UID': uid,
            'vc3': vc3,
            'uf': uf,
        }
        params = ''
        s.get(
            'https://jwc.scsw.edu.cn/jw/admin/scanLogin',
            params=params,
            cookies=jw_cookie,
            headers=headers,
            verify=False,
            allow_redirects=False
        )
        cookie_dict = dict_from_cookiejar(s.cookies)
        jw_uf = cookie_dict.get('jw_uf')
        us_xinxi = xinxi(jw_uf)
        s.close()
        return {
            "msg": "验证通过",
            "code": "200",
            "data": {
                "jw_uf": jw_uf,
                "name": us_xinxi["name"],
                "gender": us_xinxi["gender"],
                "address": us_xinxi["origin_place"],
                "student_id": us_xinxi["student_id"],
                "id_card": us_xinxi["id_card"],
                "chengji": us_xinxi["exam_score"],
            }
        }

    return res_json



@app.route("/avatar/<uid>", methods=['GET'])
def get_avatar(uid):
    """
    修改后的头像获取逻辑：
    1. 访问 photo.chaoxing.com，开启 allow_redirects=True 处理所有 301/302 重定向。
    2. 获取最终的真实图片数据并返回。
    """
    try:
        # 原始入口 URL
        entry_url = f"https://photo.chaoxing.com/p/{uid}_160"

        # 模拟浏览器头部
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://passport2.scsw.edu.cn/'
        }

        # requests 会自动跟随所有的 301/302 跳转，直到拿到最终的 200 响应内容
        response = requests.get(entry_url, headers=headers, timeout=10, allow_redirects=True)

        if response.status_code == 200:
            # 动态获取内容类型，确保返回正确的 image/png 或 image/jpeg
            content_type = response.headers.get('content-type', 'image/jpeg')
            return Response(response.content, mimetype=content_type)
        else:
            raise Exception("Failed to load image from remote")

    except Exception as e:
        print(f"获取头像失败: {e}")
        # 异常时返回默认 SVG 头像
        default_avatar = "<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160' viewBox='0 0 160 160'><circle cx='80' cy='80' r='80' fill='#409eff'/><text x='80' y='90' font-size='60' text-anchor='middle' fill='white'>👤</text></svg>"
        return Response(default_avatar, mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)