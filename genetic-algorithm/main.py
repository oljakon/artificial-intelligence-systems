from random import choice
from random import random

ALPHABET = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"


# Формирование начальной популяции
def init_population(population_number):
    p = []
    for i in range(population_number):
        gen = choice(ALPHABET) + choice(ALPHABET) + choice(ALPHABET)
        p.append(gen)
    return p


# Оценивание популяции
def fitness(current_population):
    for i, chromosome in enumerate(current_population):
        fit = 1
        if chromosome[0] == "К":
            fit += 1
        if chromosome[1] == "О":
            fit += 1
        if chromosome[2] == "Т":
            fit += 1
        if fit == 4:
            return 1
    return 0


# Скрещивание
def crossover(p, pc):
    new_population = []
    for i in range(len(p) - 1):
        parent_1 = choice(p)
        parent_2 = choice(p)
        while parent_1 == parent_2:
            parent_1 = choice(p)  # Формирование первого родителя
            parent_2 = choice(p)  # Формирование второго родителя
        if pc > random():
            child_1 = parent_1[0] + parent_2[1] + parent_1[2]  # Формирование первого потомка
            child_2 = parent_2[0] + parent_1[1] + parent_2[2]  # Формирование второго потомка
            new_population.append(child_1)
            new_population.append(child_2)
        else:
            new_population.append(parent_1)
        i += 2
    return new_population


# Мутация
def mutation(current_population, mutation_chance):
    for i, chromosome in enumerate(current_population):
        for j in range(len(chromosome)):
            if random() < mutation_chance:
                new_gen = choice(ALPHABET)
                while current_population[i][j] == new_gen:
                    new_gen = choice(ALPHABET)  # Если шанс на мутацию прошел, то меняем ген на любой другой
                current_population[i] = current_population[i].replace(current_population[i][j], new_gen)


if __name__ == '__main__':
    print("Начальная популяция")
    population = init_population(10)
    print(population)
    q = 0
    generations = 0
    while q == 0:
        q = fitness(population)
        population = crossover(population, 0.6)
        mutation(population, 1)
        generations += 1
    print("Слово КОТ сгенерировано")
    print("Размер текущей популяции: ", len(population))
    print("Количество поколений: ", generations)

