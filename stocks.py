import urllib
from datetime import datetime, date

today = date.today().strftime("%B %d, %Y")
time = datetime.now().strftime("%H:%M")

fp = urllib.urlopen("https://www.coindesk.com/price/bitcoin")
d = fp.read()
html  = d.decode("utf8")
fp.close()

start = html.index("price-large") + 42
end = start + html[start:].index('.')

price = int(html[start:end].replace(',',''))
pretty_price = "$" + html[start:end]

with open("prices.txt", 'r') as f:
    lines = f.readlines()
    prev = lines[-1]
    e = prev.index("on")
    prev = int(prev[1:e-1].replace(',', ''))

with open("prices.txt", 'a') as f:
    f.write("\n"+ pretty_price  + " on " + today + " at " + time )

print("wrote to file for " + today)

change = (price-prev)/prev 
print("% change: ", price-prev)

if change < 0:
    print("yes")
else:
    print("no")
    
    
