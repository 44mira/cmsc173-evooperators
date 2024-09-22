from numpy import exp, sqrt, cos, e, pi
from random import random, choices

# !! VALUES ARE ONLY ROUNDED ON DISPLAY, NOT FOR CALCULATIONS !!

# ---

# The Ackley Function
# Source: https://github.com/adhishagc/Ackley-Function/blob/master/ackley.py


def ackley(xs):
    # constants (e is defined in numpy as euler's number)
    a, b, c = 20, 0.2, 2 * pi

    # dimensions
    d = len(xs)

    # break down formula for readability
    part1 = -b * sqrt(1 / d * sum(x**2 for x in xs))
    part2 = 1 / d * sum(cos(c * x) for x in xs)

    value = -a * exp(part1) - exp(part2) + a + e

    return value


r_bounds = -32.768, 32.768


def generate_solution(lb, ub, dimensions):
    return [lb + (ub - lb) * random() for _ in range(dimensions)]


def get_strength(solution, optimal):
    denominator = sum(1 / (i - optimal) for i in solution)
    weights = [1 / (i - optimal) / denominator for i in solution]

    return weights


def select_parents(weights):
    parents = choices(range(1, len(weights) + 1), weights=weights, k=2)

    return parents


def uniform_crossover(p1, p2, bias=0.5):
    dimension = len(p1)
    flip = lambda: random() < bias

    baby1, baby2 = [], []

    for i in range(dimension):
        if flip():
            baby1.append(p1[i])
        else:
            baby1.append(p2[i])

        if flip():
            baby2.append(p1[i])
        else:
            baby2.append(p2[i])

    return baby1, baby2


def display_parent(parent, fitness, n):
    print(f"Selected Parent {n}: {parent}")
    print(f"Fitness of Selected Parent {n}: {fitness:.4f}")


def display_baby(baby, n):
    print(f"Offspring {n}: {[round(b, 4) for b in baby]}")


# ---


def main():
    hr = lambda: print(f"\n{"-"*5}\n")  # formatting
    dimensions = 5

    solutions = []
    solutions_fitness = []

    hr()
    print(">> After generation of population:\n")

    # i: 1 to 10
    for i in range(1, 11):
        solution = generate_solution(*r_bounds, dimensions)
        solution_fitness = ackley(solution)

        print(f"Solution {i}: {[round(s, 4) for s in solution]}")
        print(f"Fitness {i}: {solution_fitness:.4f}")

        solutions.append(solution)
        solutions_fitness.append(ackley(solution))

    hr()  # Selection ---
    strengths = get_strength(solutions_fitness, 0.0)
    parent1, parent2 = select_parents(strengths)
    print(f">> Selected Parents:\n")
    display_parent(parent1, solutions_fitness[parent1 - 1], 1)
    display_parent(parent2, solutions_fitness[parent2 - 1], 2)

    hr()  # Crossover ---
    print(f">> Produced Offspring:\n")
    baby1, baby2 = uniform_crossover(solutions[parent1 - 1], solutions[parent2 - 1])
    display_baby(baby1, 1)
    display_baby(baby2, 2)


if __name__ == "__main__":
    main()
