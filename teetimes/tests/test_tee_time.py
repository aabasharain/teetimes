from teetimes.tee_time import TeeTime
from datetime import datetime

tee_time = TeeTime(datetime(2022, 10, 22, 10, 10), 4, 50, 12)
print(tee_time.get_tee_time_table())