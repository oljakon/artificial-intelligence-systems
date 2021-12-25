import math
import random


alphabet = "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ "


def new_char():
    return random.choice(alphabet)


class DNA(object):
    def __init__(self, num):
        self.genes = []
        self.fitness = 0.0
        for i in range(num):
            self.genes.append(new_char())

    def get_phrase(self):
        return ''.join(self.genes)

    def calc_fitness(self, target):
        score = 0.0
        for i in range(len(self.genes)):
            if self.genes[i] == target[i]:
                score += 1
        self.fitness = score / len(target)

    def crossover(self, partner):
        child = DNA(len(self.genes))
        midpoint = random.randint(1, len(self.genes) - 1)
        child.genes = self.genes[0:midpoint] + partner.genes[midpoint:len(self.genes)]
        return child

    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = new_char()


class Population(object):
    def __init__(self, p, m, num):
        self.population = []
        self.mating_pool = []
        self.generations = 0
        self.finished = False
        self.target = p
        self.mutation_rate = m
        self.perfect_score = 1
        self.best = ""

        for x in range(num):
            self.population.append(DNA(len(self.target)))
        self.calc_fitness()

    def calc_fitness(self):
        for i in range(len(self.population)):
            self.population[i].calc_fitness(self.target)

    def natural_selection(self):
        self.mating_pool = []
        self.max_fitness = 0.0
        for i in range(len(self.population)):
            if self.population[i].fitness > self.max_fitness:
                self.max_fitness = self.population[i].fitness

        for x in range(len(self.population)):
            fitness = self.population[x].fitness / self.max_fitness
            n = math.floor(fitness * 100)
            for i in range(n):
                self.mating_pool.append(self.population[x])

    def generate(self):
        for i in range(len(self.population)):
            partnerA = random.choice(self.mating_pool)
            partnerB = random.choice(self.mating_pool)
            child = partnerA.crossover(partnerB)
            child.mutate(self.mutation_rate)
            self.population[i] = child
        self.generations += 1;

    def get_best(self):
        return self.best

    def evaluate(self):
        best_fitness = 0.0
        index = 0
        for x in range(len(self.population)):
            if self.population[x].fitness > best_fitness:
                index = x
                best_fitness = self.population[x].fitness

        self.best = self.population[index].get_phrase()
        if best_fitness == self.perfect_score:
            self.finished = True

    def is_finished(self):
        return self.finished

    def get_generations(self):
        return self.generations

    def get_avg_fitness(self):
        total = 0
        for i in range(len(self.population)):
            total = total + self.population[i].fitness
        return total / len(self.population)

    def all_phrases(self):
        everything = ""
        displayLimit = min(len(self.population), 50)
        for i in range(displayLimit):
            everything = everything + self.population[i].get_phrase() + "\n"
        return everything


def display_info():
    statsText = 'Всего поколений: ' + str(population.get_generations()) + "\n"
    statsText += 'Размер популяции: ' + str(population_max) + "\n"
    statsText += 'Вероятность мутации: ' + str(mutation_rate * 100) + "%\n"
    # print(population.all_phrases())
    print(statsText)
    print('Самое близкое значение: ' + population.get_best() + "\n")


if __name__ == '__main__':
    target = 'Строка для генерации'
    population_max = 200
    mutation_rate = 0.01

    population = Population(target, mutation_rate, population_max)

    while True:
        population.natural_selection()
        population.generate()
        population.calc_fitness()
        population.evaluate()
        display_info()
        if population.is_finished():
            break

    # generations = 500
    # for generation in range(generations+1):
    #     print('Поколение: ' + str(generation))
    #     population.natural_selection()
    #     population.generate()
    #     population.calc_fitness()
    #     population.evaluate()
    #     print('Самое близкое значение: ' + population.get_best() + '\n')
    #     if population.is_finished():
    #         break
