import requests
from bs4 import BeautifulSoup as Soup

url = 'https://www.naturisimo.com/freeproducts.cfm'


def get_links_to_offers(url: str = url) -> list:
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

# TODO test send_notifications
def send_notifications(token: str, chat_id: str, message: str):
    url = 'https://api.telegram.org/bot<{}>/sendMessage -d chat_id=<{}> -d text="{}"'.format(token, chat_id, message)
    requests.post(url)
