import turtle as t
from turtle import Turtle

tur = t.Screen() # setting up an instance of class
tur.title('demo') # window title
tur.bgcolor("white") # setting background color as orange
name = tur.textinput('window ', 'enter you name:')

display = t.Turtle()
display.goto(0, 250)
display.write(f'Welcome {name}', align="center", font=("Arial", 36, "bold"))
display.goto(0,200)
display.write('ID : 14', align="center", font=("Arial", 36, "bold"))

image_path = "Distance_Estimation//1. generate_markers//markers//marker_14.png"
# tur.register_shape(image_path)  # only gif files are supported
tur.bgpic(image_path)
def color_to_blue():
    tur.bgcolor('blue')

def color_to_red():
    tur.bgcolor('red')
tur.onkeypress(color_to_red, 'r')
tur.listen()
tur.onkeypress(color_to_blue, 'b')

tur.listen()
display.forward(250)
display.left(130)
t.done()
tur.tracer(0)
tur.mainloop() # holds the window unitll closing
