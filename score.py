import re

material = []
material2 = []
mat_div = []

def input_recipe(recipe):
    line = recipe.read().split('\n')
    for i in line:
        if i != '':
            text = i.split('<>', 3)[2].replace('[재료]', '').replace('[주재료]', '')
            if '[양' in text:
                text = text[:text.index('[양')]

            material.append(text)
#            recipes.append(i.split('<>', 3))

def div_material(recipe):
    mat_sum = []

    for content in recipe:
        con_div = []
        if '()' in content:
            pass
        else:
            if '.' in content:
                con_div = content.split('.')
            elif ',' in content:
                con_div = content.split(',')

        if con_div != []:
            mat_sum.append(con_div)

    return mat_sum

recipe = open("C:/Users/student/Desktop/project/recipe_db.txt", encoding='utf-8')
# 레시피 읽어오기
input_recipe(recipe)
recipe.close()

material = div_material(material)

# 파싱
for i, contents in enumerate(material):
    row = []
    sum = 0
    for j, content in enumerate(contents):
        num = re.findall(r'\d+', content)

        if len(num) == 1:
            num = (int(num[0]) / (10**(len(num[0])-1)))

        elif len(num) == 2:
            num = (int(num[0]) / int(num[1]))

        if num != []:
            sum = sum + num
            row.append([content, num])

    for j in range(len(row)):
        row[j][1] = row[j][1]/sum

#    print(row,"@", sum)
    sum = 0
    material2.append(row)

for i in material2:
    pass
    # print(i)

#파싱한 재료를 가지고 계산
line1 = material2[0]
line2 = material2[4]

print(line1)
print(line2)

words = ['소금', '식초']

for word in words:
    for line in line1:
        if word in line[0]:
            print(word)
            print((1-line[1])**2)

    for line in line2:
        if word in line[0]:
            print(word)
            print((1-line[1])**2)
