from gpiozero import Button
import random
from signal import pause
import display


class Game():
    solution = []
    guess = [0,0,0,0]
    active_digit = 0
    in_play = True
    correct = [0,0,0,0]

    def init_solution(self):
        self.solution.append(random.randint(0,9))
        for i in range(1,4):
            x = random.randint(0,9)
            while (x in self.solution):
                x = random.randint(0,9)
            self.solution.append(x)

    def left(self):
        if (self.active_digit == 0):
            self.active_digit = 3
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
        self.correct = [0,0,0,0]
        found = []
        for i in range(0,4):
            if (self.guess[i] == self.solution[i]):
                found.append(self.guess[i])
                self.correct[i] = 2
        for i in range(0,4):
            if (self.guess[i] in self.solution and self.guess[i] not in found):
                found.append(self.guess[i])
                self.correct[i] = 1

def display_results(correct):
    print(correct)

def play():

    left = Button(12)
    right = Button(5)
    up = Button(6)
    down = Button(13)
    select = Button(26)
    turns = 10
    game = Game()
    game.init_solution()
    to_display = [0,0,0,0]
    led_display = [0,0,0,0]
    won = False

    #main game loop
    while (turns > 0):
        #player controls game, ends when select is pressed
        i = 0
        while (game.in_play):
            if (to_display[game.active_digit] == 10):
                if(i % 10 == 0):
                    to_display = game.guess.copy()
            elif (i % 40 == 0):
                to_display[game.active_digit] = 10 # digits[10] is off

            display.show_num(to_display)

            for x in range(0, 4):
                if led_display[x] == 1:
                    led_display[x] = 2

            for x in range(0, 4):
                if (game.correct[x] == 1):
                    if(i % 10 == 0 and led_display[x] == 0):
                        led_display[x] = 2
                    elif (i % 40 == 0):
                        led_display[x] = 0

            display.update_leds(led_display)

            left.when_pressed = game.left
            right.when_pressed = game.right
            up.when_pressed = game.up
            down.when_pressed = game.down
            select.when_pressed = game.select

            i += 1
        #show which are right
        game.in_play = True
        #if won
        if (game.correct == [2,2,2,2]):
            won = True
            game.in_play = False
            turns = 0

        led_display = game.correct.copy()
        turns -= 1

    if (won):
        display.display_win()
    else:
        display.display_loss()
    display.clear_all()
    #add ability to play again?