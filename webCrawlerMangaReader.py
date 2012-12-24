__author__ = 'cifali dot filipe at gmail dot com'

''' # TODO #
Make a cleaner way to grab the first link, maybe re can help
Faster list usage, this list is a bit slow to be used
Create directory w/a cleaner name (w/o .html "attached")
Multiple headers may be used, build a list and randonize the usage
Learn more and more @_@"
'''

import os
import urllib2, urllib
from urllib import urlretrieve
from BeautifulSoup import BeautifulSoup

base_url   = 'http://mangareader.net' # it can be traded for http://mangapanda.com also.
target     = 'air-gear'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers    = {'User-Agent' : user_agent}
directory  = '/Users/filipecifalistangler/Downloads/manga/' # Where should be saved!
start_from = 350 # Start from what link?

url_chapters = []
list_url     = []
list_url2    = []

request  = urllib2.Request(base_url+'/'+target, headers = headers)
response = urllib2.urlopen(request)
document = response.read()
soup     = BeautifulSoup(document)
links    = soup.findAll('a')

for link in links:
    url_chapters.append(base_url+link['href'])

def listCreator(url, tag, attribute, array):
    
    # Global vars
    g_url = url
    g_request  = urllib2.Request(g_url, headers = headers)
    g_response = urllib2.urlopen(g_request)
    g_document = g_response.read()
    g_soup  = BeautifulSoup(g_document)
    g_links = g_soup.findAll('%s' %tag)

    for link in g_links:
        array.append(link['%s' %attribute])

def createDir(url):
    
    splited_name = url.split('/')
    dir_target   = directory+target+'/'
    dir_chapter  = dir_target+splited_name[-1]+'/'

    if not os.path.exists(dir_target):
        os.mkdir(dir_target)
    if not os.path.exists(dir_chapter):
        os.mkdir(dir_chapter)
    return dir_chapter

start_from += 20
final_urls = url_chapters[start_from:]
final = final_urls[:(len(final_urls)-8)]

for url in final:
    
    dir_target = createDir(url)
    list_url = []
    listCreator(url, 'option', 'value', list_url)
    
    for url2 in list_url:

        # get the images of pictures of manga
        list_url2 = []
        listCreator(base_url + url2, 'img', 'src', list_url2)

        # get the dir that the file are saved
        save_dir = os.path.join(dir_target, list_url2[-1].split('/')[-1])
        
        # case is downloading
        if not os.path.exists(save_dir):
            urlretrieve(list_url2[-1], save_dir)
            print list_url2[-1], "saved in:", save_dir
        # case already download
        elif int(urllib.urlopen(list_url2[-1]).info()['Content-Length']) == os.stat(save_dir).st_size:
            print list_url2[-1], "Already downloaded, skipping to next..."
        # problem with the download
        else:
            print "Online Length:", int(urllib.urlopen(list_url2[-1]).info()['Content-Length'])
            print "Local Length:", os.stat(save_dir).st_size
            urlretrieve(list_url2[-1], save_dir)
            print list_url2[-1], "downloading again, the size of the file differs from our."