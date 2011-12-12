__author__ = 'cifali dot filipe at gmail dot com'

import urllib2, urllib
from urllib import urlretrieve
import os
from BeautifulSoup import BeautifulSoup

# Configuration for downloads
base_url = 'http://mangareader.net' # The site, do NOT change it, if you don' know what you are doing!
target = 'air-gear' # Change to whatever manga you need :)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' # Let's fake a Firefox ;)
headers = { 'User-Agent' : user_agent } # Keep it trolling.
directory = '/Users/filipecifalistangler/Downloads/manga/' # Change to whatever directory you want to save everything.
startFrom = 338 # If the download should start from a precise chapter(default is 0, sometimes, -1 is needed, depending
# on the page itself and the links).

# Necessary lists for management of data
urlChapters = []
urlChapter = []
urlImage = []

request = urllib2.Request(base_url+'/'+target, headers = headers)
response = urllib2.urlopen(request)
document = response.read()
soup = BeautifulSoup(document) # BeautifulSoup parse HTML in a beautiful way :)
links = soup.findAll('a') # Now we make a list with all Links on the page of the manga

# New we make the list so we can later do a loop to get it all
for link in links:
    urlChapters.append(base_url+link['href'])

def downloadChapter(url):
    '''
    Creates the list of all links on the selected chapter so we can later parse the images.
    '''
    urlChap = url
    requestChap = urllib2.Request(urlChap, headers = headers)
    responseChap = urllib2.urlopen(requestChap)
    documentChap = responseChap.read()
    soupChap = BeautifulSoup(documentChap)
    linksChap = soupChap.findAll('option')  
    for link in linksChap:
        urlChapter.append(link['value'])

def downloadImage(url):
    '''
    Creates the list of all the URIs from the images, so we can later download them.
    '''
    urlImg = url
    requestImg = urllib2.Request(urlImg, headers = headers)
    responseImg = urllib2.urlopen(requestImg)
    documentImg = responseImg.read()
    soupImg = BeautifulSoup(documentImg)
    linksImg = soupImg.findAll('img')
    for link in linksImg:
        urlImage.append(link['src'])

def createDir(url):
    '''
    We need to check if the directory exists before trying to create them.
    '''
    name = url
    splitedName = name.split('/')
    dir = directory+target+'/'
    dirChapter = dir+splitedName[-1]+'/'
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(dirChapter):
        os.mkdir(dirChapter)
    return dirChapter

'''
A little "work-around" here, so we can "skip" non-related links and get only chapter links. The 20 first links are from
the header of the site, the last 8 are from the footer.
'''

startFrom += 20
finalUrls = urlChapters[startFrom:]
final = finalUrls[:(len(finalUrls)-8)]

# And then we do the loop.
for list in final:
    # Let's get a return so we can use as a save point for the file.
    dirTarget = createDir(list)
    urlChapter = []
    # We now get the list of urls from the Chapter and loop again inside them.
    downloadChapter(list)
    for urls in urlChapter:
        urlImage = []
        # Here we grab the image URI and create a complete URL
        downloadImage(base_url+urls)
        # Defines where it will be stored
        saveDir = os.path.join(dirTarget, urlImage[-1].split('/')[-1])
        if not os.path.exists(saveDir):
            # And so we download it!
            urlretrieve(urlImage[-1], saveDir)
            print urlImage[-1], "saved in:", saveDir
        else:
            # Check if the download it's a Zero-Sized / Broken file.
            if int(urllib.urlopen(urlImage[-1]).info()['Content-Length']) == os.stat(saveDir).st_size:
                # Let's not download again right?
                print urlImage[-1], "Already downloaded, skipping to next..."
            else:
                print "Online Length:", int(urllib.urlopen(urlImage[-1]).info()['Content-Length'])
                print "Local Length:", os.stat(saveDir).st_size
                urlretrieve(urlImage[-1], saveDir)
                print urlImage[-1], "downloading again, the size of the file differs from our."