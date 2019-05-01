from bs4 import BeautifulSoup
import requests
import sys
import os


URL = input('请输入小说的URL(例如http://www.biquyun.com/0_748/)：\n')
print("正在连接网站")
req = requests.get(url=URL)
# 找到html中说明的编码格式
location = str(req.text).find('charset=')
codef = str(req.text)[location + 8]
if codef == 'u':
    code = 'utf-8'
elif codef == 'G'or'g':
    code = 'GBK'
else:
    code = input('请输入网页编码格式（例如GBK）：')  # 若没有找到编码格式
req.encoding = code
html = BeautifulSoup(req.text, features="html.parser")
# 生成文件路径
book_title = input('请输入书名：')
writer = input('请输入作者名：')
path_file = '%s\\%s.txt' % (os.path.dirname(
    os.path.realpath(__file__)), book_title)
with open(path_file, 'a', encoding='utf-8') as f:
    f.write(book_title + '\n' + writer + '\n')
print("正在下载：\n" + '书名：' + book_title + '作者名：' + writer)
# 查找章节名，章节链接
temp_1 = html.find_all('dd')
if len(temp_1) == 0:
    temp_1 = html.find_all('li')
    temp_1 = temp_1[11:]
a = BeautifulSoup(str(temp_1), features="html.parser").find_all('a')
href = []
title = []
print("正在获取各章节网址及标题")
for i in range(len(a)):
    temp = a[i].get('href')
    temp = temp.split('/')
    temp = temp[-1].replace('\n', '')
    href.append(str(URL.replace('index.html', '') + temp))
    title.append(a[i].text)
print('标题获取完成')
# 判断是否有“最新章节”，若有则去除重复
start = input('请输入小说开始章节（即去掉开头最新章节部分,\
默认值为0）：')  # 过滤掉开始的重复部分
if start != '':
    start = int(start)
else:
    start = 0
N_total = len(a) - start
print('小说共%d章' % N_total)
i = start
j = 0
while i < len(href):
    sys.stdout.write("已下载%.3f%%" % ((i - start + 1) * 100 / N_total) + '\r')
    sys.stdout.flush()
    req = requests.get(url=href[i])
    req.encoding = code
    html_each = BeautifulSoup(req.text, features="html.parser")
    texts_each = html_each.find_all('div', id='content')
    # 清理空格
    if len(texts_each) > 0 and texts_each[0].text[1:6] != '正在加载中':
        with open(path_file, 'a', encoding='utf-8') as f:
            f.write('\n' + title[i] + '\n' +
                    '\n'.join(texts_each[0].text.split()))
        i = i + 1
    else:  # 防止应网络不畅通造成的错误
        j = j + 1
        if j > 10:
            print('网络连接中断或网站被封,跳过此章节')
            print(title[i])
            print(href[i])
            j = 0
            i = i + 1
        pass
print('\n下载完成')
input()
