import numpy as np
import pandas as pd
from distances import parametric_tree_metric


type = ['Професссиональные', 'Развивающие']
field = ['IT-сфера', 'Управление', 'Личностное развитие', 'Языковые курсы']
theme = ['Программирование', 'Тестирование', 'Аналитика', 'Менеджмент', 'Маркетинг', 'Речь',
                'Управление временем', 'Изучение языка', 'Синхронный перевод']
format = ['Онлайн', 'Офлайн']


def search_simular(search_dataset, type_search, field_serch, theme_serch, format_search):
    dfSearch = pd.DataFrame({'Направление курсов': [type_search],
                             'Сфера': [field_serch],
                             'Тема в сфере': [theme_serch],
                             'Формат проведения': [format_search]})

    func = parametric_tree_metric
    dataset = search_dataset
    print(find_similar_by_parametric_search(dataset, search_dataset, func, dfSearch).sort_values("Различие"))


def find_similar_by_parametric_search(ds, dataset, metric, dfSearch):
    r = []
    for i in range(len(ds.values.tolist())):
        r.append(metric(dfSearch.values.tolist()[0], ds.values.tolist()[i]))

    return pd.DataFrame(list(zip(r, map(lambda e: str("".join(e[3])), dataset.values.tolist()))),
                        index=np.arange(len(r)), columns=['Различие', 'Курс'])


if __name__ == '__main__':
    while True:
        type_search = int(input("Введите направление курсов:\n1 - Професссиональные\n2 - Развивающие\nВыбор:"))
        if type_search == 1:
            type_search = 'Професссиональные'
            break
        elif type_search == 2:
            type_search = 'Развивающие'
            break
        print("Вы ввели некорректные данные")

    while True:
        field_serch = int(input("Введите желаемую сферу:\n1 - IT-сфера\n2 - Управление\n3 - Личностное развитие\n4 - Языковые курсы\nВыбор:"))
        if field_serch == 1:
            field_serch = 'IT-сфера'
            break
        elif field_serch == 2:
            field_serch = 'Управление'
            break
        elif field_serch == 3:
            field_serch = 'Личностное развитие'
            break
        elif field_serch == 4:
            field_serch = 'Языковые курсы'
            break
        print("Вы ввели некорректные данные")

    while True:
        theme_serch = int(input("Выберите желаемую тему:\n1 - Программирование\n2 - Тестирование\n3 - Аналитика\n4 - "
                                "Менеджмент\n5 - Маркетинг\n6 - Речь\n7 - Управление временем\n8 - Изучение языка\n9 "
                                "- Синхронный перевод\nВыбор:"))
        if theme_serch == 1:
            theme_serch = 'Программирование'
            break
        elif theme_serch == 2:
            theme_serch = 'Тестирование'
            break
        elif theme_serch == 3:
            theme_serch = 'Аналитика'
            break
        elif theme_serch == 4:
            theme_serch = 'Менеджмент'
            break
        elif theme_serch == 5:
            theme_serch = 'Маркетинг'
            break
        elif theme_serch == 6:
            theme_serch = 'Речь'
            break
        elif theme_serch == 7:
            theme_serch = 'Управление временем'
            break
        elif theme_serch == 8:
            theme_serch = 'Изучение языка'
            break
        elif theme_serch == 9:
            theme_serch = 'Синхронный перевод'
            break
        print("Вы ввели некорректные данные")

    while True:
        format_search = int(input("Введите формат проведения курсов:\n1 - Онлайн\n2 - Офлайн\nВыбор:"))
        if format_search == 1:
            format_search = 'Онлайн'
            break
        elif format_search == 2:
            format_search = 'Офлайн'
            break
        print("Вы ввели некорректные данные")


    search_dataset = pd.read_csv('doc/courses.txt', delimiter=';', usecols=['Направление курсов', 'Сфера', 'Тема в сфере', 'Название', 'Формат проведения'])

    ds_searched_type = search_dataset[search_dataset["Направление курсов"] == type_search]
    ds_searched_field = ds_searched_type[ds_searched_type["Сфера"] == field_serch]
    ds_searched_theme = ds_searched_field[ds_searched_field["Тема в сфере"] == theme_serch]
    ds_searched_format = ds_searched_theme[ds_searched_theme["Формат проведения"] == format_search]
    print("\n")

    if ds_searched_format.empty:
        print("Нет курсов с заданными параметрами. Возможно вас заинтересуют: ")
        search_simular(search_dataset, type_search, field_serch, theme_serch, format_search)
    else:
        print("Результаты поиска: ")
        print(ds_searched_format)