# -*- coding: utf-8 -*-
import re
import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

def post_crawl():
    titles = []
    address = []
    material = []
    image = []

    for page in range(0, 10): #6710
        url = "http://www.10000recipe.com/recipe/list.html?order=reco&page=" + str(page)
        source_code = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(source_code, "html.parser")

        # 레시피 리스트 가져오기
        print('%d 리스트 가져오는 중' % (page))
        for title in soup.find_all("h4", class_="ellipsis_title2"):
            titles.append(title.getText().replace('\n', '').strip())

        #이미지 주소 가져오기
        for img in soup.find_all("a", class_="thumbnail"):
#            print(img.find_all("img")[1]['src'])
            image.append(img.find_all("img")[1]['src'])

        # 레시피 주소 가져오기
        print('주소 및 재료 가져오는 중')
        for add in soup.find_all("div", class_="col-xs-4"):
            input_add = add.find("a")['href']
#            print(input_add)
            if input_add.startswith('/'):
                address.append("https://www.10000recipe.com" + input_add)

                url_in = "https://www.10000recipe.com%s" %(input_add)
                source_code_in = urllib.request.urlopen(url_in).read()
                soup_in = BeautifulSoup(source_code_in, "html.parser")

                type = soup_in.find("div", class_='ready_ingre3')
                if type:
                    material.append(type.getText().replace('                                               ', '').replace('\n\n', '\n').replace('\n', '()').strip())
#                    print(type.getText().strip(), '\n')
                else:
                    material.append(soup_in.find("div", class_='cont_ingre').getText().replace('\n', '').strip())
#                    print(soup_in.find("div", class_='cont_ingre').getText().replace('\n', '').strip())


#    print(len(titles), len(address), len(material))
#     print(material)
    print('파일로 저장 중')
    recipe = open("C:/Users/student/Desktop/project/recipe_db.txt", 'w', encoding = 'utf-8')
    for i in range(len(titles)):
        print_ = titles[i] + "<>" + address[i] + "<>" + material[i] + "<>" + image[i]
        print(print_)
        recipe.write(print_+ '\n')

    recipe.close()

post_crawl()