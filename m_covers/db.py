from sqlalchemy import Column, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from m_covers import model


Base = declarative_base()
ENGINE = None


def reload_engine(db_path):
    global ENGINE
    ENGINE = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path))
    Base.metadata.create_all(bind=ENGINE)


class Cover(Base):
    __tablename__ = 'cover'

    id = Column(String, primary_key=True)
    impression = Column(String)
    book = relationship('Book', uselist=False, back_populates='cover')


class Book(Base):
    __tablename__ = 'book'

    id = Column(String, primary_key=True)
    isbn = Column(String)
    title = Column(String)
    authors = Column(String)
    description = Column(String)
    publisher = Column(String)
    published = Column(String)
    img_url = Column(String)
    cover_id = Column(String, ForeignKey('cover.id'))
    cover = relationship('Cover', back_populates='book')

    def to_dict(self):
        paras = ['id', 'cover_id', 'isbn', 'title', 'authors', 'description',
                 'publisher', 'published', 'img_url']
        return {key:getattr(self, key) for key in paras}


class Command:
    def __init__(self):
        self.session = Session(bind=ENGINE)

    def insert(self, cover):
        session = self.session
        book_base = Book(id=cover.id,
                         isbn=cover.book.isbn,
                         title=cover.title,
                         authors=cover.book.authors,
                         description=cover.book.description,
                         publisher=cover.book.publisher,
                         published=cover.book.published,
                         img_url=cover.book.img_url,
                         )
        session.add(Cover(id=cover.id, impression=cover.impression, book=book_base))
        self.flush()

    def flush(self):
        self.session.flush()

    def commit(self):
        self.session.commit()


def get_by_id(id):
    session = Session(bind=ENGINE)
    result = session.query(Cover, Book).\
        join(Book, Cover.id==Book.cover_id).\
        filter(Cover.id==id).\
        first()
    if result:
        cover_base, book_base = result
    else:
        return None
    return model.Cover(cover_base.id, cover_base.impression,
                       model.Book.from_dict(book_base.to_dict()))


def get_by_isbn(isbn):
    session = Session(bind=ENGINE)
    result = session.query(Cover, Book).\
        join(Book, Cover.id==Book.cover_id).\
        filter(Book.isbn==isbn).\
        first()
    if result:
        cover_base, book_base = result
    else:
        return None
    return model.Cover(cover_base.id, cover_base.impression,
                       model.Book.from_dict(book_base.to_dict()))


if __name__ == '__main__':
    reload_engine(':memory:')
    b = model.Book('1', 'title', 'author', 'desc', '19950809', 'gur', 'https://github.com')
    c = model.Cover('1', 'imp', b)
    command = Command()
    command.insert(c)
    command.commit()
    print(get_by_isbn('1'))
