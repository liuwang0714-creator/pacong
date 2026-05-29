import requests
import re
import threading
import schedule
import time


import requests
from requests.utils import dict_from_cookiejar
import execjs
import time
requests.packages.urllib3.disable_warnings()
import re



t = int(time.time() * 1000)
js_Code = execjs.compile(open('jm.js', encoding='utf-8').read())
name = js_Code.call('encryptByAES', '账号')
pwd = js_Code.call('encryptByAES', '密码')

session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# ====================== 核心修复：每次执行都重新获取课程 ======================
def get_all_courses():


    datae = {
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

    session.post(url='https://passport2.chaoxing.com/fanyalogin', verify=False, data=datae, headers=headers)

    try:
        data = {
            'courseType': '1', 'courseFolderId': '0', 'query': '',
            'pageHeader': '-1', 'single': '0', 'superstarClass': '0', 'isFirefly': '0'
        }
        response = session.post(
            'https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courselistdata',
             headers=headers, data=data, timeout=10
        )
        text = response.text
        kecheng = re.findall(r'<div id="stuNormalCourseListDiv">(.*?)<div id="isState">', text, re.DOTALL)
        if not kecheng:
            return []

        kecheng2 = re.findall(r'<div class="course-cover">(.*?)<div class="wisdomBtn"', kecheng[0], re.DOTALL)
        kechengidlist = []
        for i in kecheng2:
            clazz_id = re.findall(r'clazzId" value="(.*?)"', i)
            course_id = re.findall(r'courseId" value="(.*?)"', i)
            if clazz_id and course_id:
                kechengidlist.append({
                    'clazzId': clazz_id[0],
                    'courseId': course_id[0]
                })
        return kechengidlist
    except:
        return []

# ====================== 检测未交作业 ======================
weizuo_aii = []

def func(courseId, classId):
    global weizuo_aii
    try:
        res = session.get(
            f'https://mooc1.chaoxing.com/visit/stucoursemiddle?courseid={courseId}&clazzid={classId}&cpi=415080288&ismooc2=1&v=2',
            headers=headers, timeout=10
        )
        enc = re.findall(r'id="workEnc" name="workEnc" value="(.*?)"', res.text)
        if not enc:
            return

        response = session.get(
            'https://mooc1.chaoxing.com/mooc2/work/list',
            params={'courseId': courseId, 'classId': classId, 'enc': enc[0]},
             headers=headers, timeout=10
        )
        text = response.text
        items = re.findall(r'<li onclick="goTask(.*?)</li>', text, re.DOTALL)

        for item in items:
            if 'time notOver' in item and '未交' in item:
                name = re.findall(r'class="textHidden colorDeep" title="(.*?)"', res.text)
                url = re.findall(r'data="(.*?)"', item)
                if name and url:
                    weizuo_aii.append({
                        '课程名': name[0],
                        '作业链接': url[0]
                    })
    except Exception as e:
        print(f"线程出错: {e}")

# ====================== 主函数（修复版） ======================
def ev_main():
    global weizuo_aii
    weizuo_aii = []  # 每次执行清空！！！
    print("\n【开始检测未完成作业...】")

    kechengidlist = get_all_courses()
    if not kechengidlist:
        print("未获取到课程列表！Cookie可能失效")
        return

    thread_list = []
    for i in kechengidlist:
        t = threading.Thread(target=func, args=(i['courseId'], i['clazzId']))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()
    print(weizuo_aii)
    if len(weizuo_aii) > 0:
        print(f'检测到【{len(weizuo_aii)}】条未完成作业，正在推送...')
        content = f"<h3>您还有{len(weizuo_aii)}条作业未完成<h3><br>"
        for item in weizuo_aii:
            content += f"课程名：{item['课程名']}<br>"
            content += f"<br>作业链接(点击跳转)：<a href='{item['作业链接']}'>{item['作业链接']}</a><br>"

        for i in range(3):
            try:
                res = requests.post(
                    'https://push.showdoc.com.cn/server/api/push/83623a18b254b4396544a74244eb8cbd1488914159',
                    data={"title": "学习通未完成作业", "content":content},
                    timeout=10
                )
                if res.json().get('error_code') == 0:
                    print("✅ 推送成功！")
                    break
                else:
                    print(f"推送失败，{i+1}/3 重试...")
            except:
                print("推送请求异常")
            time.sleep(3)
    else:
        print("✅ 暂无未提交作业！")

# ====================== 定时任务 ======================
print("程序已启动 → 每天 17:25 自动检测作业")
ev_main()  # 启动时先执行一次测试

schedule.every().day.at("17:25").do(ev_main)

while True:
    schedule.run_pending()
    time.sleep(30)