import os
import csv
import json
from abc import ABC, abstractmethod
from datetime import datetime
from io import StringIO
from typing import List, Optional

import pandas as pd

from logger import get_logger


class BaseScraper(ABC):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"

    def __init__(self, max_items: int = 10, file_format: str = 'csv'):
        self.max_items = max_items
        self.file_format = file_format

        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def generate_page_urls(self) -> List[str]:
        return []

    @abstractmethod
    def scrape_items(self, page_url: str) -> List[dict]:
        return []

    def scrape_item_details(self, detail_url: str) -> Optional[dict]:
        return {}

    def run(self) -> None:
        self.logger.info("Starting %s", self.__class__.__name__)
        scraped_items = []

        for page_url in self.generate_page_urls():
            self.logger.info("Scraping page: %s", page_url)
            page_items = self.scrape_items(page_url)

            for item in page_items:
                detail_data = self.scrape_item_details(item.get('url'))

                if detail_data:
                    item_detailed = item | detail_data
                    scraped_items.append(item_detailed)
                else:
                    scraped_items.append(item)

            if len(scraped_items) >= self.max_items:
                self.logger.info("Found %s items. Stop scraping ...", len(scraped_items))
                break

        unique_items = [item for item in scraped_items if item is not None][:self.max_items]
        if unique_items:
            self.logger.info("Amount of unique items scraped: %s", len(unique_items))
            self.save_to_file(unique_items)
        else:
            self.logger.info("No items scraped")

    def save_to_file(self, data: List[dict]):
        os.makedirs("results", exist_ok=True)
        file_name = f'results/{self.__class__.__name__}_{datetime.now().strftime("%Y-%m-%d_%H-%M")}.{self.file_format}'

        try:
            if self.file_format == 'json':
                self.save_to_json(file_name, data)
            elif self.file_format == 'csv':
                self.save_to_csv(file_name, data)

            self.logger.info(f"Data successfully saved to: {file_name}")
        except Exception as e:
            self.logger.error('Failed to save data to: %s', e)

    @staticmethod
    def save_to_json(file_name: str, data: List[dict]):
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def save_to_csv(file_name: str, data: List[dict]):
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def get_tables_from_html(html_string: str) -> List[pd.DataFrame]:
        dfrs = pd.read_html(StringIO(html_string))
        return dfrs
