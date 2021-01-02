import urllib, schedule
from datetime import datetime, date
from twilio.rest import Client
def get_price(coin):
    u = urllib.urlopen("https://www.coindesk.com/price/" + coin)
    d = u.read()
    print("d: " , d)
    html  = d.decode("utf8")
    u.close()

    start = html.index("price-large") + 42
    end = start + html[start:].index('.')

    price = int(html[start:end].replace(',',''))
    return price

def update():
    today = date.today().strftime("%B %d, %Y")
    time = datetime.now().strftime("%H:%M")

    btc = get_price("bitcoin")
    eth = get_price("ethereum")
    epb = btc*1.0/eth

    with open("ratio.txt", 'r') as f:
        lines = f.readlines()
        prev = lines[-1]
        e = prev.index(" ")
        pretty_prev = prev[:e-1]
        prev = float(pretty_prev)

    change = (epb*1.0/prev) - 1
    msg = str(round(epb,6)) +" eth/btc = " + str(eth)+"/" + str(btc) + " on " + today + " at " + time " .  " + str(round(100*change,7)) + "% from " + str(prev)
    print(msg)

    with open("ratio.txt", 'a') as f:
        f.write(msg+"\n")

    client = Client("ACCOUNT SID","AUTH TOKEN")
    client.messages.create(to="+MY NUMBER",from_="+TWILIO NUMBER", body=msg)

print("\nrunning...")
schedule.every(3).hours.do(update)    

while True:
    schedule.run_pending()
