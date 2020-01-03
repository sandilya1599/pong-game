# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 22:58:49 2020

@author: sandi
"""

import turtle
import time
from functools import partial

class Paddle(turtle.Turtle):
    def __init__(self,left_side):
        super().__init__()
        self.points = 0
        self.left_side = left_side
        self.freezed = False
        self.speed(0)
        self.shape("square")
        self.color("white")
        self.penup()
        if left_side:
            self.goto(-350,0)
        else:
            self.goto(350,0)
        self.shapesize(stretch_wid=5,stretch_len=1)
        self.showturtle()
    # Moves the paddle up
    def move_paddle_up(self):
        if self.freezed:
            return
        y = self.ycor()
        y += 20
        if y < 250:
            self.sety(y)
    # Moves the paddle down
    def move_paddle_down(self):
        if self.freezed:
            return
        y = self.ycor()
        y -= 20
        if y > -250:
            self.sety(y)
    def freeze(self):
        self.freezed = True
    def unfreeze(self):
        self.freezed = False

class Ball(turtle.Turtle):
    def __init__(self,speed):
        super().__init__()
        self.speed(0)
        self.shape("square")
        self.color("white")
        self.penup()
        self.showturtle()
        self.goto(0,0)
        self.dx = speed
        self.dy = speed
        self.game_paused = False
        self.prev_dx = 0
        self.prev_dy = 0


    # Check the top and bottom borders
    def check_top_and_bottom_borders(self):
        # Condition for top
        touching_border = False
        if ball.ycor() > 280:
            ball.sety(280)
            touching_border = True
        if ball.ycor() < -280:
            ball.sety(-280)
            touching_border = True
        if touching_border:
            ball.dy *= -1

    def collide(self,paddle,left_paddle = False):
        if (abs(self.xcor()) > 330 and abs(self.xcor()) < 350) and  (self.ycor() <paddle.ycor()+50 and self.ycor() > paddle.ycor() -50):
            return True
        else:
            return False
    def update(self,paddle_a,paddle_b):
        collide_with_a = self.collide(paddle_a,True)
        collide_with_b = self.collide(paddle_b)

        if collide_with_a or collide_with_b:
            self.dx *= -1
            if collide_with_a:
                self.setx(-330)
            else:
                self.setx(330)
    def freeze_ball(self,paddle_a,paddle_b):
        if self.game_paused:
            return
        self.game_paused = True
        self.prev_dx,self.prev_dy = self.dx, self.dy
        self.dx = 0
        self.dy = 0
        paddle_a.freeze()
        paddle_b.freeze()

    def unfreeze_ball(self,paddle_a,paddle_b):
        if self.game_paused == False:
            return
        self.game_paused = False
        self.dx = self.prev_dx
        self.dy = self.prev_dy
        paddle_a.unfreeze()
        paddle_b.unfreeze()




window = turtle.Screen()
window.title("Pong game copy")
window.bgcolor("black")
window.setup(width =800,height=600)

score_card= turtle.Turtle()
score_card.speed(0)
score_card.color("white")
score_card.penup()
score_card.hideturtle()
score_card.goto(0,260)

score_card.write("Player A: 0   Player B: 0",align="center",font=("Courier",24,"normal"))


paddle_a = Paddle(True)
paddle_b = Paddle(False)

ball = Ball(4)
window.listen()

window.onkeypress(paddle_a.move_paddle_up,"w")
window.onkeypress(paddle_a.move_paddle_down,"s")

window.onkeypress(paddle_b.move_paddle_up,"Up")
window.onkeypress(paddle_b.move_paddle_down,"Down")


while True:
    window.update()

    # Move the ball
    ball.setx(ball.xcor()+ball.dx)
    ball.sety(ball.ycor()+ball.dy)

    # Check if the ball is touching top or bottom borders
    ball.check_top_and_bottom_borders()

    if ball.xcor() >390 or ball.xcor() < -390:
        if ball.xcor() > 390:
            paddle_a.points += 1
        else:
            paddle_b.points += 1
        score_card.clear()
        score_card.write("Player A: %d   Player B: %d"%(paddle_a.points,paddle_b.points),align="center",font=("Courier",24,"normal"))
        ball.goto(0,0)
        time.sleep(2)
        ball.dx *= -1
    ball.update(paddle_a,paddle_b)
