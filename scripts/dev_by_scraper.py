import requests
import collections
import csv
from bs4 import BeautifulSoup


# План:
# 1. Выяснить количество страниц
# 2. Сформировать список урлов на страницы выдачи
# 3. Собрать данные

def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split("&")[0]

    return int(total_pages)


def write_csv(data):
    with open('devby.csv', 'a') as f:
        writer = csv.writer(f)

        try:
            writer.writerow((data['url'], data['title'], data['description']))
        except:
            writer.writerow(('', '', ''))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    events = soup.find('div', class_='list-item-events').find_all('div', class_='item-body')
    # print(events)
    for event in events:
        # url, title, description, date
        try:
            event_body = event.find('a', class_='title')
            url = "https://events.dev.by/" + event_body.get('href')
            title = event_body.get('title').split("|")[1]

            description_html = get_html(url)
            description_soup = BeautifulSoup(description_html, 'lxml')
            descriptions = description_soup.find('div', class_='text').find_all('p')

            # date = event.find('p').find('time')

            # description = event_body.get('')
        except:
            url = ''
            title = ''
            descriptions = ''

        # Event = collections.namedtuple('Event', ['url', 'title', 'description', 'date'])
        # new_event = Event(url, title, descriptions, None)
        new_event = {'url': url,
                     'title': title,
                     'description': descriptions,
                     'date': None}
        # print(new_event)
        write_csv(new_event)


def main():
    # https: // events.dev.by / archives?page = 6
    base_url = 'https://events.dev.by/archives?'
    page_part = 'page='

    for i in range(1, 175, 1):
        url_gen = base_url + page_part + str(i)
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()
