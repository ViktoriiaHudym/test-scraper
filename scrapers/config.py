class AlsbmConfig:
    def __init__(self, search_field: str, search_value: str):
        self.BASE_URL = "https://alsbm.org"
        self.SEARCH_URL = f"{self.BASE_URL}/wp-admin/admin-ajax.php"
        self.SEARCH_FIELD = search_field
        self.SEARCH_VALUE = search_value
        self.PAYLOAD = {
            "postID": "1179",
            "target_instance": "2",
            "submit": "search",
            "listpage": "1",
            "action": "pdb_list_filter",
            "instance_index": "1",
            "pagelink": "/midwives/?listpage=%251$s",
            "search_field": self.SEARCH_FIELD,
            "operator": "LIKE",
            "value": self.SEARCH_VALUE,
        }
        self.POST_HEADERS = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'referer': 'https://alsbm.org/midwives/',
            'x-requested-with': 'XMLHttpRequest',
            'origin': self.BASE_URL,
            'priority': 'u=1, i',
        }
        self.GET_HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,uk;q=0.8,ko;q=0.7,fr;q=0.6',
            'referer': self.BASE_URL,
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
        }