#/usr/bin/python3
# -*- coding: utf-8 -*-
# This module
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from vacancyparser.dbusage import *

base_url = 'https://jobs.tut.by'
start_url = base_url + '/employers_company/informacionnye_tekhnologii_sistemnaya_integraciya_internet'  # start page

list_re = [
    '^(/employers_company/informacionnye_tekhnologii_sistemnaya_integraciya_internet/page-)\d+$',  # for find next page
    '^(/employer/)\d+$',  # for current page
]

name_class = [
    'employers-company__pager',  # for next page
    'employers-company__list employers-company__list_companies',  # for current page
    'g-user-content',  #для получения описаний компаний
]

tablenames = [
    'company',
]


def getelement(url, name_class,
               string_re):  # Получаем на вход строку ссылки, строку имени класса тега, строку регулярки
    page = urlopen(url, timeout=3)  # open page
    bsObj = BeautifulSoup(page.read(), "html.parser")  # create BeautifulSoup Object
    container = bsObj.find('div', {'class': name_class})  # find div from BS Object
    obj_from_container = container.findAll('a', href=re.compile(string_re))  # find a href to next page or employer
    dictionary_employers = {}
    if name_class != 'employers-company__pager':    #если это поиск ссылок на компании
        for i in obj_from_container:
            dictionary_employers[i.get('href')] = i.get_text()#ключи - это ссылки, значения - название
    else:
        if obj_from_container[-1].get_text() == 'дальше':   #Если это поиск ссылки на след.страницу
            dictionary_employers['next_link'] = obj_from_container[-1].get('href')
    return dictionary_employers  # Возвращаем словарь найденных ссылок(из 1 элемента, если это ссылка на некст пэйдж)

def infocollection(url, name_class): #Функция для сбора описания о компании
    page = urlopen(url, timeout=3)
    bsObj = BeautifulSoup(page.read(), "html.parser")
    container = bsObj.find('div', {'class': name_class})
    if container == None:
        return ''
    obj_from_container = container.findAll('p', attrs={'class': None})
    description = ''
    for i in obj_from_container:
        description += i.get_text()
    return description

# def writeinfile(anydict):  # Пишем в файл словарь, который передадим в функцию.
#     with open('list employers.txt', 'a') as f:
#         for i in anydict:
#             f.write(i + '\n')
#             f.write(anydict[i] + '\n')
#         f.write('----------' + '\n')


def getemployers(table_name, base_url, url, name_class, list_re):  # Получаем строку имени таблицы, строку ссылки,
    # строку имени класса тега, строку регулярки
    dict_of_employers = getelement(url, name_class[1], list_re[1])  # Получаем ссылки на текущей странице
    infodict = {}
    for i in dict_of_employers:
        infodict['url'] = i
        infodict['name'] = dict_of_employers[i]
        infodict['description'] = infocollection(base_url+i, name_class[2])
        # writeinfile(infodict)  # Пишем всю инфу по одной в файл
        print(infodict)
        add_to_db(infodict, table_name)
    next_link = list(getelement(url, name_class[0], list_re[0]).values())  # Получаем следующую ссылку
    print(next_link)
    if len(next_link) > 0:
        getemployers(table_name=table_name, base_url=base_url, url=base_url + next_link[0], name_class=name_class,
                     list_re=list_re)  # Переходим по след.ссылке и начинаем работу заново
    else:
        pass  # Необязательно писать это, может в будущем чего-нибудь допишу. Пока мне нравится так, пусть будет.

if availability_check(tablenames[0]):
    create_table(tablenames[0])
getemployers(table_name=tablenames[0], base_url=base_url, url=start_url, name_class=name_class, list_re=list_re)
