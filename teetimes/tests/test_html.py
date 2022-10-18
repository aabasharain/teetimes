from teetimes.scrapers import MonarchBay, CoricaPark, LasPositas
from datetime import datetime

date = datetime(2022, 10, 22)
num_players = 0

mb = MonarchBay(date, num_players)
cp = CoricaPark(date, num_players)
lp = LasPositas(date, num_players)

html_tables = {
    "Monarch Bay": mb.tee_times.to_html(classes='data') if mb.tee_times is not None else [],
    "Corica Park": cp.tee_times.to_html(classes='data') if cp.tee_times is not None else [],
    "Las Positas": lp.tee_times.to_html(classes='data') if lp.tee_times is not None else []
}

for title, data in html_tables.items():
    print(title)
    print(data)