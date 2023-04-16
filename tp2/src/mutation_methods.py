import math
import random
from .individual import Individual


# Mutations methods don't return anything. They work in place with the population variable.

# This is a general method that receives the color_ratios gene and applies 
def mutate_gene(color_ratio):
    change = 10
    s = random.choice([1, -1])
    return max(min(color_ratio + change * s, 100), 0)


def gen(individual: Individual, pm: float) -> None:
    if random.random() < pm:
        index_to_mutate = random.randrange(0, len(individual.color_ratios))
        individual.color_ratios[index_to_mutate][1] = mutate_gene(individual.color_ratios[index_to_mutate][1])
        individual.normalize()


def limited_multigen(individual: Individual, pm: float) -> None:
    amount_to_mutate = random.randint(0, len(individual.color_ratios))
    chosen = [(i < amount_to_mutate) for i in range(amount_to_mutate)]
    random.shuffle(chosen)
    for i in range(len(individual.color_ratios)):
        if chosen[i] and random.random() < pm:
            individual.color_ratios[i][1] = mutate_gene(individual.color_ratios[i][1])
    individual.normalize()


def uniform_multigen(individual: Individual, pm: float) -> None:
    for i in range(len(individual.color_ratios)):
        if random.random() < pm:
            individual.color_ratios[i][1] = mutate_gene(individual.color_ratios[i][1])
    individual.normalize()


def complete(individual: Individual, pm: float) -> None:
    if random.random() < pm:
        for i in range(len(individual.color_ratios)):
            individual.color_ratios[i][1] = mutate_gene(individual.color_ratios[i][1])
    individual.normalize()


mutation_list = {
    "gen": gen,
    "limited_multigen": limited_multigen,
    "uniform_multigen": uniform_multigen,
    "complete": complete
}


def mutation(config_mutation: int, population: list[Individual], generation: int) -> None:
    f = mutation_list[config_mutation]
    
    pm = 0.4
    for individual in population:
        f(individual, pm)
