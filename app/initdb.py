from sqlalchemy import Column, Integer, String, Float, DateTime
from dbsetting import Engine
from dbsetting import Base

class ModelData(Base):
    """
    Data for Create Model
    """

    __tablename__ = 'outline'
    __table_args__ = {
        'comment': 'あらすじ保存テーブル'
    }

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    class_ = Column('class', String(50))
    text = Column('text', String(1000))
    time = Column('datetime', DateTime)

if __name__ == '__main__':
    Base.metadata.create_all(bind=Engine)