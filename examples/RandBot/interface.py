#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, json
from bot import Bot
# ==============================================================================
# Interfaz
# ==============================================================================

class Interface(object):
    def __init__(self, bot_class):
        self.bot_class = bot_class
        self.bot = None
    
    def _recv(self):
        line = sys.stdin.readline()
        if not line:
            sys.exit(0)
        return json.loads(line)

    def _send(self, msg):
        sys.stdout.write(json.dumps(msg) + "\n")
        sys.stdout.flush()

    def run(self):
        init = self._recv()
        self.bot = self.bot_class(init)
        self._send({"name": self.bot.NAME})
        while True:
            state = self._recv()
            move = self.bot.play(state)
            self._send(move)
            status = self._recv()
            if status["success"]:
                self.bot.success()
            else:
                self.bot.error(status["message"], move)

if __name__ == "__main__":
    iface = Interface(Bot)
    iface.run()
