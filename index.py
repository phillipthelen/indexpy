#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CGI
import sys
sys.stderr = sys.stdout
import cgi, cgitb, os, subprocess, re, urllib2, datetime, platform
from time import time
import markdown
import ConfigParser
cgitb.enable()

class Index():

	def __init__(self):
		self.loadConfig()
		self.bloginfo = dict(self.config.items("INFORMATION"))
		template = open(self.config.get("TEMPLATE", "indexfile"))
		self.md = markdown.Markdown(output_format=self.config.get("TEMPLATE", "format"))
		self.form = cgi.FieldStorage()
		print "Content-type: text/html"
		if self.form.getvalue("post") != None:
			content = self.getPost(self.form.getvalue("post"))
		else:
			content = self.listArticles()
		self.bloginfo["content"] = content
		templatestr = template.read()
		
		print
		print templatestr.format(**self.bloginfo)
				
	def loadConfig(self):
		name = "config.cfg"
		if os.path.isfile(name):
			self.config=ConfigParser.ConfigParser()
			# Config exists and gets opened
			configfile= open(name)
			self.config.readfp(configfile)
			self.config.read(configfile)
			configfile.close()
								
		else:
			print "Missing configfile"
			sys.exit()

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