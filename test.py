# 导入requests库
import requests

# 定义API密钥
API_KEY = 'PyHRKtUKt1kPJt4Ror2teXeczj'
 
# 设置url
url = f'https://api2.wer.plus/api/weather?key={API_KEY}'
 
# 发送post请求
response = requests.post(url, data={'city': '北京市'})
 
# 获取响应内容
result = response.json()
 
# 打印结果
print(result)