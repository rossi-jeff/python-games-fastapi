from dotenv import dotenv_values
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
# import logging

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

config = dotenv_values(".env")

url_object = URL.create(
    "mysql+pymysql",
    username = config["DB_USER"],
    password = config["DB_PASS"],
    host = config["DB_HOST"],
    database = config["DB_NAME"]
)

engine = create_engine(url_object)

Session = sessionmaker(engine)

session = Session()

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()
