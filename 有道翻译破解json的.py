import requests
from hashlib import md5
import time
import random
import json

# url一定要写F12抓包抓到的POST的地址
url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
headers = {
        # 下面三个是反爬检查较多的三个字段
        'Cookie':'OUTFOX_SEARCH_USER_ID=1516386930@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=760569518.7197; JSESSIONID=aaa1dHsc8I4yNgrvW7LNw; td_cookie=18446744069709674982; ___rl__test__cookies=1554368672202',
        'Referer':'http://fanyi.youdao.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# ts
ts = str(int(time.time()*1000))
# salt
salt = str(int(time.time()*1000))+\
                   str(random.randint(0,10))
# sign
key = input('请输入要翻译的单词:')
string = "fanyideskweb" + key + salt + \
                   "1L5ja}w$puC.v_Kz3@yYn"
sign = md5()
sign.update(string.encode('utf-8'))
sign = sign.hexdigest()
# 定义form表单数据为字典
data = {
        'i': key,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'ts': ts,
        'bv': 'd6c3cd962e29b66abe48fcb8f4dd7f7d',
        'doctype':'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME',
        'typoResult': 'false',
}

# 发请求获取响应内容
res = requests.post(url,data=data,headers=headers)
res.encoding = 'utf-8'
# html为json格式的字符串: '{"":"","":"","":""}'
html = res.text
# json.loads()方法把json格式的字符串转为python数据类型
html = json.loads(html)

result = html['translateResult'][0][0]['tgt']
print(result)

# {
# "translateResult":[[{"tgt":"老虎","src":"tiger"}]],
# "errorCode":0,
# "type":"en2zh-CHS",
# "smartResult":
# {"entries":["","n. 老虎；凶暴的人\r\n","n. (Tiger)人名；(英)泰格；(法)蒂热；(瑞典)蒂格\r\n"],"type":1}
# }








