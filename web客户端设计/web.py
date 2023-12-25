import datetime
import re
import time

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from requests_toolbelt.utils import dump

# 指定要访问的网站
# url = 'https://www.zhihu.com/'
url = 'http://www.aas.net.cn/zcustom/review'

# 设置自定义的HTTP头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
    # 发送GET请求
    response = requests.get(url, headers=headers)

    # 显示完整的HTTP请求和响应消息
    data = dump.dump_all(response)
    print("HTTP请求和响应消息:\n")
    
    print(data.decode('utf-8')[:3000])

    # 检查状态码是否为200
    if response.status_code == 200:
        print("\n\n请求成功！\n")

        # 生成动态文件名
        filename = f"downloaded_page_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        # 将网页内容保存到本地文件
        with open(filename, "w", encoding='utf-8') as file:
            file.write(response.text)
        print(f"网页已保存到本地: {filename}")

        # 显示部分HTML内容
        print("\n网页内容预览：")
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.prettify()[:300])  # 打印HTML

        savepath = "《自动化学报》优秀综述.xlsx"               #保存路径
        book = Workbook()                                       #创建工作簿
        sheet = book.worksheets[0]                             #创建工作表
        # TODO:
        sheet.append(["标题","作者","dio号","关键字","项目基金"])            #表头

        for page in range(1,7):                                       #翻页爬取
            form_data = {
                'journalId': '88888888',                                    #带入数据
                'url':'http://www.aas.net.cn/zcustom/review',
                'type': 'pichttp://www.aas.net.cn/fileZDHXB/journal/img/cover/27cc2081-86d9-4d9b-a3e0-4668b2280b35.jpg,http://www.aas.net.cn/fileZDHXB/cms/news/info/ffded5ed-c556-44ac-b09b-6d5ecbc60d77.png,http://www.aas.net.cn/fileZDHXB/cms/news/info/38724dca-018e-42bf-b828-4a5ae9b502c1.png,http://www.aas.net.cn/fileZDHXB/cms/news/info/8d73be68-5f26-4ab4-8efa-569cd2f05954.png,',  
                'imgs': 'http://www.aas.net.cn/fileZDHXB/cms/news/info/6dcda166-faf4-41c3-9251-a43818694ee0.jpg,http://www.aas.net.cn/fileZDHXB/cms/news/info/decdd555-6e2b-4bc0-9fd7-783a406566c8.png,http://www.aas.net.cn/fileZDHXB/cms/news/info/88b9e75f-89c2-4645-8da8-50a925311911.jpg,http://www.aas.net.cn/fileZDHXB/cms/news/info/3c76e102-8d51-4ef9-b002-67feef70c2f8.jpg',
                'page':page
                }
            
            baseurl = "http://www.aas.net.cn/zcustom/review"                  #指定URL
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
            html = requests.post(baseurl,data=form_data,headers=headers)            #post请求

            #print(html.text)
            #strhtml = str(html)
            strhtml = html.text
            pattern = r'<a href="(.+)" class="" target="_blank">(.+)</a>'              #正则表达式锁定每篇文章的超链接和标题
            result = re.findall(pattern,strhtml)                                   #正则匹配
            
            data = []                                                          #存储所有信息
            
            
            for item in result:
                perUrl, name = item
                #print(perUrl,name)                                              #测试爬取到的链接
                
                html2 = requests.post(perUrl,headers=headers)
                strhtml2 = html2.text
                #爬取标题
                pattern = r'<meta name="dc.title" content="(.+)" />'           #正则表达式锁定标题
                result = re.findall(pattern,strhtml2)
                data.append(result)
                
                #爬取作者
                pattern = r'<meta name="citation_authors"  content="(.+)" />'
                result = re.findall(pattern,strhtml2)
                data.append(result)
                
                #爬取dio号
                pattern = r'<meta name="citation_doi" content="(.+)"/>'
                result = re.findall(pattern,strhtml2)
                data.append(result)
                
                #爬取关键词
                pattern = r'<meta name="keywords" content="(.+)" />'
                result = re.findall(pattern,strhtml2)
                data.append(result)
                
                #爬取项目基金
                pattern = r'<div class="com-author-info"><b>基金项目:&nbsp;</b>(.+)</div>'
                result = re.findall(pattern,strhtml2)
                data.append(result)
            
            print(data)
            
            #轻点
            time.sleep(3)
            
            #保存数据

            print("保存中...") 

            for i in range(50):
                sheet.append(data[i]) 
                
        print('爬取完成')   
        book.save(savepath)

    else:
        print(f"请求失败，状态码：{response.status_code}, 原因：{response.reason}")

except requests.exceptions.RequestException as e:
    print(f"请求过程中出现异常：{e}")
