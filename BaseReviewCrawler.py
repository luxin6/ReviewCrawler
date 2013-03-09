#encoding=utf-8
from bs4 import BeautifulSoup
from DictUnicodeWriter import DictUnicodeWriter
import codecs
import csv
import os
import socket
import urllib2
import urllib
from twisted.internet import reactor,defer
from twisted.web.client import getPage

TIMEOUT = 20
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.91 Safari/537.11"
}

class BaseReviewCrawler:
    def __init__(self,url):
        self.title = ""
     
    def writeToCSV(self,dataL,title):
        if len(dataL)==0:
            return
        print "writeToCSV"
        fieldnames = ['id','reviewContent', 'reviewTime', 'degree','userNick', 'userId','userLink','appendId','appendReview','appendTime']
        #dict_writer = csv.DictWriter(codecs.open(title+".csv", "w","utf-8"), fieldnames=fieldnames)
    #   dict_writer.writerow(fieldnames) # CSV??????????????????
        fname = "CSV/"+title.decode("utf-8")+".csv"
        new = False
        if not os.path.exists(fname):
            new = True
        f = open(fname,'a')
        dict_writer = DictUnicodeWriter(f,fieldnames,delimiter="\t")
        if new:
            dict_writer.writeheader()
        dict_writer.writerows(dataL)  # rows??????????????????
        dataL=[]
        f.close()

    def getPageFromUrl(self,url,params = None,timeout=20,coding=None):
        try:
            socket.setdefaulttimeout(timeout)
            if params:
                #print params
                req = urllib2.Request(url=url, data=urllib.urlencode(params), headers=headers)
            else:
                req = urllib2.Request(url=url,headers=headers)
            response = urllib2.urlopen(req)
            if coding is None:
                coding= response.headers.getparam("charset")
            if coding is None:
                page=response.read()
                print "coding = None"
            else:
                page=response.read()
                page=page.decode(coding).encode('utf-8')
                print "coding = %s"%coding
            return page       
        except Exception,e:
            print e
            print "try again"
            return self.getPageFromUrl(url,params,timeout,coding)

    def crawlReviews(self,url,timeout=20,coding=None):
      #  try:
            #socket.setdefaulttimeout(timeout)
            req = urllib2.Request(url=url,headers = headers)
            response = urllib2.urlopen(req)
            if coding is None:
                coding= response.headers.getparam("charset")
            if coding is None:
                page=response.read()
            else:
                page=response.read()
                page=page.decode(coding).encode('utf-8')
            #print response.url
            self.getReviewsInPage(url,page)         
       # except Exception,e:
       #     print e
       
    def generateReviewUrl(self,prefix,params):
        for key in params.keys():
            prefix=prefix+"%s=%s"%(key,params[key])+"&"
        return str(prefix[:-1])

    def getItemTitle(self,soup):
        raise NotImplementedException

    def crawlQueryParams(self,soup):
        raise NotImplementedException

    def getReviewsFromPage(self,title,params):
        raise NotImplementedException

    def parseReviewJson(self,info,cp):
        raise NotImplementedException

    def crawl(self,url):
        print url
        page = self.getPageFromUrl(url)
        soup = BeautifulSoup(page)
        self.title = self.getItemTitle(soup)
        print self.title.decode("utf-8").encode("gb2312")
        params = self.crawlQueryParameters(soup)
        print params
        self.getReviewsFromPage(self.title,params)
        #reactor.run()
        # self.writeToCSV(title,dataList)

    def getPageError(self,content,url):
        print "Error! url=%s"%url        
        print content
        #return defer.returnValue(getPage(url,timeout=TIMEOUT))
        return

    def writeJsonToFile(self,jsondata,path,name):
        import json
        path = path.strip("/").decode("utf-8")
        if not os.path.exists(path):
            os.mkdir(path)
        with codecs.open(path+"/"+str(name)+".json","w",'utf-8') as outfile:
            outfile.write(unicode(json.dumps(jsondata,ensure_ascii=False)))
        
