#################################################
# Python implementation of the Royal Game of Ur #
#################################################

#################
# Configuration #
#################
PLAYER_STARTS = True
PLAYER_GUI    = False

###########
# Imports #
###########
import numpy as np
import random
import os
import copy
import time
from sys import platform
from ur_heuristic import calculate
from expectiminimax import EMM
import tkinter as tk

###############
# Board class #
###############
class board:
    #Constructor building the board
    def __init__(self, STARTING_PLAYER = "B", NUMBER_OF_TOKENS = 4, NUMBER_OF_DICES = 4):
                #" "/0 - Empty tile, "B"/1 - Black tile, "R"/2 - Red tile
        self.tile_type = [" ", "B", "R"]
        #0-3 - black player home path #4-7 - red player home path #8-15 - middle path #16-17 black player finish path #18-19 red player finish path
        self.board_tiles = 20 * [self.tile_type[0]]
        #Set the paths indexes
        self.black_path_indexes = [0, 1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        self.red_path_indexes = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19]
        #Set the starting player
        self.current_player = STARTING_PLAYER
        #Set the number of tokens
        self.starting_tokens = NUMBER_OF_TOKENS
        self.black_tokens_in_home = NUMBER_OF_TOKENS
        self.red_tokens_in_home = NUMBER_OF_TOKENS
        self.black_tokens_finished = 0
        self.red_tokens_finished = 0
        #Dices result and their number
        self.number_of_dices = NUMBER_OF_DICES
        self.dices_result = 0
    
    #Board as a string
    def __str__(self) -> str:
        board_string = ""
        for i in range(4):
            board_string += "[" + self.board_tiles[3 - i] + "]" + "[" + self.board_tiles[8 + i] + "]" + "[" + self.board_tiles[7 - i] + "]\n"
        for i in range(2):
            board_string += "   [" + self.board_tiles[12 + i] + "]\n"
        for i in range(2):
            board_string += "[" + self.board_tiles[17 - i] + "]" + "[" + self.board_tiles[14 + i] + "]" + "[" + self.board_tiles[19 - i] + "]\n"
        return board_string
    
    #This function rolls the all the dices, each dice can roll 1 or 0 (50/50)
    def roll(self):
        self.dices_result = 0
        for i in range(self.number_of_dices):
            self.dices_result += random.randint(0, 1)
        # if self.dices_result == 0:
        #     self.change_player()
    
    #This function changes the current player
    def change_player(self):
        if self.current_player == self.tile_type[1]:
            self.current_player = self.tile_type[2]
        elif self.current_player == self.tile_type[2]:
            self.current_player = self.tile_type[1]
    
    #This function returns the player who has won or None if no one has won yet
    def check_for_winner(self):
        if self.black_tokens_finished == self.starting_tokens:
            return self.tile_type[1]
        elif self.red_tokens_finished == self.starting_tokens:
            return self.tile_type[2]
        return None
    
    #This function returns the player who waits for his turn
    def get_oposite_player(self):
        if self.current_player == self.tile_type[1]:
            return self.tile_type[2]
        elif self.current_player == self.tile_type[2]:
            return self.tile_type[1]
        
    #This function puts a token on the board and switches turn
    def put_token_on_board(self):
        #Account for the indexes of the arrays
        steps = self.dices_result - 1
        #Black player
        if self.current_player == self.tile_type[1]:
            if self.black_tokens_in_home < 1:
                return False
            if self.board_tiles[steps] == self.tile_type[1]:
                return False
            self.board_tiles[steps] = self.tile_type[1]
            self.black_tokens_in_home -= 1
            self.change_player()
            return True
        #Red player
        elif self.current_player == self.tile_type[2]:
            if self.red_tokens_in_home < 1:
                return False
            if self.board_tiles[steps + 4] == self.tile_type[2]:
                return False
            self.board_tiles[steps + 4] = self.tile_type[2]
            self.red_tokens_in_home -= 1
            self.change_player()
            return True

    #This function moves the token on the board, checks for collisions and switches turn
    def move(self, token):
        #If move is equal to 0, put token on the board
        if token == 0:
            return self.put_token_on_board()
        
        #Check if the chosen token exists
        if token > np.count_nonzero(np.asarray(self.board_tiles) == self.current_player) or token < 1:
            return False
        
        #Select the index of the chosen token
        token_index = np.where(np.asarray(self.board_tiles) == self.current_player)[0][token - 1]
        
        #Check if token is finishing the path
        if self.current_player == self.tile_type[1]:
            if token_index + self.dices_result > 18:
                return False
            elif token_index + self.dices_result == 18:
                self.black_tokens_finished += 1
                self.board_tiles[token_index] = self.tile_type[0]
                self.change_player()
                return True
        elif self.current_player == self.tile_type[2]:
            if token_index < 16 and token_index + self.dices_result > 15:
                self.dices_result += 2
            if token_index + self.dices_result > 20:
                return False
            elif token_index + self.dices_result == 20:
                self.red_tokens_finished += 1
                self.board_tiles[token_index] = self.tile_type[0]
                self.change_player()
                return True
            
        #Check for collisions and move the token if possible
        if self.current_player == self.tile_type[1]:
            if token_index < 4 and token_index + self.dices_result > 3:
                self.dices_result += 4
            #When there is a black token on tha tile
            if self.board_tiles[token_index + self.dices_result] == self.tile_type[1]:
                return False
            #When there is a red token on the tile
            elif self.board_tiles[token_index + self.dices_result] == self.tile_type[2]:
                self.board_tiles[token_index + self.dices_result] = self.current_player
                self.board_tiles[token_index] = self.tile_type[0]
                self.red_tokens_in_home += 1
                self.change_player()
                return True
            #When there is no token on the tile
            else:
                self.board_tiles[token_index + self.dices_result] = self.current_player
                self.board_tiles[token_index] = self.tile_type[0]
                self.change_player()
                return True
        elif self.current_player == self.tile_type[2]:
            # if token_index < 16 and token_index + self.dices_result > 15:
            #     self.dices_result += 2
            #When there is a black token on the tile
            if self.board_tiles[token_index + self.dices_result] == self.tile_type[1]:
                self.board_tiles[token_index + self.dices_result] = self.current_player
                self.board_tiles[token_index] = self.tile_type[0]
                self.black_tokens_in_home += 1
                self.change_player()
                return True
            #When there is a red token on the tile
            elif self.board_tiles[token_index + self.dices_result] == self.tile_type[2]:
                return False
            #When there is no token on the tile
            else:
                self.board_tiles[token_index + self.dices_result] = self.current_player
                self.board_tiles[token_index] = self.tile_type[0]
                self.change_player()
                return True

    #This function returns the list of possible moves for the current player 
    def get_moves(self):
        possible_moves = []
        for move in [0, 1, 2, 3, 4]:
            if copy.deepcopy(self).move(move):
                possible_moves.append(move)
        return possible_moves
            

#################
# Main function #
#################
if __name__ == '__main__':
    # Create board
    b = board()
    
    # Check for system
    clear_command = ''
    if platform == "linux" or platform == "linux2":
        clear_command = 'clear'
    elif platform == "win32":
        clear_command = 'cls'

    if PLAYER_STARTS:
        if PLAYER_GUI:
            # Main loop
            while True:
                #time.sleep(0.25)
                # Clear console
                # os.system(clear_command)

                # Print and input
                print ("Player B home:     " + str(b.black_tokens_in_home) + "   Player R home:     " + str(b.red_tokens_in_home))
                print ("Player B finished: " + str(b.black_tokens_finished) +"   Player R finished: " + str(b.red_tokens_finished))
                print ("Current player: " + b.current_player)
                print("Position value: " + str(calculate(b.board_tiles, b.black_tokens_in_home, b.red_tokens_in_home, b.black_tokens_finished, b.red_tokens_finished, b.starting_tokens)))        
                print(b)
                
                #Player turn
                print("Press any key to roll the dices")
                input()
                b.roll()
                print("Rolled " + str(b.dices_result))

                # Check for possible moves
                if b.dices_result != 0:
                    no_moves = False
                    possible_moves = b.get_moves()
                    if possible_moves == []:
                        b.change_player()
                        no_moves = True
                    print("Possible moves: " + str(possible_moves))
                
                # Make move
                if b.dices_result !=0 and no_moves == False:
                    while True:
                        try:
                            move = int(input("Your move: "))
                            if b.move(move):
                                break
                            else:
                                print("Wrong move: ")
                        except ValueError:
                            print("Wrong input, please try again")
                else:
                    print("Skipping to cpomputers turn...")
                
                # Check for winner
                if b.check_for_winner() != None:
                    print(str(b.check_for_winner()) + " has won!")
                    print(b)
                    print("Position value: " + str(calculate(b.board_tiles, b.black_tokens_in_home, b.red_tokens_in_home, b.black_tokens_finished, b.red_tokens_finished, b.starting_tokens)))
                    break
                
                #Computer turn
                b.roll()
                if b.dices_result == 0: 
                    print("================================================================")
                    print("Computer rolled 0, skiping turn...")
                    print("================================================================")
                    continue

                # Check for possible moves
                possible_moves = b.get_moves()
                if possible_moves == []:
                    b.change_player()
                    print("================================================================")
                    print("Computer has no possible moves, skiping turn...")
                    print("================================================================")
                    continue

                print("================================================================")
                print("Computer has rolled: " + str(b.dices_result))
                computer_move = EMM(copy.deepcopy(b), 4)
                print("Computer move: " + str(computer_move))
                print("================================================================")
                b.move(computer_move)
                
                # Check for winner
                if b.check_for_winner() != None:
                    print(str(b.check_for_winner()) + " has won!")
                    print(b)
                    print("Position value: " + str(calculate(b.board_tiles, b.black_tokens_in_home, b.red_tokens_in_home, b.black_tokens_finished, b.red_tokens_finished, b.starting_tokens)))
                    break
        else:
            
            #######
            # GUI #
            #######
            def draw_tokens(canvas, width, height, token_radius=30):
                # Delete old tokens on the board
                canvas.delete("token")
                
                # Draw tokens on the first 4 rows
                for i in range(4):
                    x = [0, 1 * width, 2 * width]
                    y = i * height
                    token_x1 = x[0] + width // 2
                    token_x2 = x[1] + width // 2
                    token_x3 = x[2] + width // 2
                    token_y = y + height // 2
                    
                    if b.board_tiles[3 - i] != " ":
                        canvas.create_oval(token_x1 - token_radius, token_y - token_radius,
                                           token_x1 + token_radius, token_y + token_radius,
                                           fill="black", tags="token")
                    if b.board_tiles[8 + i] == "B":
                        canvas.create_oval(token_x2 - token_radius, token_y - token_radius,
                                           token_x2 + token_radius, token_y + token_radius,
                                           fill="black", tags="token")   
                    if b.board_tiles[8 + i] == "R":
                        canvas.create_oval(token_x2 - token_radius, token_y - token_radius,
                                           token_x2 + token_radius, token_y + token_radius,
                                           fill="red", tags="token")
                    if b.board_tiles[7 - i] != " ":
                        canvas.create_oval(token_x3 - token_radius, token_y - token_radius,
                                           token_x3 + token_radius, token_y + token_radius,
                                           fill="red", tags="token")
                    
                # Draw tokens on the next 2 rows
                for i in range(2):
                    x = width
                    y = (i + 4) * height
                    token_x2 = x + width // 2
                    token_y = y + height // 2
                    
                    if b.board_tiles[12 + i] == "B":
                        canvas.create_oval(token_x2 - token_radius, token_y - token_radius,
                                           token_x2 + token_radius, token_y + token_radius,
                                           fill= "black", tags="token")
                    if b.board_tiles[12 + i] == "R":
                        canvas.create_oval(token_x2 - token_radius, token_y - token_radius,
                                           token_x2 + token_radius, token_y + token_radius,
                                           fill= "red", tags="token")
                    
                # Draw tokens on the last 2 rows    
                for i in range(2):
                    x = [0, 1 * width, 2 * width]
                    y = (i + 6) * height
                    token_x1 = x[0] + width // 2
                    token_x2 = x[1] + width // 2
                    token_x3 = x[2] + width // 2
                    token_y = y + height // 2

                    if b.board_tiles[17 - i] != " ":
                        canvas.create_oval(token_x1 - token_radius, token_y - token_radius, 
                                           token_x1 + token_radius, token_y + token_radius, 
                                           fill="black", tags="token")
                    if b.board_tiles[14 + i] == "B":
                        canvas.create_oval(token_x2 - token_radius, token_y - token_radius,
                                           token_x2 + token_radius, token_y + token_radius,
                                           fill= "black", tags="token")
                    if b.board_tiles[14 + i] == "R":
                        canvas.create_oval(token_x2 - token_radius, token_y - token_radius,
                                           token_x2 + token_radius, token_y + token_radius,
                                           fill= "red", tags="token")
                    if b.board_tiles[19 - i] != " ":
                        canvas.create_oval(token_x3 - token_radius, token_y - token_radius,
                                           token_x3 + token_radius, token_y + token_radius,
                                           fill="red", tags="token")
                    
                    

            ###################################################################
            def get_move_ui():
                # If player rolled 0
                if b.dices_result == 0:
                    # Computer turn
                    b.change_player()
                    b.roll()
                    if b.dices_result != 0:
                        possible_moves = b.get_moves()
                        if possible_moves == []:
                            b.change_player()
                        else:
                            computer_move = EMM(copy.deepcopy(b), 5)
                            b.move(computer_move)
                            
                # If player rolled between 1 and 4
                else:
                    # Player turn
                    try:
                        move = int(entry_field.get())
                        print(move)
                    except ValueError:
                            return
                    possible_moves = b.get_moves()
                    print(possible_moves)
                    if possible_moves == []:
                        b.change_player()
                    else:
                        try:
                            if not b.move(move):
                                return
                        except ValueError:
                            return
                    # Computer turn    
                    b.roll()
                    if b.dices_result != 0:
                        possible_moves = b.get_moves()
                        if possible_moves == []:
                            b.change_player()
                        else:
                            computer_move = EMM(copy.deepcopy(b), 4)
                            b.move(computer_move)
                    else:
                        b.change_player()
                
                # Draw tokens and upadte text field
                draw_tokens(canvas, width, height)
                b.roll()
                text="Player B home:    " + str(b.black_tokens_in_home) + "  Player R home:   " + str(b.red_tokens_in_home) +"\nPlayer B finished:" + str(b.black_tokens_finished) +" Player R finished:" + str(b.red_tokens_finished)+"\nCurrent player: " + b.current_player  +"\nRolled " + str(b.dices_result)              
                text_field.config(state=tk.NORMAL)  
                text_field.delete(1.0, tk.END)  
                text_field.insert(tk.END, text)  
                text_field.config(state=tk.DISABLED)  
            ###################################################################

            window = tk.Tk()
            window.title("Royal Game of Ur")
            
            # Size of each single board field
            width = 90
            height = 90
            
            # Upper text field 
            text_field = tk.Text(window, height=5, width=40, state=tk.DISABLED) 
            text_field.pack()
            
            # Create the board fields
            canvas = tk.Canvas(window, width=width*3, height=height*8)
            canvas.pack()
            for i in range(8):
                for j in range(3):
                    if not ((i > 3 and i < 6) and (j != 1)):
                        x1 = j * width
                        y1 = i * height
                        x2 = x1 + width
                        y2 = y1 + height
                        canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")

            # Firld to entry move 
            entry_field = tk.Entry(window)
            entry_field.pack()
            # Submit button
            submit_button = tk.Button(window, text="Make Move", command=get_move_ui)
            submit_button.pack()
            ##################################################################
            # First turn
            b.roll()
            text="Player B home:    " + str(b.black_tokens_in_home) + "  Player R home:   " + str(b.red_tokens_in_home) +"\nPlayer B finished:" + str(b.black_tokens_finished) +" Player R finished:" + str(b.red_tokens_finished)+"\nCurrent player: " + b.current_player  +"\nRolled " + str(b.dices_result)              
            text_field.config(state=tk.NORMAL)  
            text_field.delete(1.0, tk.END)  
            text_field.insert(tk.END, text)  
            text_field.config(state=tk.DISABLED)  
            ##################################################################
            # Start the app
            window.mainloop()
            #######
    else:
        # Main loop
        while True:
            #time.sleep(0.25)
            # Clear console
            # os.system(clear_command)
            #Computer turn
            b.roll()
            if b.dices_result == 0: 
                print("================================================================")
                print("Computer rolled 0, skiping turn...")
                print("================================================================")
            else:
                # Check for possible moves
                possible_moves = b.get_moves()
                if possible_moves == []:
                    b.change_player()
                    print("================================================================")
                    print("Computer has no possible moves, skiping turn...")
                    print("================================================================")
                else:
                    print("================================================================")
                    print("Computer has rolled: " + str(b.dices_result))
                    computer_move = EMM(copy.deepcopy(b), 24)
                    print("Computer move: " + str(computer_move))
                    print("================================================================")
                    b.move(computer_move)
            
            # Check for winner
            if b.check_for_winner() != None:
                print(str(b.check_for_winner()) + " has won!")
                print(b)
                print("Position value: " + str(calculate(b.board_tiles, b.black_tokens_in_home, b.red_tokens_in_home, b.black_tokens_finished, b.red_tokens_finished, b.starting_tokens)))
                break
            
            # Print and input
            print ("Player B home:     " + str(b.black_tokens_in_home) + "   Player R home:     " + str(b.red_tokens_in_home))
            print ("Player B finished: " + str(b.black_tokens_finished) +"   Player R finished: " + str(b.red_tokens_finished))
            print ("Current player: " + b.current_player)
            print("Position value: " + str(calculate(b.board_tiles, b.black_tokens_in_home, b.red_tokens_in_home, b.black_tokens_finished, b.red_tokens_finished, b.starting_tokens)))        
            print(b)
            
            #Player turn
            print("Press any key to roll the dices")
            input()
            b.roll()
            print("Rolled " + str(b.dices_result))

            # Check for possible moves
            if b.dices_result != 0:
                no_moves = False
                possible_moves = b.get_moves()
                if possible_moves == []:
                    b.change_player()
                    no_moves = True
                print("Possible moves: " + str(possible_moves))
            
            # Make move
            if b.dices_result !=0 and no_moves == False:
                while True:
                    try:
                        move = int(input("Your move: "))
                        if b.move(move):
                            break
                        else:
                            print("Wrong move: ")
                    except ValueError:
                        print("Wrong input, please try again")
            else:
                print("Skipping to cpomputers turn...")
            
            # Check for winner
            if b.check_for_winner() != None:
                print(str(b.check_for_winner()) + " has won!")
                print(b)
                print("Position value: " + str(calculate(b.board_tiles, b.black_tokens_in_home, b.red_tokens_in_home, b.black_tokens_finished, b.red_tokens_finished, b.starting_tokens)))
                break
