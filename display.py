import RPi.GPIO as GPIO
from gpiozero import LED
from time import sleep

dataPIN = 17 #placeholders
latchPIN = 27
clockPIN = 22
digitPINS = [25,23,24,16]

leds = [LED(9), LED(10), LED(8), LED(7)]

#for 7-seg sending:
digits = ["11111100", "01100000", "11011010", "11110010", "01100110", "10110110", "10111110", "11100000", "11111110", "11110110", "00000000"]

GPIO.setmode(GPIO.BCM)
GPIO.setup((dataPIN,latchPIN,clockPIN, digitPINS[0], digitPINS[1], digitPINS[2], digitPINS[3]),GPIO.OUT)

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

def set_digit(input, digit):
    for i in range(0,4):
        if i != digit:
            GPIO.output(digitPINS[i], 1)
    GPIO.output(digitPINS[digit], 0)
    shift_update(digits[input], dataPIN, clockPIN, latchPIN)

def show_num(input):
    for i in range(0,4):
        set_digit(input[i], i)
        sleep(0.005)

def manual_show_num(input):
    for k in range(500):
        for i in range(0,4):
            for j in range(0,4):
                if j != i:
                    GPIO.output(digitPINS[j], 1)
            GPIO.output(digitPINS[i], 0)
            shift_update(input[i], dataPIN, clockPIN, latchPIN)
            sleep(0.005)

def clear_all():
    for i in range(0,4):
        shift_update("00000000", dataPIN, clockPIN, latchPIN)
        GPIO.output(digitPINS[i], 1)
        leds[i].off()

def display_win():
    manual_show_num(["01110110", "10011110", "10110111", "00000000"])

def display_loss():
    manual_show_num(["00011100", "00111010", "10110110", "10011110"])

def update_leds(correct):
    for i in range(0,4):
        if correct[i] == 0:
            leds[i].off()
        elif correct[i] == 2:
            leds[i].on()