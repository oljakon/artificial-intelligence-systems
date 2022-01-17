import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from distances import euclidean, manhattan, parametric_tree_metric, tree_metric


def plot_correlation(ds, metric):
    matr = []
    for i in range(len(ds.values.tolist())):
        r = []
        for k in range(len(ds.values.tolist())):
            r.append(metric(ds.values.tolist()[i], ds.values.tolist()[k]))
        matr.append(np.array(r))
    matr = np.array(matr)

    plt.imshow(matr)
    plt.title(metric)
    plt.xticks(np.arange(0, len(ds.values.tolist())))
    plt.yticks(np.arange(0, len(ds.values.tolist())))
    figure(figsize=(10, 10), dpi=150)
    plt.show()


def find_similar_for_one_course(ds, dataset, metric, id):
    r = []
    for i in range(len(ds.values.tolist())):
        r.append(metric(ds.values.tolist()[id], ds.values.tolist()[i]))

    return pd.DataFrame(list(zip(r, map(lambda e: str("".join(e[3])),dataset.values.tolist()))),
                        index=np.arange(len(r)), columns=['Различие', 'Курс'])


def find_similar_for_liked_courses(ds, data, metric, likes, dislikes):
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

    # matr = r
    # plt.imshow(matr)
    # plt.xticks(np.arange(0, len(ds.values.tolist())))
    # plt.yticks(np.arange(0, len(ds.values.tolist())))
    # figure(figsize=(10, 10), dpi=150)
    # plt.show()

    most_related = most_related.drop_duplicates(subset='id', keep="last")
    idx = most_related.index
    for k in dislikes:
        if k in idx:
            most_related = most_related.drop(k)

    most_related = most_related.sort_values('Разница')
    print(most_related)

    return r


if __name__ == '__main__':
    data = pd.read_csv('doc/courses.txt', delimiter=';')
    dataset = data.copy(deep=True)

    dataset["Направление курсов"], _ = pd.factorize(dataset["Направление курсов"])
    dataset["Сфера"], _ = pd.factorize(dataset["Сфера"])
    dataset["Тема в сфере"], _ = pd.factorize(dataset["Тема в сфере"])
    dataset["Название"], _ = pd.factorize(dataset["Название"])
    dataset["Формат проведения"], _ = pd.factorize(dataset["Формат проведения"])
    dataset["Кол-во отзывов"], _ = pd.factorize(dataset["Кол-во отзывов"])
    dataset["Средний рейтинг"], _ = pd.factorize(dataset["Средний рейтинг"])
    dataset["Год выпуска"], _ = pd.factorize(dataset["Год выпуска"])
    dataset["Форма общения"], _ = pd.factorize(dataset["Форма общения"])

    #plot_correlation(dataset, euclidean)
    #plot_correlation(dataset, manhattan)
    #plot_correlation(data, diff_tree)

    id = 2
    metric = tree_metric
    print('Курс: ', data.values.tolist()[id])
    print('Похожие курсы:\n')
    similar = find_similar_for_one_course(dataset, data, metric, id)
    print(similar.sort_values("Различие"))

    # likes = [25, 26, 27]
    # dislikes = [6, 7]
    # find_similar_for_liked_courses(dataset, data, metric, likes, dislikes)
