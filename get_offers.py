import requests
from bs4 import BeautifulSoup as Soup


def get_links_to_offers(url: str) -> list:
    links = []
    r = requests.get(url)
    html = Soup(r.text, 'html.parser')
    divs = html.findAll("div", {"class": "col-xxs-12 col-xs-6 col-sm-6 col-md-6 col-lg-6 no-gutter mb10"})
    for i in divs:
        link = i.a.get('href')
        if 'http' not in link:
            link = 'https://www.naturisimo.com/{}'.format(link)
        links.append(link)
    return links


def get_links_on_main_page(url: str) -> list:
    links = []
    r = requests.get(url)
    html = Soup(r.text, 'html.parser')
    a = html.findAll("a")
    for i in a:
        link = i.get('href')
        if 'cfm' in link and 'www.naturisimo.com/' in link:
            links.append(link)
    return links


def send_notifications(token: str, chat_id: str, message: str):
    requests.post(
        url='https://api.telegram.org/bot{}/sendMessage'.format(token),
        data={'chat_id': chat_id, 'text': message}
    ).json()
