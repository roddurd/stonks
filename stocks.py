import urllib, schedule
from datetime import datetime, date
from twilio.rest import Client


def get_price(coin):

    fp = urllib.urlopen("https://www.coindesk.com/price/" + coin)
    d = fp.read()
    html  = d.decode("utf8")
    fp.close()

    start = html.index("price-large") + 42
    end = start + html[start:].index('.')

    price = int(html[start:end].replace(',',''))
    return price


def update():
    today = date.today().strftime("%B %d, %Y")
    time = datetime.now().strftime("%H:%M")

    btc = get_price("bitcoin")
    eth = get_price("ethereum")

    e2b = eth*1.0/btc

    with open("ratio.txt", 'r') as f:
        lines = f.readlines()
        prev = lines[-1]
        e = prev.index(" ")
        pretty_prev = prev[:e-1]
        prev = float(pretty_prev)

    change = (e2b*1.0/prev) - 1
    msg = str(round(e2b,6)) +" eth/btc = " + str(eth)+"/" + str(btc) + ". Up " + str(round(100*change,7)) + " from " + str(prev)
    print(msg)

    with open("ratio.txt", 'a') as f:
        f.write(msg+"\n")

    if change < -3:
        print("price drop!")
        client = Client("ACab89ceac87267849a5aaa930b7866270", "9ff469eb513f4904c059d7ba3156ca0f")
        client.messages.create(to="+19499813457",from_="+12059736827", body=msg)
    else:
        print("no")

print("\nrunning...")
schedule.every(1).seconds.do(update)    

while True:
    schedule.run_pending()
