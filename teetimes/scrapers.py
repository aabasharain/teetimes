import requests
import json
import pandas as pd
from abc import abstractmethod
from datetime import datetime
from teetimes.tee_time import TeeTime
from typing import List

class Scraper:
    """Interface class for website scrapers.
    """

    def __init__(self, date: datetime, num_players: int) -> None:
        self._date = date
        self._num_players = num_players
        self._tee_times = self._scrape_tee_times()

    @abstractmethod
    def _scrape_tee_times(self) -> pd.DataFrame:
        pass

    @property
    def tee_times(self) -> pd.DataFrame:
        """Get tee time in pandas data frame

        Returns:
            pd.DataFrame: Tee time with columns Date, Time, Number of Players, Green Fee, Cart Fee
        """
        if self._tee_times is None:
            return pd.DataFrame(TeeTime(self._date, 0, 0, 0).tee_time_table)
        return self._tee_times

class MonarchBay(Scraper):
    """Web scraper for Monarch Bay golf course in San Leandro, CA
    """

    def _scrape_tee_times(self) -> pd.DataFrame:
        base_url = "https://foreupsoftware.com/index.php/api/booking/"
        query_url = f"times?time=all&date={self._date.month}-{self._date.day}-{self._date.year}&holes=18&players={self._num_players}&booking_class=3767&schedule_id=4306&schedule_ids[]=0&schedule_ids[]=4306&schedule_ids[]=4334&specials_only=0&api_key=no_limits"
        request = requests.get(f"{base_url}{query_url}")
        results = (json.loads(request.text))
        tee_times = None
        for result in results:
            # date and time comes out from scrape as YYYY-MM-DD HH:MM as a string
            hour, minute = [int(x) for x in str(result['time']).split()[1].split(":")]
            date_and_time = datetime(self._date.year, self._date.month,
                                     self._date.day, hour=hour, minute=minute)
            new_tee_time = TeeTime(date_and_time, result['available_spots'],
                                   result['green_fee'], result['cart_fee'])
            if tee_times is None:
                tee_times = pd.DataFrame(new_tee_time.tee_time_table)
            else:
                tee_times = pd.concat([tee_times, new_tee_time.tee_time_table], ignore_index=True)

        return tee_times

class CoricaPark(Scraper):
    """Web scraper for Corica Park golf course
    """

    def _scrape_tee_times(self) -> pd.DataFrame:
        base_url = "https://coricapark.ezlinksgolf.com/api/search/search"
        #original post request 
        # {"date":"01/20/2021","numHoles":0,"numPlayers":4,
        #  "startTime":"5:00 AM","endTime":"7:00 PM","courseIDs":[6063,6064],
        #  "holdAndReturnOne":False}
        post_request = {"date":f"{self._date.month}/{self._date.day}/{self._date.year}","numHoles":0,"numPlayers":4,"startTime":"5:00 AM","endTime":"7:00 PM","courseIDs":[6063],"holdAndReturnOne":False}

        request = requests.post(base_url, post_request)

        results = json.loads(request.text).get("Reservations", None)
        tee_times = None
        if results is not None:
            for result in results:
                date_and_time = datetime(self._date.year, self._date.month,
                                         self._date.day,
                                         hour=result["TeeTimeDisplay"],
                                         minute=0)
                new_tee_time = TeeTime(date_and_time,
                                       result["PlayersAvailable"],
                                       result["PriceMin"], 0)
                if tee_times is None:
                    tee_times = pd.DataFrame(new_tee_time.tee_time_table)
                else:
                    tee_times = pd.concat([tee_times, new_tee_time.tee_time_table],
                                           ignore_index=True)

        return tee_times

class LasPositas(Scraper):
    """Web scraper for Las Positas golf course
    """

    def _scrape_tee_times(self) -> pd.DataFrame:
        base_url = "https://www.chronogolf.com/marketplace/clubs/18173/teetimes"
        query_url = f"?date={self._date.year}-{self._date.month}-{self._date.day}&course_id=21211&affiliation_type_ids%5B%5D=85452&affiliation_type_ids%5B%5D=85452&affiliation_type_ids%5B%5D=85452&affiliation_type_ids%5B%5D=85452&nb_holes=18"

        request = requests.get(f"{base_url}{query_url}")
        results = json.loads(request.text)
        tee_times = None
        for result in results:
            if result is not None and not result["out_of_capacity"]:
                hour, min = [int(x) for x in result['start_time'].split(":")]
                date_and_time = datetime(self._date.year, self._date.month, 
                                         self._date.day, hour=hour, minute=min)
                new_tee_time = TeeTime(date_and_time, self._num_players, 
                                       result["green_fees"][0]["green_fee"], 0)
                if tee_times is None:
                    tee_times = pd.DataFrame(new_tee_time.tee_time_table)
                else:
                    tee_times = pd.concat([tee_times,
                                           new_tee_time.tee_time_table],
                                           ignore_index=True)

        return tee_times
