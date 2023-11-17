
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from domain.data.sqlalchemy_models import Base

DB_URL = "postgresql://postgres:123@localhost:5432/deliveat-tests"

engine = create_engine(DB_URL)

Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
