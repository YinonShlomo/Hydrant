import random
import urllib.request

URL_FULL = "https://hyd-srv.oz-tms.com/bingoqr/api/addHydrantLog/I/05XXXXXXXX/T/6/V/0/S/0" #currect url
URL_BASIC = "https://hyd-srv.oz-tms.com/bingoqr/api/addHydrantLog/I/" 
TRIGERS_LIST = [1, 2, 3, 5, 6, 7] 
STATUS_LIST = [0, 1]
HYDRANTS_PHONES = ["0544555444", "0544564654", "0545554545", "0526663334"]
VALUE_START = 1
VALUE_END = 250


triger = random.choice(TRIGERS_LIST)
status = random.choice(STATUS_LIST)
phone = random.choice(HYDRANTS_PHONES)
value = random.randrange(VALUE_START, VALUE_END)
value = value if triger in [1,2] else 0 #only in triger==1 or 2(flow/reversed flow), value =! 0

url = f"{URL_BASIC}{phone}/T/{triger}/V/{value}/S/{status}" #valid url


response = urllib.request.urlopen(url) #reading url http code
html = response.read()
#print(type(html))
print(html)


print(f"url = {url}\nhydrant phone = {phone}, triger = {triger}, value = {value}, status = {status}")


