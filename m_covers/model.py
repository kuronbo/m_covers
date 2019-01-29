from uuid import uuid4


class Cover:
    def __init__(self, id, impression, book):
        self.id = id
        self.impression = impression
        self.book = book

    @classmethod
    def new_instance(cls, impression, book):
        id = str(uuid4())[:8]
        return cls(id, impression, book)

    @property
    def title(self):
        return self.book.title

    @property
    def caption(self):
        return self.book.description.replace('\n', ' ')[:50] or \
               self.impression.replace('\n', ' ')[:50]

    def to_dict(self):
        return {
            'id': self.id,
            'impression': self.impression,
            'book': self.book.to_dict()
        }

    def __repr__(self):
        clsname = type(self).__name__
        return '{clsname}(id={self.id!r}, impression={self.impression!r}, ' \
               'book={self.book!r})'.format(clsname=clsname, self=self)


class Book:
    def __init__(self, isbn, title, authors, description, published, publisher, img_url):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.description = description if description else ''
        self.published = published
        self.publisher = publisher
        self.img_url = img_url

    @classmethod
    def from_dict(cls, d):
        return cls(
            isbn=d.get('isbn'),
            title=d.get('title'),
            authors=d.get('authors'),
            description=d.get('description'),
            published=d.get('published'),
            publisher=d.get('publisher'),
            img_url=d.get('img_url')
        )

    def to_dict(self):
        paras = ['isbn', 'title', 'authors', 'description',
                 'published', 'publisher', 'img_url']
        return {key: getattr(self, key) for key in paras}

    def __repr__(self):
        clsname = type(self).__name__
        return '{clsname}(isbn={self.isbn!r}, id={self.title!r}, ' \
               'author={self.authors!r}, description={self.description!r}, ' \
               'published={self.published!r}, publisher={self.publisher!r},' \
               ' img_url={self.img_url!r})'.\
            format(clsname=clsname, self=self)
