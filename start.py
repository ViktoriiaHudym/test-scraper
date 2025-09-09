import argparse

from scrapers.alsbm_scraper import AlsbmScraper


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--site_domain', '-s', type=str, required=True, help='Site domain')
    parser.add_argument('--max_items', '-m', type=int, help='Maximum number of items to scrape')
    parser.add_argument('--file_format', '-f', type=str, choices=['csv', 'json'], help='File format where the data will be saved')

    # AlsbmScraper arguments
    parser.add_argument('--search_field', '-sf', type=str, default='last_name', help='Search field to use for searching')
    parser.add_argument('--search_value', '-sv', type=str, default='smith', help='Search field to use for searching')

    args = parser.parse_args()

    if args.site_domain == 'alsbm.org':
        s = AlsbmScraper(
            max_items=args.max_items,
            file_format=args.file_format,
            search_field=args.search_field,
            search_value=args.search_value,
        )
        s.run()
    else:
        print('Scraper not available for this site.')


if __name__ == "__main__":
    main()