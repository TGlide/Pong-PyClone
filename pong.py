import pygame
import os
import random

from PPlay.window import *
from PPlay.sprite import *
from PPlay.collision import *
from PPlay.gameimage import *
from PPlay.sound import *
from PPlay.font import *

#############
# Functions #
#############


def predict_ball(ball, width, height, dx, direction="right"):
    # sx_mod = abs(bsx)
    # sy_mod = abs(bsy)
    bx, by, bsx, bsy = ball.x, ball.y, ball.speed_x, ball.speed_y
    distx = disty = 0
    while [bx >= dx, bx + ball.width <= dx][direction == "right"]:
        if bsy < 0:
            distx = (bsx*(by))/abs(bsy)
            disty = by
            by = 0
        elif bsy > 0:
            distx = bsx*(height-by-ball.height)/bsy
            disty = height - by
            by = height - ball.height
        else:
            return by
        bx += distx
        bsy *= -1

    bx -= distx
    by = [by - disty, by + disty][bsy > 0]
    bsy *= -1
    distx = dx-bx
    if bsy < 0:
        return by - distx*abs(bsy)/bsx
    return by + distx*abs(bsy)/bsx


def font_path(name):
    return os.path.realpath(__file__)[:-(len("pong.py"))] + "assets" + os.sep + name + ".ttf"


###########
# Classes #
###########


class Ball(Sprite):
    base_speed = 1000

    def __init__(self):
        Sprite.__init__(self, os.path.realpath(__file__)[
                        :-(len("pong.py"))] + "assets" + os.sep + "ball.png")

        self.speed = self.base_speed
        self.speed_x = (self.speed*(2**0.5))/2
        self.speed_y = (self.speed*(2**0.5))/2
        # self.speed_x = self.speed
        # self.speed_y = 0

    def update(self):
        self.move_x(self.speed_x * wn.delta_time())
        self.move_y(self.speed_y * wn.delta_time())


class Paddle(Sprite):
    base_speed = 1000

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
    base_speed = 500

    def move(self, ball):
        speed = self.base_speed * wn.delta_time()
        if self.prediction > self.y + self.height/2 + 5 and self.y + self.height < wn.height:
            self.set_position(self.x, self.y + speed)
        elif self.prediction + ball.height < self.y + self.height/2 - 5 and self.y > 0:
            self.set_position(self.x, self.y - speed)


class Score(Font):
    def __init__(self):
        Font.__init__(self, "0", size=100, aa=True, color=(
            255, 255, 255), font_family=font_path("arcadeclassic"),local_font=True)
        self.score = 0

    def add_score(self):
        self.score += 1
        self.change_text(str(self.score))

##################
# Game variables #
##################


GAME_STATE = 1
SPEED_MULT = 1.1
SPEED_ADD = 50
SPEED_MAX = 2500
last_speed = 0
WIN_W = 1200
WIN_H = 800

################
# Game objects #
################

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 1024)

wn = Window(WIN_W, WIN_H)
wn.set_title("PONG")

# Menu Objects
title = Font("PONG", font_family=font_path("arcadeclassic"),
             size=150, color=(255, 255, 255), local_font=True)
title.set_position(WIN_W/2 - title.width/2, WIN_H/2 - title.height)

prompt = Font("Press space to start", font_family=font_path("arcadeclassic"),
              size=50, color=(255, 255, 255), local_font=True)
prompt.set_position(WIN_W/2 - prompt.width/2, title.y + title.height + 100)

# Main Game Objects
wallHitSFX = Sound(os.path.realpath(__file__)[
                        :-(len("pong.py"))] + "assets" + os.sep + "wallBlip.ogg")
paddleHitSFX = Sound(os.path.realpath(__file__)[
                        :-(len("pong.py"))] + "assets" + os.sep + "pb.ogg")
pointSFX = Sound(os.path.realpath(__file__)[
                        :-(len("pong.py"))] + "assets" + os.sep + "pointBlip.ogg")

fundo = GameImage(os.path.realpath(__file__)[
                        :-(len("pong.py"))] + "assets" + os.sep + "bg.png", size=(WIN_W, WIN_H))

ball = Ball()
ballPred = Sprite(os.path.realpath(__file__)[
                        :-(len("pong.py"))] + "assets" + os.sep + "ball_pred.png")

# CPU vs CPU
# paddlePlayer = PaddleCPU()
# paddlePlayer.prediction = wn.height/2 - ball.height/2

# P1 vs CPU
paddlePlayer = Paddle()

paddleCPU = PaddleCPU()
paddleCPU.prediction = predict_ball(ball, wn.width, wn.height, paddleCPU.x)
scorePlayer = Score()
scoreCPU = Score()

ball.set_position(paddlePlayer.x + 100, random.randint(0, WIN_H - ball.height))
paddlePlayer.set_position(50, wn.height/2 - paddlePlayer.height/2)
paddleCPU.set_position(wn.width - 50 - paddleCPU.width,
                       wn.height/2 - paddlePlayer.height/2)
scorePlayer.set_position(wn.width/4 - scorePlayer.width/2, 50)
scoreCPU.set_position(wn.width/2 + wn.width/4 - scoreCPU.width/2, 50)

# Menu Loop
while True:
    if wn.get_keyboard().key_pressed("space"):
        break
    wn.set_background_color((0, 0, 0))
    title.draw()
    prompt.draw()
    wn.update()
while GAME_STATE:
    # Ball Collision against paddles
    if ball.collided(paddlePlayer) and ball.speed_x < 0:
        # Play SFX
        paddleHitSFX.play()
        # Calculate ball angle hit
        paddle_center = paddlePlayer.y + paddlePlayer.height/2
        ball_center = ball.y + ball.height/2
        dif = ball_center - paddle_center
        hipoten = ((ball.width)**2 + dif**2)**0.5
        sen = (ball.width)/hipoten
        cos = dif/hipoten
        # Update ball speeds according to angle
        if ball.speed < SPEED_MAX:
            ball.speed += SPEED_ADD
            # ball.speed *= SPEED_MULT
        ball.speed_x = ball.speed * sen
        ball.speed_y = ball.speed * cos
        # Ball prediction
        paddleCPU.prediction = predict_ball(
                ball, wn.width, wn.height, paddleCPU.x)
        ballPred.x = paddleCPU.x - ball.width
        ballPred.y = paddleCPU.prediction


    elif ball.collided(paddleCPU) and ball.speed_x > 0:
        # Play SFX
        paddleHitSFX.play()
        # Calculate ball angle hit
        paddle_center = paddleCPU.y + paddleCPU.height/2
        ball_center = ball.y + ball.height/2
        dif = ball_center - paddle_center
        hipoten = ((ball.width)**2 + dif**2)**0.5
        sen = (ball.width)/hipoten
        cos = dif/hipoten
        # Update ball speeds according to angle
        if ball.speed < SPEED_MAX:
            ball.speed += SPEED_ADD
            # ball.speed *= SPEED_MULT
        ball.speed_x = -ball.speed * sen
        ball.speed_y = ball.speed * cos
        # Ball Prediction (CPU vs CPU)
        # paddlePlayer.prediction = predict_ball(
        #         ball, wn.width, wn.height, paddlePlayer.x, direction="left")
        # ballPred.x = paddlePlayer.x+paddlePlayer.width
        # ballPred.y = paddlePlayer.prediction


    # Ball hits wall
    if ball.y <= 0 and ball.speed_y < 0:
        ball.speed_y *= -1
        # Play SFX
        wallHitSFX.play()

    elif ball.y + ball.height >= wn.height and ball.speed_y > 0:
        ball.speed_y *= -1
        # Play SFX
        wallHitSFX.play()

    # Someone Scored: Reset game and update score
    if ball.x <= 0 or ball.x + ball.width >= wn.width:
        # Update Score
        if ball.x <= 0:
            scoreCPU.add_score()
            scoreCPU.set_position(wn.width/2 + wn.width /
                                  4 - scoreCPU.width/2, 50)
        else:
            scorePlayer.add_score()
            scorePlayer.set_position(wn.width/4 - scorePlayer.width/2, 50)
        # Reset Game
        paddlePlayer.set_position(50, wn.height/2 - paddlePlayer.height/2)
        paddleCPU.set_position(wn.width - 50 - paddleCPU.width,
                               wn.height/2 - paddlePlayer.height/2)
        ball.__init__()
        ball.set_position(paddlePlayer.x + 50, wn.height/2 - ball.height / 2)
        # Play SFX
        pointSFX.play()

    # Update Screen
    fundo.draw()
    paddlePlayer.draw()
    paddlePlayer.move_key_y()
    
    # CPU vs CPU ball pred
    # if ball.speed_x < 0:
    #     paddlePlayer.prediction = predict_ball(
    #             ball, wn.width, wn.height, paddlePlayer.x, direction="left")
    #     ballPred.x = paddlePlayer.x+paddlePlayer.width
    #     ballPred.y = paddlePlayer.prediction
    #     ballPred.draw()
    # paddlePlayer.move(ball)
    
    paddleCPU.draw()
    if ball.speed_x > 0:
        paddleCPU.prediction = predict_ball(
                ball, wn.width, wn.height, paddleCPU.x)
        ballPred.x = paddleCPU.x - ball.width
        ballPred.y = paddleCPU.prediction
        ballPred.draw()
    paddleCPU.move(ball)

    ball.draw()
    ball.update()

    scorePlayer.draw()
    scoreCPU.draw()

    # if ball.speed != last_speed:
    #     last_speed = ball.speed
    #     print(ball.speed)

    wn.update()


print("Game over.")
