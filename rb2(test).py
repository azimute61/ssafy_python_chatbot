# data = [
#     ['소고기조림', 'http://naver.com', '소고기 간장'],
#     ['소고기무국', 'http://naver.com', '소고기 무'],
#     ['소고기무침', 'http://naver.com', '소고기 간장 무']
# ]

emotion = {
    '기쁨':['간장 소고기'],
    '슬픔':['간장 무']
}

recipes = []

# recipe 입력 시 해당 음식 찾아서 출력
def recipe_title(recipe_name, data):
#    result_ = ["음식 이름 : %s\n" % (recipe_name)]
    result_= []
    for recipe in data:
#        print(recipe)
        if recipe_name in recipe[0]:
            result_.append([recipe[0], recipe[2], recipe[1]])

    return result_


# emotion 입력 시 해당 음식 추천
def recipe_emotion(emo, data):
    materials = emotion[emo][0].split()
    score = 0
    recipe_emotion = []

    for recipe in data:
        for material in materials:
            if material in recipe[2]:
                score += 1

        recipe_emotion.append([recipe[0], recipe[1], score, score / len(recipe[2].split(' '))])
        score = 0

    # 일치하는 항목 개수가 우선으로 정렬되어야 함 (일치 개수, 점수 정렬)
    recipe_emotion = sorted(recipe_emotion, key=lambda recipe_emotion: recipe_emotion[3], reverse=True)[0:10]
    return sorted(recipe_emotion, key=lambda recipe_emotion: recipe_emotion[2], reverse=True)[0:10]



# 재료 입력 시 음식 추천
def recipe_material(material_list, data):
    materials = material_list.split()

    score = 0
    recipe_score = []
#    print('데이터', data)
    for recipe in data:
        for material in materials:
#            print("레시피", len(recipe))
            if len(recipe) >= 3 and material in recipe[2]:
                # print(recipe[2], '/', material)
                score += 1

        # 레시피명, 링크, 점수, 일치율
        # if len(recipe >= 3):
        recipe_score.append([recipe[0], recipe[1], score, score/len(recipe[2].split(' '))])
        score = 0

#    return recipe_score
    return sorted(recipe_score, key=lambda recipe_score:recipe_score[3], reverse=True)[:10]

def input_recipe(recipe):
    line = recipe.read().split('\n')
    for i in line:
        if i != '':
            recipes.append(i.split(',', 2))

def print_title(recipe):
    for i in recipe:
        print(i)

def print_emotion(recipe):
    for i in recipe:
        print(i)

def print_material(recipe):
    for i in recipe:
        print(i)

recipe = open("C:/Users/student/Desktop/project/recipe_db.txt")

# 레시피 읽어오기
input_recipe(recipe)
# print(recipes)

# 음식명 입력하면 해당 음식 출력
# ex) 찌개, 탕, ....
print('\nTEST1')
print_title(recipe_title('두부', recipes))

# 재료 입력하면 해당 재료가 들어간 음식
# ex) 두부, 삼겹살, ...
print('\nTEST2')
print_material(recipe_material('두부 무', recipes))

# 감정을 선택하여 입력하면 해당 음식 출력
# ex) 슬픔, 기쁨, ...
print('\nTEST3')
print_emotion(recipe_emotion('슬픔', recipes))

recipe.close()