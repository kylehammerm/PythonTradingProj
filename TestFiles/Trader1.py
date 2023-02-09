import pandas as pd

class Trader:
    def __init__(self, money, price):
        self.initPrice = price
        self.initCash = money

        self.price = price
        self.cash = money

        self.stocks = 0
        self.own = 0

        d = {'Price': [self.initPrice], 'Own': [self.own]}
        self.df = pd.DataFrame(data=d)

    def buystock(self):
        if self.cash != 0:
            self.own = 1
            self.stocks = self.cash / self.price
            self.cash = 0

    def sellStock(self):
        if self.stocks != 0:
            self.own = 0
            self.cash = self.price * self.stocks
            self.stocks = 0

    def singalInterp(self, signal, price):
        self.price = price
        if signal == 0:
            self.buystock()
        else:
            self.sellStock()

    def report(self):
        self.sellStock()

        cp = (self.cash - self.initCash) / self.initCash * 100
        pp = (self.price - self.initPrice) / self.initPrice * 100

        if self.initCash > self.cash:
            print('You only have {:.2f} of your initial {:.2f}$'.format(self.initCash + (cp * self.initCash / 100), self.initCash))
        else:
            print("You gained {:.2f} percent you now have {:.2f}$".format(cp, self.cash))

        if self.initPrice > self.price:
            print("The stock price went down by {:.2f} percent".format(pp))
        else:
            print("The stock price went up by {:.2f} percent".format(pp))

        if (self.cash / self.initCash) > (self.price / self.initPrice):
            print("You performed {:.2f} percent better than the market".format(cp - pp))
        else:
            print("You performed {:.2f} percent worse than the market".format(cp - pp))
