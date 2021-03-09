#!/usr/bin/python3

import sys, time
import engine, botplayer
import view_colab as view
import argparse
from google.colab.patches import cv2_imshow
from google.colab import output
import PIL 
import cv2
from matplotlib.pyplot import imshow
from IPython.display import Image
from IPython.display import clear_output 



parser = argparse.ArgumentParser(description='LightHouses AI Contest')
parser.add_argument('-fps', '--fps', type=int, required=False, default=20, help='FPS value to use to display game')
parser.add_argument('-map', '--map', type=str, required=False, default="maps/grid.txt", help='Map file to be used')
parser.add_argument('-bots', '--bots', type=str, nargs='+', required=False, default = ['python examples/RandBot/randbot.py'], help='Bots to play with :) ')
args = parser.parse_args()

cfg_file = args.map
bots = args.bots
DEBUG = False
CONTINUE_ON_ERROR = False

config = engine.GameConfig(cfg_file)
game = engine.Game(config, len(bots))
actors = [botplayer.BotPlayer(game, i, cmdline, debug=DEBUG) for i, cmdline in enumerate(bots)]

for actor in actors:
    actor.initialize()

view = view.GameView(game)

round = 0
while True:
    game.pre_round()
    view.update(args.fps)
    for actor in actors:
        try:
            actor.turn()
        except botplayer.CommError as e:
            if not CONTINUE_ON_ERROR:
                raise
            else:
                print("CommError: " + str(e))
                actor.close()
        view.update(args.fps)
    game.post_round()
    
    clear_output()
    img = cv2.imread("screen.jpeg")
    cv2_imshow(img)
    s = "ROUND {} SCORE: \n".format(round)
    for i in range(len(bots)):
        s += "{} (Robot-{}) : {} points \n".format( game.players[i].name , i, game.players[i].score)
    print(s)
    sys.stdout.flush()

    round += 1

view.update(args.fps)
