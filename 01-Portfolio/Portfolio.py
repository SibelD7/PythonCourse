from random import uniform

class Stock(object):

    def __init__(self, buyPrice, tickerSymbol):
        self.buyPrice = buyPrice
        self.tickerSymbol = tickerSymbol

    def __repr__(self):
        return "Stock: {0!s} (Share bought at {1!s})".format(self.tickerSymbol, self.buyPrice)

class MutualFund(object):

    def __init__(self, tickerSymbol):
        self.tickerSymbol = tickerSymbol

    def __repr__(self):
        return "Mutual Fund: {0!s}".format(self.tickerSymbol)

class Portfolio(object):

    def __init__(self):
        self._cashAvailable = 0
        self._auditLog = []
        self._stockPortfolio = {}      # { "GOOG": [s, s, s, s], "AAPL": [s, s, s, s], ... }
        self._mutualFundPortfolio = {} # { "DBNK": 2.3, "SNCF": 10.6, ... }

    def __repr__(self):
        reprString = ""

        # Cash first
        reprString += "Cash:\n    {0!s}\n".format(self._cashAvailable)

        # Now stocks
        reprString += "Stocks:\n"
        for tickerSymbol in self._stockPortfolio.keys():
            reprString += "    {0!s}: {1!s} units\n".format(tickerSymbol, len(self._stockPortfolio[tickerSymbol]))

        # And finally mutual funds
        reprString += "Mutual Funds:\n"
        for tickerSymbol in self._mutualFundPortfolio.keys():
            reprString += "    {0!s}: {1!s} units\n".format(tickerSymbol, self._mutualFundPortfolio[tickerSymbol])

        return reprString

    def _addAuditMessage(self, message):
        self._auditLog.append(message)

    def history(self):
        for item in self._auditLog:
            print(item)

    def addCash(self, amount):
        self._cashAvailable = self._cashAvailable + amount
        self._addAuditMessage("Cash deposited: " + str(amount))

    def withdrawCash(self, amount):
        if amount > self._cashAvailable:
            self._addAuditMessage("Cash withdrawal of amount " + str(amount) +" failed: insufficient balance")
            return
        self._cashAvailable = self._cashAvailable - amount
        self._addAuditMessage("Cash widthdrawn: " + str(amount))

    def buyStock(self, units, stock):
        # Check if enough cash balance is available to buy the stock
        if (units * stock.buyPrice) > self._cashAvailable:
            self._addAuditMessage("Stock buy failed due to insufficient balance: {0!s} units of {1!s} stock".format(
                units, stock.tickerSymbol))
            return

        # Deduct the money from the account
        self._cashAvailable -= (units * stock.buyPrice)

        # Store the stock
        # If we never bought this stock before, then create a new key in our portfolio,
        # and put an empty list there
        if stock.tickerSymbol not in self._stockPortfolio.keys():
            self._stockPortfolio[stock.tickerSymbol] = []

        # Now store unit copies of this stock in our list
        for _ in range(0, units):
            self._stockPortfolio[stock.tickerSymbol].append(stock)

        # Add the audit message
        self._addAuditMessage("Stock purchased: {0!s} units of {1!s}".format(units, stock.tickerSymbol))

    def sellStock(self, tickerSymbol, units):
        # Do we even have enough stock avaiilable to sell?
        if not tickerSymbol in self._stockPortfolio.keys():
            self._addAuditMessage("Sell stock failed: no {0!s} stock available".format(tickerSymbol))
            return
        if len(self._stockPortfolio[tickerSymbol]) < units:
            self._addAuditMessage("Sell stock failed: not enough units of {0!s} stock available (requested {1!s}, available {2!s})".format(
                tickerSymbol, units, len(self._stockPortfolio[tickerSymbol])))
            return

        # Sell stock - pop the last n items off the stock list and add the sellPrice to
        # our cash balance
        for _ in range(0, units):
            share = self._stockPortfolio[tickerSymbol].pop()
            self._cashAvailable += uniform(0.5 * share.buyPrice, 1.5 * share.buyPrice)
        self._addAuditMessage("Sold {0!s} units of {1!s} stock".format(units, tickerSymbol))

    def buyMutualFund(self, units, fund):
        # Since all mutual funds cost 1 currency unit, we just need to check we have
        # "units" amount of money available
        if units > self._cashAvailable:
            self._addAuditMessage("Mutual Fund buy failed due to insufficient balance: {0!s} units of {1!s} funds".format(
                units, fund.tickerSymbol))
            return

        # Deduct the money from the account
        self._cashAvailable -= units

        # Store the fund
        # If we never bought this fund before, then create a new key in our portfolio,
        # and put zero
        if fund.tickerSymbol not in self._mutualFundPortfolio.keys():
            self._mutualFundPortfolio[fund.tickerSymbol] = 0.0

        # Now add units of the mutual funds to our fund portfolio
        self._mutualFundPortfolio[fund.tickerSymbol] += units

        # Add the audit message
        self._addAuditMessage("Mutual Fund purchased: {0!s} units of {1!s}".format(units, fund.tickerSymbol))

    def sellMutualFund(self, tickerSymbol, units):
        # Do we even have enough stock avaiilable to sell?
        if not tickerSymbol in self._mutualFundPortfolio.keys():
            self._addAuditMessage("Sell mutual fund failed: no {0!s} funds available".format(tickerSymbol))
            return
        if self._mutualFundPortfolio[tickerSymbol] < units:
            self._addAuditMessage("Sell mutual fund failed: not enough units of {0!s} fund available (requested {1!s}, available {2!s})".format(
                tickerSymbol, units, self._mutualFundPortfolio[tickerSymbol]))
            return

        # Sell mutual funds
        sellPrice = uniform(0.9, 1.2)
        self._mutualFundPortfolio[tickerSymbol] -= units
        self._cashAvailable += sellPrice * units
        self._addAuditMessage("Sold {0!s} units of {1!s} mutual funds".format(units, tickerSymbol))
