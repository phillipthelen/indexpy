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
		self.loadConfig()
		self.bloginfo = dict(self.config.items("INFORMATION"))
		self.md = markdown.Markdown(output_format=self.config.get("TEMPLATE", "format"))
		self.form = cgi.FieldStorage()
		print "Content-type: text/html"
		if self.form.getvalue("rss") != None:
			template = open(self.config.get("TEMPLATE", "rssfile"))
			self.rssdom = parse(template);

			self.createRSS()

			print
			print self.rssdom.toxml().format(**self.bloginfo)
		else:
			template = open(self.config.get("TEMPLATE", "indexfile"))
			if self.form.getvalue("post") != None:
				content = self.getPost(self.form.getvalue("post"))
			else:
				content = self.listArticles()
			self.bloginfo["content"] = content
			templatestr = template.read()

			print
			print templatestr.format(**self.bloginfo)

	def createRSS(self):
		posts = sorted(os.listdir("content"), reverse=True)
		for post in posts:
			if post[-3:] == ".md":
				f = open("content/" + post)
				title = f.readline().strip()
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
				f.close()

	def loadConfig(self):
		self.config=ConfigParser.ConfigParser()
		name = "config.cfg"
		if os.path.isfile(name):
			# Config exists and gets opened
			configfile= open(name)
			self.config.readfp(configfile)
			self.config.read(configfile)
			configfile.close()

		else:
			print "Missing configfile"

	def listArticles(self):
		posts = sorted(os.listdir("content"), reverse=True)
		postlist = ""
		liststr = self.config.get("TEMPLATE", "listblock")
		for post in posts:
			if post[-3:] == ".md":
				itemstr = self.config.get("TEMPLATE", "listitem")
				f = open("content/" + post)
				title = f.readline().strip()
				postlist += ("\n" + itemstr.format(post=title, link=post[:-3]))
				f.close()
		return liststr.format(posts=postlist)

	def getPost(self, post):
		postfile = "content/{0}.md".format(post)
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
