#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import time
from matplotlib.ticker import ScalarFormatter

class Stat():
    def __init__(self, balance):
        self.buffer = []
        self.trades = []
        self.initial_account_balance = balance
        self.final_account_balance = balance

        self.profit = []
        self.balance = []

        pd.options.display.mpl_style = 'default'
        plt.ion()

    def add_tick(self, tick):
        self.buffer.append(tick)

    def add_trade(self, trade):
        """
        Add closed trade to the stats module for future processing.
        @param Trade: Trade class isntance
        @return: none
        """
        self.trades.append(trade)
        # add to profit
        self.profit.append((trade.close_datetime, trade.profit))
        # add to balance
        self.balance.append((trade.open_datetime, self.final_account_balance))
        self.final_account_balance += trade.profit
        self.balance.append((trade.close_datetime, self.final_account_balance))

    def prepare_plot(self, resample='5min'):
        """
        Perpare data sent to the Statistics module for the plotting purpose
        @param resample: String Resample output data for faster plot. See pandas resample for viable inputs
        @return: dictitonary with prices, balance and profit keys
        """
        ret = {}
        prices_df = pd.DataFrame(self.buffer, columns=['datetime', 'buy', 'sell'])
        prices_df.set_index('datetime', inplace=True)
        ret['prices'] = prices_df.resample(resample, how={'buy':'mean', 'sell':'mean'})

        balance_df = pd.DataFrame(self.balance, columns=['datetime', 'balance'])
        balance_df.set_index('datetime', inplace=True)
        ret['balance'] = balance_df.resample(resample, how={'balance':'last'}).fillna(method='bfill')

        profit_df = pd.DataFrame(self.profit, columns=['datetime', 'profit'])
        profit_df.set_index('datetime', inplace=True)
        ret['profit'] = profit_df.resample(resample, how={'profit':'last'}).fillna(method='bfill')
        return ret

    def __str__(self):
        profitable_trade_count = 0
        profitable_trade_profit = 0
        nonprofitable_trade_count = 0
        nonprofitable_trade_profit = 0
        trade_count = len(self.trades)
        for trade in self.trades:
            if trade.profit > 0:
                profitable_trade_count += 1
                profitable_trade_profit += trade.profit
            else:
                nonprofitable_trade_count += 1
                nonprofitable_trade_profit += trade.profit

        ret = "Statistics:\n"
        ret += "\tTrade count: " + str(trade_count) + "\n"
        ret += "\tProfitable trades:\n"
        ret += "\t\tCount: " + str(profitable_trade_count) + "\n"
        ret += "\t\tProfit: " + str(profitable_trade_profit) + "\n"
        ret += "\tNon-profitable trades \n"
        ret += "\t\tCount: " + str(nonprofitable_trade_count) + "\n"
        ret += "\t\tProfit: " + str(nonprofitable_trade_profit) + "\n"
        ret += "\tOverall profit: " + str(profitable_trade_profit + nonprofitable_trade_profit) + "\n"
        ret += "\tInitial account balance: " + str(self.initial_account_balance) + "\n"
        ret += "\tFinal account balance: " + str(self.final_account_balance) + "\n"
        return ret

    def plot(self, what=['balance'], show_trades='all'):
        """
        Prints out graphical representation of all the trades
        @param what: List. Describes what should be drawn to the target graph (['balance'], ['profit'] or ['balance', 'profit'])
        @param show_tradesL String. Show all the trades ('all', '+' - profitable in green, '-' - non profitable in red)
        @return: none
        """
        data = self.prepare_plot()

        fig, ax = plt.subplots(nrows=len(what)+1, sharex=True)

        # allways plot prices
        data['prices'].plot(ax=ax[0])
        ax[0].ticklabel_format(axis='y', useOffset=False)
        ax[0].set_ylabel('prices')

        # plot other parameters
        for i, key in enumerate(what):
            if key in data:
                data[key].plot(ax=ax[i+1])
                ax[i+1].ticklabel_format(axis='y', useOffset=False)
                ax[i+1].set_ylabel(key)
        if show_trades:
            for trade in self.trades:
                if show_trades == 'all':
                    for axe in ax:
                        if trade.profit > 0:
                            if trade.volume > 0:
                                axe.axvspan(xmin=trade.open_datetime, xmax=trade.close_datetime, facecolor='g', alpha=0.5)
                            else:
                                axe.axvspan(xmin=trade.open_datetime, xmax=trade.close_datetime, facecolor='g', alpha=0.5)
                        else:
                            if trade.volume > 0:
                                axe.axvspan(xmin=trade.open_datetime, xmax=trade.close_datetime, facecolor='r', alpha=0.5)
                            else:
                                axe.axvspan(xmin=trade.open_datetime, xmax=trade.close_datetime, facecolor='r', alpha=0.5)
                elif show_trades == '+':
                    if trade.profit > 0:
                        for axe in ax:
                            axe.axvspan(xmin=trade.open_datetime, xmax=trade.close_datetime, facecolor='g', alpha=0.5)
                elif show_trades == '-':
                    if trade.profit <= 0:
                        for axe in ax:
                            axe.axvspan(xmin=trade.open_datetime, xmax=trade.close_datetime, facecolor='r', alpha=0.5)
        plt.show(block=True)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
