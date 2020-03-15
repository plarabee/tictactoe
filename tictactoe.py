"""
MIT License

Copyright (c) 2020 Patrick Larabee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from functools import partial
from os import sys
from time import sleep
from tkinter import *
from tkinter import messagebox

from square import *


"""
Creates the TKinter UI window as well
as 9 buttons to be used as TicTacToe 
squares.

Returns:
    - window (Tk window)
    - Squares[] (our Square objects with buttons
                 and scores)

"""
def create_board():
    """ window settings """
    window = Tk()
    window.title('TicTacToe')
    window.geometry('900x900')
    window.configure(bg = 'white')

    """ create our square objects and buttons """
    squares = {}
    for i in range(0 , 9):
        squares[i] = Square(Button(window,
                            text = '',
                            command = partial(clicked, i),
                            bg ='white',
                            fg = 'black',
                            font = 'Verdana 32 bold'), 0)

    """ place each row on the window """
    for i in range(0, 3):
        squares[i].button.place(x = i * 300, y = 0, width = 300, height = 300)
    for i in range(3, 6):
        squares[i].button.place(x = (i - 3) * 300, y = 300, width = 300, height = 300)  
    for i in range(6, 9):
        squares[i].button.place(x = (i - 6) * 300, y = 600, width = 300, height = 300) 

    return window, squares


""" 
Handles the functionality of clicking a square.

This includes:

    - Preventing square from being used twice
    - Changing button text to X or O
    - Changing player turn (X to O or vice versa)
    - Assigning a score to the Square object

"""
def clicked(i):
    """ space is already used """
    if squares[i].button['text'] != '':
        return

    """ change the button text to X or O """
    squares[i].button.configure(text=turn)

    """ 
    assign a score so we can check win condition:
      - X = 1
      - O = -1
    """
    if turn == 'X':
        squares[i].score = 1
    else:
        squares[i].score = -1
    
    if check_for_game_over() == False:
        change_turn()


"""
Toggles turn between X and O.
Global variable turn necessary because 
function is called from the Tkinter button press.

"""
def change_turn():
    global turn
    if turn == 'X':
        turn = 'O'
    else:
        turn = 'X'


"""
Checks the board for a win or draw condition.
There are eight potential combinations
that can win the game using either X
or O. 

If the sum of all three squares in a 
pattern is 3 or -3 then the game is over.
Positive 3 means X has won while negative
means O has won.

If no winner is found and no
square has a score of 0 (empty space), 
we have a draw.

"""
def check_for_game_over():
    """ all eight ways to win """
    patterns = [squares[0].score + squares[1].score + squares[2].score,
                squares[3].score + squares[4].score + squares[5].score,
                squares[6].score + squares[7].score + squares[8].score,
                squares[0].score + squares[3].score + squares[6].score,
                squares[1].score + squares[4].score + squares[7].score,
                squares[2].score + squares[5].score + squares[8].score,
                squares[0].score + squares[4].score + squares[8].score,
                squares[2].score + squares[4].score + squares[6].score]

    """ 3 means X wins, -3 means O wins """
    for pattern in patterns:
        if pattern == 3:
            game_over('X')
            return True
        if pattern == -3:
            game_over('O')
            return True

    """ no winner yet, check for draw """
    for square in squares:
        if squares[square].score == 0:
            return False

    """ no winner and no empty spaces, draw """
    game_over(None)
    return True


"""
Creates a pop-up dialog to notify the player that
the game has ended and gives them the result. It
also prompts to see if they want to play again.

If yes, it starts a new game. If no, it exits.

"""
def game_over(winner):

    if winner == None:
        message = 'Draw!'
    else:
        message = f'{winner} Wins!'

    play_again = messagebox.askyesno(title = message, message = "Play Again?")

    if play_again:
        new_game()
    else:
        sys.exit(0)

"""
Starts a new game by resetting the turn to X and 
resetting the squares.

"""
def new_game():
    global turn
    turn = 'X'

    for i in squares:
        squares[i].button.configure(text='')
        squares[i].score = 0


turn = 'X'
window, squares = create_board()
window.mainloop()
