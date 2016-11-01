from listing import Listing, session
from scraper import Scraper
from slack import Slack

import sys
import traceback
import time

slack = Slack()

def scrape():
    results = 0
    duplicates = 0

    for result in Scraper().results():
        results += 1

        listing = Listing(result).process()

        if listing is None:
            duplicates += 1
            continue

        session.add(listing)
        session.commit()

        if listing.transit_stop is None:
            continue

        post = (
                ':house: {0} :moneybag: ${1} :round_pushpin: {2} :station: {3} '
                ':link: <{4}>'
                .format(listing.name, listing.price, listing.area,
                        listing.transit_stop, listing.link)
            )

        slack.post(post)

    print("%s: processed %s listings, %s were duplicates." %
          (time.ctime(), results, duplicates)
          )

if __name__ == '__main__':
    while True:
        try:
            scrape()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print("Error:", sys.exc_info()[0])
            traceback.print_exc()

        time.sleep(3600)
