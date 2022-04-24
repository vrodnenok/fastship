import sqlalchemy as sqlalchemy
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

DB_URL = "postgresql://postgres:325324@localhost:5432/fastapi"

engine = sqlalchemy.create_engine(DB_URL, echo=True)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()
