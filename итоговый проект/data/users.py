import sqlalchemy
from sqlalchemy import orm
import datetime
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    patronymic = sqlalchemy.Column(sqlalchemy.String)
    login = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    level = sqlalchemy.Column(sqlalchemy.Integer)
    password = sqlalchemy.Column(sqlalchemy.String)


class Orders(SqlAlchemyBase):
    __tablename__ = 'orders'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    quality = sqlalchemy.Column(
        sqlalchemy.Integer)  # кол - во заказов    status = sqlalchemy.Column(sqlalchemy.Integer) #(По умолчанию)Новые 0, подтвержденные 1, отмененные 2    created_date = sqlalchemy.Column(sqlalchemy.DateTime,                                      default=datetime.datetime.now)


class Products(SqlAlchemyBase):
    __tablename__ = 'products'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    images = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    prise = sqlalchemy.Column(sqlalchemy.Integer)
    quality = sqlalchemy.Column(
        sqlalchemy.Integer)  # количесвто, < наличие    nal = sqlalchemy.Column(sqlalchemy.Integer) # наличие    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    notes = sqlalchemy.Column(sqlalchemy.String)
    data = sqlalchemy.Column(sqlalchemy.DateTime)

  
class Ticket(SqlAlchemyBase):
    __tablename__ = 'ticket'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.String)
    notes = sqlalchemy.Column(sqlalchemy.String)
    file = sqlalchemy.Column(sqlalchemy.String)



