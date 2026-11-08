import turtle
import random
import time  # 1. Přidán import času

wn = turtle.Screen()
wn.title("birdo")
wn.bgcolor("blue")
wn.setup(width=800, height=600) 
wn.tracer(0)

# birdo
bird = turtle.Turtle()
bird.shape("square")
bird.color("yellow")
bird.penup()
bird.goto(-200, 0)
bird.dx = 0
bird.dy = 0
bird.gravity = 0.5

def flap():
    bird.dy = 8

wn.listen()
wn.onkeypress(flap, "space")

# trubky
pipes = []

def create_pipe():
    pipe_top = turtle.Turtle() 
    pipe_top.speed(0)
    pipe_top.shape("square")
    pipe_top.color("green")
    pipe_top.penup()
    pipe_top.shapesize(stretch_wid=20, stretch_len=4)
    pipe_top.goto(400, random.randint(100, 300))

    pipe_bottom = turtle.Turtle()  
    pipe_bottom.speed(0)
    pipe_bottom.shape("square")
    pipe_bottom.color("green")
    pipe_bottom.penup()
    pipe_bottom.shapesize(stretch_wid=20, stretch_len=4)
    pipe_bottom.goto(400, pipe_top.ycor() - 500)

    pipes.append((pipe_top, pipe_bottom))

def move_pipes():
    for pipe_top, pipe_bottom in list(pipes):
        pipe_top.setx(pipe_top.xcor() - 3) 
        pipe_bottom.setx(pipe_bottom.xcor() - 3)

        if pipe_top.xcor() < -400:
            pipe_top.hideturtle()
            pipe_bottom.hideturtle()
            pipes.remove((pipe_top, pipe_bottom))

def move_birdo():
    bird.dy += bird.gravity
    bird.sety(bird.ycor() + bird.dy)

score = 0
pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

def update_score():
    global score
    score += 1
    pen.clear()
    pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

counter = 0

# Hlavní herní smyčka
while True:
    wn.update()

    counter += 1
    if counter >= 100:
        create_pipe()
        counter = 0

    move_birdo()
    move_pipes()

    # Kolize se zemí
    if bird.ycor() < -290:
        bird.sety(-290)
        bird.dy = 0

    # Kontrola kolizí s trubkami
    for pipe_top, pipe_bottom in pipes:
        if (bird.xcor() + 10 > pipe_top.xcor() - 40 and bird.xcor() - 10 < pipe_top.xcor() + 40) and \
           (bird.ycor() + 10 > pipe_top.ycor() - 200 or bird.ycor() - 10 < pipe_bottom.ycor() + 200):
            bird.goto(-200, 0)
            bird.dy = 0
            score = 0
            pen.clear()
            pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

        # Přičtení skóre
        if abs(pipe_top.xcor() - bird.xcor()) < 1.5 and not getattr(pipe_top, "passed", False):
            pipe_top.passed = True
            update_score()

    time.sleep(0.02)  # 2. Zabrání zamrznutí okna a zajistí plynulý pohyb