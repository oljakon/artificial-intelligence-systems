import math


def euclidean(a, b):
    distance = 0
    for i in range(len(a)):
        distance += pow(a[i] - b[i], 2)
    return math.sqrt(distance)


def manhattan(a, b):
    distance = 0
    for i in range(len(a)):
        distance += abs(a[i] - b[i])
    return distance


tree_structure_parametric = [
    ['Професссиональные', 'Развивающие'],
    ['IT-сфера', 'Управление', 'Личностное развитие', 'Языковые курсы'],
    ['Программирование', 'Тестирование', 'Аналитика', 'Менеджмент', 'Маркетинг',
     'Речь', 'Управление временем', 'Изучение языка', 'Синхронный перевод'],
    ['Онлайн', 'Офлайн']
]
weights_parametric = [0.4, 0.3, 0.2, 0.1]


def parametric_tree_metric(t1, t2):
    diff = []
    for i in range(0, 4):
        try:
            diff.append(abs(tree_structure_parametric[i].index(t1[i]) - tree_structure_parametric[i].index(t2[i])))
        except ValueError:
            i += 1
    similarity = 0
    for i in range(len(diff)):
        similarity += diff[i] * weights_parametric[i]
    return similarity


tree_structure = [
    ['Професссиональные', 'Развивающие'],
    ['IT-сфера', 'Управление', 'Личностное развитие', 'Языковые курсы'],
    ['Программирование', 'Тестирование', 'Аналитика', 'Менеджмент', 'Маркетинг',
     'Речь', 'Управление временем', 'Изучение языка', 'Синхронный перевод'],
    ['Онлайн', 'Офлайн'],
    ['Группа', 'Чат', 'Индивидуально']
]
weights = [0.5, 0.4, 0.3, 0.2, 0.1]


def tree_metric(t1, t2):
    diff = []
    for i in range(0, 5):
        try:
            diff.append(abs(tree_structure[i].index(t1[i]) - tree_structure[i].index(t2[i])))
        except ValueError:
            i += 1
    similarity = 0
    for i in range(len(diff)):
        similarity += diff[i] * weights[i]

    numeric_diff = []
    numeric_diff.append(abs(t1[5] - t2[5]) * 0.1)
    numeric_diff.append(abs(t1[6] - t2[6]) * 0.1)
    numeric_diff.append(abs(t1[7] - t2[7]) * 0.1)

    for i in range(len(numeric_diff)):
        similarity += numeric_diff[i] * numeric_diff[i]

    return similarity


