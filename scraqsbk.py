# -*- coding:utf-8 -*-
__author__='lrr'
import urllib
import urllib2
import re
import thread
import time
class qsbk:
	def __init__(self):
		self.pageIndex=1
		self.user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers={'User-Agent':self.user_agent}
		self.stories=[]
		self.enable=False
	def getPage(self,pageIndex):
		try:
			url='http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
			request=urllib2.Request(url,headers=self.headers)
			response=urllib2.urlopen(request)
			pageCode=response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError,e:
			if hasattr(e,'reason'):
				print u"糗事百科连接发生错误，reason:",e.reason
				return None
	def getPageItems(self,pageIndex):
		pattern=re.compile('h2>(.*?)</h2.*?content">(.*?)</div>(.*?)<div class="stats.*?number">(.*?)</',re.S)
		pageCode=self.getPage(pageIndex)
		if not pageCode:
			print "fail!"
			return None
		items=re.findall(pattern,pageCode)
		pageStories=[]
		for item in items:
			haveImg=re.search("img",item[2])
			if not haveImg:
				replace=re.compile('<br/>')
				content=re.sub(replace,"\n",item[0])
				pageStories.append([content.strip(),item[1].strip(),item[2].strip(),item[3].strip()])
		return pageStories
	def loadPage(self):
		if self.enable==True:
			if len(self.stories)<2:
				pageStories=self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex+=1
	def getOneStory(self,pageStories,page):
		print "page:%d"%page
		"""
		input=raw_input()
		if input=='Q':
			self.enable=False
			return
		print pageStories
		"""
		for story in pageStories:
			input=raw_input()
			#self.loadPage()
			if input=='Q':
				self.enable=False
				return
			print u"用户名：%s\n段子：\n%s\n%s点赞数：%s"%(story[0],story[1],story[2],story[3])
	def start(self):
		print u"阅读爬虫提取的糗事百科段子，Q退出"
		self.enable=True
		nowPage=0
		while self.enable:
			self.loadPage()
			if len(self.stories)>0:
				pageStories=self.stories[0]
				self.getOneStory(pageStories,nowPage)
				del self.stories[0]
				nowPage+=1
spider=qsbk()
spider.start()


























