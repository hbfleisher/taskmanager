from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from taskmanager.core.database import Base
DATABASE_URL = "sqlite:///./taskmanager.db"

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)