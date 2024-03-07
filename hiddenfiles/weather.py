#!/usr/bin/env python3

import calendar
import datetime
import math
import requests
import sys
import subprocess

FG = '\033[0;32;1;7m'
NC = '\033[0m'

LOCATION_URL = "https://api.ip2location.com/v2/?ip=%s&key=demo&package=WS11&addon=time_zone_info"
IP_URL = 'https://ipinfo.io/ip'

def get_location():
    #ip = requests.get(IP_URL).text
    #r = requests.get(LOCATION_URL % ip).json()
    r = requests.get("http://ifconfig.co/json").json()
    #print(r['city'], r['region_code'], r['latitude'], r['longitude'])
    return (r['latitude'], r['longitude'])

def get_calendar():
    today = datetime.datetime.today()

    day = today.day
    month = today.month
    year = today.year

    cal = calendar.TextCalendar(6).formatmonth(year, month)
    
    tl = cal.find(str(day), cal.find(str(year)) + 4)

    return (cal[:tl] + FG + cal[tl:tl+len(str(day))] + NC + cal[tl+len(str(day)):]).split('\n')

def get_weather(postal = ''):
    url = 'http://wttr.in/%s?days=0' % postal
    try:
        weather = requests.get(url,timeout=2).text
        return weather.split('\n')[:]
    except requests.exceptions.ReadTimeout:
        return None
        

def get_covid_stats(country='us'):
    a = subprocess.run('curl -s -L https://covid19-cli.wareneutron.com/quiet/USA | head -n 11', capture_output=True, shell=True) # | cowsay -f stegosaurus -n

    data = a.stdout.decode('utf-8')
    data = data.replace('Mortaility %', 'Mortality % ')

    lines = data.split('\n')
    return lines

def intro(calendar = [], weather = [], stats = [], city = '', state = '', sunrise = '', sunset = ''):
    printing = []
    pad_length = (len(stats) - len(calendar)) * ['']

    if weather != None:
        weather[1] = ','.join(weather[0].split(':')[1].split(',')[:2])
        weather = weather[1:-1]
    else:
        weather = []

    max_lines = max(len(calendar), len(weather), len(stats))
    weather.extend([f'    Sunrise: {sunrise}', f'    Sunset:  {sunset}'])
    calendar.extend((max_lines - len(calendar)) * [''])    
    #calendar.extend(weather)
    weather.extend([''] * (max_lines - len(weather)))
    stats.extend([''] * (max_lines - len(stats)))


    
#    pad_length = (len(stats) - len(calendar))

#    printing = pad_length // 2 * [''] + calendar + (pad_length // 2 + pad_length % 2) * ['']

    # if sunrise != '':
    #     weather.append('\t\t     Sunrise:\t' + sunrise)
    # if sunset != '':
    #     weather.append('\t\t     Sunset:\t' + sunset)

    for i in range(max_lines):
        if calendar[i].find(FG) != -1:
            print(f'{calendar[i]:<40}{stats[i]:>50}{weather[i]:>30}')
        else:
            print(f'{calendar[i]:<25}{stats[i]:>50}{weather[i]:>30}')
    
def main():
    lat, lon = get_location()
    
    if float(lon) < 0:
        lon = str(math.fabs(lon)) + 'W'
    else:
        lon = str(lon) + 'E'

    if float(lat) < 0:
        lat = str(math.fabs(lat)) + 'S'
    else:
        lat = str(lat) + 'N'

    #print(lat, lon)
        
    a = subprocess.run('~/bin/sunwait list ' + lat + ' ' + lon , capture_output=True, shell=True).stdout.decode('utf-8')
    sunrise = a.split(',')[0].strip()
    sunset = a.split(',')[1].strip()

    
    calendar = get_calendar()
    weather = get_weather()
    stats = get_covid_stats()
    intro(calendar, weather, stats, sunrise = sunrise, sunset = sunset)

if __name__ == '__main__':
    main()
