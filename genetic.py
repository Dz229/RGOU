from ur import board
import ur_heuristic
from expectiminimax import EMM
import random
import math
import copy
import numpy as np
from numba import jit

# Constants
POPULATION_SIZE = 512
GENERATIONS = 100
MUTATION_RATE = 0.1

# Initialize the population
def initialize_population():
    return [[0, 100, 1, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]] for _ in range(POPULATION_SIZE)]

# Play the game
def play(black_values, red_values):
    b = board()
    # Main loop
    while True:

        #Black player turn
        can_move = True
        ur_heuristic.set_values(black_values[0], black_values[1], black_values[2], black_values[3], black_values[4])
        b.roll()
        if b.dices_result == 0: 
            can_move = False
        possible_moves = b.get_moves()
        if possible_moves == []:
            b.change_player()
            can_move = False
        if can_move:
            computer_move = EMM(copy.deepcopy(b), 4)
            b.move(computer_move)
        if b.check_for_winner() != None:
            break
        
        #Red player turn
        ur_heuristic.set_values(red_values[0], red_values[1], red_values[2], red_values[3], red_values[4])
        b.roll()
        if b.dices_result == 0: 
            continue
        possible_moves = b.get_moves()
        if possible_moves == []:
            b.change_player()
            continue
        computer_move = EMM(copy.deepcopy(b), 4)
        b.move(computer_move)
        if b.check_for_winner() != None:
            break
        
    if b.check_for_winner() == "B":
        return black_values
    else:
        return red_values

# Mutate function
def mutate(current_population):
    for individual in current_population:
        # Mutating HOME_VALUE, FINISH_VALUE, and SINGLE_STEP_VALUE
        if random.random() < MUTATION_RATE:
            individual[0] += np.random.normal(0, 1)  # HOME_VALUE mutation

        if random.random() < MUTATION_RATE:
            individual[1] += np.random.normal(0, 10)  # FINISH_VALUE mutation

        if random.random() < MUTATION_RATE:
            individual[2] += np.random.normal(0, 1)  # SINGLE_STEP_VALUE mutation

        # Mutating ENEMY_TOKENS_VALUE
        if random.random() < MUTATION_RATE:
            individual[3] += np.random.normal(0, 5)  # ENEMY_TOKENS_VALUE mutation

        # Mutating BOARD_VALUES
        for j in range(len(individual[4])):
            if random.random() < MUTATION_RATE:
                individual[4][j] += np.random.normal(0, 5)  # BOARD_VALUES mutation

    return current_population


# Genetic Algorithm
@jit
def genetic_algorithm():
    population = initialize_population()

    for generation in range(GENERATIONS):
        print(f"Generation: {generation}/{GENERATIONS}")

        # Play games to determine fitness
        fitness_scores = []
        for i in range(0, len(population), 2):
            print(f"|-Fitness: {i}/{len(population)}")
            winner = play(population[i], population[i+1])
            fitness_scores.append((winner, 1))  # Winner gets a score

        # Sort by fitness and select the best half of the population
        population = [x for x, _ in sorted(fitness_scores, key=lambda x: x[1], reverse=True)][:POPULATION_SIZE//2]

        # Ensure population size remains constant
        while len(population) < POPULATION_SIZE:
            population.append(random.choice(population))  # Randomly duplicate existing members


        # Crossover (naive approach: pair-wise swap)
        new_population = []
        for i in range(0, len(population), 2):
            print(f"|-Crossover: {i}/{len(population)}")
            crossover_point = random.randint(1, len(population[i]) - 1)
            child1 = population[i][:crossover_point] + population[i+1][crossover_point:]
            child2 = population[i+1][:crossover_point] + population[i][crossover_point:]
            new_population.extend([child1, child2])

        # Mutate the new population
        population = mutate(new_population)

    return population

def fight(current_population):
    winners = []
    half = int(len(current_population) / 2)
    for i in range (half):
        winners.append(play(current_population[i], current_population[i+half]))
    return winners

# Run the genetic algorithm
best_population = genetic_algorithm()

# Get winners
num_log = int(math.log(POPULATION_SIZE, 2))
for pop in range (num_log):
    best_population = fight(best_population)

print("Best individual:")
print(best_population)
