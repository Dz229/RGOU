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

def EMM (board, depth):
    # Get possible moves
    possible_moves = board.get_moves()
    
    # Return -1 if there is no possible move
    if possible_moves ==[]:
        return -1
    
    # Iterate trough children and select best move based on value
    best_move = possible_moves[0]
    best_child_value = 0
    
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
        child = copy.deepcopy(board)
        child.move(move)
        child_value = EMM_ALG(child, depth-1)
        if (child_value > best_child_value) and board.current_player == "B":
            best_child_value = child_value
            best_move = move
        elif (child_value < best_child_value) and board.current_player == "R":
            best_child_value = child_value
            best_move = move
    
    # Return best move
    if best_move not in possible_moves:
        return possible_moves[0]
    return best_move
    
def EMM_ALG(board, depth):
    try:
        # Chances of diffrent rolls
        chances = [1/16, 4/16, 6/16, 4/16, 1/16]
        
        # If node is a leaf, return the value
        if depth == 0:
            return calculate(board.board_tiles, board.black_tokens_in_home, board.red_tokens_in_home, board.black_tokens_finished, board.red_tokens_finished, board.starting_tokens)
        
        # Get the possible moves
        possible_moves = board.get_moves()
        
        # Max player
        if board.current_player == "B":
            children_values = []
            for move in possible_moves:
                child = copy.deepcopy(board)
                child.move(move)
                child_value = chances[move] * EMM_ALG(child, depth-1)
                children_values.append(child_value)
            return max(children_values)

        # Min player
        else:
            children_values = []
            for move in possible_moves:
                child = copy.deepcopy(board)
                child.move(move)
                child_value = chances[move] * EMM_ALG(child, depth-1)
                children_values.append(child_value)
            return min(children_values)

    except Exception:
        print(Exception)
        return 0


# def EMM(b, depth, chance_node = False, original_board = True):
#     # Return value if b is a leaf
#     if depth == 0:
#         return calculate(b.board_tiles, b.black_tokens_in_home, b.red_tokens_in_home, b.black_tokens_finished, b.red_tokens_finished, b.starting_tokens)
#     if chance_node is True:
#         b0 = copy.deepcopy(b)
#         b0.dices_result = 0
#         b1 = copy.deepcopy(b)
#         b1.dices_result = 1
#         b2 = copy.deepcopy(b)
#         b2.dices_result = 2
#         b3 = copy.deepcopy(b)
#         b3.dices_result = 3
#         b4 = copy.deepcopy(b)
#         b4.dices_result = 4
#         return (1/16*EMM(b0, depth, False, False)) + (4/16*EMM(b1, depth, False, False)) + (6/16*EMM(b2, depth, False, False)) + (4/16*EMM(b3, depth, False, False)) + (1/16*EMM(b4, depth, False, False))
#     # Get list of possible children
#     children = []
#     best_move = 0
#     best_move_value = 0
#     for move in [0, 1, 2, 3, 4]:
#         child = copy.deepcopy(b)
#         if child.move(move):
#             children.append(EMM(child, depth-1, True, False))
#             if original_board:
#                 if b.current_player == "B":
#                     if children[-1] > best_move_value:
#                         best_move_value = children[-1]
#                         best_move = move
#                 else:
#                     if children[-1] < best_move_value:
#                         best_move_value = children[-1]
#                         best_move = move
           
#     if original_board:
#         return best_move
#     try:
#         if b.current_player == "B":
#             return max(children)
#         else:
#             return min(children)
#     except Exception:
#         return 0
    
    