#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CGI
import sys
sys.stderr = sys.stdout
import cgi, cgitb, os, subprocess, re, urllib2, datetime, platform
from time import time
from xml.dom.minidom import parse, parseString
import markdown
import ConfigParser
cgitb.enable()

class Index():

	def __init__(self):
		basefile = os.path.realpath(__file__)
		self.basepath = os.path.dirname(basefile) + "/"
		self.loadConfig()
		self.md = markdown.Markdown(output_format=self.config.get("TEMPLATE", "format"))
		self.form = cgi.FieldStorage()
		print "Content-type: text/html"
		if self.form.getvalue("rss") != None:
			template = open(self.basepath + self.config.get("TEMPLATE", "rssfile"))
			self.rssdom = parse(template);

			self.createRSS()

			print
			print self.rssdom.toxml().format(**self.bloginfo)
		else:
			template = open(self.basepath + self.config.get("TEMPLATE", "indexfile"))
			if self.form.getvalue("post") != None:
				content = self.getPost(self.form.getvalue("post"))
			else:
				content = self.listArticles()
			self.bloginfo["content"] = content
			templatestr = template.read()

			print
			print templatestr.format(**self.bloginfo)

	def createRSS(self):
		posts = sorted(os.listdir(self.basepath + "content"), reverse=True)
		for post in posts:
			if post[-3:] == ".md":
				f = open(self.basepath + "content/" + post)
				title = f.readline().strip()
				f.close()
				channel = self.rssdom.getElementsByTagName('channel')[0]
				itemelem = self.rssdom.createElement('item')
				channel.appendChild(itemelem)
				urlelem = self.rssdom.createElement('url')
				itemelem.appendChild(urlelem)
				urlstr = self.rssdom.createTextNode(self.bloginfo["url"] + '?post=' + post[:-3])
				urlelem.appendChild(urlstr)
				guidelem = self.rssdom.createElement('guid')
				itemelem.appendChild(guidelem)
				guidelem.appendChild(urlstr.cloneNode(False))
				titleelem = self.rssdom.createElement('title')
				itemelem.appendChild(titleelem)
				titlestr = self.rssdom.createTextNode(title)
				titleelem.appendChild(titlestr)
				authorelem = self.rssdom.createElement('author')
				itemelem.appendChild(authorelem)
				authorstr = self.rssdom.createTextNode(self.bloginfo["author"])
				authorelem.appendChild(authorstr)
				descriptionelem = self.rssdom.createElement('description')
				itemelem.appendChild(descriptionelem)
				contentstr = self.md.convert(f.read())
				descriptionstr = self.rssdom.createTextNode(contentstr)
				descriptionelem.appendChild(descriptionstr)
				

	def loadConfig(self):
		name = self.basepath + "config.cfg"
		if os.path.isfile(name):
			self.config=ConfigParser.ConfigParser()
			# Config exists and gets opened
			configfile= open(name)
			self.config.readfp(configfile)
			self.config.read(configfile)
			configfile.close()
			self.bloginfo = dict(self.config.items("INFORMATION"))
		else:
			print "Missing configfile"
			sys.exit()

	def listArticles(self):
		posts = sorted(os.listdir(self.basepath + "content"), reverse=True)
		postlist = ""
		liststr = self.config.get("TEMPLATE", "listblock")
		for post in posts:
			if post[-3:] == ".md":
				itemstr = self.config.get("TEMPLATE", "listitem")
				f = open(self.basepath + "content/" + post)
				title = f.readline().strip()
				f.close()
				postlist += ("\n" + itemstr.format(post=title, link=post[:-3]))
		return liststr.format(posts=postlist)

	def getPost(self, post):
		postfile = self.basepath + "content/{0}.md".format(post)
		validation = self.validateFile(postfile)
		if validation != None:
			return validation
		else:
			f = open(postfile)
			poststr = self.md.convert(f.read())
			f.close()
			return poststr.format(self.bloginfo)


	def validateFile(self, post):
		postpath = post.split("/")
		if ".." in postpath:
			print "\nStatus: 403 Forbidden"
			sys.exit()
		if not os.path.isfile(post):
			print "\nStatus: 404 Not Found"
			sys.exit()


if __name__ == '__main__':
	Index()
