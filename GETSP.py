from bs4 import BeautifulSoup
import os
import requests

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

# 发送GET请求
response = requests.get('https://www.south-plus.net/', cookies=cookies, headers=headers)

# 检查请求是否成功
if response.status_code != 200:
    print(f"请求失败，状态码: {response.status_code}")
    print("响应内容:", response.text)
    exit(1)

# 获得HTML代码
html_code = response.text

# 使用BeautifulSoup解析HTML代码
soup = BeautifulSoup(html_code, 'html.parser')

# 找到包含SP币值的<span>标签
sp_coin_span = soup.find('span', class_='s3 f10')

# 检查是否找到SP币值
if sp_coin_span is not None:
    # 提取SP币值
    sp_coin_value = sp_coin_span.text.strip()
    # 输出SP币值
    print("SP币:", sp_coin_value)
else:
    print("未能找到SP币值，请检查HTML结构或类名")
