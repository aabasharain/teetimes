from datetime import datetime
from teetimes.scrapers import MonarchBay, CoricaPark, LasPositas

date = datetime(2022, 10, 22)
num_players = 0

mb = MonarchBay(date, num_players)
print(mb.tee_times)

cb = CoricaPark(date, num_players)
print(cb.tee_times)

lp = LasPositas(date, num_players)
print(lp.tee_times)