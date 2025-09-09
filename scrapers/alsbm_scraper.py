import os
import pickle

import requests

from .base_scraper import BaseScraper
from .config import AlsbmConfig


class AlsbmScraper(BaseScraper):
    def __init__(self, max_items, file_format, search_field, search_value):
        super().__init__(max_items, file_format)
        self.config = AlsbmConfig(search_field=search_field, search_value=search_value)
        self.session = requests.Session()

    def generate_page_urls(self):
        # Single URL for the page returned, because data can be scraped using a POST request with an AJAX URL
        return [self.config.SEARCH_URL]

    def scrape_items(self, page_url: str):
        results = []

        self._set_session_cookies()
        self._set_session_headers(self.config.POST_HEADERS)

        try:
            response = self.session.post(page_url, data=self.config.PAYLOAD, timeout=15)
            response.raise_for_status()

            page_tables = self.get_tables_from_html(response.text)

            if page_tables:
                # The target site has only one table, so we extract the first DataFrame
                dict_items = page_tables[0].to_dict(orient='records')

                results.extend(dict_items)

        except requests.exceptions.RequestException as e:
            self.logger.error('Failed to make request to %s: %s', page_url, e)
        except Exception as e:
            self.logger.error("Failed to parse items on page. Error: %s", e)

        return results


    def _set_session_cookies(self):
        os.makedirs("cookies", exist_ok=True)
        cookies_file = f'cookies/{self.__class__.__name__}_cookies.pkl'

        self._set_session_headers(self.config.GET_HEADERS)

        # Try to load cookies from the file created in a previous run
        if os.path.exists(cookies_file):
            try:
                with open(cookies_file, "rb") as f:
                    old_cookies = pickle.load(f)
                    self.session.cookies.update(old_cookies)
                    self.logger.info("Cookies loaded from file: %s", old_cookies)
            except Exception as e:
                self.logger.warning(f"Could not load cookies from file: {e}")

        if "PHPSESSID" not in self.session.cookies.get_dict():
            resp = self.session.get('https://alsbm.org/midwives')
            resp.raise_for_status()

        if "PHPSESSID" not in self.session.cookies.get_dict():
            self.logger.warning("Could not obtain PHPSESSID cookies from server")
        else:
            self.logger.info("PHPSESSID cookies loaded from server successfully")
            with open(cookies_file, "wb") as f:
                pickle.dump(self.session.cookies, f)

    def _set_session_headers(self, headers):
        self.session.headers.clear()
        self.session.headers.update({'user-agent': self.USER_AGENT})
        self.session.headers.update(headers)
