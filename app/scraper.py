from craigslist import CraigslistHousing
import settings

class Scraper:
    def results(self):
        cl_h = CraigslistHousing(
                    site=settings.CRAIGSLIST_SITE,
                    category=settings.CRAIGSLIST_CATEGORY,
                    filters={
                        'min_ft2': settings.MIN_FT2,
                        'min_price': settings.MIN_PRICE,
                        'max_price': settings.MAX_PRICE,
                        'search_distance': 3.5,
                        'zip_code': '07307'
                    }
            )

        return cl_h.get_results(sort_by='newest', geotagged=True, limit=25)
