import requests
from threading import Thread
from multiprocessing import Queue
import json
from urllib import parse
import time

class XiaomiSpider(object):
    def __init__(self):
        # baseurl为抓包工具抓到的地址(去掉查询参数的)
        self.baseurl = 'http://app.mi.com/categotyAllListApi?'
        self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
        # 两个队列(url队列和解析队列)
        self.url_queue = Queue()
        self.parse_queue = Queue()
    # URL入队列(拼10个url放入队列)
    def get_url(self):
        for i in range(50):
            params = {
                'page': str(i),
                'categoryId': '2',
                'pageSize': '30'
            }
            params = parse.urlencode(params)
            # 拼接url地址,并入队列
            url = self.baseurl + params
            self.url_queue.put(url)

    # 采集线程事件函数(从url队列中获取地址,发请求获取响应,放到解析队列)
    def get_html(self):
        while True:
            if not self.url_queue.empty():
                url = self.url_queue.get()
                res = requests.get(url,headers=self.headers)
                res.encoding = 'utf-8'
                html = res.text
                # 把html放到解析队列中
                self.parse_queue.put(html)
            else:
                break
    # 解析线程事件函数(解析+保存数据)
    def parse_html(self):
        while True:
            try:
                # get()不到值一定会阻塞
                html = self.parse_queue.get(block=True,timeout=2)
                # html ：json格式的字符串,转为python数据类型
                html = json.loads(html)
                with open('小米.txt','a') as f:
                    for h in html['data']:
                        name = h['displayName']
                        link = 'http://app.mi.com/details?id=' + h['packageName']
                        f.write(name + '\t' + link + '\n')
            except:
                break
    # 主函数
    def work_on(self):
        # url入队列
        self.get_url()
        all_list = []
        # 创建多个采集线程
        for i in range(10):
            t = Thread(target=self.get_html)
            all_list.append(t)
            t.start()
        # 创建多个解析线程
        for i in range(10):
            t = Thread(target=self.parse_html)
            all_list.append(t)
            t.start()
        # 统一回收所有线程
        for p in all_list:
            p.join()

if __name__ == '__main__':
    start = time.time()
    spider = XiaomiSpider()
    spider.work_on()
    end = time.time()
    print('执行时间:%.2f' % (end-start))










