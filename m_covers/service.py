from m_covers.book_net import BookInfo
from m_covers import model
from m_covers import db


class create_cover:
    def __init__(self, isbn, impression):
        self.isbn = isbn
        self.impression = impression

        self.command = db.Command()
        self.cover = None
        self.flushed = False

    def flush(self):
        book_info = BookInfo()
        book_info.load(self.isbn)
        book = model.Book.from_dict(book_info.simple_info())
        self.cover = model.Cover.new_instance(self.impression, book)
        self.command.insert(self.cover)
        self.command.flush()

    def values_recorded(self, members):
        return {member:getattr(self.cover, member) for member in members}

    def commit(self):
        self.command.commit()


def request_cover_by_id(id):
    cover = db.get_by_id(id)
    return cover.to_dict()


def request_cover_by_isbn(isbn):
    cover = db.get_by_isbn(isbn)
    return cover.to_dict()


if __name__ == '__main__':
    from m_covers.config import configure

    configure(':memory:')
    com = create_cover('9784873117386', 'aa')
    com.flush()
    com.commit()