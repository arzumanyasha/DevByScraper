import requests
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


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    events = soup.find('div', class_='list-item-events').find_all('div', class_='item-body')
    print(events)


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
