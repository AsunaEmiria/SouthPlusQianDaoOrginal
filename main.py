import os
import subprocess
import re
import asyncio
from telegram import Bot

def run_process(script_name):
    """运行指定的 Python 脚本并返回其输出"""
    try:
        process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            raise Exception(f"Error running {script_name}: {error.decode()}")
        return output.decode()
    except Exception as e:
        print(str(e))
        return ""

# 运行各个脚本并捕获输出
output_1 = run_process('APPLYDAILY.py')
output_2 = run_process('COLLECTDAILY.py')
output_3 = run_process('APPLYWEEKLY.py')
output_4 = run_process('COLLECTWEEKLY.py')
output_5 = run_process('GETSP.py')

# 检查结果并生成标题
response_text1 = output_2
title1 = "南+ 日常成功，" if re.search(r"完成", response_text1) else "南+ 日常失败，"

response_text2 = output_4
title2 = "周常成功，" if re.search(r"完成", response_text2) else "周常失败，"

title3 = output_5.strip()

# 合并输出为一个变量
merged_content = "\n".join([output_1, output_2, output_3, output_4])
merged_title = title1 + title2 + title3

print(merged_title)
print(merged_content)

bot_token = os.environ.get('BOTTOKEN')
chat_id = os.environ.get('USERID')

if not bot_token or not chat_id:
    print("未找到 BOTTOKEN 或 USERID，请检查环境变量设置")
    exit(1)

# 创建 Bot 实例
bot = Bot(token=bot_token)

# 发送消息的异步函数
async def send_message():
    try:
        await bot.send_message(chat_id=chat_id, text=merged_title + '\n' + merged_content)
    except Exception as e:
        print(f"发送消息时出错: {str(e)}")

# 运行异步函数
asyncio.run(send_message())
