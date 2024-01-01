from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.data.sqlalchemy_models import Base
import os
DB_URL = os.getenv('POSTGRES_URL', 'postgresql://postgres:123@postgres:5432/deliveat')

engine = create_engine(DB_URL)

Base.metadata.create_all(engine)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
