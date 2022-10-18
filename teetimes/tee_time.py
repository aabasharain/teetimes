
import pandas as pd
from datetime import datetime


class TeeTime:
    """
    Holds date, time, number of players, green fee, and cart fee values for a
    tee time.
    """

    def __init__(self, date: datetime, num_players: int, green_fee: float, cart_fee: float) -> None:
        """Create Tee Time Object

        Args:
            date (datetime): datetime object of tee time day and time
            num_players (int): number of players available for tee time
            green_fee (float): cost of green fee
            cart_fee (float): cost of cart fee
        """

        self._date = date.date()
        self._time = date.time()
        self._num_players = num_players
        self._green_fee = green_fee
        self._cart_fee = cart_fee
        self._tee_time_table = self._make_tee_time_table()

    @property
    def tee_time_table(self) -> pd.DataFrame:
        """Get dataframe of tee time

        Returns:
            pd.DataFrame: pandas dataframe of tee time
        """
        return self._tee_time_table

    def _make_tee_time_table(self) -> pd.DataFrame:
        data = {
            "Date": [str(self._date)],
            "Time": [str(self._time)],
            "Number of Players": [self._num_players],
            "Green Fee": [self._green_fee],
            "Cart Fee": [self._cart_fee]
        }
        return pd.DataFrame(data)
        
    