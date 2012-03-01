__author__ = 'cifali dot filipe at gmail dot com'

import urllib2, urllib
from urllib import urlretrieve
import os
from BeautifulSoup import BeautifulSoup

base_url = 'http://mangareader.net'
target = 'one-piece' # Change to whatever manga you need :)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
directory = '/Users/filipecifalistangler/Downloads/manga/'
startFrom = 0 # If the download should start from a precise chapter(default is 0, sometimes, -1 is needed, depending
# on the page itself and the links).

urlChapters = []
listUrl = []
listUrl2 = []

request = urllib2.Request(base_url+'/'+target, headers = headers)
response = urllib2.urlopen(request)
document = response.read()
soup = BeautifulSoup(document)
links = soup.findAll('a')

for link in links:
    urlChapters.append(base_url+link['href'])

def listCreator(url, type, grab):
    gUrl = url
    grequest = urllib2.Request(gUrl, headers = headers)
    gresponse = urllib2.urlopen(grequest)
    gdocument = gresponse.read()
    gsoup = BeautifulSoup(gdocument)
    glinks = gsoup.findAll('%s' %type)
    for link in glinks:
        if type == 'option':
            listUrl.append(link['%s' %grab])
        else:
            listUrl2.append(link['%s' %grab])

def createDir(url):
    name = url
    splitedName = name.split('/')
    dir = directory+target+'/'
    dirChapter = dir+splitedName[-1]+'/'
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(dirChapter):
        os.mkdir(dirChapter)
    return dirChapter

startFrom += 20
finalUrls = urlChapters[startFrom:]
final = finalUrls[:(len(finalUrls)-8)]

for list in final:
    dirTarget = createDir(list)
    listUrl = []
    listCreator(list, 'option', 'value')
    for urls in listUrl:
        listUrl2 = []
        listCreator(base_url+urls, 'img', 'src')
        saveDir = os.path.join(dirTarget, listUrl2[-1].split('/')[-1])
        if not os.path.exists(saveDir):
            urlretrieve(listUrl2[-1], saveDir)
            print listUrl2[-1], "saved in:", saveDir
        else:
            # Check if the download it's a Zero-Sized / Broken file.
            if int(urllib.urlopen(listUrl2[-1]).info()['Content-Length']) == os.stat(saveDir).st_size:
                print listUrl2[-1], "Already downloaded, skipping to next..."
            else:
                print "Online Length:", int(urllib.urlopen(listUrl2[-1]).info()['Content-Length'])
                print "Local Length:", os.stat(saveDir).st_size
                urlretrieve(listUrl2[-1], saveDir)
                print listUrl2[-1], "downloading again, the size of the file differs from our."