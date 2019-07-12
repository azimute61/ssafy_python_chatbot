# -*- coding: utf-8 -*-
# 7-11 집에서 수정

import re
import urllib.request

from bs4 import BeautifulSoup

import math
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from slack.web.classes import extract_json
from slack.web.classes.blocks import *

# OAuth & Permissions로 들어가서
# Bot User OAuth Access Token을 복사하여 문자열로 붙여넣습니다
SLACK_TOKEN = 'input_yours'
# Basic Information으로 들어가서
# Signing Secret 옆의 Show를 클릭한 다음, 복사하여 문자열로 붙여넣습니다
SLACK_SIGNING_SECRET = 'input_yours'

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

# 데이터 형식
# data = [
#     ['소고기조림', 'http://naver.com', '소고기 간장'],
#     ['소고기무국', 'http://naver.com', '소고기 무'],
#     ['소고기무침', 'http://naver.com', '소고기 간장 무']
# ]

emotion = {
    '행복': ['쇠고기', '돼지고기', '닭고기'],
    '우울': ['요구르트', '우유', '시금치', '아메리카노', '헤이즐넛', '버섯', '연어'],
    '슬픔': ['바나나', '푸딩', '아이스크림', '참깨', '우유', '닭고기', '오리고기'],
    '분노': ['양파', '고추', '사과', '로즈마리', '감자'],
    '스트레스': ['대추', '단호박', '고구마', '초콜릿', '사과', '고등어', '당근', '블루베리'],
    '기쁨': ['간장, 소고기']
}

file_name = 'C:/Users/student/Desktop/project/recipe_db.txt'
recipes = []
result_num = 3


# recipe 입력 시 해당 음식 찾아서 출력
def recipe_title(recipe_name, data):
    # result_ = ["음식 이름 : %s\n" % (recipe_name)]
    result_ = []
    for recipe in data:
        if recipe_name in recipe[0]:
            result_.append([recipe[0], recipe[2], recipe[1], recipe[3]])

    return result_


# emotion 입력 시 해당 음식 추천
def recipe_emotion(emo, data):
    materials = emotion[emo][0].split()
    score = 0
    recipe_emotion = []

    # for recipe in data:
    #     for material in materials:
    #         if material in recipe[2]:
    #             score += 1
    #
    #     recipe_emotion.append([recipe[0], recipe[1], score, score, recipe[3]])
    #     score = 0

    # # 일치하는 항목 개수가 우선으로 정렬되어야 함 (일치 개수, 점수 정렬)
    # recipe_emotion = sorted(recipe_emotion, key=lambda recipe_emotion: recipe_emotion[3], reverse=True)[0:result_num]
    # return sorted(recipe_emotion, key=lambda recipe_emotion: recipe_emotion[2], reverse=True)


    # 레시피 리스트 하나 씩
    for recipe in data:
        total = recipe[2]
        test = 0

        # 유클리드 거리 계산
        # 입력받은 재료에서 하나 씩 가져옴
        for material in materials:
            for recipe_mat in recipe[2]:
 #               print(material, recipe_mat)
                if material in recipe_mat[0]:
                    score += 1
                    test += (1 - recipe_mat[1]) ** 2

        if test == 0:
            test = 100
        else:
            test = 1/math.sqrt(test)

        # 레시피명, 링크, 점수, 일치율, 이미지 주소, 재료, 유클리드 거리
        # recipe_score.append([recipe[0], recipe[1], score, score / len(recipe[2]), recipe[3], test])
        recipe_emotion.append([recipe[0], recipe[1], score, score, recipe[3], test])
        score = 0

    recipe_emotion = sorted(recipe_emotion, key=lambda recipe_score: recipe_score[5])[:result_num]

    # for i in recipe_score:
    #     print(i)
    return recipe_emotion

# 재료 입력 시 음식 추천
def recipe_material(material_list, data):
    materials = material_list.split()
    score = 0
    recipe_score = []

    # 레시피 리스트 하나 씩
    for recipe in data:
        total = recipe[2]
        test = 0

        # 유클리드 거리 계산
        # 입력받은 재료에서 하나 씩 가져옴
        for material in materials:
            for recipe_mat in recipe[2]:
 #               print(material, recipe_mat)
                if material in recipe_mat[0]:
                    score += 1
                    test += (1 - recipe_mat[1]) ** 2

        if test == 0:
            test = 100
        else:
            test = 1/math.sqrt(test)

        # 레시피명, 링크, 점수, 일치율, 이미지 주소, 재료, 유클리드 거리
        # recipe_score.append([recipe[0], recipe[1], score, score / len(recipe[2]), recipe[3], test])
        recipe_score.append([recipe[0], recipe[1], score, score, recipe[3], test])
        score = 0

    recipe_score = sorted(recipe_score, key=lambda recipe_score: recipe_score[5])[:result_num]

    # for i in recipe_score:
    #     print(i)
    return recipe_score


# 재료들 전처리
def div_material(recipe_line):
    mat_sum = []
    content = recipe_line
    con_div = []

    if '()' in content:
        con_temp = content.split('()')[2:]
        con_temp = con_temp[:len(con_temp) - 2]
        text = ''
        for i in range(1, len(con_temp), 2):
            text = con_temp[i - 1] + con_temp[i]
            con_div.append(text)
    else:
        if '.' in content:
            con_div = content.split('.')
        elif ',' in content:
            con_div = content.split(',')

    if con_div == []:
        con_temp =  content.split(' ')
        text = ''
        for i in range(1, len(con_temp), 2):
            text = con_temp[i - 1] + con_temp[i]
            con_div.append(text)

    print('con',con_div, content)
    if con_div != []:
        mat_sum.append(div_material_detail(con_div))

    return mat_sum

#상세하게 쪼개줌
def div_material_detail(material):
    # 파싱
    material2 = []
    for i, contents in enumerate(material):
        num = re.findall(r'\d+', contents.strip())

        # 점수
        if len(num) == 1:
            num = (int(num[0]) / (10 ** (len(num[0]) - 1)))

        elif len(num) == 2:
            if int(num[1]) != 0:
                num = (int(num[0]) / int(num[1]))
            else:
                #?
                num = int(num[0])

        else:
            num = 1 / len(material)

        material2.append([contents.strip(), num])

    total = 0
    for content in material2:
        total = total + content[1]

    for content in material2:
        content[1] = content[1]/total

#    print(material2)
#    print('')
    return material2


# 파일에서 읽은 레시피를 변수에 입력
def input_recipe(recipe):
    line = recipe.read().split('\n')

    for i in line:
        if i != '':
            recipes.append(i.split('<>', 4))

    # 재료에 점수를 매기기 위한 전처리 과정
    for index, i in enumerate(recipes):
        if i != '':
            text = i[2].replace('[재료]', '').replace('[주재료]', '')
            if '[양' in text:
                text = text[:text.index('[양')]

            # 재료 분할
            text = div_material(text)[0]
            recipes[index][2] = text

    for i in recipes:
        print('recipe', i)


# 채팅창에 출력해주는 함수
# print_title, print_material, print_emotion
def print_title(recipe):
    res = []
    for i in recipe:
        # 0 : 이름, 1 : 재료, 2 : 링크, 3 : 이미지 주소
        # res = res + "*<{2}|{0}>*\n재료 {1}\n\n".format(i[0], i[1], i[2])
        material_text = ""
        # 재료를 예쁘게 출력
        for text in i[1]:
#            print(text)
            material_text = material_text + text[0] + "\n"
#            print(material_text)

        img = ImageBlock(
            image_url=i[3],
            alt_text="test"
        )
        content = SectionBlock(
            fields=["*<{2}|{0}>*\n<들어가는 재료>\n {1}\n \n".format(i[0], material_text, i[2])]
        )

        res.append(img)
        res.append(content)

    return res


def print_material(recipe):
    res = []
    sum = 0
    count = 0

    for i in recipe:
        if(i[5]):
            sum = sum+ i[5]
            count += 1

    for i in recipe:
        # res = res + "*<{3}|{0}>*\n유사도 {1:0.2f}% / 일치하는 재료 {2}개\n\n".format(i[0], i[3]*100, i[2], i[1])
        if i[3]:
            img = ImageBlock(
                image_url=i[4],
                alt_text="test"
            )
            content = SectionBlock(
                fields=["*<{3}|{0}>*\n신뢰도 {4:0.2f}%\n일치재료 {2}개\n\n".format(i[0], i[3] * 100, i[2], i[1], (100-i[5]/sum * 100))]
            )

            res.append(img)
            res.append(content)

    return res


def print_emotion(recipe):
    res = []
    for i in recipe:
        # res = res + "{0}\n링크 {1}\n\n".format(i[0], i[1])
        if i[3]:
            img = ImageBlock(
                image_url=i[4],
                alt_text="test"
            )

            content = SectionBlock(
                fields=["*<{1}|{0}>*\n\n".format(i[0], i[1])]
            )

            res.append(img)
            res.append(content)

    return res


# 크롤링 함수 구현하기
def _crawl(text):
    # 여기에 함수를 구현해봅시다.

    # 1. 레시피 이름 검색
    if "이름" in text:
        # 음식명 입력하면 해당 음식 출력
        # ex) 찌개, 탕, ...
        message = print_title(recipe_title(text[text.index('이름') + 2:].strip(), recipes))
        print(message)

    # 2. 레시피 재료 검색
    elif "냉장고" in text:
        # 재료 입력하면 해당 재료가 들어간 음식
        # ex) 두부, 삼겹살, ...
        # print(text)
        # print(recipe_material(text[text.index('냉장고')+2:]))
        message = print_material(recipe_material(text[text.index('냉장고') + 3:].strip(), recipes))

    # 3. 레시피 감정 검색
    elif "기분" in text:
        # 감정을 선택하여 입력하면 해당 음식 출력
        # ex) 슬픔, 기쁨, ...
        # print('\nTEST3')

        message = [SectionBlock(
                fields=["*오늘 기분이 어때유???*\n행복 / 우울 / 분노 / 슬픔 / 기쁨 / 스트레스"]
        )]

    # 예외.
    else:
        message = []
        print("emo")
        # 3-2. 감정을 선택했을 경우
        for emo in emotion.keys():
            if emo in text:
                message = print_emotion(recipe_emotion(text[text.index(emo):].strip(), recipes))
        # print("error!!!@#!#")
        # message = [SectionBlock(
        #         fields=["에러야"]
        # )]

    return message


def read_recipe():
    recipe = open(file_name, encoding='utf-8')
    # 레시피 읽어오기
    input_recipe(recipe)
    recipe.close()
#    print(print_material(recipe_material('돼지 마늘', recipes)))


# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    message = _crawl(text)

    if message == []:
        message = [SectionBlock(fields=["검색된 레시피가 없거나 오류입니다."])]

    slack_web_client.chat_postMessage(
        channel=channel,
        blocks=extract_json(message)
    )
    # message = _crawl(text)
    # slack_web_client.chat_postMessage(
    #     channel=channel,
    #     text=message
    # )


# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    read_recipe()
    app.run('127.0.0.1', port=4040)
