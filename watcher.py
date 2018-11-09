# global
from datetime import datetime

# project
from manage_db import DataHandler
from get_offers import get_links_to_offers, get_links_on_main_page, send_notifications

db = DataHandler()
db.connect()
db.create_table('offers', 'link')

offers_links = get_links_to_offers('https://www.naturisimo.com/freeproducts.cfm')
main_page_links = get_links_on_main_page('https://www.naturisimo.com')
all_links = offers_links + main_page_links

for link in all_links:
    created_at = int(datetime.utcnow().strftime('%s'))
    db.check_updates('offers', link)
