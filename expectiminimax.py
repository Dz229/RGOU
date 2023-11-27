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


def EMM(b, depth):
    # Return value if b is a leaf
    if depth == 0:
        return calculate(b.board_tiles, b.black_tokens_in_home, b.red_tokens_in_home, b.black_tokens_finished, b.red_tokens_finished, b.starting_tokens)
    # Get list of possible children
    