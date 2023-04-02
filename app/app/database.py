from sqlalchemy import Column, String, Date, Time, Integer, create_engine, ForeignKey
from flask_login import UserMixin
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///app.db?check_same_thread=False")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    nickname = Column("nickname", String)
    password = Column("password", String)
    email = Column("email", String)

    def __init__(self, nickname, password, email):
        super().__init__()
        self.nickname = nickname
        self.password = password
        self.email = email

# user = User("user", "uasruaf@gamil.com", "pwd")

class Event(Base, UserMixin):
    __tablename__ = "events"

    id = Column("id", Integer, primary_key=True)
    date = Column("date", Date)
    time = Column("time", Time, nullable=True)
    header = Column("header", String(80))
    descritpion = Column("description", String(240), nullable=True)
    user = Column("user", Integer, ForeignKey("users.id"))

    def __init__(self, date, time, header, description, user):
        super().__init__()
        self.date = date
        self.time = time
        self.header = header
        self.descritpion = description
        self.user = user

Base.metadata.create_all(engine)
print("Done!")



