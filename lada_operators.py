from numpy import exp, sqrt, cos, e, pi
from random import random, randint, choices

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


def generate_solution(lb, ub, dimensions):
    return [lb + (ub - lb) * random() for _ in range(dimensions)]


def get_strength(solution, optimal):
    denominator = sum(1 / (i - optimal) for i in solution)
    weights = [1 / (i - optimal) / denominator for i in solution]

    return weights


def select_parents(weights):
    # parents are randomized based on weights, they are labelled 1 to `len(weights)`
    parents = choices(range(1, len(weights) + 1), weights=weights, k=2)

    return parents


def uniform_crossover(p1, p2, count=2, bias=0.5):
    dimension = len(p1)
    flip = lambda: random() < bias

    babies = [[] for _ in range(count)]

    # for each gene: each baby retains the gene either from p1 or p2, based on `bias`
    for i in range(dimension):
        for baby in babies:
            if flip():
                baby.append(p1[i])
            else:
                baby.append(p2[i])

    return babies


def inverse_mutation(solution):
    upper_bound = len(solution)
    index1 = randint(0, upper_bound)
    index2 = randint(0, upper_bound)

    # make sure the indices are not equal
    while index1 == index2:
        index2 = randint(0, upper_bound)

    # make sure index1 is the left bound
    if index1 > index2:
        index1, index2 = index2, index1

    # reverse the subarray
    reversed_subarray = solution[index1 : index2 + 1][::-1]
    solution[index1 : index2 + 1] = reversed_subarray

    return solution


def display_parent(parent, fitness, n):
    print(f"Selected Parent {n}: {parent}")
    print(f"Fitness of Selected Parent {n}: {fitness:.4f}")


def display_baby(baby, n):
    print(f"Offspring {n}: {[round(b, 4) for b in baby]}")


# ---


def main():
    hr = lambda: print(f"\n{"-"*5}\n")  # formatting
    dimensions = 5
    r_bounds = -32.768, 32.768

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

    hr()  # Mutation ---
    print(f">> Mutated Offspring:\n")
    m_baby1, m_baby2 = map(inverse_mutation, (baby1, baby2))
    display_baby(m_baby1, 1)
    display_baby(m_baby2, 2)


if __name__ == "__main__":
    main()
