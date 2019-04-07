from bs4 import BeautifulSoup
import requests
import sys
import os


URL = input('请输入小说的URL(例如http://www.biquyun.com/0_748/)：\n')
print("正在连接网站")
req = requests.get(url=URL)
location = str(req.text).find('charset=')
codef = str(req.text)[location + 8]
if codef == 'u':
    code = 'utf-8'
elif codef == 'G'or'g':
    code = 'GBK'
else:
    code = input('请输入网页编码格式（例如GBK）')
req.encoding = code
html = BeautifulSoup(req.text, features="html.parser")
# 生成文件路径
book_title = input('请输入书名')
writer = input('请输入作者名')
path_file = '%s\\%s.txt' % (os.path.dirname(
    os.path.realpath(__file__)), book_title)
with open(path_file, 'a', encoding='utf-8') as f:
    f.write(book_title + '\n' + writer + '\n')
print("正在下载 " + book_title, end=' ')
print(writer)
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
    href.append(str(URL + temp))
    title.append(a[i].text)
print('标题获取完成')
# 判断是否有“最新章节”，若有则去除重复
start = int(input('请输入小说开始章节（即去掉开头最新章节部分,若无就输入0）'))  # 过滤掉开始的重复部分
N_total = len(a) - start
print('小说共%d章' % N_total)
i = start
while i < len(href):
    sys.stdout.write("已下载%.3f%%" % ((i - start + 1) * 100 / N_total) + '\r')
    sys.stdout.flush()
    req = requests.get(url=href[i])
    req.encoding = code
    html_each = BeautifulSoup(req.text, features="html.parser")
    texts_each = html_each.find_all('div', id='content')
    if len(texts_each) > 0:
        temp_2 = texts_each[0].text.replace('\xa0', '\n')
        temp_2 = texts_each[0].text.replace('  ', '\n')
        temp_2 = texts_each[0].text.replace('　　', '\n')
        with open(path_file, 'a', encoding='utf-8') as f:
            f.write('\n' + title[i] + '\n' + temp_2)
        i = i + 1
    else:  # 防止应网络不畅通造成的错误
        pass
print('\n下载完成')
input()
