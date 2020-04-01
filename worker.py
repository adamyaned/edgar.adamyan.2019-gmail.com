import os
import schedule
import time

def job():
    os.system("covid-19.py")

schedule.every(1).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)



