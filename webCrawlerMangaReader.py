__author__ = 'filipecifalistangler'

import urllib2
from urllib import urlretrieve
import os
from BeautifulSoup import BeautifulSoup
from subprocess import call

base_url = 'http://mangareader.net'
target = 'air-gear'
request = urllib2.Request(base_url+'/'+target)
response = urllib2.urlopen(request)
document = response.read()
soup = BeautifulSoup(document)

links = soup.findAll('a')

urlChapters = []
urlChapter = []
urlImage = []

for link in links:
    urlChapters.append(base_url+link['href'])

def downloadChapter(url):
    urlChap = url
    requestChap = urllib2.Request(urlChap)
    responseChap = urllib2.urlopen(requestChap)
    documentChap = responseChap.read()
    soupChap = BeautifulSoup(documentChap)
    linksChap = soupChap.findAll('option')  
    for link in linksChap:
        urlChapter.append(link['value'])


def downloadImage(url):
    urlImg = url
    requestImg = urllib2.Request(urlImg)
    responseImg = urllib2.urlopen(requestImg)
    documentImg = responseImg.read()
    soupImg = BeautifulSoup(documentImg)
    linksImg = soupImg.findAll('img')
    for link in linksImg:
        urlImage.append(link['src'])

def createDir(url):
    name = url
    splitedName = name.split('/')
    dir = '/Users/filipecifalistangler/Downloads/'+target+'/'
    dirChapter = dir+splitedName[-1]+'/'
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(dirChapter):
        os.mkdir(dirChapter)
    return dirChapter

finalUrls = urlChapters[20:]
final = finalUrls[:(len(finalUrls)-8)]

for list in final:
    dirTarget = createDir(list)
    downloadChapter(list)
    for urls in urlChapter:
        downloadImage(base_url+urls)
        saveDir = os.path.join(dirTarget, urlImage[-1].split('/')[-1])
        if not os.path.exists(saveDir):
            urlretrieve(urlImage[-1], saveDir)
            print urlImage[-1], " saved in:", saveDir
        else:
            print urlImage[-1], "Already downloaded, skipping to next..."