import schedule
import time
import subprocess

subprocess.Popen("covid-19.py", shell=True)

def job():
    subprocess.Popen("covid-19.py", shell=True)

schedule.every(5).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)



