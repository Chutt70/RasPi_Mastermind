from gpiozero import Button
import random
from signal import pause


class Game():
    solution = [random.randint(0,9), random.randint(0,9), random.randint(0,9), random.randint(0,9)]
    guess = [0,0,0,0]
    active_digit = 0
    in_play = True
    correct = []

    def left(self):
        if (self.active_digit == 0):
            self.active_digit = 4
            return
        self.active_digit -= 1

    def right(self):
        if (self.active_digit == 3):
            self.active_digit = 0
            return
        self.active_digit += 1

    def up(self):
        if (self.guess[self.active_digit] == 9):
            self.guess[self.active_digit] = 0
            return
        self.guess[self.active_digit] += 1

    def down(self):
        if (self.guess[self.active_digit] == 0):
            self.guess[self.active_digit] = 9
            return
        self.guess[self.active_digit] -= 1

    def select(self):
        self.in_play = False
        self.correct = []
        for i in range(0,3):
            if (self.guess[i] == self.solution[i]):
                self.correct.append(2)
            elif (self.guess[i] in self.solution):
                self.correct.append(1)
            else:
                self.correct.append(0)

def display_results(correct):
    print(correct)

def display_win():
    print("won!")

def display_loss():
    print("you lost")

def play():

    left = Button(5)
    right = Button(12)
    up = Button(6)
    down = Button(13)
    select = Button(26)
    turns = 15

    #main game loop, still need to add display
    while (turns > 0):
        game = Game()
        won = False
        turns = 15
        #player controlls control game, ends when select is pressed
        while (game.in_play):
            left.when_pressed = game.left
            right.when_pressed = game.right
            up.when_pressed = game.up
            down.when_pressed = game.down
            select.when_pressed = game.select
        #show which are right
        game.in_play = True
        display_results(game.correct)
        #if won
        if (game.correct == [2,2,2,2]):
            won = True
            game.in_play = False
            turns = 0

        turns -= 1

    if (won):
        display_win()
    else:
        display_loss()
    #add ability to play again?