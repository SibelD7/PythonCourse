from Portfolio import Portfolio, Stock, MutualFund

p = Portfolio()

p.addCash(250)       # Always works
p.withdrawCash(50)   # Should work
p.withdrawCash(3000) # Insufficient balance

print(p)
p.history()

s1 = Stock(20, "AAPL")
s2 = Stock(35, "GOOG")
p.buyStock(3, s1)   # Should work
p.buyStock(2, s2)   # Should work
p.buyStock(100, s1) # Insufficient balance

print(p)
p.history()

p.sellStock("AAPL", 2)  # Should work
p.sellStock("GOOG", 10) # Not enough GOOG stock
p.sellStock("NASA", 15) # No NASA stock

p.addCash(200)
mf1 = MutualFund("SNCF")
mf2 = MutualFund("DBHN")
p.buyMutualFund(36.8, mf1)  # Should work
p.buyMutualFund(29.45, mf2) # Should work
p.buyMutualFund(9000, mf1)  # Insufficient balance

print(p)
p.history()

p.sellMutualFund("DBHN", 22)  # Should work
p.sellMutualFund("SNCF", 100) # Not enough SNCF funds
p.sellMutualFund("NMBS", 20)  # No NMBS funds

print(p)
p.history()
