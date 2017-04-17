#!/usr/bin/python3
# -*- coding: utf-8 -*-
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib.request
import sys
import os.path

class myContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.titulo_nuevo = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.html_nuevo = self.theContent
                BarraPunto.write("<li><a href='" + self.html_nuevo + "'>" +
                           self.titulo_nuevo + "</a></li>\n")
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog
# Load parser and driver
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

if os.path.exists("RSS.html"):
    BarraPunto = open("RSS.html", "w")
else:
    BarraPunto = open("RSS.html", "a")

url = "http://barrapunto.com/index.rss"
xmlFile = urllib.request.urlopen(url)
theParser.parse(xmlFile)

print("Parse complete")
