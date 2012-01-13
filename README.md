About
=====

Index.py is a tiny blog system written in python. It loads markdown files from a folder and displays them as blogposts. It uses pythons built in CGI module.

---

Installation
============

You need the python-markdown module to install *index.py*.

The easiest way is to use easy\_install (easy\_install markdown).

You need to configure your webserver to accept *index.py* files as Indexfiles and it has to execute python code. Consult the documentation of your webserver to find out how to do so.

Then just clone the git repository into your webroot and it should work.

---

Configuration
=============

the configuration file has different options.

* indexfile - specifies where the templatefile is located.
* format - html-format that markdown will generate
* listblock - html code that is wrapped around the list of blogposts
* listitem - html code for the unique blogposts in the list.

everything after the *[INFORMATION]* tag can be edited freely and addet to the template as variable. p.e. you could add *licence = cc-by* to the config file and insert it via *{licence}*.

---

Usage
=====

You create a *.md* file in the *content* folder for each blogpost. The filename will make up the url for the post and is important for the order of the posts. So I recommend a system such as YYYY-MM-DD-INDEX-POSTNAME.md. Whereas you have to make sure that *POSTNAME* doesn't contain any characters, that aren't safe.

The first line of each file will be the Title of the blogpost when it's listed on the first page.

After that it's completely up to you, what you write. Be creative :)

**Important:** as *{}* are used as delimiters for template tags, you have to escape them through writing them two times. (*{{* and *}}* )

[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=viirus&url=https://github.com/vIiRuS/Indexpy&title=Index.py&language=de_DE&tags=github&category=software)