import requests
import os
import xml.etree.ElementTree as ET

# 获取环境变量 COOKIE
cookie_value = os.getenv('COOKIE')
if not cookie_value:
    print("未找到COOKIE，请检查环境变量设置")
    exit(1)

# 解析Cookie字符串
cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_value.split('; ')}

# 设置请求头
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7',
    'dnt': '1',
    'referer': 'https://www.south-plus.net/plugin.php?H_name-tasks-actions-newtasks.html.html',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

# 设置请求参数
params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'actions': 'job2',
    'cid': '14',
    'nowtime': '1717167492479',
    'verify': '5af36471',
}

# 发送GET请求
response = requests.get('https://www.south-plus.net/plugin.php', params=params, cookies=cookies, headers=headers)

# 检查响应状态
if response.status_code != 200:
    print(f"请求失败，状态码: {response.status_code}")
    print("响应内容:", response.text)
    exit(1)

# 尝试解析XML
try:
    root = ET.fromstring(response.content)
    cdata = root.text.strip() if root.text else ''
    
    # 提取变量值
    values = cdata.split('\t')
    if len(values) == 3:
        action = values[0]
        message = values[1]
        number = values[2]
        print('周常-' + message)
    else:
        print("XML格式不正确，请检查COOKIE设置")

except ET.ParseError as e:
    print(f"XML解析错误: {e}")
    print("返回的内容:", response.text)
