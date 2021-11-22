from gpiozero import Button, LED

led1 = LED(10)
led2 = LED(9)
led3 = LED(8)
led4 = LED(7)

def goleft():
    led1.on()
def goright():
    led2.on()
def goup():
    led3.on()
def godown():
    led4.on()
def goselect():
    led1.off()
    led2.off()
    led3.off()
    led4.off()

left = Button(5)
right = Button(12)
up = Button(6)
down = Button(13)
select = Button(26)

left.when_pressed = goleft
right.when_pressed = goright
up.when_pressed = goup
down.when_pressed = godown
select.when_pressed = goselect