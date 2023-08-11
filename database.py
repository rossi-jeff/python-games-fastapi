from dotenv import dotenv_values
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

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
