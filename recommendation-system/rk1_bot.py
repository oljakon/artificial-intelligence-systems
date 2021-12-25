import telebot
from telebot import types
import pandas as pd
import numpy as np

token = TOKEN_API

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    key_list = types.InlineKeyboardButton(text='Показать список всех курсов', callback_data="courses_list")
    keyboard.add(key_list)
    key_filt = types.InlineKeyboardButton(text='Подобрать себе курс по параметрам', callback_data="courses_filter")
    keyboard.add(key_filt)
    bot.send_message(message.from_user.id, "Привет ✌️\nЧем я могу помочь?", reply_markup=keyboard)


courses_dataset_search = pd.read_csv(
    'doc/courses.txt',
    delimiter=';',
    usecols=['Направление курсов', 'Сфера', 'Тема в сфере', 'Название', 'Формат проведения']
)

likes = ''
dislikes = ''

courses_tree = [
    ['Професссиональные', 'Развивающие'],
    ['IT-сфера', 'Управление', 'Личностное развитие', 'Языковые курсы'],
    ['Программирование', 'Тестирование', 'Аналитика', 'Менеджмент', 'Маркетинг',
     'Речь', 'Управление временем', 'Изучение языка', 'Синхронный перевод'],
    ['Онлайн', 'Офлайн']
]
weights = [0.4, 0.3, 0.2, 0.1]


def diff_tree(t1, t2):
    diff = []
    for i in range(0, 4):
        try:
            diff.append(abs(courses_tree[i].index(t1[i]) - courses_tree[i].index(t2[i])))
        except ValueError:
            i += 1
    similarity = 0
    for i in range(len(diff)):
        similarity += diff[i] * weights[i]
    return similarity

# courses_tree = [
#     ['Професссиональные', 'Развивающие'],
#     ['IT-сфера', 'Управление', 'Личностное развитие', 'Языковые курсы'],
#     ['Программирование', 'Тестирование', 'Аналитика', 'Менеджмент', 'Маркетинг',
#      'Речь', 'Управление временем', 'Изучение языка', 'Синхронный перевод'],
#     ['Онлайн', 'Офлайн'],
#     ['Группа', 'Чат', 'Индивидуально']
# ]
# weights = [0.5, 0.4, 0.3, 0.2, 0.1]

# def diff_tree(t1, t2):
#     diff = []
#     for i in range(0, 5):
#         print(i)
#         try:
#             diff.append(abs(courses_tree[i].index(t1[i]) - courses_tree[i].index(t2[i])))
#         except ValueError:
#             i += 1
#     similarity = 0
#     for i in range(len(diff)):
#         similarity += diff[i] * weights[i]
#
#     numeric_diff = []
#     numeric_diff.append(abs(t1[5] - t2[5]) * 0.1)
#     numeric_diff.append(abs(t1[6] - t2[6]) * 0.1)
#     numeric_diff.append(abs(t1[7] - t2[7]) * 0.1)
#
#     for i in range(len(numeric_diff)):
#         similarity += numeric_diff[i] * numeric_diff[i]
#
#     return similarity
#

def search_simular():
    dfSearch = pd.DataFrame({'Направление курсов': [type_choice],
                             'Сфера': [field],
                             'Тема в сфере': [theme],
                             'Формат проведения': [format]})

    func = diff_tree
    dataset = courses_dataset_search
    return find_similar_by_parametric_search(dataset, courses_dataset_search, func, dfSearch).sort_values("Различие")


def find_similar_by_parametric_search(ds, dataset, metric, dfSearch):
    r = []
    for i in range(len(ds.values.tolist())):
        r.append(metric(dfSearch.values.tolist()[0], ds.values.tolist()[i]))

    return pd.DataFrame(list(zip(r, map(lambda e: str("".join(e[3])), dataset.values.tolist()))),
                        index=np.arange(len(r)), columns=['Различие', 'Курс'])


def find_similar_for_one_course(ds, dataSet, metric, serial_number):
    r = []
    for i in range(len(ds.values.tolist())):
        r.append(metric(ds.values.tolist()[serial_number], ds.values.tolist()[i]))

    return pd.DataFrame(list(zip(r, map(lambda e: str("   ".join(e[-1:])),
                                        dataSet.values.tolist()))), index=np.arange(len(r)),
                        columns=['Различие', 'Курс'])


def find_similar_for_liked_courses(ds, data, metric, likes, dislikes, message):
    liked = []
    if len(likes) > 0:
        for k in likes:
            liked.append(np.array(find_similar_for_one_course(ds, data, metric, k)['Различие']))

    most_related = pd.DataFrame()
    r = []
    for k in range(len(ds.values.tolist())):
        if len(likes) > 0:
            tt = np.sum([np.array(find_similar_for_one_course(ds, data, metric, k)['Различие']),
                         np.average(liked, 0)], 0)

        most_related = most_related.append(
            {"id": np.argmin(tt),
             "Характеристики": " ".join(list(map(str, data.values.tolist()[np.argmin(tt)]))),
             "Разница": np.amin(tt)}, ignore_index=True)
        r.append(tt)

    most_related = most_related.drop_duplicates(subset='id', keep="last")
    idx = most_related.index
    for k in dislikes:
        if k in idx:
            most_related = most_related.drop(k)
    most_related = most_related.sort_values('Разница')

    most_related = most_related.sort_values('Разница')
    courses_list_counter = 0
    for x in most_related.values.tolist():
        if courses_list_counter == 5:
            break
        courses_list_counter = courses_list_counter + 1
        str1 = x[1] + '\n'
        bot.send_message(message.chat.id, str(courses_list_counter) + " " + str1)
    return r


def get_likes(message):
    global likes
    likes = message.text
    bot.register_next_step_handler(message, get_dislikes)
    bot.send_message(message.from_user.id, "Введи номера курсов, которые тебе не понравились")


def get_dislikes(message):
    global dislikes
    global likes
    dataSetFromTxt = pd.read_csv('doc/courses.txt', delimiter=';')
    ds = dataSetFromTxt.copy(deep=True)
    dislikes = message.text
    func = diff_tree

    ds["Направление курсов"], _ = pd.factorize(ds["Направление курсов"])
    ds["Сфера"], _ = pd.factorize(ds["Сфера"])
    ds["Тема в сфере"], _ = pd.factorize(ds["Тема в сфере"])
    ds["Название"], _ = pd.factorize(ds["Название"])
    ds["Формат проведения"], _ = pd.factorize(ds["Формат проведения"])
    ds["Кол-во отзывов"], _ = pd.factorize(ds["Кол-во отзывов"])
    ds["Средний рейтинг"], _ = pd.factorize(ds["Средний рейтинг"])
    ds["Год выпуска"], _ = pd.factorize(ds["Год выпуска"])
    ds["Форма общения"], _ = pd.factorize(ds["Форма общения"])

    likes = np.fromstring(likes, dtype=int, sep=' ')
    likes = [x - 1 for x in likes]
    dislikes = np.fromstring(dislikes, dtype=int, sep=' ')
    dislikes = [x - 1 for x in dislikes]
    find_similar_for_liked_courses(ds, dataSetFromTxt, func, likes, dislikes, message)

    keyboard = types.InlineKeyboardMarkup()
    key_list = types.InlineKeyboardButton(text='Показать список всех курсов', callback_data="courses_list")
    keyboard.add(key_list)
    key_filt = types.InlineKeyboardButton(text='Подобрать курс по параметрам', callback_data="courses_filter")
    keyboard.add(key_filt)
    key_like = types.InlineKeyboardButton(text='Оценить курсы', callback_data="courses_like")
    keyboard.add(key_like)
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global type_choice
    global field
    global theme
    global format
    if call.data == "courses_list":
        dataSetSearch = pd.read_csv(
            'doc/courses.txt',
            delimiter=';',
            usecols=['Направление курсов', 'Сфера', 'Тема в сфере', 'Название', 'Формат проведения']
        )
        columns_titles = ['Направление курсов', 'Сфера', 'Тема в сфере', 'Название', 'Формат проведения']
        dataSetSearch = dataSetSearch.reindex(columns=columns_titles)

        courses_list_counter = 0
        for x in dataSetSearch.values.tolist():
            courses_list_counter = courses_list_counter + 1
            str1 = x[3] + "\n" + "Направление курсов: " + x[0] + "\n" + "Сфера: " + x[1] + "\n" + \
                   "Тема в сфере: " + x[2] + "\n" + "Формат проведения: " + x[4]
            bot.send_message(call.message.chat.id, str(courses_list_counter) + ". " + str1)
        keyboard = types.InlineKeyboardMarkup()
        key_list = types.InlineKeyboardButton(text='Показать список всех курсов', callback_data="courses_list")
        keyboard.add(key_list)
        key_filt = types.InlineKeyboardButton(text='Подобрать курс по параметрам', callback_data="courses_filter")
        keyboard.add(key_filt)
        key_like = types.InlineKeyboardButton(text='Оценить курсы', callback_data="courses_like")
        keyboard.add(key_like)
        bot.send_message(call.message.chat.id, "Что дальше?", reply_markup=keyboard)
    elif call.data == "courses_like":
        bot.send_message(call.message.chat.id, "Введи номера понравившихся курсов через пробел")
        bot.register_next_step_handler(call.message, get_likes)
    elif call.data == "courses_filter" or call.data == "filt_no":
        keyboard = types.InlineKeyboardMarkup()
        type_prof = types.InlineKeyboardButton(text='Профессиональные', callback_data="prof")
        keyboard.add(type_prof)
        type_hobby = types.InlineKeyboardButton(text='Развивающие', callback_data="hobby")
        keyboard.add(type_hobby)
        type_f = types.InlineKeyboardButton(text='Неважно', callback_data="n1")
        keyboard.add(type_f)
        if call.data == "courses_filter":
            bot.send_message(call.message.chat.id, 'Подбор курсов по параметрам')
        elif call.data == "filter_no":
            bot.send_message(call.message.chat.id, 'Попробуем еще раз')
        bot.send_message(call.message.chat.id, 'Выберите направление развития', reply_markup=keyboard)
    elif call.data == "prof":
        type_choice = "Професссиональные"
        keyboard = types.InlineKeyboardMarkup()
        it_field = types.InlineKeyboardButton(text='IT-сфера', callback_data="it")
        keyboard.add(it_field)
        price_l = types.InlineKeyboardButton(text='Управление', callback_data="manage")
        keyboard.add(price_l)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n3")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите сферу курсов', reply_markup=keyboard)
    elif call.data == "hobby":
        type_choice = "Развивающие"
        keyboard = types.InlineKeyboardMarkup()
        it_field = types.InlineKeyboardButton(text='Личностное развитие', callback_data="personal")
        keyboard.add(it_field)
        price_l = types.InlineKeyboardButton(text='Языковые курсы', callback_data="language")
        keyboard.add(price_l)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n3")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите сферу курсов', reply_markup=keyboard)
    elif call.data == "n1":
        type_choice = "nil"
        print(type_choice)
        keyboard = types.InlineKeyboardMarkup()
        it_field = types.InlineKeyboardButton(text='IT-сфера', callback_data="it")
        keyboard.add(it_field)
        price_l = types.InlineKeyboardButton(text='Управление', callback_data="manage")
        keyboard.add(price_l)
        it_field = types.InlineKeyboardButton(text='Личностное развитие', callback_data="personal")
        keyboard.add(it_field)
        price_l = types.InlineKeyboardButton(text='Языковые курсы', callback_data="language")
        keyboard.add(price_l)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n3")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите сферу курсов', reply_markup=keyboard)
    elif call.data == "n3":
        field = "nil"
        keyboard = types.InlineKeyboardMarkup()
        progr = types.InlineKeyboardButton(text='Программирование', callback_data="progr")
        keyboard.add(progr)
        testing = types.InlineKeyboardButton(text='Тестирование', callback_data="testing")
        keyboard.add(testing)
        analytic = types.InlineKeyboardButton(text='Аналитика', callback_data="analytic")
        keyboard.add(analytic)
        management = types.InlineKeyboardButton(text='Менеджмент', callback_data="management")
        keyboard.add(management)
        marketing = types.InlineKeyboardButton(text='Маркетинг', callback_data="marketing")
        keyboard.add(marketing)
        speach = types.InlineKeyboardButton(text='Речь', callback_data="speach")
        keyboard.add(speach)
        time = types.InlineKeyboardButton(text='Управление временем', callback_data="time")
        keyboard.add(time)
        lang = types.InlineKeyboardButton(text='Изучение языка', callback_data="lang")
        keyboard.add(lang)
        syn = types.InlineKeyboardButton(text='Синхронный перевод', callback_data="syn")
        keyboard.add(syn)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n4")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите тему курсов в выбранной сфере', reply_markup=keyboard)
    elif call.data == "it":
        field = "IT-сфера"
        keyboard = types.InlineKeyboardMarkup()
        progr = types.InlineKeyboardButton(text='Программирование', callback_data="progr")
        keyboard.add(progr)
        testing = types.InlineKeyboardButton(text='Тестирование', callback_data="testing")
        keyboard.add(testing)
        analytic = types.InlineKeyboardButton(text='Аналитика', callback_data="analytic")
        keyboard.add(analytic)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n4")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите тему курсов в выбранной сфере', reply_markup=keyboard)
    elif call.data == "manage":
        field = "Управление"
        keyboard = types.InlineKeyboardMarkup()
        management = types.InlineKeyboardButton(text='Менеджмент', callback_data="management")
        keyboard.add(management)
        marketing = types.InlineKeyboardButton(text='Маркетинг', callback_data="marketing")
        keyboard.add(marketing)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n4")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите тему курсов в выбранной сфере', reply_markup=keyboard)
    elif call.data == "personal":
        field = "Личностное развитие"
        keyboard = types.InlineKeyboardMarkup()
        speach = types.InlineKeyboardButton(text='Речь', callback_data="speach")
        keyboard.add(speach)
        time = types.InlineKeyboardButton(text='Управление временем', callback_data="time")
        keyboard.add(time)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n4")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите тему курсов в выбранной сфере', reply_markup=keyboard)
    elif call.data == "language":
        field = "Личностное развитие"
        keyboard = types.InlineKeyboardMarkup()
        lang = types.InlineKeyboardButton(text='Изучение языка', callback_data="lang")
        keyboard.add(lang)
        syn = types.InlineKeyboardButton(text='Синхронный перевод', callback_data="syn")
        keyboard.add(syn)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n4")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите тему курсов в выбранной сфере', reply_markup=keyboard)
    elif call.data == "n4":
        theme = "nil"
        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton(text='Онлайн', callback_data="online")
        keyboard.add(online)
        offline = types.InlineKeyboardButton(text='Офлайн', callback_data="offline")
        keyboard.add(offline)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n5")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите формат проведения курсов', reply_markup=keyboard)
    elif call.data == "progr":
        theme = "Программирование"
        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton(text='Онлайн', callback_data="online")
        keyboard.add(online)
        offline = types.InlineKeyboardButton(text='Офлайн', callback_data="offline")
        keyboard.add(offline)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n5")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите формат проведения курсов', reply_markup=keyboard)
    elif call.data == "testing":
        theme = "Тестирование"
        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton(text='Онлайн', callback_data="online")
        keyboard.add(online)
        offline = types.InlineKeyboardButton(text='Офлайн', callback_data="offline")
        keyboard.add(offline)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n5")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите формат проведения курсов', reply_markup=keyboard)
    elif call.data == "analytic":
        theme = "Аналитика"
        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton(text='Онлайн', callback_data="online")
        keyboard.add(online)
        offline = types.InlineKeyboardButton(text='Офлайн', callback_data="offline")
        keyboard.add(offline)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n5")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите формат проведения курсов', reply_markup=keyboard)
    elif call.data == "management":
        theme = "Менеджмент"
        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton(text='Онлайн', callback_data="online")
        keyboard.add(online)
        offline = types.InlineKeyboardButton(text='Офлайн', callback_data="offline")
        keyboard.add(offline)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n5")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите формат проведения курсов', reply_markup=keyboard)
    elif call.data == "marketing":
        theme = "Маркетинг"
        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton(text='Онлайн', callback_data="online")
        keyboard.add(online)
        offline = types.InlineKeyboardButton(text='Офлайн', callback_data="offline")
        keyboard.add(offline)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n5")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите формат проведения курсов', reply_markup=keyboard)
    elif call.data == "speach":
        theme = "Речь"
        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton(text='Онлайн', callback_data="online")
        keyboard.add(online)
        offline = types.InlineKeyboardButton(text='Офлайн', callback_data="offline")
        keyboard.add(offline)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n5")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите формат проведения курсов', reply_markup=keyboard)
    elif call.data == "time":
        theme = "Управление временем"
        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton(text='Онлайн', callback_data="online")
        keyboard.add(online)
        offline = types.InlineKeyboardButton(text='Офлайн', callback_data="offline")
        keyboard.add(offline)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n5")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите формат проведения курсов', reply_markup=keyboard)
    elif call.data == "lang":
        theme = "Изучение языка"
        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton(text='Онлайн', callback_data="online")
        keyboard.add(online)
        offline = types.InlineKeyboardButton(text='Офлайн', callback_data="offline")
        keyboard.add(offline)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n5")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите формат проведения курсов', reply_markup=keyboard)
    elif call.data == "syn":
        theme = "Синхронный перевод"
        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton(text='Онлайн', callback_data="online")
        keyboard.add(online)
        offline = types.InlineKeyboardButton(text='Офлайн', callback_data="offline")
        keyboard.add(offline)
        price_f = types.InlineKeyboardButton(text='Неважно', callback_data="n5")
        keyboard.add(price_f)
        bot.send_message(call.message.chat.id, 'Выберите формат проведения курсов', reply_markup=keyboard)
    elif call.data == "online":
        format = "Онлайн"
        keyboard = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton(text='Да', callback_data="filt_yes")
        keyboard.add(yes)
        no = types.InlineKeyboardButton(text='Нет', callback_data="filt_no")
        keyboard.add(no)
        bot.send_message(call.message.chat.id,
                         'Вы выбрали –\nНаправление курсов: ' + type_choice + '\nСфера: ' + field
                         + '\nТема в сфере: ' + theme + '\nФормат проведения: ' + format
                         + '\nПродолжить с выбранными параметрами?', reply_markup=keyboard)
    elif call.data == "offline":
        format = "Офлайн"
        keyboard = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton(text='Да', callback_data="filt_yes")
        keyboard.add(yes)
        no = types.InlineKeyboardButton(text='Нет', callback_data="filt_no")
        keyboard.add(no)
        bot.send_message(call.message.chat.id,
                         'Вы выбрали –\nНаправление курсов: ' + type_choice + '\nСфера: ' + field
                         + '\nТема в сфере: ' + theme + '\nФормат проведения: ' + format
                         + '\nПродолжить с выбранными параметрами?', reply_markup=keyboard)
    elif call.data == "n5":
        format = "nil"
        keyboard = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton(text='Да', callback_data="filt_yes")
        keyboard.add(yes)
        no = types.InlineKeyboardButton(text='Нет', callback_data="filt_no")
        keyboard.add(no)
        bot.send_message(call.message.chat.id,
                         'Вы выбрали –\nНаправление курсов: ' + type_choice + '\nСфера: ' + field
                         + '\nТема в сфере: ' + theme + '\nФормат проведения: ' + format
                         + '\nПродолжить с выбранными параметрами?', reply_markup=keyboard)
    elif call.data == "filt_yes":
        search_dataset = pd.read_csv('doc/courses.txt', delimiter=';',
                                     usecols=['Направление курсов', 'Сфера', 'Тема в сфере', 'Название',
                                              'Формат проведения'])

        print(type_choice, field, theme, format)
        if type_choice != "nil":
            ds_searched_type = search_dataset[search_dataset["Направление курсов"] == type_choice]
        else:
            ds_searched_type = search_dataset

        if field != "nil":
            ds_searched_field = ds_searched_type[ds_searched_type["Сфера"] == field]
        else:
            ds_searched_field = ds_searched_type

        if theme != "nil":
            ds_searched_theme = ds_searched_field[ds_searched_field["Тема в сфере"] == theme]
        else:
            ds_searched_theme = ds_searched_field

        if format != "nil":
            ds_searched_format = ds_searched_theme[ds_searched_theme["Формат проведения"] == format]
        else:
            ds_searched_format = ds_searched_theme

        if ds_searched_format.empty:
            bot.send_message(call.message.chat.id, "Нет курсов с заданными параметрами. Возможно заинтересуют:")
            courses_array = search_simular().values.tolist()
            courses_list_counter = 0
            for x in courses_array:
                if courses_list_counter == 5:
                    break
                courses_list_counter = courses_list_counter + 1
                str1 = x[1] + '\n'
                bot.send_message(call.message.chat.id, str(courses_list_counter) + ". " + str1)
            keyboard = types.InlineKeyboardMarkup()
            key_list = types.InlineKeyboardButton(text='Показать список всех курсов',
                                                  callback_data="courses_list")
            keyboard.add(key_list)
            key_filt = types.InlineKeyboardButton(text='Подобрать курс по параметрам', callback_data="courses_filter")
            keyboard.add(key_filt)
            bot.send_message(call.message.chat.id, "Что дальше?", reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, "Результаты поиска")
            columns_titles = ['Направление курсов', 'Сфера', 'Тема в сфере', 'Название', 'Формат проведения']
            dataSetSearch = ds_searched_format.reindex(columns=columns_titles)

            courses_list_counter = 0
            for x in dataSetSearch.values.tolist():
                courses_list_counter = courses_list_counter + 1
                str1 = x[3] + "\n" + "Направление курсов: " + x[0] + "\n" + "Сфера: " + x[1] + "\n" + \
                   "Тема в сфере: " + x[2] + "\n" + "Формат проведения: " + x[4]
                bot.send_message(call.message.chat.id, str(courses_list_counter) + ". " + str1)
            keyboard = types.InlineKeyboardMarkup()
            key_list = types.InlineKeyboardButton(text='Показать список всех курсов',
                                                  callback_data="courses_list")
            keyboard.add(key_list)
            key_filt = types.InlineKeyboardButton(text='Подобрать курс по параметрам', callback_data="courses_filter")
            keyboard.add(key_filt)
            bot.send_message(call.message.chat.id, "Что дальше?", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    keyboard = types.InlineKeyboardMarkup()
    key_list = types.InlineKeyboardButton(text='Показать список всех курсов', callback_data="courses_list")
    keyboard.add(key_list)
    key_filt = types.InlineKeyboardButton(text='Подобрать курс по параметрам', callback_data="courses_filter")
    keyboard.add(key_filt)
    bot.send_message(message.from_user.id, "Привет ✌️\nЧем я могу помочь?", reply_markup=keyboard)


bot.polling()
