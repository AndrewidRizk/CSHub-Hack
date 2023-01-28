from bs4 import BeautifulSoup
import requests
import mysql.connector

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
                event_list.append(f"{year}-{month_dict[month]}-{day_of_month} | {event_title} | {event_time} | {addr}")

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
        date_str = f"{year}-{month}-{date}"

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

    return event_list
#-----------------------------------------------------SQL------------------------------------------------------------------
def create_one_List():
    list1 = events_york()
    list2 = get_current_month_events()
    list3 =  get_next_month_events()
    list4 = []
    for i in range(len(list1)):
        list4.append(i)
    for j in range(len(list2)):
        list4.append(j)
    for z in range(len(list3)):
        list4.append(z)
        return list4
def get_date(str):
    year = str[0,9]
    return year
def get_title(str):
    str1 = str[11, -1]
    return str1.split("|")[0]
def get_time(str):
    return str.split("|")[1]
def get_location(str):
    return str.split("|")[2]



def create_table(list_of_strings):
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Androwmaged3030",
        database="events"
    )

    # Create a cursor
    cursor = mydb.cursor()

    # Create the table
    cursor.execute("CREATE TABLE events (date DATE, title VARCHAR(255), time VARCHAR(255), location VARCHAR(255))")
    
    # Iterate through the list of strings
    for event_string in list_of_strings:
        # Extract the date, title, time, and location from the string
        date = get_date(event_string)
        title = get_title(event_string)
        time = get_time(event_string)
        location = get_location(event_string)
        
        # Insert the data into the table
        cursor.execute(f"INSERT INTO events (date, title, time, location) VALUES ('{date}', '{title}', '{time}', '{location}')")

    # Commit the changes to the database
    mydb.commit()

    # Close the cursor and connection
    cursor.close()
    mydb.close()

if __name__=="__main__":
    events_york()
    get_current_month_events()
    get_next_month_events()