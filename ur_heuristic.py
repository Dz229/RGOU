#####################################################
# Function calculating value of a Ur board position #
#####################################################

#Max player (B or R)
MAX_PLAYER = "B"

#Heuristic values - subject to potential change
HOME_VALUE         = 0
FINISH_VALUE       = 10000
SINGLE_STEP_VALUE  = 1
ENEMY_TOKENS_VALUE = 100 
BOARD_VALUES       = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

#Set the values of heuristic 
def set_values(home, finish, single, enemy, board_val):
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
        value = ('inf')
        return maxing_player_case(value)
    if red_tokens_finished == starting_tokens:
        value = ('-inf')
        return maxing_player_case(value)
    
    #Add value from tokens in home and those who finished 
    value += (black_tokens_in_home * HOME_VALUE) - (red_tokens_in_home * HOME_VALUE) + (black_tokens_finished * FINISH_VALUE) - (red_tokens_finished * FINISH_VALUE)

    #Add value from tokens on the board 
    #Home paths
    for i in range (4):
        if board[i] == "B":
            value += (i+1) * SINGLE_STEP_VALUE + (i ** 2) + BOARD_VALUES(i)
        if board[i+4] == "R":
            value -= (i+1) * SINGLE_STEP_VALUE + (i ** 2) + BOARD_VALUES(i)
    #Sared path
    for i in range (8):
        if board[i+8] == "B":
            value += (i+5) * SINGLE_STEP_VALUE + ((i+8) ** 2) + BOARD_VALUES(i+4)
        if board[i+8] == "R":
            value -= (i+5) * SINGLE_STEP_VALUE + ((i+8) ** 2) + BOARD_VALUES(i+4)
    #Finish paths
    for i in range (2):
        if board[i+16] == "B":
            value += (i+13) * SINGLE_STEP_VALUE + ((i+13) ** 2) + BOARD_VALUES(i+12)
        if board[i+18] == "R":
            value -= (i+13) * SINGLE_STEP_VALUE + ((i+13) ** 2) + BOARD_VALUES(i+12)      

    #Add fixed value for enemy tokens on the board_tiles
    value += ENEMY_TOKENS_VALUE * ((4 - black_tokens_in_home - black_tokens_finished) - (4 - red_tokens_in_home - red_tokens_finished))

    return maxing_player_case(value)

#Flip the values when the red is a maxing player
def maxing_player_case(value):
    if MAX_PLAYER == "R":
        return -(value)
    return value 
