from database_server import Database
from config import db_url

db = Database(db_url)

db.update_data(data={'is_form': 0}, filters={'id': 7107852221}, table='users')