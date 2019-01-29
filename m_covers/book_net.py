import json

from requests import get


class BookInfo:
    OPENBD_URL = 'https://api.openbd.jp/v1/get?isbn={}'

    def __init__(self):
        self.raw_data = None
        self.is_loaded = False

    def load(self, isbn):
        res = get(self.OPENBD_URL.format(isbn))
        data = json.loads(res.content.decode('utf-8'))[0]
        if data:
            self.raw_data = data
            self.is_loaded = True
        else:
            raise ValueError('本の情報を取得できませんでした。isbn: {}'.format(isbn))

    def simple_info(self):
        if not self.is_loaded:
            raise ValueError('本の情報が取得されていません。(not loaded)')
        summary = self.raw_data.get('summary', {})
        description = self._description()
        info = {
            'isbn': summary.get('isbn'),
            'title': summary.get('title'),
            'description': description,
            'publisher': summary.get('publisher'),
            'published': summary.get('pubdate'),
            'img_url': summary.get('cover'),
            'authors': summary.get('author')
        }
        return info

    def _description(self):
        onix = self.raw_data.get('onix', {})
        collateral_detail = onix.get('CollateralDetail', {})
        text_content = collateral_detail.get('TextContent', [])
        for c in text_content:
            if c.get('TextType', '') in ['02', '03']:
                return c.get('Text')
