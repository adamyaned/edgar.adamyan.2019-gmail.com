from covid import Covid
import time
covid = Covid(source="worldometers")
data=covid.get_status_by_country_name('armenia')
print(data)