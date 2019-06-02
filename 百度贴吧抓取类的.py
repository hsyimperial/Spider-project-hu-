from urllib import request
from urllib import parse
import random
from useragents import *

class BaiduSpider:
  def __init__(self):
    self.baseurl = 'http://tieba.baidu.com/f?'

  # 获取页面
  def get_page(self,url,headers):
    req = request.Request(url,headers=headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')
    return html

  # 解析页面,提取数据
  def parse_page(self):
    pass

  # 保存数据
  def write_page(self,filename,html):
    with open(filename,'w') as f:
      f.write(html)

  # 主函数
  def run(self):
    name = input('请输入贴吧名称:')
    start = int(input('请输入起始页:'))
    end = int(input('请输入终止页:'))
    # for循环拼接URL地址,发请求
    for page in range(start, end + 1):
      headers = random.choice(header_list)
      pn = (page - 1) * 50
      # string : 'kw=%E8...&pn=...'
      string = parse.urlencode(
        {'kw': name, 'pn': str(pn)})
      url = self.baseurl + string
      filename = '%s-第%d页.html' % (name, page)
      html = self.get_page(url,headers)
      self.write_page(filename,html)

      print('第%d页爬取成功' % page)

if __name__ == '__main__':
  spider = BaiduSpider()
  spider.run()











