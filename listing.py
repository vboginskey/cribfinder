from dateutil.parser import parse
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geo import distance, in_box
import settings

Base = declarative_base(constructor=None)


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    cl_id = Column(Integer, unique=True)
    posted = Column(DateTime)
    name = Column(String)
    location = Column(String)
    price = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    area = Column(String)
    transit_stop = Column(String)
    transit_dist = Column(Float)

    def __init__(self, scraped_listing):
        self.scraped_listing = scraped_listing

        self.process()

    def process(self):
        self.cl_id = self.scraped_listing['id']
        self.posted = parse(self.scraped_listing['datetime'])
        self.name = self.scraped_listing['name']
        self.location = self.scraped_listing['where']

        if self.scraped_listing['geotag'] is not None:
            self.lat = self.scraped_listing['geotag'][0]
            self.lon = self.scraped_listing['geotag'][1]

        if self.is_existing():
            return

        return (
            self
            .parse_price()
            .find_transit()
            .assign_area()
        )

    def is_existing(self):
        db_listing = (
            session.query(Listing)
            .filter_by(cl_id=self.cl_id).first()
            )

        if db_listing is not None:
            return True

        filters = {'name': self.name, 'location': self.location}

        if self.lat is not None:
            filters.update({'lat': self.lat, 'lon': self.lon})

        db_listing = session.query(Listing).filter_by(**filters).first()

        return db_listing is not None

    def parse_price(self):
        self.price = int(self.scraped_listing['price'].replace('$', ''))

        return self

    def find_transit(self):
        if self.lat is None:
            return self

        min_dist = None

        for station, coords in settings.STATIONS.items():
            this_dist = distance(coords[0], coords[1], self.lat, self.lon)

            if min_dist is None or this_dist < min_dist:
                min_dist = this_dist

                if this_dist < settings.MAX_TRANSIT_DISTANCE:
                    self.transit_stop = station
                    self.transit_dist = this_dist

        return self

    def assign_area(self):
        if self.lat is not None:
            for area, coords in settings.BOXES.items():
                if in_box(self.lat, self.lon, coords):
                    self.area = area
                    break
        else:
            for hood in settings.NEIGHBORHOODS:
                if hood in self.location.lower():
                    self.area = hood.title()
                    break

        return self

engine = create_engine('sqlite:///listings.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
