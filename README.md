### Simple scraping project

-----
To run the scraper, you'll need Python >= 3.10 and the required libraries. You can install them using pip:

```bash
pip install -r requirements.txt
```

-----

#### **Usage**

To start the scraping process, run the `start.py` file from your terminal.

```bash
python start.py [options]
```

-----

#### **Command-line Arguments**

| Argument | Shorthand | Type | Description |
| :--- | :--- | :--- | :--- |
| `--site_domain` | `-s` | `str` | **(Required)** The domain of the website to scrape. Currently, only `alsbm.org` is supported. |
| `--max_items` | `-m` | `int` | The maximum number of items to scrape. |
| `--file_format` | `-f` | `str` | The format for the output file. Choices are `csv` or `json`. |

-----

#### **Example**

To run a scraper for **_alsbm.org_** you can use the following command:
```bash
python start.py -s alsbm.org -m 100 -f csv
```

Scraper for **_alsbm.org_** has two additional arguments:

- `--search_field` (`-sf`) The field to search by (e.g., `last_name`, `state`). Defaults to `last_name`
- `--search_value` (`-sv`) The value to search for (e.g., `smith`, `Alabama`). Defaults to `smith`

Example usage:
```bash
python start.py -s alsbm.org -m 20 -sf state -sv alabama -f csv
```

-----

#### **Output**

After the scraper finishes it work the results will be saved to corresponding file in _**results**_ folder.
