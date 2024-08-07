import requests
import os
import xml.etree.ElementTree as ET

# 获取 COOKIE 环境变量
cookie_value = os.getenv('COOKIE')
if not cookie_value:
    print("未找到 COOKIE，请检查环境变量设置")
    exit(1)

# 解析 COOKIE 字符串
cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_value.split('; ')}

# 设置请求头
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7',
    'dnt': '1',
    'referer': 'https://www.south-plus.net/plugin.php?H_name-tasks-actions-newtasks.html.html',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

# 请求参数
params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'actions': 'job',
    'cid': '15',
    'nowtime': '1717167492479',  # 时间戳可以动态生成
    'verify': '5af36471',         # 验证码应动态获取
}

# 发送请求
response = requests.get('https://www.south-plus.net/plugin.php', params=params, cookies=cookies, headers=headers)

# 检查请求是否成功
if response.status_code != 200:
    print(f"请求失败，状态码: {response.status_code}")
    print("响应内容:", response.text)
    exit(1)

# 解析 XML 数据
data = response.text
try:
    root = ET.fromstring(data)
except ET.ParseError:
    print("响应不是有效的 XML，请检查服务器返回的数据")
    exit(1)

# 提取内容
cdata = root.text
if cdata is not None:
    values = cdata.split('\t')
    if len(values) == 2:
        action = values[0]
        message = values[1]
        print('日常-' + message)
    else:
        print("CDAT 区域格式不正确，请检查数据内容")
else:
    print("未能找到 CDATA 文本，请检查响应结构")
