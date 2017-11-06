#/usr/bin/python3
# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

base_url = 'https://jobs.tut.by'
start_url = base_url + '/employers_company/informacionnye_tekhnologii_sistemnaya_integraciya_internet' #start page


list_re = [
    '^(/employers_company/informacionnye_tekhnologii_sistemnaya_integraciya_internet/page-)\d+$', #for find next page
    '^(/employer/)\d+$' #for current page
]

name_class = [
    'b-pager__next', #for next page
    'employers-company__list employers-company__list_companies' #for current page
]

def getelement(url, name_class, string_re):
    page = urlopen(url, timeout=3)     #open page
    bsObj = BeautifulSoup(page.read(), "html.parser") #create BeautifulSoup Object
    container = bsObj.find('div', {'class': name_class})    #find div from BS Object
    obj_from_container = container.findAll('a', href=re.compile(string_re)) #find a href to next page or employer
    listofurls = []
    for i in obj_from_container:
        listofurls.append(i.get('href')) #get all urls
    return listofurls

def writeinfile(urllist):
    with open('list employers.txt', 'a') as f:
        for i in urllist:
            f.write('URL:' + '\n')
            f.write(i + '\n')
            f.write('----------' + '\n')

def getemployers(url, name_class, list_re):
    global base_url
    list_of_employers = getelement(url, name_class[1], list_re[1])
    writeinfile(list_of_employers)
    next_link = getelement(url, name_class[0], list_re[0])
    print(next_link)
    if len(next_link) > 0:
        getemployers(url=base_url + next_link[-1], name_class=name_class, list_re=list_re)
    else:
        pass

getemployers(url=start_url, name_class=name_class, list_re=list_re)
