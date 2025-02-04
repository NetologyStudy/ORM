import re
from sqlalchemy import or_
from models import PublisherORM, BookORM, ShopORM, StockORM, SaleORM
from database import sync_engine, session_factory, Base


class SyncORM:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def insert_publisher():
        with session_factory() as session:
            publisher_pushkin = PublisherORM(name='Пушкин')
            publisher_lermontov = PublisherORM(name='Лермонтов')
            publisher_griboedov = PublisherORM(name='Грибоедов')
            session.add_all([publisher_pushkin, publisher_lermontov, publisher_griboedov])
            session.commit()

    @staticmethod
    def insert_book():
        with session_factory() as session:
            book_pushkin_1 = BookORM(
                title="Капитанская дочка", id_publisher=1)
            book_pushkin_2 = BookORM(
                title="Руслан и Людмила", id_publisher=1)
            book_pushkin_3 = BookORM(
                title="Евгений Онегин", id_publisher=1)
            session.add_all([book_pushkin_1, book_pushkin_2, book_pushkin_3])
            session.commit()

    @staticmethod
    def insert_shop():
        with session_factory() as session:
            shop_bukvoed = ShopORM(name='Буквоед')
            shop_labirint = ShopORM(name='Лабиринт')
            shop_dom_knigi = ShopORM(name='Дом книги')
            session.add_all([shop_bukvoed, shop_labirint, shop_dom_knigi])
            session.commit()

    @staticmethod
    def insert_stock():
        with session_factory() as session:
            stock_1 = StockORM(id_book=1, id_shop=1, count=3)
            stock_2 = StockORM(id_book=2, id_shop=2, count=2)
            stock_3 = StockORM(id_book=3, id_shop=3, count=1)
            session.add_all([stock_1, stock_2, stock_3])
            session.commit()

    @staticmethod
    def insert_sale():
        with session_factory() as session:
            sale_1 = SaleORM(price=600, id_stock=1, count=1)
            sale_2 = SaleORM(price=550, id_stock=2, count=1)
            sale_3 = SaleORM(price=500, id_stock=3, count=1)
            session.add_all([sale_1, sale_2, sale_3])
            session.commit()

    @staticmethod
    def get_sales_by_publisher(publisher_name: str):
        with session_factory() as session:
            try:
                publisher_id = int(publisher_name)
                filter_condition = PublisherORM.id == publisher_id
            except ValueError:
                no_repeats = re.sub(r'(.+?)\1+', r'\1', publisher_name)
                clean_publisher = re.sub(r'[^А-Яа-я]', '', no_repeats)
                filter_condition = or_(PublisherORM.name.ilike(f"%{clean_publisher}%"),
                                       PublisherORM.name == clean_publisher)
            query = (
                session.query(
                    BookORM.title.label("Название книги"),
                    ShopORM.name.label("Магазин"),
                    SaleORM.price.label("Стоимость"),
                    SaleORM.data_sale.label("Дата покупки")
                )
                .join(SaleORM.stock)
                .join(StockORM.book)
                .join(StockORM.shop)
                .join(BookORM.publisher)
                .filter(filter_condition)
            )
            result = query.all()
            return result
