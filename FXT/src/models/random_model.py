#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from datetime import datetime, timedelta

from src.model import Model

class RandomModel(Model):
    """
    Model class
    """
    def __init__(self, *args, **kwargs):
        super(RandomModel, self).__init__(*args, **kwargs)
        self.last_trade_datetime = None
        self.trade_now = False
    
    def train(self):
        pass

    def pre_trade_loop(self):
        pass

    def post_trade_loop(self):
        print(self.broker.stat)
        self.broker.stat.plot(show_trades='all', what=['balance'])

    def trade_loop(self, tick):
        # trade decision
        if not self.last_trade_datetime:
            self.last_trade_datetime = tick.datetime
            self.trade_now = True
        else:
            if (tick.datetime > self.last_trade_datetime + timedelta(minutes=120)):
                self.last_trade_datetime = self.last_trade_datetime + timedelta(minutes=120)
                self.trade_now = True
            else:
                self.trade_now = False
        
        # open a trade
        # should we buy or sell?
        if self.trade_now:
            # is there some open trade? If so close it
            for trade in self.trades:
                ret = self.close_position(self.broker, trade)
                print(ret)
 
            choice_list = [1, -1]
            operation = random.choice(choice_list)
            in_trade = self.open_position(self.broker, self.instrument, 1000*operation)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
