from selenium import webdriver
import time
import csv

class JdSpider(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://www.jd.com/'
        self.page = 1
    # 发请求获取商品信息,发送内容到文本框,点击搜索按钮
    def get_page(self,key):
        self.driver.get(self.url)
        self.driver.find_element_by_class_name('text').send_keys(key)
        self.driver.find_element_by_class_name('button').click()
        # 休眠3秒,等待页面加载
        time.sleep(4)
    # 解析页面
    def parse_page(self):
        # 执行JS脚本,进度条拉到最下面(Ajax动态加载)
        self.driver.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        time.sleep(3)
        # xpath匹配所有的商品信息
        r_list = self.driver.find_elements_by_xpath(
                             '//div[@id="J_goodsList"]//li')
        for r in r_list:
            # info_list : ['￥29','拍拍','书名','评论','专营店']
            info_list = r.text.split('\n')
            if info_list[1] == '拍拍':
                price = info_list[0]
                name = info_list[2]
                comment = info_list[3]
                shop = info_list[4]
            else:
                price = info_list[0]
                name = info_list[1]
                comment = info_list[2]
                shop = info_list[3]
            L = [price,comment,shop,name]
            self.write_csv(L)
    # 保存数据
    def write_csv(self,L):
        with open('product.csv','a',newline='',encoding='gb18030') as f:
            writer = csv.writer(f)
            writer.writerow(L)
    # 主函数
    def work_on(self):
        key = input('请输入商品:')
        self.get_page(key)
        while True:
            self.parse_page()
            print('第%d页爬取完成' % self.page)
            self.page += 1
            # 点击下一页,如果为 -1 说明不是最后1页
            if self.driver.page_source.find('pn-next disabled') == -1:
                self.driver.find_element_by_class_name('pn-next').click()
                time.sleep(3)
            else:
                break

if __name__ == '__main__':
    start = time.time()
    spider = JdSpider()
    spider.work_on()
    end = time.time()
    print('执行时间:%.2f' % (end-start))

# ￥28.70
# 拍拍
# 奇妙的爬虫 正版书籍 新华书店发货 二手99新
# 0条评价
# 古的旧书图书专营店
# **********************
# ￥97.50
# 包邮 玩转Django 2.0+玩转Python网络爬虫书籍 黄永祥 区域包邮基于Python3从零基础到项目实战书籍深入剖析Django2.0书籍
# 20+条评价
# 蓝墨水图书专营店






