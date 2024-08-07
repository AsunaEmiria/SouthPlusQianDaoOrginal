import requests
import os
import xml.etree.ElementTree as ET

# 获取 cookies
cookie_value = os.getenv('COOKIE')
if cookie_value:
    cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_value.split('; ')}
else:
    print("请确保环境变量 COOKIE 已设置")
    exit(1)

# 设置请求头
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

# 请求参数
params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'actions': 'job',
    'cid': '14',
    'nowtime': '1717167492479',
    'verify': '5af36471',
}

# 发起 GET 请求
response = requests.get('https://www.south-plus.net/plugin.php', params=params, cookies=cookies, headers=headers)

# 打印响应内容以进行调试
print("Response Status Code:", response.status_code)
print("Response Text:", response.text)

# 检查状态码
if response.status_code == 200:
    try:
        # 尝试解析 XML 数据
        root = ET.fromstring(response.text)
        cdata = root.text
        
        # 提取变量值
        values = cdata.split('\t')
        if len(values) == 2:
            action = values[0]
            message = values[1]
            print('周常-' + message)
        else:
            print("XML格式不正确，请检查COOKIE设置")
            
    except ET.ParseError as e:
        print(f"XML 解析错误: {e}")
else:
    print(f"请求失败，状态码: {response.status_code}")
