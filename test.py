from gpiozero import Button

def goleft():
    print("left")
def goright():
    print("right")
def goup():
    print("up")
def godown():
    print("down")
def goselect():
    print("select")

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