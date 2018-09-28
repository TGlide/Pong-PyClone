import pygame
import os

from PPlay.window import *
from PPlay.sprite import *
from PPlay.collision import *
from PPlay.gameimage import *

###########
# Classes #
###########


class Ball(Sprite):
    base_speed = 700

    def __init__(self):
        Sprite.__init__(self, os.path.realpath(__file__)[
                        :-(len("pong.py"))] + "assets" + os.sep + "ball.png")

        self.speed = self.base_speed
        self.speed_x = (self.base_speed*(2**0.5))/2
        self.speed_y = (self.base_speed*(2**0.5))/2

    def update(self):
        self.move_x(self.speed_x * wn.delta_time())
        self.move_y(self.speed_y * wn.delta_time())


class Paddle(Sprite):
    base_speed = 900

    def __init__(self):
        Sprite.__init__(self, os.path.realpath(__file__)[
                        :-(len("pong.py"))] + "assets" + os.sep + "paddle.png")

    def move_key_y(self):
        speed = self.base_speed * wn.delta_time()
        if(Window.get_keyboard().key_pressed("up")):
            if not self.y - speed < 0:
                self.set_position(self.x, self.y - speed)

        if(Window.get_keyboard().key_pressed("down")):
            if not self.y + self.height + speed > wn.height:
                self.set_position(self.x, self.y + speed)


class PaddleCPU(Paddle):
    def move(self, ball):
        speed = self.base_speed * wn.delta_time()
        if ball.y + ball.height > self.y + self.height:
            self.set_position(self.x, self.y + speed)
        elif ball.y < self.y:
            self.set_position(self.x, self.y - speed)


##################
# Game variables #
##################

GAME_STATE = 1
SPEED_MULT = 1.1

################
# Game objects #
################

wn = Window(1280, 800)
wn.set_title("PONG")

fundo = GameImage("assets" + os.sep + "bg.jpg")

ball = Ball()
paddlePlayer = Paddle()
paddleCPU = PaddleCPU()

paddlePlayer.set_position(50, wn.height/2 - paddlePlayer.height/2)
paddleCPU.set_position(wn.width - 50 - paddleCPU.width,
                       wn.height/2 - paddlePlayer.height/2)
ball.set_position(paddlePlayer.x + 50, wn.height/2 - ball.height / 2)

while GAME_STATE:
    # Ball Collision
    # if ball.collided(paddlePlayer) and ball.speed_x < 0:
    #     paddle_center = paddlePlayer.y + paddlePlayer.height/2
    #     ball_center = ball.y + ball.height/2
    #     dif = ball_center - paddle_center
    #     hipoten = ((ball.width)**2 + dif**2)**0.5
    #     sen = (ball.width)/hipoten
    #     cos = dif/hipoten

    #     ball.speed *= SPEED_MULT
    #     ball.speed_x = ball.speed * sen 
    #     ball.speed_y = ball.speed * cos 

    # elif ball.collided(paddleCPU) and ball.speed_x > 0:
    #     paddle_center = paddleCPU.y + paddleCPU.height/2
    #     ball_center = ball.y + ball.height/2
    #     dif = ball_center - paddle_center
    #     hipoten = ((ball.width)**2 + dif**2)**0.5
    #     sen = (ball.width)/hipoten
    #     cos = dif/hipoten

    #     ball.speed *= SPEED_MULT
    #     ball.speed_x = -ball.speed * sen 
    #     ball.speed_y = ball.speed * cos 

    # if ball.y <= 0 and ball.speed_y < 0:
    #     ball.speed_y *= -1
    # elif ball.y + ball.height >= wn.height and ball.speed_y > 0:
    #     ball.speed_y *= -1

    
    if ball.x <= 0 or ball.x + ball.width >= wn.width:
        # paddlePlayer.set_position(50, wn.height/2 - paddlePlayer.height/2)
        # paddleCPU.set_position(wn.width - 50 - paddleCPU.width,
        #                wn.height/2 - paddlePlayer.height/2)
        # ball.__init__()
        # ball.set_position(paddlePlayer.x + 50, wn.height/2 - ball.height / 2)
        ball.speed_x *= -1
    if ball.y <= 0 or ball.y + ball.height >= wn.height:
        ball.speed_y *= -1
        

    # Update Screen
    fundo.draw()
    # paddlePlayer.draw()
    # paddlePlayer.move_key_y()
    # paddleCPU.draw()
    # paddleCPU.move(ball)
    ball.draw()
    ball.update()
    wn.update()

print("Game over.")
