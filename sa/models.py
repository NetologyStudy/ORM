from typing import Annotated, Optional
from datetime import date
from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256

intpk = Annotated[int, mapped_column(primary_key=True)]


class PublisherORM(Base):
    __tablename__ = 'publisher'

    id: Mapped[intpk]
    name: Mapped[str_256] = mapped_column(nullable=False, unique=True)

    books: Mapped[list['BookORM']] = relationship(back_populates='publisher', lazy='joined')


class BookORM(Base):
    __tablename__ = 'book'

    id: Mapped[intpk]
    title: Mapped[str_256] = mapped_column(nullable=False, unique=True)
    id_publisher: Mapped[int] = mapped_column(ForeignKey('publisher.id', ondelete='CASCADE'), nullable=False)

    publisher: Mapped['PublisherORM'] = relationship(back_populates='books', lazy='joined')
    stocks: Mapped[list['StockORM']] = relationship(back_populates='book', lazy='joined')


class ShopORM(Base):
    __tablename__ = 'shop'

    id: Mapped[intpk]
    name: Mapped[str_256] = mapped_column(nullable=False, unique=True)

    stocks: Mapped[list['StockORM']] = relationship(back_populates='shop', lazy='joined')


class StockORM(Base):
    __tablename__ = 'stock'

    id: Mapped[intpk]
    id_book: Mapped[int] = mapped_column(ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    id_shop: Mapped[int] = mapped_column(ForeignKey('shop.id', ondelete='CASCADE'), nullable=False)
    count: Mapped[Optional[int]]

    book: Mapped['BookORM'] = relationship(back_populates='stocks', lazy='joined')
    shop: Mapped['ShopORM'] = relationship(back_populates='stocks', lazy='joined')
    sales: Mapped[list['SaleORM']] = relationship(back_populates='stock', lazy='joined')


class SaleORM(Base):
    __tablename__ = 'sale'

    id: Mapped[intpk]
    price: Mapped[int] = mapped_column(nullable=False)
    data_sale: Mapped[date] = mapped_column(server_default=func.current_date(), nullable=False)
    id_stock: Mapped[int] = mapped_column(ForeignKey('stock.id', ondelete='CASCADE'), nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)

    stock: Mapped['StockORM'] = relationship(back_populates='sales', lazy='joined')

    __table_args__ = (
        CheckConstraint('data_sale <= CURRENT_DATE', name='valid_data_sale'),
    )
