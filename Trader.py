class Trader:

    def __init__(self, money, price):
        self.initPrice = price
        self.initCash = money

        self.price = price
        self.cash = money
        self.stocks = 0

    def buystock(self, price):
        self.price = price
        self.stocks = self.cash / price
        self.cash = 0

    def sellStock(self, price):
        self.price = price
        self.cash = price * self.stocks
        self.stocks = 0

    def report(self):
        if self.initCash > self.cash:
            print("You only have %f of your initial %f$" % (100 * (self.initCash / self.cash), self.initCash))
        else:
            print("You gained %f percent you now have %f$" % ((self.initCash / self.cash) * 100), self.cash)

        if self.initPrice > self.price:
            print("The stock price went down by %f percent" % (100 - (self.price / self.initPrice) * 100))
        else:
            print("The stock price went up by %f percent" % (100 - (self.price / self.initPrice) * 100))

        if (self.cash / self.initCash) > (self.price / self.initPrice):
            print("You performed %f percent better than the market" % 100 * (
                    (self.cash / self.initCash) - (self.price / self.initPrice)))
        else:
            print("You performed %f percent worse than the market" % 100 * (
                    (self.cash / self.initCash) - (self.price / self.initPrice)))
