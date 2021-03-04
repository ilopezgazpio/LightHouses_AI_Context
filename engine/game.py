#!/usr/bin/python3

import sys, time
import engine, botplayer
import view
import argparse

parser = argparse.ArgumentParser(description='LightHouses AI Contest')
parser.add_argument('-map', '--map', type=str, required=True, default="maps/grid.txt", help='Map file to be used')
parser.add_argument('-bots', '--bots', type=str, nargs='+', required=True, help='Bots to play with :) ')
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
    view.update()
    for actor in actors:
        try:
            actor.turn()
        except botplayer.CommError as e:
            if not CONTINUE_ON_ERROR:
                raise
            else:
                print("CommError: " + str(e))
                actor.close()
        view.update()
    game.post_round()
    s = "########### ROUND %d SCORE: " % round
    for i in range(len(bots)):
        s += "P%d: %d " % (i, game.players[i].score)
    print(s)
    round += 1

view.update()
