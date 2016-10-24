from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    cl_id = Column(Integer, unique=True)
    posted = Column(DateTime)
    name = Column(String)
    price = Column(Integer)
    location = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    area = Column(String)
    transit = Column(String)

engine = create_engine('sqlite://listings.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
