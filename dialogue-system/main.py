import pandas as pd
import pymorphy2

from parametric_search import parametric_search


morph = pymorphy2.MorphAnalyzer()
pd.set_option('display.max_columns', None)
pd.options.display.expand_frame_repr = False
step = 0
scenarios = -1

data = pd.read_csv('doc/courses.txt', delimiter=';')

attributes = [
    ["Направление курсов", "направление", "\nКакое направление?"],
    ["Сфера", "сфера", "\nКакаая сфера?"],
    ["Тема в сфере", "тема", "\nКакаая тема?"],
    ["Название", "название", "\nНапиши название"],
    ["Формат проведения", "формат", "\nОнлайн или офлайн?"],
    ["Кол-во отзывов", "популярность", "\nВведи диапазон количества отзывов на курс"],
    ["Средний рейтинг", "рейтинг", "\nВведи диапазон рейтинга курса"],
    ["Год выпуска", "год", "\nВведи год выхода курса"],
    ["Форма общения", "общение", "\nКак ты хочешь принимать участие в курсе?"],
]
selected_attributes = ''


def parser(s):
    phrase = s.lower().split()
    norm_phrase = list()
    for word in phrase:
        try:
            float(word)
            norm_phrase.append(word)
        except ValueError:
            norm_phrase.append(morph.parse(word)[0].normal_form)
    return norm_phrase


def handle(phrase):
    global step, scenarios, attributes, selected_attributes
    if len(set(phrase) & {'привет', 'добрый', 'приветствовать', 'здравствуй', 'здравствуйте'}) != 0:
        greeting()
        return

    if len(set(phrase) & {'спасибо', 'благодарить'}) != 0:
        you_are_welcome()
        return

    elif len(set(phrase) & {'пока', 'до свидания', 'нет', 'закончить', 'конец'}) != 0:
        print('\nДо встречи!')
        exit(0)

    if len(set(phrase) & {'сфера'}) != 0:
        print('\nТы можешь выбрать среди следующих сфер деятельности: ')
        if len(set(phrase) & {'профессиональный', 'профессия', 'работа'}) != 0:
            s = pd.Series(data[data['Направление курсов'] == 'Професссиональные']['Сфера'].unique())
            print(s)
        elif len(set(phrase) & {'развивающий', 'развитие', 'саморазвитие'}) != 0:
            s = pd.Series(data[data['Направление курсов'] == 'Развивающие']['Сфера'].unique())
            print(s)
        else:
            print(pd.Series(data['Сфера'].unique()))
        return

    if len(set(phrase) & {'тема'}) != 0:
        print('\nТы можешь выбрать среди следующих тем: ')
        if len(set(phrase) & {'айти', 'it', 'программирование', 'программист', 'аналитик'}) != 0:
            s = pd.Series(data[data['Сфера'] == 'IT-сфера']['Тема в сфере'].unique())
            print(s)
        elif len(set(phrase) & {'управление', 'менеджмент', 'менеджер', 'маркетинг', 'маркетолог'}) != 0:
            s = pd.Series(data[data['Сфера'] == 'Управление']['Тема в сфере'].unique())
            print(s)
        if len(set(phrase) & {'речь', 'время', 'развитие'}) != 0:
            s = pd.Series(data[data['Сфера'] == 'Личностное развитие']['Тема в сфере'].unique())
            print(s)
        elif len(set(phrase) & {'язык', 'переводить', 'переводчик', 'английский', 'немецкий', 'французский'}) != 0:
            s = pd.Series(data[data['Сфера'] == 'Языковые курсы']['Тема в сфере'].unique())
            print(s)
        else:
            print(pd.Series(data['Тема в сфере'].unique()))
        return

    elif (len(set(phrase) & {'какой', 'вывести', 'показать', 'покажи', 'написать', 'перечислить', 'список'}) != 0
          and len(set(phrase) & {'всё', 'все', 'перечень', 'каталог', 'список'}) != 0
          and len(set(phrase) & {'курс'}) != 0):
        show_all()
        return

    elif len(set(phrase) & {'случайный', 'рандомный', 'любой'}) != 0:
        show_random()
        return

    elif (len(set(phrase) & {'порекомендовать', 'рекомендовать', 'рекомендация', 'предложить'}) != 0
          and len(set(phrase) & {'курс'}) != 0):
        parametric_search()
        return

    elif len(set(phrase) & {'программировать', 'программирование', 'программист'}) != 0:
        if len(set(phrase) & {'не'}):
            print('Вот что мне удалось найти: ')
            if len(set(phrase) & {'python', 'питон', 'пайтон'}):
                courses = find_courses_with_exception('Программирование', 'Python')
                print(courses)
                more()
            elif len(set(phrase) & {'golang', 'Go', 'го', 'голанг', 'голэнг'}):
                courses = find_courses_with_exception('Программирование', 'Golang')
                print(courses)
                more()
        else:
            print('\nКакой язык программирования ты бы хотел изучить?')
            string = input('>>> ')
            if string == 'python' or string == 'питон' or string == 'пайтон':
                python_course = find_course_by_str('Python')
                if python_course.empty:
                    courses = find_theme('Программирование')
                    print('Удалось найти похожие курсы: ')
                    print(courses)
                    more()
                else:
                    print('Курсы по языку Python: ')
                    print(python_course)
                    more()
            elif string == 'golang' or string == 'Go' or string == 'го' or string == 'голанг' or string == 'голэнг':
                go_course = find_course_by_str('Golang')
                if go_course.empty:
                    courses = find_theme('Программирование')
                    print('Удалось найти похожие курсы: ')
                    print(courses)
                    more()
                else:
                    print('Курсы по языку Golang: ')
                    print(go_course)
                    more()
            elif string == 'c++' or string == 'си++' or string == 'плюс':
                c_course = find_course_by_str('C++')
                if c_course.empty:
                    courses = find_theme('Программирование')
                    print('Удалось найти похожие курсы: ')
                    print(courses)
                    more()
                else:
                    print('Курсы по языку C++: ')
                    print(c_course)
                    more()
            else:
                courses = find_theme('Программирование')
                print('Удалось найти похожие курсы: ')
                print(courses)
                more()
            return

    elif len(set(phrase) & {'c++', 'си++', 'плюс'}) != 0:
        go_course = find_course_by_str('C++')
        if go_course.empty:
            courses = find_theme('Программирование')
            print('Удалось найти похожие курсы: ')
            print(courses)
            more()
        else:
            print('Курсы по языку C++: ')
            print(go_course)
            more()
        return

    elif len(set(phrase) & {'python', 'питон', 'пайтон'}) != 0:
        go_course = find_course_by_str('Python')
        if go_course.empty:
            courses = find_theme('Программирование')
            print('Удалось найти похожие курсы: ')
            print(courses)
            more()
        else:
            print('Курсы по языку Python: ')
            print(go_course)
            more()
        return

    elif len(set(phrase) & {'golang', 'Go', 'го', 'голанг', 'голэнг'}) != 0:
        go_course = find_course_by_str('Golang')
        if go_course.empty:
            courses = find_theme('Программирование')
            print('Удалось найти похожие курсы: ')
            print(courses)
            more()
        else:
            print('Курсы по языку Golang: ')
            print(go_course)
            more()
        return

    elif len(set(phrase) & {'английский', 'англия', 'сша'}) != 0:
        eng_course = find_course_by_str('Английский')
        print('Курсы по английскому языку: ')
        print(eng_course)
        more()
        return

    elif len(set(phrase) & {'французский', 'франция'}) != 0:
        french_course = find_course_by_str('Французский')
        print('Курсы по французскому языку: ')
        print(french_course)
        more()
        return

    elif len(set(phrase) & {'немецкий', 'германия'}) != 0:
        german_course = find_course_by_str('Немецкий')
        print('Курсы по немецкому языку: ')
        print(german_course)
        more()
        return

    elif len(set(phrase) & {'язык', 'языковой', 'иностранный', 'переводчик', 'переводить'}) != 0:
        print('\nКакой иностранный язык ты бы хотел изучить?')
        string = input('>>> ')
        if string == 'английский' or string == 'англии' or string == 'сша':
            eng_course = find_course_by_str('Английский')
            if eng_course.empty:
                courses = find_theme('Изучение языка')
                print('Удалось найти похожие курсы: ')
                print(courses)
                more()
            else:
                print('Курсы по английскому языку: ')
                print(eng_course)
                more()
        elif string == 'французский' or string == 'френч' or string == 'франции' or string == 'голанг' or string == 'голэнг':
            french_course = find_course_by_str('Французский')
            if french_course.empty:
                courses = find_theme('Изучение языка')
                print('Удалось найти похожие курсы: ')
                print(courses)
                more()
            else:
                print('Курсы по французскому языку: ')
                print(french_course)
                more()
        elif string == 'немецкий' or string == 'германии':
            german_course = find_course_by_str('Немецкий')
            if german_course.empty:
                courses = find_theme('Изучение языка')
                print('Удалось найти похожие курсы: ')
                print(courses)
                more()
            else:
                print('Курсы по немецкому языку: ')
                print(german_course)
                more()
        else:
            courses = find_theme('Изучение языка')
            print('Удалось найти похожие курсы: ')
            print(courses)
            more()
        return

    elif len(set(phrase) & {'синхронный'}) != 0:
        print('Курсы по синхронному переводу: ')
        searched = data[data['Тема в сфере'] == 'Синхронный перевод']
        if len(set(phrase) & {'английский'}) != 0:
            searched_eng = searched[searched['Название'] == 'Английский']
            print(searched_eng)
        elif len(set(phrase) & {'немецкий'}) != 0:
            searched_german = searched[searched['Название'] == 'Немецкий']
            print(searched_german)
        else:
            print(searched)
        more()

    elif len(set(phrase) & {'анализировать', 'аналитик', 'данные', 'машинный'}) != 0:
        courses = find_theme('Аналитика')
        print('Курсы, связанные с аналитикой: ')
        print(courses)
        more()
        return

    elif len(set(phrase) & {'тестировать', 'тестирование', 'тестировщик'}) != 0:
        courses = find_theme('Тестирование')
        print('Курсы по изучению тестирования: ')
        print(courses)
        more()
        return

    elif len(set(phrase) & {'менеджмент', 'менеджер', 'управление', 'управлять', 'персонал'}) != 0:
        courses = find_theme('Менеджмент')
        print('Курсы, связанные с менеджментом: ')
        print(courses)
        more()
        return

    elif len(set(phrase) & {'выступать', 'говорить', 'сцена', 'конференция', 'театр', 'публика', 'речь'}) != 0:
        courses = find_theme('Речь')
        print('Курсы, связанные с развитием собственной речи: ')
        print(courses)
        more()
        return

    elif len(set(phrase) & {'время', 'ерунда', 'успевать', 'продуктивный', 'продуктивность', 'лень', 'лениться'}) != 0:
        courses = find_theme('Управление временем')
        print('Курсы, помогающие освоить тайм-менеджмент: ')
        print(courses)
        more()
        return

    elif len(set(phrase) & {'хобби', 'свободный', 'досуг', 'саморазвитие'}) != 0:
        print('Курсы для саморазвития: ')
        courses = data[data['Направление курсов'] == 'Развивающие']
        print(courses)
        more()
        return

    elif len(set(phrase) & {'популярный', 'известный'}) != 0:
        print('Курсы с наибольшим количеством отзывов: ')
        courses = sorted_courses('Кол-во отзывов', False)
        print(courses)
        more()
        return

    elif len(set(phrase) & {'лучший', 'понравиться', 'востребованный'}) != 0:
        print('Курсы с наибольшим рейтингом: ')
        courses = sorted_courses('Средний рейтинг', False)
        print(courses)
        more()
        return

    elif len(set(phrase) & {'новый'}) != 0:
        print('Курсы 2021 года: ')
        courses = data[data['Год выпуска'] == 2021]
        print(courses)
        more()
        return

    elif (len(set(phrase) & {'не'}) != 0
          and len(set(phrase) & {'проходить', 'изучать'})) != 0:
        print('Курсы, которые вы могли пропустить: ')
        courses = sorted_courses('Кол-во отзывов', True)
        print(courses)
        more()
        return

    elif (len(set(phrase) & {'какой', 'вывести', 'показать', 'покажи', 'написать', 'найти', 'искать', 'подсказать'}) != 0
          and len(set(phrase) & {'курс'}) != 0) or scenarios >= 3:
        if scenarios == -1:
            scenarios = 3

        if step == 0:
            print('\nТы ищешь конкретный курс или по какому-либо критерию?')
            string = input('>>> ')
            string_parser = parser(string)

            if 'конкретный' in string_parser:
                step = 2
                scenarios = 4
                print('\nКак он называется?')
                string = input('>>> ')
                step = 0
                scenarios = -1

                course = search_by_name(string)
                if course.empty:
                    not_found()
                else:
                    print(course)
                    more()
            elif 'критерий' in string_parser:
                step = 2
                scenarios = 5
                print('\nПо какому критерию?')
            else:
                step = 0
                scenarios = -1

                course = search_course(selected_attributes, string)
                if course == -1:
                    not_found()
                else:
                    print(course)
                    more()
            return
        elif step == 2:
            if scenarios == 5:
                attr = ''
                for i in range(len(attributes)):
                    if attributes[i][1].lower() in set(phrase):
                        attr = attributes[i][0]
                        selected_attributes = attributes[i][0]
                        print(attributes[i][2])
                        step = 3
                        scenarios = 5
                        # course = search_course(selected_attributes, string)
                if attr == '':
                    print('\nПовтори аттрибут еще раз, пожалуйста')
        elif step == 3:
            step = 0
            scenarios = -1

            if selected_attributes == 'Год выпуска':
                if len(phrase) == 1:
                    try:
                        year = int(phrase[0])
                        searched = search_course_by_year(year)
                    except ValueError:
                        invalid()
                        return
                else:
                    invalid()
                    return

            elif selected_attributes == 'Средний рейтинг':
                if len(phrase) == 2:
                    try:
                        min_rating = float(phrase[0])
                        max_rating = float(phrase[1])
                        searched = search_course_by_rating(min_rating, max_rating)
                    except ValueError:
                        invalid()
                        return
                else:
                    invalid()
                    return

            elif selected_attributes == 'Кол-во отзывов':
                if len(phrase) == 2:
                    try:
                        min_com = int(phrase[0])
                        max_com = int(phrase[1])
                        searched = search_course_by_comments(min_com, max_com)
                    except ValueError:
                        invalid()
                        return
                else:
                    invalid()
                    return

            else:
                searched = search_course(selected_attributes, phrase)
            if searched.empty:
                print('\nК сожалению, ничего не удалось найти')
            else:
                print(searched)
            more()
    else:
        not_found()


def search_by_name(phrase):
    phrase_list = phrase.split()

    for index, term in enumerate(phrase_list):
        if term == 'питон' or term == 'пайтон':
            phrase_list[index] = 'Python'
        elif term == 'го' or term == 'голанг' or term == 'голэнг':
            phrase_list[index] = 'Golang'
        elif term == 'си++' or term == 'плюс':
            phrase_list[index] = 'C++'

    phrase_list[0] = phrase_list[0].title()
    phrase = " ".join(phrase_list)
    searched = data[data['Название'].str.contains(phrase)]
    return searched


def search_course(column, phrase):
    phrase = " ".join(phrase)
    searched = data[data[column] == phrase.title()]
    return searched


def search_course_by_year(year):
    searched = data[data['Год выпуска'] == year]
    return searched


def search_course_by_rating(min_rating, max_rating):
    searched = data.loc[(data['Средний рейтинг'] >= min_rating) & (data['Средний рейтинг'] <= max_rating)]
    result = searched.sort_values(by='Средний рейтинг')
    return result


def search_course_by_comments(min_com, max_com):
    searched = data.loc[(data['Кол-во отзывов'] >= min_com) & (data['Кол-во отзывов'] <= max_com)]
    result = searched.sort_values(by='Кол-во отзывов')
    return result


def more():
    print('\nМогу ли я еще чем-нибудь помочь?')


def not_found():
    print('\nПрости, я не понимаю, что ты говоришь, повтори еще раз, пожалуйста')


def invalid():
    print('\nКажется, ты ввел некорректные данные. Давай попробуем еще раз')


def greeting():
    print('Привет! Чем могу помочь?')


def you_are_welcome():
    print('Всегда рад помочь :)')


def show_random():
    df = data.sample(n=1, random_state=0)
    print(df)


def show_all():
    print('\nВот что мне удалось найти:\n')
    print(data)


def find_theme(theme):
    searched = data[data['Тема в сфере'] == theme]
    return searched


def find_course_by_str(key_word):
    searched = data[data['Название'].str.contains(key_word)]
    return searched


def find_courses_with_exception(theme, exception):
    searched = data[data['Тема в сфере'] == theme]
    excepted = data[data['Название'].str.contains(exception)]
    result = searched[~searched.index.isin(excepted.index)]
    return result


def sorted_courses(column, asc_bool):
    result = data.sort_values(by=column, ascending=asc_bool)[:5]
    return result


def main():
    p = True
    while p:
        string = input('>>> ')
        print(string)
        norm_phrase = parser(string)
        print(norm_phrase)
        handle(norm_phrase)


if __name__ == "__main__":
    main()
