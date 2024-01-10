#####################################################
# Function calculating value of a Ur board position #
#####################################################

#Max player (B or R)
MAX_PLAYER = "B"

#Heuristic values - subject to potential change
# HOME_VALUE         = 0
# FINISH_VALUE       = 1000
# SINGLE_STEP_VALUE  = 1
# ENEMY_TOKENS_VALUE = 100 
# BOARD_VALUES       = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

# HOME_VALUE         = -1.8850861019751801
# FINISH_VALUE       = 5092.74610962674711
# SINGLE_STEP_VALUE  = 4.668100982513829
# ENEMY_TOKENS_VALUE = -4.296115903271434
# BOARD_VALUES       = [-62.26471323294646, 
#                       217.04928447366996, 
#                       399.96197726312744, 
#                       291.9830116589317, 
#                       39.896610293852284, 
#                       -293.67706162031425, 
#                       211.26242460008632, 
#                       -86.2713459368435, 
#                       19.189287469080618, 
#                       60.53453746976433, 
#                       164.42230512251132, 
#                       11.411840431804649, 
#                       -22.87925683967131, 
#                       82.00112332463466]

HOME_VALUE         = -1.6749437499203839
FINISH_VALUE       = 1071.67792062044293
SINGLE_STEP_VALUE  = -3.7552945293894444
ENEMY_TOKENS_VALUE = 26.358455922566854
BOARD_VALUES       = [39.77672061568756, -55.40650470285588, 36.35937519074401, -22.540476141314997, 64.15679680805859, 74.20050042779252, -98.88968539257307, 10.42763489237641, -20.393451198513482, 75.46353421286679, 72.97372986103845, 11.334512859266304, -22.316414795176403, 2.502879188082158]


#Set the values of heuristic 
def set_values(home, finish, single, enemy, board_val):
    global HOME_VALUE, FINISH_VALUE, SINGLE_STEP_VALUE, ENEMY_TOKENS_VALUE, BOARD_VALUES
    HOME_VALUE         = home
    FINISH_VALUE       = finish
    SINGLE_STEP_VALUE  = single
    ENEMY_TOKENS_VALUE = enemy
    BOARD_VALUES       = board_val

#This function takes the board list (board_tiles from ur board implementation) and information on tokens that are not on the boad and then returns the value of the board
def calculate(board, black_tokens_in_home, red_tokens_in_home, black_tokens_finished, red_tokens_finished, starting_tokens):
    value = 0.0

    #If someone has finished
    if black_tokens_finished == starting_tokens:
        value = float('inf')
        return maxing_player_case(value)
    if red_tokens_finished == starting_tokens:
        value = float('-inf')
        return maxing_player_case(value)
    
    #Add value from tokens in home and those who finished 
    value += (black_tokens_in_home * HOME_VALUE) - (red_tokens_in_home * HOME_VALUE) + (black_tokens_finished * FINISH_VALUE) - (red_tokens_finished * FINISH_VALUE)

    #Add value from tokens on the board 
    #Home paths
    for i in range (4):
        if board[i] == "B":
            value += (((i+1) * SINGLE_STEP_VALUE) ** 2) + BOARD_VALUES[i]
        if board[i+4] == "R":
            value -= (((i+1) * SINGLE_STEP_VALUE) ** 2) + BOARD_VALUES[i]
    #Sared path
    for i in range (8):
        if board[i+8] == "B":
            value += (((i+5) * SINGLE_STEP_VALUE) ** 2) + BOARD_VALUES[i+4]
        if board[i+8] == "R":
            value -= (((i+5) * SINGLE_STEP_VALUE) ** 2) + BOARD_VALUES[i+4]
    #Finish paths
    for i in range (2):
        if board[i+16] == "B":
            value += (((i+13) * SINGLE_STEP_VALUE) ** 2) + BOARD_VALUES[i+12]
        if board[i+18] == "R":
            value -= (((i+13) * SINGLE_STEP_VALUE) ** 2) + BOARD_VALUES[i+12]      

    #Add fixed value for token diffrence on the board_tiles
    value += ENEMY_TOKENS_VALUE * ((4 - black_tokens_in_home - black_tokens_finished) - (4 - red_tokens_in_home - red_tokens_finished))

    return maxing_player_case(value)

#Flip the values when the red is a maxing player
def maxing_player_case(value):
    if MAX_PLAYER == "R":
        return -(value)
    return value 
