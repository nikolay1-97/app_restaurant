"""Модели"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import Session
from config import DB_URL


metadata = MetaData()
engine = create_engine(DB_URL)

def connect_db():
    session = Session(bind=engine.connect())
    return session


Menu_model = Table(
    "menu",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('title', String, nullable=False, unique=True),
    Column("description", String, nullable=False, unique=True),
)

Submenu_model = Table(
    'submenu',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('title', String, nullable=False, unique=True),
    Column('description', String, nullable=False, unique=True),
    Column('from_menu', Integer, ForeignKey("menu.id")),
)

Dish_model = Table(
   'dish',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=False),
    Column('price', Float, nullable=False),
    Column('from_submenu', Integer, ForeignKey("submenu.id")),
)
