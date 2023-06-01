import schedule
import time
import telebot
import requests
from bs4 import BeautifulSoup as bs4

# ADD YOUR TELEGRAM BOT KEY
bot = telebot.TeleBot('')

# Specification
filters_url = "http://127.0.0.1:8000/kolesafilters/"
clients_url = 'http://127.0.0.1:8000/kolesaclients/'
car_page_url = "https://kolesa.kz/a/show/"
update_lc_url = "http://127.0.0.1:8000/updatelastcar/"
num_of_views_url = "https://kolesa.kz/ms/views/kolesa/live/"
avg_price_url = "https://kolesa.kz/a/average-price/"

def send_mess(mess, car_key, filter_key):
    #get clients list
    clients_r = requests.get(clients_url)
    if not clients_r.ok:
        return
    
    clients_json_data = clients_r.json()

    if clients_json_data:
        for ckey in clients_json_data:
            # ctgid = client telegram ID
            ctgid = clients_json_data[ckey]
            bot.send_message(ctgid, mess)

    # update database
    # get csrf token from page
    s = requests.Session()
    r_lc = s.get(update_lc_url)
    lchtml = bs4(r_lc.content, 'html.parser')
    csrf = lchtml.select('input[name=csrfmiddlewaretoken]')[0]['value']

    payload = {
        'csrfmiddlewaretoken': csrf,
        'lcid': car_key,
        'fid': filter_key
    }
    s.post(update_lc_url, data=payload)

# website scraper and message sender
def job():
    # getting filters list from website
    filters_r = requests.get(filters_url)

    if filters_r.ok:
        filters_json_data = filters_r.json()

        for key in filters_json_data:
            # cf = current filter
            cf_url = filters_json_data[key]['url']
            cf_lastcar = filters_json_data[key]['lastcar']
            cf_title = filters_json_data[key]['title']
            cf_perc = filters_json_data[key]['cheap_perc']
            cf_viewcount = filters_json_data[key]['view_count']
            # get page from current url
            r = requests.get(cf_url)
            if not r.ok:
                continue

            html = bs4(r.content, 'html.parser')
            # get latest car item
            data_list = html.find_all("div", class_='a-list__item')

            if not data_list:
                continue

            for data in data_list:

                try:
                    uri = data.find('a', class_="a-card__link")['href']
                    title = data.find('h5', class_="a-card__title").text.strip()
                except:
                    continue
                
                # get ID of the latest car
                car_key = uri.split('/')[-1]

                # Compare with ID stored in DB
                if cf_lastcar != car_key:
                    # getting number of views from kolesa api
                    views_url = num_of_views_url + car_key + '/'
                    r = requests.get(views_url)
                    if not r.ok:
                        continue

                    json_data = r.json()
                    num_of_views = json_data['data'][car_key]['nb_views']

                    # check filter requirements for viewcount\
                    if num_of_views < cf_viewcount:  
                        # getting cheap percentage
                        car_url = car_page_url + car_key + "/"
                        r_car = requests.get(avg_price_url + car_key + '/')
                        if not r_car.ok:
                            continue
                        car_data_json = r_car.json()
                        perc_diff = car_data_json['data']['diffInPercents']
                        
                        if (float(perc_diff) < 0):
                            perc_diff = float(perc_diff) * -1
                            if perc_diff > float(cf_perc):
                                # filter parameter is met
                                # sending message to client
                                mess = f"По фильтру: {cf_title}\n{title}\nДешевле на {str(perc_diff)}%, просмотрено {str(num_of_views)} раз\n{car_url}"
                                send_mess(mess, car_key, key)
                                

schedule.every(10).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
