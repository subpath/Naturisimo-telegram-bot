# global
from datetime import datetime

# project
from manage_db import DataHandler
from get_offers import get_links_to_offers

db = DataHandler()
db.connect()
db.create_table('offers', 'link')

offers_links = get_links_to_offers()
for link in offers_links:
    created_at = int(datetime.utcnow().strftime('%s'))
    db.check_updates('offers', link)