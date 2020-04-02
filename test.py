from covid import Covid
import time
covid = Covid(source="worldometers")
data=covid.get_status_by_country_name('armenia')
result = round(((data['confirmed']-data['new_cases'])*100)/(data['confirmed']-data['new_cases']), 2)
print(result)