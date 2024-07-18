from database_server import Database
from config import db_url

db = Database(db_url)

db.update_data(data={'date': '02.02.2030'}, filters={'id': 13}, table='events')