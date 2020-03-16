import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def get_python_news():
    html = get_html('https://www.python.org/blogs/')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for new in all_news:
            title = new.find('a').text
            url = new.find('a')['href']
            published = new.find('time').text
            result_news.append({
                'title': title,
                'url': url,
                'published': published,
            })
        return result_news
    return False