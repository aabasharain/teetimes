import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import sys
#import pandas as pd

#urls = "https://foreupsoftware.com/index.php/api/booking/times?time=all&date=01-16-2021&holes=18&players=4&booking_class=3767&schedule_id=4306&schedule_ids[]=0&schedule_ids[]=4306&schedule_ids[]=4334&specials_only=0&api_key=no_limits"

day = {"month":sys.argv[1], "day":sys.argv[2], "year":sys.argv[3]}
#day = {"month":"01", "day":"17", "year":"2021"}
players = 4
# dates = ["01-16-2021", "01-17-2021", "01-18-2021", "01-24-2021"]
# players = ["1", "2", "3", "4"]

##### Monarch #####
base_url = "https://foreupsoftware.com/index.php/api/booking/"
query_url = "times?time=all&date={}-{}-{}&holes=18&players={}&booking_class=3767&schedule_id=4306&schedule_ids[]=0&schedule_ids[]=4306&schedule_ids[]=4334&specials_only=0&api_key=no_limits".format(day["month"], day["day"], day["year"], players)
r = requests.get("{}{}".format(base_url, query_url))
results = (json.loads(r.text))
print("Monarch Bay - {} Tee Times".format(len(results)))
print("Time\tAvail\tGrnFee\tCarFee")
for result in results:
    print(result["time"], result["available_spots"], result["green_fee"], result["cart_fee"])


##### Corica Park #####
base_url = "https://coricapark.ezlinksgolf.com/api/search/search"
#original post request {"date":"01/20/2021","numHoles":0,"numPlayers":4,"startTime":"5:00 AM","endTime":"7:00 PM","courseIDs":[6063,6064],"holdAndReturnOne":False}
post_request = {"date":"{}/{}/{}".format(day["month"], day["day"], day["year"]),"numHoles":0,"numPlayers":4,"startTime":"5:00 AM","endTime":"7:00 PM","courseIDs":[6063],"holdAndReturnOne":False}

r = requests.post(base_url, post_request)

results = json.loads(r.text).get("Reservations", None)
if results is not None:
    print("Corica Park - {} Tee Times".format(len(results)))
    for result in results:
        #print(result)
        print(result["TeeDateDisplay"], result["TeeTimeDisplay"], result["PlayersAvailable"], result["PriceMin"])

##### Las Posita #####
#las pos https://www.chronogolf.com/club/las-positas-golf-course#?date=2021-01-20&course_id=21211&nb_holes=18&affiliation_type_ids=85452,85452,85452,85452
base_url = "https://www.chronogolf.com/marketplace/clubs/18173/teetimes"
query_url = "?date={}-{}-{}&course_id=21211&affiliation_type_ids%5B%5D=85452&affiliation_type_ids%5B%5D=85452&affiliation_type_ids%5B%5D=85452&affiliation_type_ids%5B%5D=85452&nb_holes=18".format(day["year"], day["month"], day["day"])

r = requests.get(f"{base_url}{query_url}")
results = json.loads(r.text)
print("Las Pos - {} Tee Times".format(len([x for x in results if not x["out_of_capacity"]])))
for result in results:
    if not result["out_of_capacity"]:
        print(result["date"], result["start_time"], 4, result["green_fees"][0]["green_fee"])
