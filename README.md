TITLE : 오늘 뭐 먹지
===========
Slack Chat Bot (PYTHON)
-----------
>FEATURES

#### 1. 음식 이름으로 레시피 찾기 

  1. COMMAND
    1. @bot_name 이름 레시피명
    
  2. RESULT
    1. ex) @bot_name 이름 감자
    2. ex) @bot_name 이름 치즈

#### 2. 특정 재료가 들어가는 음식 찾기

@bot_name 냉장고 재료1 재료2 ....

ex) @bot_name 냉장고 감자 치즈
ex) @bot_name 냉장고 김치

#### 3. 감정을 입력하여 음식 찾기

@bot_name 기분
@bot_name [행복, 우울, 분노, 슬픔, 기쁨, 스트레스]

ex) @bot_name 기분
response] bot_name> "*오늘 기분이 어때유???*\n행복 / 우울 / 분노 / 슬픔 / 기쁨 / 스트레스"
ex) @bot_name 분노

Documents
---------

#### 1. crawl.py

10000recipe.com 의 레시피 db를 크롤링하여 [지정된 파일]에 write해주는 파일

#### 2. rb2.py

서버없이 테스트환경을 조성하기 위해 함수를 작성하였던 dummy

#### 3. rb.py

crawl.py에
