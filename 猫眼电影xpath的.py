from urllib import request
import time
import pymongo
from lxml import etree

class MaoyanSpider(object):
  def __init__(self):
    self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
    # 用来计数
    self.page = 1
    # 连接对象
    self.conn = pymongo.MongoClient('localhost',27017)
    # 库对象
    self.db = self.conn['maoyandb']
    # 集合对象
    self.myset = self.db['top100']

  # 获取页面
  def get_page(self,url):
    req = request.Request(url,headers=self.headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')
    # 直接调用解析函数,去对html做解析
    self.parse_page(html)

  # 解析页面
  def parse_page(self,html):
    # 创建解析对象
    parse_html = etree.HTML(html)
    # 基准xpath匹配
    filmobj_list = parse_html.xpath('//dl[@class="board-wrapper"]//dd')
    # filmobj_list : ['element dd at ','']
    # 循环遍历
    for film in filmobj_list:
      name = film.xpath('./a/@title')[0].strip()
      star = film.xpath('.//p[@class="star"]/text()')[0].strip()
      time = film.xpath('.//p[@class="releasetime"]/text()')[0].strip()
      d = {
        '电影名称:': name,
        '电影主演:': star,
        '上映时间:': time
      }
      print(d)






  # 保存数据
  def write_mongo(self,r_list):
    for r_t in r_list:
      d = {
        '电影名称:' : r_t[0].strip(),
        '电影主演:' : r_t[1].strip(),
        '上映时间:' : r_t[2].strip()
      }
      # 插入数据库
      self.myset.insert_one(d)

  # 主函数
  def work_on(self):
    for pn in range(0,41,10):
      url = 'https://maoyan.com/board/4?offset=%s'\
                                          % str(pn)
      self.get_page(url)
      print('第%d页爬取成功' % self.page)
      self.page += 1
      time.sleep(2)


if __name__ == '__main__':
  begin = time.time()
  spider = MaoyanSpider()
  spider.work_on()
  end = time.time()
  print('执行时间:%.2f' % (end-begin))











