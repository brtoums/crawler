# coding: UTF-8
from bs4 import BeautifulSoup,SoupStrainer
import urllib.request
from urllib.parse import urlparse
import os
import codecs
import re
import sqlite3
import time
import xmlhandle

class Spider_Model:
	def now(self):
		return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	
	def GetPage(self,url):
		self.myUrl = url
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
		self.headers = {'User_Agent':self.user_agent}
		self.proxy_support = urllib.request.ProxyHandler({"http":"http://127.0.0.1:8087"})
		self.opener = urllib.request.build_opener(self.proxy_support)
		urllib.request.install_opener(self.opener) 
		self.req = urllib.request.Request(self.myUrl,headers = self.headers)
<<<<<<< HEAD
		print("打开地址:‘%s’   。。。"%self.myUrl)
		xmlhandle.makeXmlTag('task.xml',clear = True,url=self.myUrl)
		self.myResponse = urllib.request.urlopen(self.req)
		self.myPage = self.myResponse.read()
		self.myResponse.close()
=======
		print("Open the url:‘%s’   。。。"%self.myUrl)
		# xmlhandle.makeXmlTag('task.xml',clear = True,url=self.myUrl)
		try:
			self.myResponse = urllib.request.urlopen(self.req)
		except Exception as e:
			print(e,'please Try again!')
		else:
			self.myPage = self.myResponse.read()
		finally:
			self.myResponse.close()
		
>>>>>>> 2b98abfe6c7703d4cde62dc0a1c17381bf0d0f69
		# print(type(self.myPage))
		# fileHandle =codecs.open ( "D:/note/python/crawler/test.txt", 'w' ,encoding='gb2312')
		# fileHandle .write(self.myPage.decode('gb2312', 'ignore'))
		# fileHandle.close()
<<<<<<< HEAD
		
=======
>>>>>>> 2b98abfe6c7703d4cde62dc0a1c17381bf0d0f69
		return self.myPage	



	def GetList(self,page):
		self.url_list = []
<<<<<<< HEAD
		self.html = BeautifulSoup(page)
		self.dom = self.html.select("#ajaxtable .tr3 h3")
		# dom =html.find_all(style = "text-align:left;padding-left:8px" )//其他搜索文档方式
		self.con = sqlite3.connect("D:/note/python/crawler/db.sqlite3")
=======
		self.host = 'http://cl.man.lv/'
		self.html = BeautifulSoup(page)
		self.dom = self.html.select("#ajaxtable .tr3 h3")
		# dom =html.find_all(style = "text-align:left;padding-left:8px" )//其他搜索文档方式
		self.con = sqlite3.connect("E:/note/python/python/crawler/db.sqlite3")
>>>>>>> 2b98abfe6c7703d4cde62dc0a1c17381bf0d0f69
		self.cu = self.Connect_DB(self.con)
		for item in self.dom:
			i =0
			category = item.find_previous(text=True).replace('[','').replace(']','').strip()
			title = item.a.get_text().strip()
			sub_url =item.a["href"]
			# print(category,title,sub_url)
			if self.cu.execute('select sub_url from url_list where sub_url=?',(sub_url,)).fetchone()==None:
<<<<<<< HEAD
				self.cu.execute('insert  into url_list values(?,?,?,?,?)',(category,title,sub_url,sub_url,0))
=======
				self.cu.execute('insert  into url_list values(?,?,?,?,?)',(category,title,self.host+sub_url,sub_url,0))
>>>>>>> 2b98abfe6c7703d4cde62dc0a1c17381bf0d0f69
				print('%sinsert succeed'%title)
			else:
				print('%salready exists'%title)
				continue

		self.con.commit()
		self.cu.close()
		self.con.close()
		return True


	def Connect_DB(self,con):
		self.tb = ('url_list',)
		if isinstance(con,sqlite3.Connection): #类型检查
			
			self.cu = con.cursor()
			self.tbl_list = self.cu.execute("SELECT tbl_name  FROM sqlite_master WHERE type='table'")
			if (self.tb not in self.tbl_list):
				self.cu.execute("CREATE TABLE url_list (category VARCHAR(10),title VARCHAR(30), url VARCHAR(30),sub_url VARCHAR(30),state_type INTEGER(1)) ")
				print('CREATE TABLE "url_list" succeed')
				return self.cu
			else:
				return self.cu
			print('connect DB is succeefully')
			
		else:
			print('ERRO:argument mast a "sqlite3.Connection"!')
			return
			
	def Get_Next_Page(self,html):
<<<<<<< HEAD
		self.html = BeautifulSoup(html)
		self.dom = self.html.select('.pages input')[0].find_previous('a').find_previous('a')
		self.num = int(self.dom.get_text())
		self.link = self.dom['href'].replace('../../../','').replace('&page=%s'%self.num,'&page=')
=======
		self.host = 'http://cl.man.lv/'
		self.html = BeautifulSoup(html)
		self.dom = self.html.select('.pages input')[0].find_previous('a').find_previous('a')
		self.num = int(self.dom.get_text())
		self.link = self.host+self.dom['href'].replace('../../../','').replace('&page=%s'%self.num,'&page=')
>>>>>>> 2b98abfe6c7703d4cde62dc0a1c17381bf0d0f69
		self.link_list = [self.link+str(n) for n in range(1,self.num+1)]
		print('获取分页列表成功')
		return self.link_list

	def Get_Content(self,html):
		self.html = BeautifulSoup(html)
		self.contents = self.html.select('.tpc_content')
		self.content = (item.get_text() for item in self.contents if (len(item.get_text())>200))
		return self.content
		
	def inser_book(self,con,str):
		self.cu = ss.Connect_DB(con)
<<<<<<< HEAD
		self.cu.execute('insert into mimimatica_category(category_name) select "{}" where not exists(select * from mimimatica_category where category_name="{}")'.format(str[1],str[1]))
		print('category:"{}"insert succeed!'.format(str[1]))
=======
		print(self.cu.execute('insert into mimimatica_category(category_name) select "{}" where not exists(select * from mimimatica_category where category_name="{}")'.format(str[1],str[1])))
		print('category_name:"{}"insert succeed!'.format(str[1]))
>>>>>>> 2b98abfe6c7703d4cde62dc0a1c17381bf0d0f69
		self.rowid = int(self.cu.execute('select category_id from mimimatica_category where category_name="{}"'.format(str[1])).fetchone()[0]) #获取category 主键
		self.cu.execute('insert into mimimatica_books(book_name,put_time,category_id) select "{}","{}","{}" where not exists(select * from mimimatica_books where book_name="{}")'.format(str[2],self.now(),self.rowid,str[2]))

		self.book_id = int(self.cu.execute('select book_id from mimimatica_books where book_name="{}"'.format(str[2])).fetchone()[0]) #获取 book表主键
		print('insert book:"{}"OK,bookid:{}'.format(str[2],self.book_id))
		self.i = 1
<<<<<<< HEAD
		for temp in self.content_generator(str[3]):
			self.cu.execute('insert into mimimatica_content(book_id,put_time,content,content_title) values(?,?,?,?)',(self.book_id,self.now(),temp,'第{}章'.format(self.i)))
=======
		xmlhandle.makeXmlTag('task.xml',category=str[1],category_id = self.rowid,book_id=self.book_id)
		for temp in self.content_generator(str[3]):
			# print('temp[1]',temp[0])
			self.cu.execute('insert into mimimatica_content(book_id,put_time,content,content_title) values(?,?,?,?)',(self.book_id,self.now(),temp[0],'第{}章'.format(self.i)))
>>>>>>> 2b98abfe6c7703d4cde62dc0a1c17381bf0d0f69
			self.i = self.i+1
			con.commit()

			

	def content_generator(self,url):
<<<<<<< HEAD
		self.host = 'http://www.zlvc.net/'
		self.article_list=ss.Get_Next_Page(ss.GetPage(self.host+url))#获取文章分页列表
		for item in self.article_list:
			self.contents = ss.Get_Content(ss.GetPage(self.host+item))
			for temp in self.contents:
				yield(temp)
=======
		self.article_list=ss.Get_Next_Page(ss.GetPage(url))#获取文章分页列表
		for item in self.article_list:
			self.contents = ss.Get_Content(ss.GetPage(item))
			for temp in self.contents:
				yield((temp,item))
>>>>>>> 2b98abfe6c7703d4cde62dc0a1c17381bf0d0f69
			print('sleep 5 S')
			time.sleep(5)
		
		

	

if __name__ == '__main__':

	ss = Spider_Model()
	# article_list=ss.Get_Next_Page(ss.GetPage("http://cl.man.lv/htm_data/20/1409/1197832.html"))
	# for item in article_list:
	# 	print(ss.Get_Content(ss.GetPage(item)))
<<<<<<< HEAD
	con = sqlite3.connect("D:/note/python/crawler/db.sqlite3")
=======
	con = sqlite3.connect("E:/note/python/python/crawler/db.sqlite3")
>>>>>>> 2b98abfe6c7703d4cde62dc0a1c17381bf0d0f69
	cu = ss.Connect_DB(con)
	b= 0
	i=True
	while i:
<<<<<<< HEAD
		sql = 'select rowid,category,title,sub_url from url_list aec limit {},{}'.format(b,5)
		book_info = cu.execute(sql).fetchall()
		b=b+1
		# print (book_info)
=======
		sql = 'select rowid,category,title,url from url_list desc limit {},{}'.format(b,5)
		book_info = cu.execute(sql).fetchall()
		b=b+1
		print (book_info)
>>>>>>> 2b98abfe6c7703d4cde62dc0a1c17381bf0d0f69
		if not book_info:
			i = False
			b=0
			print('没有更多记录，程序退出')
			continue
		for item in book_info:
			book_list = [item[0],item[1],item[2],item[3]]
			ss.inser_book(con,book_list)
			print('暂停5秒')
			time.sleep(5)
		con.commit()

		time.sleep(5)
	cu.close()
		






