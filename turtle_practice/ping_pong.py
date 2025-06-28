import turtle as t # importing modules
import random

playerAscore = 0 # initiating playerAscore and playerBscore to track the scores after each time the opponent leaves the ball
playerBscore = 0

window = t.Screen() # it creates a screen or a window to be displayed
window.title('Ping Pong Game') # this will be displayed in the top center of the window opened
window.setup(width=800, height=600) # setting up the height and width
window.tracer(0)

# Available colors

colors = ['black', 'blue', 'green', 'red', 'purple', 'yellow', 'white', 'orange', 'pink']

# Function to choose the background color

def choose_background_color():
    window.bgcolor('black')  # Default background color
    color_message = "Choose your background color:\n"
    color_message += "\n".join([f"{i + 1}: {colors[i]}" for i in range(len(colors))])
    color_choice = window.textinput("Choose Background Color", color_message)
    
    if color_choice is not None:
        try:
            color_choice = int(color_choice) - 1
            if 0 <= color_choice < len(colors):
                window.bgcolor(colors[color_choice])
            else:
                window.bgcolor('black')  # Default if invalid choice
        except ValueError:
            window.bgcolor('black')  # Default if invalid input

# Function to choose the paddle color

def choose_paddle_color():
    paddle_color = 'white'  # Default paddle color
    while True:
        paddle_color_message = "Choose your paddle color:\n"
        paddle_color_message += "\n".join([f"{i + 1}: {colors[i]}" for i in range(len(colors))])
        paddle_color_choice = window.textinput("Choose Paddle Color", paddle_color_message)
        
        if paddle_color_choice is not None:
            try:
                paddle_color_choice = int(paddle_color_choice) - 1
                if 0 <= paddle_color_choice < len(colors):
                    if colors[paddle_color_choice] != window.bgcolor():
                        paddle_color = colors[paddle_color_choice]
                        break
                    else:
                        window.textinput("Invalid Color", "Paddle color cannot be the same as the background color. Please choose another color.")
                else:
                    paddle_color = 'white'  # Default if invalid choice
                    break
            except ValueError:
                paddle_color = 'white'  # Default if invalid input
                break
    return paddle_color

# Function to choose the ball color

def choose_ball_color():
    ball_color = 'green'  # Default ball color
    while True:
        ball_color_message = "Choose your ball color:\n"
        ball_color_message += "\n".join([f"{i + 1}: {colors[i]}" for i in range(len(colors))])
        ball_color_choice = window.textinput("Choose Ball Color", ball_color_message)
        
        if ball_color_choice is not None:
            try:
                ball_color_choice = int(ball_color_choice) - 1
                if 0 <= ball_color_choice < len(colors):
                    if colors[ball_color_choice] != window.bgcolor():
                        ball_color = colors[ball_color_choice]
                        break
                    else:
                        window.textinput("Invalid Color", "Ball color cannot be the same as the background color. Please choose another color.")
                else:
                    ball_color = 'green'  # Default if invalid choice
                    break
            except ValueError:
                ball_color = 'green'  # Default if invalid input
                break
    return ball_color

# Separate function to ask for and return the winning score

def choose_winning_score():
    while True:
        try:
            winning_score = window.numinput("Set Winning Score", "Choose the winning score (Default is 5):", minval=1, maxval=100)
            if winning_score is None:
                winning_score = 5  # Default to 5 if the user cancels or doesn't input anything
            return int(winning_score)
        except ValueError:
            return 5  # Default to 5 if input is invalid

# Function to ask for difficulty level

def choose_difficulty():
    difficulty = window.textinput("Choose Difficulty", "Choose your difficulty:\n1: Easy\n2: Medium\n3: Hard")
    
    if difficulty is not None:
        try:
            difficulty = int(difficulty)
            if difficulty == 1:
                return 2  # Slow speed for easy
            elif difficulty == 2:
                return 3  # Medium speed for medium
            elif difficulty == 3:
                return 4  # Fast speed for hard
            else:
                return 2  # Default to easy if input is invalid
        except ValueError:
            return 2  # Default to easy if input is invalid

# Function to display the current winning score at the bottom of the screen

def display_winning_score(winning_score):
    score_display = t.Turtle()
    score_display.speed(0)
    score_display.color("white")
    score_display.penup()
    score_display.hideturtle()
    score_display.goto(0, -260)
    score_display.clear()
    score_display.write("Winning Score: {}".format(winning_score), align="center", font=("Arial", 18, "normal"))

# Get player preferences for colors and winning score

choose_background_color()
paddle_color = choose_paddle_color()
ball_color = choose_ball_color()
winning_score = choose_winning_score()

# Get difficulty speed
ball_speed = choose_difficulty()

# Set the score text color based on the background color
score_color = "blue"  # Default score color
if window.bgcolor() == "blue":
    score_color = "black"

# Creating left paddle
leftpaddle = t.Turtle()
leftpaddle.shape("square")
leftpaddle.color(paddle_color)
leftpaddle.shapesize(stretch_wid=5, stretch_len=1)
leftpaddle.penup()
leftpaddle.goto(-350, 0)

# Creating right paddle
rightpaddle = t.Turtle()
rightpaddle.shape("square")
rightpaddle.color(paddle_color)
rightpaddle.shapesize(stretch_wid=5, stretch_len=1)
rightpaddle.penup()
rightpaddle.goto(350, 0)

# Creating ball
ball = t.Turtle()
ball.shape("circle")
ball.color(ball_color)
ball.penup()
ball.goto(0, 0)
ballxdirection = ball_speed  # Ball's speed in the X direction
ballydirection = ball_speed  # Ball's speed in the Y direction

# Creating pen for scoreboard
pen = t.Turtle()
pen.speed(0)
pen.color(score_color)
pen.penup()
pen.goto(0, 260)
pen.write("Player A: 0   Player B: 0", align='center', font=('Arial', 24, 'normal'))

# Moving the left paddle
def leftpaddleup():
    y = leftpaddle.ycor()
    if y < 240:
        leftpaddle.sety(y + 20)

def leftpaddledown():
    y = leftpaddle.ycor()
    if y > -240:
        leftpaddle.sety(y - 20)

# Moving the right paddle
def rightpaddleup():
    y = rightpaddle.ycor()
    if y < 240:
        rightpaddle.sety(y + 20)

def rightpaddledown():
    y = rightpaddle.ycor()
    if y > -240:
        rightpaddle.sety(y - 20)

# Function to maintain the ball's speed
def maintain_speed():
    global ballxdirection, ballydirection
    speed = ball_speed
    if ballxdirection > 0:
        ballxdirection = speed
    else:
        ballxdirection = -speed

    if ballydirection > 0:
        ballydirection = speed
    else:
        ballydirection = -speed

# Function to increase ball speed gradually

def increase_ball_speed():
    global ballxdirection, ballydirection
    factor = 1.05
    ballxdirection *= factor
    ballydirection *= factor

# Assign keys to play
window.listen()
window.onkeypress(leftpaddleup, 'w')
window.onkeypress(leftpaddledown, 's')
window.onkeypress(rightpaddleup, 'Up')
window.onkeypress(rightpaddledown, 'Down')

# Flash effect for scoring

def flash_score(player):
    flash = t.Turtle()
    flash.hideturtle()
    flash.color("yellow")
    flash.penup()
    flash.goto(0, 0)
    flash.write(f"Player {player} scores!", align="center", font=("Arial", 24, "bold"))
    t.delay(1000)  # Delay to show the score
    flash.clear()

# Function to display game over screen
def game_over(winner):
    pen.clear()
    pen.goto(0, 0)
    pen.color("red")
    pen.write(f"Player {winner} wins!!", align="center", font=("Arial", 36, "bold"))
    window.update()
    t.delay(2000)  # Delay for 2 seconds
    reset_game()

# Function to reset the game

def reset_game():
    global playerAscore, playerBscore
    playerAscore = 0
    playerBscore = 0
    pen.clear()
    pen.write(f"Player A: {playerAscore}   Player B: {playerBscore}", align='center', font=('Arial', 24, 'normal'))
    ball.goto(0, 0)
    window.update()

# Main game loop
while True:
    window.update()

    # Display the winning score at the bottom of the screen
    display_winning_score(winning_score)

    # Moving the ball
    ball.setx(ball.xcor() + ballxdirection)
    ball.sety(ball.ycor() + ballydirection)

    # Set up border collision
    if ball.ycor() > 290:
        ball.sety(290)
        ballydirection *= -1
        increase_ball_speed()  # Gradually increase ball speed after bounce

    if ball.ycor() < -290:
        ball.sety(-290)
        ballydirection *= -1
        increase_ball_speed()  # Gradually increase ball speed after bounce

    # Ball passes right side (Player A scores)
    if ball.xcor() > 390:
        ball.goto(0, 0)  # Reset ball position
        ballxdirection *= -1
        playerAscore += 1
        pen.clear()
        pen.write(f"Player A: {playerAscore}   Player B: {playerBscore}", align='center', font=('Arial', 24, 'normal'))
        flash_score("A")

    # Ball passes left side (Player B scores)
    if ball.xcor() < -390:
        ball.goto(0, 0)  # Reset ball position
        ballxdirection *= -1
        playerBscore += 1
        pen.clear()
        pen.write(f"Player A: {playerAscore}   Player B: {playerBscore}", align='center', font=('Arial', 24, 'normal'))
        flash_score("B")

    # Handling the collision with the right paddle
    if (340 < ball.xcor() < 350) and (rightpaddle.ycor() - 50 < ball.ycor() < rightpaddle.ycor() + 50):
        ball.setx(340)
        ballxdirection *= -1
        maintain_speed()  # Ensure speed is maintained after bouncing

    # Handling the collision with the left paddle
    if (-350 < ball.xcor() < -340) and (leftpaddle.ycor() - 50 < ball.ycor() < leftpaddle.ycor() + 50):
        ball.setx(-340)
        ballxdirection *= -1
        maintain_speed()  # Ensure speed is maintained after bouncing

    # Check for a winner
    if playerAscore >= winning_score:
        game_over("A")
        break  # Exit loop

    if playerBscore >= winning_score:
        game_over("B")
        break  # Exit loop