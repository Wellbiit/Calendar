from database import session, User, Event
from db_controls import add_new_item
from werkzeug.security import generate_password_hash

# pwd = generate_password_hash("admin")
# admin = User("admin", pwd, "admin@ad.com")
# add_new_item(admin)

event = session.query(User).first()
print(event, "query")