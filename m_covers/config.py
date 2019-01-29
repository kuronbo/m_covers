from m_covers import db


def configure(db_path):
    db.reload_engine(db_path)
