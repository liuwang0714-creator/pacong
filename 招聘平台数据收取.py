import requests
import pandas as pd
import time

cookies = {
    'inited_user': '2d526278bba9692d34af9d36720d0fc9',
    '__gc_id': '26f2df8383454d0cb013a73a656eac0d',
    '__uuid': '1773650468927.45',
    '__sessionId': '1773654604142.63',
    'XSRF-TOKEN': 'ta_NRUlEQJaK_mkyi9ym3g',
    'hpo_role-sec_project': 'sec_project_liepin',
    'hpo_sec_tenant': '0',
    'acw_tc': '0000000017736546240593025e11d8a83157e511f11e8f7cdc91fb9cb2b41e',
    'UniqueKey': '6edbe90f4697a6f840d501f6e766523c',
    'liepin_login_valid': '0',
    'lt_auth': '7r0CPHVQmVmo4XbcjGJe5fsf3N2vAmXN8i4I00tT1oK%2BXKHj4PziRgmFr7IE9CoIq0hyfv4zMLf5Nu77zXVM7Eca%2B1Gkk57ht%2F%2B4hSwKTeRlLfijg%2Fj0m8SGEZZ3lS8AwSJjpnsRk0TxsC0yW5fT2WP1t5nX0Y2my%2FP0iCyWqBg8',
    'user_roles': '0',
    'user_photo': '5f8fa395dfb13a7dee343d2d08u.png',
    'need_bind_tel': 'false',
    'new_user': 'true',
    'c_flag': '7e40543a9b5510b4824bd86d697eaba8',
    'inited_user': '2d526278bba9692d34af9d36720d0fc9',
    'imId_0': 'ac2ad47eade6d2d482de234259c39d38',
    'imClientId_0': 'ac2ad47eade6d2d43b8feb91c6db0485',
    '__session_seq': '7',
    '__tlg_event_seq': '33',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://www.liepin.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.liepin.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'X-Client-Type': 'web',
    'X-Fscp-Bi-Stat': '{"location":"https://www.liepin.com/zhaopin/?city=410&dq=410&pubTime=&currentPage=0&pageSize=40&key=java%E5%BC%80%E5%8F%91&suggestTag=&workYearCode=0&compId=&compName=&compTag=&industry=&salaryCode=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&otherCity=&sfrom=search_job_pc&ckId=kwfji6dcrd4zb72i7qlts5eeu9h8v1na&scene=input&skId=kwfji6dcrd4zb72i7qlts5eeu9h8v1na&fkId=kwfji6dcrd4zb72i7qlts5eeu9h8v1na&suggestId="}',
    'X-Fscp-Fe-Version': '',
    'X-Fscp-Std-Info': '{"client_id": "40108"}',
    'X-Fscp-Trace-Id': 'a7889c85-e37a-47f9-a108-40005315841c',
    'X-Fscp-Version': '1.1',
    'X-Requested-With': 'XMLHttpRequest',
    'X-XSRF-TOKEN': 'yBV2rJuTSNa1U80fAzYEgw',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
# for item in text:
#     print(item)
#     # 公司名称
#     print(item['comp']['compName'])
#     # 岗位类型
#     print(item['comp']['compIndustry'])
#     # # 岗位名称
#     print(item['job']['title'])
#     # 岗位明细啊url,前缀https://www.liepin.com/job/1980512461.shtml?
#     # print(item['job']['dataPromId'])
#     # 薪资待遇
#     print(item['job']['salary'])
#     # 地区
#     print(item['job']['dq'])
#     # 工作经验要求
#     print(item['job']['requireWorkYears'])
#     # 学历要求
#     print(item['job']['requireEduLevel'])
#     # 联系人
#     print(item['recruiter']['recruiterName'])
data_list = []

i=0
a=0
while True:
    json_data = {
        'data': {
            'mainSearchPcConditionForm': {
                'city': '410',
                'dq': '410',
                'currentPage': 0,
                'pageSize': 50,
                'key': '前端开发',
                'suggestTag': '',
                'workYearCode': '0',
                'compId': '',
                'compName': '',
                'compTag': '',
                'industry': '',
                'salaryCode': '',
                'jobKind': '',
                'compScale': '',
                'compKind': '',
                'compStage': '',
                'eduLevel': '',
                'salaryLow': '',
                'salaryHigh': '',
                'hrActiveTimeCode': '',
            },
            'passThroughForm': {
                'ckId': '5voc1q9qyf7h6x04hvymiou6a0sdh16b',
                'scene': 'page',
                'skId': 'g48wuhhn5pjtsrbrg0uppq6jqsibewhb',
                'fkId': 'g48wuhhn5pjtsrbrg0uppq6jqsibewhb',
                'sfrom': 'search_job_pc',
            },
        },
    }
    response = requests.post(
        'https://api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    text = response.json()['data']['data']['jobCardList']
    for item in text:
        row_data = {
            '公司名称': item['comp']['compName'],
            '岗位类型': item['comp']['compIndustry'] if 'compIndustry' in item['comp'] else '无',
            '岗位名称': item['job']['title'],
            '薪资待遇': item['job']['salary'],
            '地区': item['job']['dq'],
            '工作经验要求': item['job']['requireWorkYears'] if 'requireWorkYears' in item['job'] else '无',
            '学历要求': item['job']['requireEduLevel'] if 'requireEduLevel' in item['job'] else '无',
            '联系人': item['recruiter']['recruiterName']
        }
        data_list.append(row_data)
        a+=1
    print(i)
    if i >=25  :
        break
    i+=1
    time.sleep(2)

df = pd.DataFrame(data_list)
df.to_excel('前端开发.xlsx', index=False)

print("数据已成功写入Excel文件！")
