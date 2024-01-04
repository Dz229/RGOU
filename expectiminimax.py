from ur_heuristic import calculate
import copy

############################
# Expectiminimax algorithm #
############################
# Based on a pseudocode from:
#
# Melkó, Ervin, and Benedek Nagy.
# "Optimal strategy in games with chance nodes." 
# Acta Cybernetica 18.2 (2007): 171-192.

NUMBER_OF_VISITED_STATES = 0

def EMM (board, depth):
    global NUMBER_OF_VISITED_STATES
    NUMBER_OF_VISITED_STATES = 0
    # Get possible moves
    possible_moves = board.get_moves()
    
    # Return -1 if there is no possible move
    if possible_moves == []:
        return -1
    
    # Iterate trough children and select best move based on value
    best_move = possible_moves[0]
    first_child = copy.deepcopy(board)
    first_child.move(best_move)
    best_child_value = chance_node(first_child, depth-1)
    
    # If there is no depth to algorithm
    if depth == 0:
        for move in possible_moves:
            child = copy.deepcopy(board)
            child.move(move)
            child_value = calculate(child.board_tiles, child.black_tokens_in_home, child.red_tokens_in_home, child.black_tokens_finished, child.red_tokens_finished, child.starting_tokens)
            if (child_value > best_child_value) and board.current_player == "B":
                best_child_value = child_value
                best_move = move
            elif (child_value < best_child_value) and board.current_player == "R":
                best_child_value = child_value
                best_move = move
    
    # When there is depth
    for move in possible_moves:
        #print(board.current_player)
        child = copy.deepcopy(board)
        child.move(move)
        child_value = chance_node(child, depth-1)
        if (child_value > best_child_value) and board.current_player == "B":
            best_child_value = child_value
            best_move = move
        elif (child_value < best_child_value) and board.current_player == "R":
            best_child_value = child_value
            best_move = move
        #print(f"Move {move}: {child_value}")
    
    #print(f"Visited states: {NUMBER_OF_VISITED_STATES}")
    
    # Return best move
    if best_move not in possible_moves:
        return possible_moves[0]
    return best_move

def chance_node(board, depth):
    value = 0
    chances = [1/16, 4/16, 6/16, 4/16, 1/16]
    rolls   = [0, 1, 2, 3, 4]
    for roll in rolls:
        child = copy.deepcopy(board)
        child.dices_result = roll
        try:
            value += chances[roll] * EMM_ALG(child, depth, roll)
        except Exception:
            value = EMM_ALG(child, depth, roll)
    return value

def EMM_ALG(board, depth, roll):
    global NUMBER_OF_VISITED_STATES
    NUMBER_OF_VISITED_STATES += 1

    # If node is a leaf, return the value
    if depth == 0 or board.check_for_winner() != None:
        return calculate(board.board_tiles, board.black_tokens_in_home, board.red_tokens_in_home, board.black_tokens_finished, board.red_tokens_finished, board.starting_tokens)
    
    # Get the possible moves
    possible_moves = board.get_moves()
  
    if roll == 0 or possible_moves == []:
        child = copy.deepcopy(board)
        child.change_player()
        return chance_node(child, depth-1)

    # Max player
    if board.current_player == "B":
        children_values = []
        for move in possible_moves:
            child = copy.deepcopy(board)
            child.move(move)
            child_value = chance_node(child, depth-1)
            children_values.append(child_value)
        return max(children_values)

    # Min player
    else:
        children_values = []
        for move in possible_moves:
            child = copy.deepcopy(board)
            child.move(move)
            child_value = chance_node(child, depth-1)
            children_values.append(child_value)
        return min(children_values)

