import requests
from datetime import datetime
import smtplib
import time
my_email = "<EMAIL>"
my_password = "<PASSWORD>"
MY_LAT = 'your'
MY_LONG = 'your'
overhead = False

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()
iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])
if (MY_LAT + 5) <= iss_latitude <= (MY_LAT - 5) and (MY_LAT + 5) <= iss_longitude <= (MY_LONG - 5):
    overhead = True
else:
    overhead = False
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = datetime.now().hour
is_dark = time_now >= sunset or time_now < sunrise
def send():
    if overhead and is_dark:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(my_email, my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="<EMAIL>",
                msg="Look up! There's ISS overhead!"
            )
    else:
        print("You must to wait...")
    time.sleep(60)
    send()
send()



