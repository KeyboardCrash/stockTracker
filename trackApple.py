import requests
import json
from datetime import datetime
import time
import os
from win10toast import ToastNotifier
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

os.system('color')
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

ONE_MIN = 60

timestamp = ''

toast = ToastNotifier()

def trackStock():
    while(True):

        storeIdentifier = 'R301'
        product = ''

        proMax128_SB = 'MLJ73VC/A'
        pro128_SB = 'MLUK3VC/A'
        pro256_SB = 'MLUU3VC/A'
        proMax256_G = 'MLJ83VC/A'

        productList = [proMax128_SB, pro128_SB]
        
        for p in productList:
            print("Attempting product", p)
            product = p
            url = f"https://www.apple.com/ca/shop/fulfillment-messages?pl=true&mt=compact&parts.0={product}&searchNearby=true&store={storeIdentifier}"
            print(url, "\n")
            try:
                # r = requests.get(url)
                s = requests.Session()
                retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
                s.mount('https://', HTTPAdapter(max_retries=retries))
                r = s.get(url)
                if (r.status_code == 200):
                    content = r.json()
                else:
                    print("Request failed with status code", r.status_code)
                    break
                s.close()
            except Exception as err:
                print('Exception thrown', err)
                break

            timestamp = datetime.now()
            # print(jsonobj)

            # print(content['body']['availableStoresText'],"\n")

            # Array of stores
            stores = content['body']['content']['pickupMessage']['stores']

            # Iterate over the stores
            for store in stores:
                print("------------------------------------------")
                # print(json.dumps(store['partsAvailability'], indent=4, sort_keys=True))
                availableStock = store['partsAvailability']
                print(timestamp, "-", "Querying inventory at", store['storeName'])
                for stock in availableStock:
                    if ("unavailable" not in availableStock[stock]['pickupDisplay']):
                        print(style.GREEN + str(timestamp), "MODEL IS IN STOCK" + style.RESET)
                        # toast.show_toast("Stock available","Tracked product is in stock",duration=20)

                    print("Product ID:", stock, "Name:", availableStock[stock]['storePickupProductTitle'])
                    print(style.RED + availableStock[stock]['pickupSearchQuote'], "at", store['storeName'], "\n"+style.RESET)

                if not availableStock:
                    print("Location", store['storeName'], "has no stock available")

        print("================================================================================")
        # Check every 5 minutes
        time.sleep(ONE_MIN * 5)


def main():
    print("Starting tracking...")
    trackStock()

main()