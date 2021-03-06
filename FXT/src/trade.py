#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from src.stat import Stat

class Trade():
    def __init__(self, instrument, volume, open_price, open_datetime, id=None, **args):
        self.id = id
        self.instrument = instrument
        self.volume = volume
        self.open_rate = open_price
        self.open_datetime = open_datetime
        self.close_rate = "STILL OPEN"
        self.close_datetime = "STILL OPEN"
        self.profit = "STILL OPEN"
        self.args = args
        self.sl = args['sl'] if 'sl' in args else None
        self.tp = args['tp'] if 'tp' in args else None
        self.ts = args['ts'] if 'ts' in args else None

    def __str__(self):
        if self.volume < 0:
            side = "sell"
        else:
            side = "buy"
        ret = "TRADE: " + side + " " + self.instrument[0] + "/" + self.instrument[1] + "\n"
        ret += "\tprofit:\t" + str(self.profit) + "\n"
        ret += "\topen rate:\t" + str(self.open_rate) + "\n"
        ret += "\tclose rate:\t" + str(self.close_rate) + "\n"
        ret += "\trate diff:\t%0.5f" % (self.close_rate - self.open_rate) + "\n"
        ret += "\topen datetime:\t" + str(self.open_datetime) + "\n"
        ret += "\tclose datetime:\t" + str(self.close_datetime) + "\n"
        ret += "\tvolume:\t\t" + str(abs(self.volume)) + "\n"
        ret += "\ttake profit:\t" + str(self.tp) + "\n"
        ret += "\tstop loss:\t" + str(self.sl) + "\n"
        ret += "\ttrailing stop:\t" + str(self.sl) + "\n"
        ret += "\tID:\t\t" + str(self.id) + "\n"
        return ret

    def close(self, close_price, close_datetime):
        self.close_rate = close_price
        self.close_datetime = close_datetime

    def set_profit(self, profit):
        self.profit = profit

    def get_profit(self):
        return (self.close_rate - self.open_rate) * self.volume

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
