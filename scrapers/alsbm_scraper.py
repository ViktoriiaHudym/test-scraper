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

        # Handles the PHPSESSID and sets the correct User-Agent and other headers for a POST request
        self._set_session_cookies()
        self._set_session_headers(self.config.POST_HEADERS)

        try:
            response = self.session.post(page_url, data=self.config.PAYLOAD, timeout=15)
            response.raise_for_status()

            # Get all tables from page as a list of DataFrame objects
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
        """
        Updates session cookies with a valid PHPSESSID.

        Reuses cookies from previous run if available.
        If PHPSESSID missing or expired, fetches a fresh one from self.base_url.
        Saves cookies back to file for future runs.
        """

        # here we will store cookies
        os.makedirs("cookies", exist_ok=True)
        cookies_file = f'cookies/{self.__class__.__name__}_cookies.pkl'

        # set the GET headers, which are needed for the initial request to collect cookies
        self._set_session_headers(self.config.GET_HEADERS)

        # try to load cookies from the file created in a previous run
        if os.path.exists(cookies_file):
            try:
                with open(cookies_file, "rb") as f:
                    old_cookies = pickle.load(f)
                    self.session.cookies.update(old_cookies)
                    self.logger.info("Cookies loaded from file: %s", old_cookies)
            except Exception as e:
                self.logger.warning(f"Could not load cookies from file: {e}")

        if "PHPSESSID" not in self.session.cookies.get_dict():
            # Make a request to a page that make request in new session and sets a PHPSESSID cookie
            resp = self.session.get('https://alsbm.org/midwives')
            resp.raise_for_status()

        if "PHPSESSID" not in self.session.cookies.get_dict():
            self.logger.warning("Could not obtain PHPSESSID cookies from server")
        else:
            self.logger.info("PHPSESSID cookies successfully loaded from server")

            # Save the current session cookies to a file for reuse in the next run
            with open(cookies_file, "wb") as f:
                pickle.dump(self.session.cookies, f)

    def _set_session_headers(self, headers):
        self.session.headers.clear()
        self.session.headers.update({'user-agent': self.USER_AGENT})
        self.session.headers.update(headers)
