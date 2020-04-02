from covid import Covid
import time
covid = Covid(source="worldometers")
data={'active':covid.get_total_active_cases(),'confirmed':covid.get_total_confirmed_cases(),'deaths':covid.get_total_deaths(),'recovered':covid.get_total_recovered(),'last_update':int(round(time.time()*1000))}
recoveredPercent = data['recovered']*100/data['confirmed']
replyMessage = f"COVID-19-ի վերջին տվյալները Աշխարհում։ Աշխարհում կա <b>{data['confirmed']}</b> վարակված անձ որոնցից ապաքինվել է <b>{data['recovered']}({data['recovered']*100/data['confirmed']}%)</b> մարդ, մահացել <b>{data['deaths']}</b>-ը և այժմ բուժում է ստանում <b>{data['active']}</b> մարդ։"
