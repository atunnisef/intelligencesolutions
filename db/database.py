from databases import Database
from sqlalchemy import MetaData, create_engine

DATABASE_URL = "postgresql://user:password@localhost:5432/yourdbname"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
