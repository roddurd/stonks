import urllib, schedule
from datetime import datetime, date
from twilio.rest import Client

def update():
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
        pretty_prev = prev[:e-1]
        prev = int(prev[1:e-1].replace(',', ''))

    change = round(100*(price-prev)/prev, 2)
    print(pretty_price, " , % change: ", change, "\n")

    with open("prices.txt", 'a') as f:
        f.write("\n"+ pretty_price  + " on " + today + " at " + time + ". " + str(change) + "% change from last logged price.")

    client = Client("ACab89ceac87267849a5aaa930b7866270", "9ff469eb513f4904c059d7ba3156ca0f")
    if change < -3:
        print("price drop!")
        client.messages.create(to="+19499813457",from_="+12059736827", body="BTC @ " + pretty_price + ", down " + str(change) + "% from " + pretty_prev)
    elif price < 20000:
        print("below 20k!")
        client.messages.create(to="+19499813457",from_="+12059736827", body="BTC @ " + pretty_price + ", down " + str(change) + "% from " + pretty_prev)
    else:
        print("nothing interesting...")

print("running...")
schedule.every(1).hour.do(update)    

while True:
    schedule.run_pending()
