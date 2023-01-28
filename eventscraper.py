from bs4 import BeautifulSoup
import requests

month_dict = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May':'05', 'June':'06',
                'July': '07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}
calendar = requests.get('https://yorkinternational.yorku.ca/calendar').text
calendar = calendar.replace('<!--', '').replace('-->', '')
calendar_soup = BeautifulSoup(calendar, 'lxml')

def get_current_month_events():
    days = calendar_soup.find_all('div', class_='ai1ec-day')
    month_and_year = calendar_soup.find('span', class_='ai1ec-calendar-title').text.strip()
    month = month_and_year.split(' ')[0]
    year = month_and_year.split(' ')[1]

    out_list = populate_list(days, month, year)
    return out_list

def get_next_month_events():
    change_date_buttons = calendar_soup.find('div', class_='ai1ec-pagination ai1ec-btn-group')
    next_month_link = change_date_buttons.find('a', class_='ai1ec-next-month ai1ec-load-view ai1ec-btn ai1ec-btn-sm ai1ec-btn-default')['href']

    next_calendar = requests.get(next_month_link).text
    next_calendar = next_calendar.replace('<!--', '').replace('-->', '')
    next_soup = BeautifulSoup(next_calendar, 'lxml')

    days = next_soup.find_all('div', class_='ai1ec-day')
    month_and_year = next_soup.find('span', class_='ai1ec-calendar-title').text.strip()
    month = month_and_year.split(' ')[0]
    year = month_and_year.split(' ')[1]

    out_list = populate_list(days, month, year)
    return out_list

def populate_list(days, month, year):
    event_list = []

    for day in days:
        event_name = ''
        event_names = day.find_all('a')
        day_of_month = day.find('a', class_='ai1ec-load-view').text.strip()

        for event in event_names:
            event_title = 'N/A'
            event_time = 'N/A'

            try:
                event_title = event.find('span', class_='ai1ec-event-title').text.strip()
                event_time = event.find('span', class_='ai1ec-event-time').text.strip()
            except AttributeError:
                pass

            addr = 'York International'

            if event_title != 'N/A': 
                event_list.append(f"{day_of_month}/{month_dict[month]}/{year} | {event_title} | {event_time} | {addr}")

    return event_list

def events_york():
    events_calendar = requests.get('https://events.yorku.ca').text
    events_soup = BeautifulSoup(events_calendar, 'lxml')

    days = events_soup.find_all('div', class_='mec-calendar-events-sec')

    event_list = []

    for day in days: 
        id_elements = day.get('id').split('-')
        date = id_elements[len(id_elements)-1]
        year = date[:4]
        month = date[4:6]
        date = date[6:8]
        date_str = f"{date}/{month}/{year}"

        events = day.find_all('article', class_='mec-event-article')

        for event in events:
            time = 'Unavailable'
        
            try:
                time = event.find('div', class_='mec-event-time mec-color').text
            except AttributeError:
                pass

            time = time.strip()

            if '-' in time:
                time = time.replace(' ', '')
                time = time.split('-')[0]
            
            try:
                addr = event.find('div', class_='mec-event-loc-place').text.replace('\n', '').strip()
            except AttributeError:
                pass

            if addr == '' or 'zoom' in addr.lower() or 'online' in addr.lower() or 'email' in addr.lower():
                addr = 'York University'

            title = ''

            try: 
                title = event.find('h4', class_='mec-event-title').find('a').text
            except AttributeError:
                pass 

            if title != '':
                event_list.append(f'{date_str} | {title} | {time} | {addr}')
                print(addr)

    return event_list

if __name__=="__main__":
    events_york()
    get_current_month_events()
    get_next_month_events()