import requests
from datetime import datetime,timedelta
import schedule
import time

presentday = datetime.now()
today_date=presentday.strftime("%d-%m-%Y")

tomorrow = presentday + timedelta(1)
tomorrow_date=tomorrow.strftime("%d-%m-%Y")


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

def fetch_district_id(state_name,district_name):
	
	url_state='https://cdn-api.co-vin.in/api/v2/admin/location/states'
	
	response_state_id=requests.get(url_state,headers=header)
	json_state_id=response_state_id.json()
	data_state=json_state_id["states"]
	for i in data_state:
		if(i["state_name"]==state_name):
			state_id=i["state_id"]

	
	url_district='https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}'.format(state_id)
	
	response_district_id=requests.get(url_district,headers=header)
	json_district_id=response_district_id.json()
	data_district=json_district_id["districts"]
	for i in data_district:
		if(i["district_name"]==district_name):
			return i["district_id"]


def fetch_data_today(dist_id,age_group,dose,feetype):
	
	messages=[]
	
	url_today= 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}'.format(dist_id,today_date)

	response_today=requests.get(url_today,headers=header)
	response_today_json=response_today.json()
	data_today=response_today_json["sessions"]
	
	heading="-------------------TODAY-----------------"
	if(len(data_today)==0):
		heading=heading+"\nSlots Not Available\n"
		messages.append(heading)
	else:
		c=1
		msg=''
		count=1
		for i in data_today:
			if(dose==1 and (i["available_capacity_dose1"]>0) and (i["min_age_limit"]==int(age_group)) and (i["fee_type"]==feetype)):
				msg=msg+f"\nRecord {count}"
				msg=msg+"\nCenter Name :\n{}\n".format(i["name"])
				msg=msg+"Center Address :\n{}\n".format(i["address"])
				msg=msg+"Vaccine Name : {}\n".format(i["vaccine"])
				msg=msg+"Vaccine Capacity : {}\n".format(i["available_capacity_dose1"])
				msg=msg+"Vaccine Fee : Rs.{}\n".format(i["fee"])
				c=c+1
				count=count+1
				if c<=4:
					pass
				else:
					c=1
					messages.append(msg)
					msg=""
					if len(messages)==1:
						messages[0]=heading+messages[0]    
			elif(dose==2 and (i["available_capacity_dose2"]>0) and (i["min_age_limit"]==int(age_group)) and (i["fee_type"]==feetype)):
				msg=msg+f"\nRecord {count}"
				msg=msg+"\nCenter Name :\n{}\n".format(i["name"])
				msg=msg+"Center Address :\n{}\n".format(i["address"])
				msg=msg+"Vaccine Name : {}\n".format(i["vaccine"])
				msg=msg+"Vaccine Capacity : {}\n".format(i["available_capacity_dose1"])
				msg=msg+"Vaccine Fee : Rs.{}\n".format(i["fee"])
				c=c+1
				count=count+1
				if c<=4:
					pass
				else:
					c=1
					messages.append(msg)
					msg=""
					if len(messages)==1:
						messages[0]=heading+messages[0]    
		return messages
	
   
	
	
def fetch_data_tomorrow(dist_id,age_group,dose,feetype):
	
	
	messages=[]
	
	url_today= 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}'.format(dist_id,tomorrow_date)

	response_today=requests.get(url_today,headers=header)
	response_today_json=response_today.json()
	data_today=response_today_json["sessions"]
	
	heading="-------------------TOMORROW-----------------"
	if(len(data_today)==0):
		heading=heading+"\nSlots Not Available\n"
		messages.append(heading)
	else:
		c=1
		msg=''
		count=1
		for i in data_today:
			if(dose==1 and (i["available_capacity_dose1"]>0) and (i["min_age_limit"]==int(age_group)) and (i["fee_type"]==feetype)):
				msg=msg+f"\nRecord {count}"
				msg=msg+"\nCenter Name :\n{}\n".format(i["name"])
				msg=msg+"Center Address :\n{}\n".format(i["address"])
				msg=msg+"Vaccine Name : {}\n".format(i["vaccine"])
				msg=msg+"Vaccine Capacity : {}\n".format(i["available_capacity_dose1"])
				msg=msg+"Vaccine Fee : Rs.{}\n".format(i["fee"])
				c=c+1
				count=count+1
				if c<=4:
					pass
				else:
					c=1
					messages.append(msg)
					msg=""
					if len(messages)==1:
						messages[0]=heading+messages[0]    
			elif(dose==2 and (i["available_capacity_dose2"]>0) and (i["min_age_limit"]==int(age_group)) and (i["fee_type"]==feetype)):
				msg=msg+f"\nRecord {count}"
				msg=msg+"\nCenter Name :\n{}\n".format(i["name"])
				msg=msg+"Center Address :\n{}\n".format(i["address"])
				msg=msg+"Vaccine Name : {}\n".format(i["vaccine"])
				msg=msg+"Vaccine Capacity : {}\n".format(i["available_capacity_dose1"])
				msg=msg+"Vaccine Fee : Rs.{}\n".format(i["fee"])
				c=c+1
				count=count+1
				if c<=4:
					pass
				else:
					c=1
					messages.append(msg)
					msg=""
					if len(messages)==1:
						messages[0]=heading+messages[0]    
		return messages
	

 
def main():
	
	url_update='https://api.telegram.org/bot1817658461:AAGwZYzU_pBocwbyrMPpwDV8isjsVvcM9eU/getUpdates'
	bot=requests.get(url_update)
	bot1=bot.json()
	
	user_input=bot1["result"][-1]["message"]["text"]
		
	split=user_input.split("_")
	state=split[0]
	district=split[1]
	age_group=split[2]
	dose=int(split[3])
	feetype=split[4]
	day=split[5]
	
	dist_id=fetch_district_id(state,district)
		
	
	  
	url_telegram='https://api.telegram.org/bot1817658461:AAGwZYzU_pBocwbyrMPpwDV8isjsVvcM9eU/sendMessage?chat_id=@__groupid__&text='
	group_id="covid_vaccine_slots"
	final1=url_telegram.replace("__groupid__",group_id)
	if day=='Today':
		for i in fetch_data_today(dist_id,age_group,dose,feetype):
			# final=final1 + i
			response_bot=requests.get(final1 +i)
			print(response_bot.json())
			
	else:
		for i in fetch_data_tomorrow(dist_id,age_group,dose,feetype):
			response_bot=requests.get(final1 +i)
			print(response_bot.json())
	
	


schedule.every(30).seconds.do(main)

while 1:
	schedule.run_pending()
	time.sleep(1)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


	

