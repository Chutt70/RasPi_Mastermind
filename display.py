import RPi.GPIO as GPIO
from gpiozero import LED
from time import sleep

# Shift Reg Pin setup -------
dataPIN = 17
latchPIN = 27
clockPIN = 22
#----------------------------

# 7-Segment digit pin setup -
digitPINS = [25,23,24,16]
#----------------------------

# LED pin setup--------------
leds = [LED(9), LED(10), LED(8), LED(7)]
#----------------------------

# Bits for each number 0-9 + null for 7-seg sending:
digits = ["11111100", "01100000", "11011010", "11110010", "01100110", "10110110", "10111110", "11100000", "11111110", "11110110", "00000000"]

# set pins to output mode
GPIO.setmode(GPIO.BCM)
GPIO.setup((dataPIN,latchPIN,clockPIN, digitPINS[0], digitPINS[1], digitPINS[2], digitPINS[3]),GPIO.OUT)

# Shift Register function:

def shift_update(input,data,clock,latch):
  #put latch down to start data sending
  GPIO.output(clock,0)
  GPIO.output(latch,0)
  GPIO.output(clock,1)

  #load data in reverse order
  for i in range(7, -1, -1):
    GPIO.output(clock,0)
    GPIO.output(data, int(input[i]))
    GPIO.output(clock,1)

  #put latch up to store data on register
  GPIO.output(clock,0)
  GPIO.output(latch,1)
  GPIO.output(clock,1)

# 7-Segment functions:

def set_digit(input, digit): #set 1 digit to the input integer
    for i in range(0,4):
        if i != digit:
            GPIO.output(digitPINS[i], 1)
    GPIO.output(digitPINS[digit], 0)
    shift_update(digits[input], dataPIN, clockPIN, latchPIN)

def show_num(input): #show a 4 digit number (takes int array)
    for i in range(0,4):
        set_digit(input[i], i)
        sleep(0.005)

def manual_show_num(input): # show 4 custom characters (takes array of 8-bit binary strings)
    for i in range(0,4):
        for j in range(0,4):
            if j != i:
                GPIO.output(digitPINS[j], 1)
        GPIO.output(digitPINS[i], 0)
        shift_update(input[i], dataPIN, clockPIN, latchPIN)
        sleep(0.005)

def clear_all(): #sets all 7 segment digits and LEDs to off
    for i in range(0,4):
        shift_update("00000000", dataPIN, clockPIN, latchPIN)
        GPIO.output(digitPINS[i], 1)
        leds[i].off()

def display_win(): #Shows the word Yes for a bit
    update_leds([1,1,1,1])
    for k in range(350):
        manual_show_num(["01110110", "10011110", "10110111", "00000000"])

def display_loss(): #Shows the word Lose for a bit
    update_leds([0,0,0,0])
    for k in range(350):
        manual_show_num(["00011100", "00111010", "10110110", "10011110"])

def display_play(): #Shows the word play
    input = ["11001110", "00011100", "11101110", "01110110"]
    for i in range(0,4):
            for j in range(0,4):
                if j != i:
                    GPIO.output(digitPINS[j], 1)
            GPIO.output(digitPINS[i], 0)
            shift_update(input[i], dataPIN, clockPIN, latchPIN)
            sleep(0.005)

# LED function

def update_leds(correct): #sets leds to on or off depending on correct array from main.py
    for i in range(0,4):
        if correct[i] == 0:
            leds[i].off()
        elif correct[i] == 2:
            leds[i].on()