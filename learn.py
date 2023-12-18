from ur import board
import ur_heuristic
from expectiminimax import EMM
import random
import math
import copy

#Algorithm settings
POPULATION    = 1024
GENERATIONS   = 50
MUTATION_RATE = 0.1

#Starting values 
HOME_VALUE         = 0
FINISH_VALUE       = 100
SINGLE_STEP_VALUE  = 1
ENEMY_TOKENS_VALUE = 10
BOARD_VALUES       = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

STARTING_VALUES = [HOME_VALUE, FINISH_VALUE, SINGLE_STEP_VALUE, ENEMY_TOKENS_VALUE, BOARD_VALUES]

#Play the game using the set values for heuristic 
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

#This function return the generated population as list
def init_population(current_best = STARTING_VALUES):
    return [current_best[:] for _ in range(POPULATION)]

#Mutate the population
def mutate(current_population):
    for i in range (POPULATION):
        for j in range (len(BOARD_VALUES)):
            if random.random() < MUTATION_RATE:
                current_population[i][4][j] += random.uniform(-0.1, 0.1)
        if random.random() < MUTATION_RATE:
            current_population[i][0] += random.uniform(-1, 1)
            current_population[i][1] += random.uniform(-1, 1)

        return current_population

def fight(current_population):
    winners = []
    half = int(len(current_population) / 2)
    for i in range (half):
        print(f"--{i+1}/{half}")
        winners.append(play(current_population[i], current_population[i+half]))
    return winners

def evaluate():
    #Current best values
    current_best = STARTING_VALUES
    
    #Iterate over generations 
    for generation in range (GENERATIONS):
        print(f"Starting generation {generation+1} out of {GENERATIONS}...")
        # Initialize population
        current_population = init_population(current_best)
        # Mutate
        current_population = mutate(current_population)

        # Get winners
        num_log = int(math.log(POPULATION, 2))
        for pop in range (num_log):
            print(f"-{pop+1}/{num_log}")
            current_population = fight(current_population)

        # Return winner 
        current_best = current_population

        # Print the results
        print(f"Best out of generation {generation}:")
        print(current_best)

evaluate()
