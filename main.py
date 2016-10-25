from listing import Listing, session
from scraper import Scraper

for result in Scraper().results():
    listing = Listing(result).process()

    if listing is not None:
        session.add(listing)
        session.commit()

        if listing.area is not None or listing.transit_stop is not None:
            print(listing.__dict__)
