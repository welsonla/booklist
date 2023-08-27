import sqlalchemy.orm
from sqlalchemy import Column,Integer, String, create_engine, Float, Text, text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = sqlalchemy.orm.declarative_base()


class DBManager:
    engine = create_engine("sqlite+pysqlite:///booklist.sqlite")


    def __init__(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.create_tables()

    def create_tables(self):
        # 创建所有表
        Base.metadata.create_all(bind=self.engine, checkfirst=True)


    def insert_book(self, book):
        print(f"插入图书:{book.name}")
        with self.session as s:
            # item = self.session.query(Book).filter(Book.douban_url == book.douban_url).all()
            # print(f"item:{len(item)} ---- {item} ")
            # if item is None:
            item = s.query(Book).filter(Book.douban_url == book.douban_url).all()
            if len(item) == 0:
                self.session.add(book)
                self.session.commit()
            else:
                print("已存在相同数据，跳过")


    def check(self,url):
        with self.session as s:
            item = s.query(Book).filter(Book.douban_url == url).all()
            print(f"item:{len(item)} ---- {item} ")
            if len(item) == 0:
                print("None")
            else:
                print(len(item))

    def books(self):
        with self.session as s:
            return s.query(Book).all()

class Book(Base):
    __tablename__='book'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), comment="书名")
    cover_url = Column(String(255), comment="封面")
    image_url = Column(String(255), comment="封面地址")
    author = Column(String(50), comment="作者")
    price = Column(Float, default=0, comment="定价")
    desc = Column(Text, nullable=True, comment="简介")
    isbn = Column(String(50), nullable=True, comment="图书编号")
    rating = Column(Float, comment="用户评分")
    rating_count = Column(Integer, comment="评分人数")
    pages = Column(Integer, default=0, comment="总页数")
    publisher = Column(String(255), nullable=True, comment='出版社')
    publish_date = Column(String(50), comment="出版日期")
    douban_url = Column(String(255), nullable=True, comment="豆瓣图书主页")
    category = Column(String(255), nullable=True, comment="图书种类")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
