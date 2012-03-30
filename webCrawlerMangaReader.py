__author__ = 'cifali dot filipe at gmail dot com'

import urllib2, urllib
from urllib import urlretrieve
import os
from BeautifulSoup import BeautifulSoup

base_url = 'http://mangareader.net'
target = 'air-gear'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
directory = '/Users/filipecifalistangler/Downloads/manga/'
start_from = 330 # Start from what link?

url_chapters = []
list_url = []
list_url2 = []

request = urllib2.Request(base_url+'/'+target, headers = headers)
response = urllib2.urlopen(request)
document = response.read()
soup = BeautifulSoup(document)
links = soup.findAll('a')

for link in links:
    url_chapters.append(base_url+link['href'])

def ListCreator(url, type, grab, array):
    # Global vars
    g_url = url
    g_request = urllib2.Request(g_url, headers = headers)
    g_response = urllib2.urlopen(g_request)
    g_document = g_response.read()
    g_soup = BeautifulSoup(g_document)
    g_links = g_soup.findAll('%s' %type)
    for link in g_links:
        array.append(link['%s' %grab])

def CreateDir(url):
    name = url
    splited_name = name.split('/')
    dir = directory+target+'/'
    dir_chapter = dir+splited_name[-1]+'/'
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(dir_chapter):
        os.mkdir(dir_chapter)
    return dir_chapter

start_from += 20
final_urls = url_chapters[start_from:]
final = final_urls[:(len(final_urls)-8)]

for list in final:
    dir_target = CreateDir(list)
    list_url = []
    ListCreator(list, 'option', 'value', list_url)
    for urls in list_url:
        list_url2 = []
        ListCreator(base_url+urls, 'img', 'src',list_url2)
        save_dir = os.path.join(dir_target, list_url2[-1].split('/')[-1])
        if not os.path.exists(save_dir):
            urlretrieve(list_url2[-1], save_dir)
            print list_url2[-1], "saved in:", save_dir
        else:
            if int(urllib.urlopen(list_url2[-1]).info()['Content-Length']) == os.stat(save_dir).st_size:
                print list_url2[-1], "Already downloaded, skipping to next..."
            else:
                print "Online Length:", int(urllib.urlopen(list_url2[-1]).info()['Content-Length'])
                print "Local Length:", os.stat(save_dir).st_size
                urlretrieve(list_url2[-1], save_dir)
                print list_url2[-1], "downloading again, the size of the file differs from our."