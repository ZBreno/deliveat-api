from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..domain.data.sqlalchemy_models import Base

DB_URL = "postgresql://postgres:123@localhost:5432/deliveat"

engine = create_engine(DB_URL)

Base.metadata.create_all(engine)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
