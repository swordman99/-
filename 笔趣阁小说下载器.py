from bs4 import BeautifulSoup
import requests,sys,os

URL=input('请输入小说的URL(以http://www.biquyun.com开头,例如http://www.biquyun.com/0_748/)：\n')
print("正在连接网站")
req=requests.get(url=URL)
req.encoding='GBK'
html=BeautifulSoup(req.text, features="html.parser")
temp_1=html.find_all('dd')
a=BeautifulSoup(str(temp_1), features="html.parser").find_all('a')
info=html.find_all('div', id='info')
temp_2=BeautifulSoup(str(info), features="html.parser")
book_title=temp_2.find_all('h1')[0].text
writer=temp_2.find_all('p')[0].text.replace('\xa0','')
with open('%s\\%s.txt'%(os.path.dirname(os.path.realpath(__file__)),book_title),'a',encoding='utf-8') as f:
	f.write(book_title+'\n'+writer+'\n')
print("正在下载 "+book_title,end=' ')
print(writer)
href=[]
title=[]
print("正在获取各章节网址及标题")
for i in range(len(a)):
	href.append('http://www.biquyun.com'+a[i].get('href'))
	title.append(a[i].text)
print('标题获取完成')
print('小说共%d章'%len(a))
i=0
while i < len(href):
	sys.stdout.write("正在下载第%d章内容"%(i+1)+'\r')
	sys.stdout.flush()
	URL_each=href[i]
	req=requests.get(url=URL_each)
	req.encoding='GBK'
	html_each=BeautifulSoup(req.text, features="html.parser")
	texts_each=html_each.find_all('div', id='content')
	if len(texts_each)>0:
		with open('%s\\%s.txt'%(os.path.dirname(os.path.realpath(__file__)),book_title),'a',encoding='utf-8') as f:
			f.write('\n'+title[i]+'\n'+texts_each[0].text.replace('\xa0',''))
		i=i+1
	else:
		pass
print('\n下载完成')
input()