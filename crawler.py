# coding: UTF-8
from bs4 import BeautifulSoup,SoupStrainer
import requests
import sys
from urllib.parse import urlparse
import os
import codecs
import re
import sqlite3
import time
import xmlhandle
host = 'http://gfw74.tk/'
class Spider_Model:
	def now(self):
		return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

	def GetPage(self,url):
		self.headers = dict()
		self.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
		self.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
		self.gg=1 
		while 1:
			self.s= requests.Session()
			try:
				self.ss = self.s.get(url,proxies = {"http":"http://127.0.0.1:8087",},headers=self.headers,timeout=19)
				self.ct = self.ss.headers['Content-Type']
				# print('Content-Type:',self.ct)
				if self.ct.find('text/html') ==-1:
					return 'no,data'
				return self.ss.content
			except Exception as e:
				self.errstr= str(e)
				print("GetPage error:",self.errstr)
				if self.errstr.find('HTTP Error 400') !=-1:
					return 'no,data'
				if self.gg>2:
					print("have try again , system exit")
					sys.exit(-1)
				print("2:......try again"+str(self.gg))
				time.sleep(2)
				self.gg=self.gg+1

	def GetList(self,page):
		self.url_list = []
		self.html = BeautifulSoup(page)
		self.dom = self.html.select("#ajaxtable .tr3 h3")
		# dom =html.find_all(style = "text-align:left;padding-left:8px" )//其他搜索文档方式
		self.con = sqlite3.connect("E:/note/python/python/crawler/db.sqlite3")
		self.cu = self.Connect_DB(self.con)
		self.num=0
		self.i =0
		for item in self.dom:
			category = item.find_previous(text=True).replace('[','').replace(']','').strip()
			title = item.a.get_text().strip()
			sub_url =item.a["href"]
			# print(category,title,sub_url)
			if self.i<5:
				if self.cu.execute('select sub_url from url_list where sub_url=?',(sub_url,)).fetchone()==None and len(category)==4:
					self.cu.execute('insert  into url_list values(?,?,?,?)',(category,title,sub_url,0))
					self.num=self.num+1
					print('%sinsert succeed'%title)
				else:
					self.i=self.i+1
					print('%salready exists'%title)
					continue
			else:
				print('超过%d条记录重复停止添加'%self.i)
				self.con.commit()
				self.cu.close()
				self.con.close()
				return -1
		self.con.commit()
		self.cu.close()
		self.con.close()
		return self.num

	def Connect_DB(self,con):
		self.tb = ('url_list',)
		if isinstance(con,sqlite3.Connection): #类型检查
			
			self.cu = con.cursor()
			self.tbl_list = self.cu.execute("SELECT tbl_name  FROM sqlite_master WHERE type='table'")
			if (self.tb not in self.tbl_list):
				self.cu.execute("CREATE TABLE url_list (category VARCHAR(10),title VARCHAR(30),sub_url VARCHAR(30),state_type INTEGER(1)) ")
				print('CREATE TABLE "url_list" succeed')
				return self.cu
			else:
				return self.cu
			print('connect DB is succeefully')
			
		else:
			print('ERRO:argument mast a "sqlite3.Connection"!')
			return
			
	def Get_Next_Page(self,html):
		# self.host = 'http://gfw74.tk/'
		if html!='no,data':
			self.html = BeautifulSoup(html)
			self.dom = self.html.select('.pages input')[0].find_previous('a').find_previous('a')
			self.num = int(self.dom.get_text())
			# print(self.num)
			self.link = host+self.dom['href'].replace('../../../','').replace('&page=%s'%self.num,'&page=')
			self.link_list = [self.link+str(n) for n in range(1,self.num+1)]
			print('获取分页列表成功共%d页'%len(self.link_list))
			return self.link_list
		else:
			print('没有数据，请检查网络和url是否正常')
			return

	def Get_Content(self,html):
		self.html = BeautifulSoup(html)
		self.contents = self.html.select('.tpc_content')
		self.content = [item.get_text() for item in self.contents if (len(item.get_text())>200)]
		return self.content
		
	def inser_book(self,con,str):
		self.cu = ss.Connect_DB(con)
		self.cu.execute('insert into mimimatica_category(category_name) select "{}" where not exists(select * from mimimatica_category where category_name="{}")'.format(str[1],str[1]))
		self.rowid = int(self.cu.execute('select category_id from mimimatica_category where category_name="{}"'.format(str[1])).fetchone()[0]) #获取category 主键
		
		if not self.cu.execute('select book_id from mimimatica_books where book_name="{}"'.format(str[2])).fetchone():
			self.cu.execute('insert into mimimatica_books(book_name,put_time,category_id) select "{}","{}","{}" where not exists(select * from mimimatica_books where book_name="{}")'.format(str[2],self.now(),self.rowid,str[2])).fetchone()
			# print(cu.execute('select typeof(1)'))
			self.book_id = int(self.cu.execute('select book_id from mimimatica_books where book_name="{}"'.format(str[2])).fetchone()[0]) #获取 book表主键
			print('insert book:"[{}]{}"OK,bookid:{}'.format(str[1],str[2],self.book_id))
			self.i = 1
			# xmlhandle.makeXmlTag('task.xml',category=str[1],category_id = self.rowid,book_id=self.book_id)
			for temp in self.content_generator(host+str[3]):
				# print('temp',temp)
				self.cu.execute('insert into mimimatica_content(book_id,put_time,content,content_title) values(?,?,?,?)',(self.book_id,self.now(),temp,'第{}章'.format(self.i)))
				print('获取第%d章成功'%self.i)
				self.i = self.i+1
			
			if self.i<=1:
				return -1
			else:
				con.commit()
				print('%s入库成功'%str[2])
				return 1
		else:
			print('记录"{}"已经存在'.format(str[2]))
			return 0

			

	def content_generator(self,url):
		self.article_list=ss.Get_Next_Page(ss.GetPage(url))#获取文章分页列表
		if self.article_list:
			for item in self.article_list:
				self.contents = ss.Get_Content(ss.GetPage(item))
				if self.contents:
					for temp in self.contents:
						yield(temp)
						
				else:
					print('之后内容为空停止遍历')
					return 
				print('sleep 10 S')
				time.sleep(10)
		else:
			print('获取数据失败')
			return 
		

	

if __name__ == '__main__':

	ss = Spider_Model()
	# html = ss.GetPage('http://gfw74.tk/thread0806.php?fid=20')
	# n=2
	# print('开始更新文章列表')
	# for url in ss.Get_Next_Page(html):
	# 	if n>0:
	# 		n=n+ss.GetList(ss.GetPage(url))
	# 		print('暂停5秒')
	# 		time.sleep(5)
	# 	else:
	# 		print('超过两页重复记录停止添加')
	# 		break
	# # article_list=ss.Get_Next_Page(ss.GetPage("http://cl.man.lv/htm_data/20/1409/1197832.html"))
	# # for item in article_list:
	# # 	print(ss.Get_Content(ss.GetPage(item)))
	# print('更新完成，更新%d篇文章，开始爬取正文'%n)
	con = sqlite3.connect("E:/note/python/python/crawler/db.sqlite3")
	cu = ss.Connect_DB(con)
	b= 0
	i=1
	while  i>0:
		sql = 'select rowid,category,title,sub_url from url_list where state_type=0 order by rowid desc limit {},{}'.format(b,5)
		book_info = cu.execute(sql).fetchall()
		b=b+1
		print (book_info)
		if not book_info:
			i = 0
			b=0
			print('没有更多记录，程序退出')
			continue
		for item in book_info:
			book_list = [item[0],item[1],item[2],item[3]]
			re =ss.inser_book(con,book_list)
			if re==1:
				cu.execute('update url_list set state_type= 1 where sub_url ="{}"'.format(item[3]))
				con.commit()
				print('插入成功')
			elif re==0:
				print('记录重复插入，开始下一条')
				cu.execute('update url_list set state_type= 1 where sub_url ="{}"'.format(item[3]))
				con.commit()
				continue
			elif re==-1:
				continue
			#cu.close()
		print('sleep 5 S')
		time.sleep(5)
		
	cu.close()
		






