from craigslist import CraigslistHousing
from random import randint
import settings

class Scraper:
    def results(self):
        cl_h = CraigslistHousing(
                    site=settings.CRAIGSLIST_SITE,
                    category=settings.CRAIGSLIST_CATEGORY,
                    filters={
                        'min_ft2': settings.MIN_FT2 + randint(-5, 5) * 10,
                        'min_price': settings.MIN_PRICE + randint(-10, 10) * 10,
                        'max_price': settings.MAX_PRICE + randint(-10, 10) * 10
                    }
            )

        return cl_h.get_results(sort_by='newest', geotagged=True, limit=50)
