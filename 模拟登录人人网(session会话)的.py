import requests


## 第1步 ：把用户名和密码信息发给服务器
post_url = "http://www.renren.com/PLogin.do"
data = {"email":"13603263409","password":"zhanshen001"}
headers = {
	'Referer': 'http://www.renren.com/SysHome.do',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
# 创建session对象,可以保存cookie信息
session = requests.session()
# 发送带有用户名和密码的请求,获取登录后的cookie保存在
# session对象中
session.post(post_url,data=data,headers=headers)

## 第2步 ：访问个人主页(第1步已经有了cookie)
url = 'http://www.renren.com/967469305/profile'
res = session.get(url,headers=headers)
res.encoding = 'utf-8'
print(res.text)






