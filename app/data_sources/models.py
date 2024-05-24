"""Модели таблиц базы данных."""

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import DB_URL


metadata = MetaData()
engine = create_async_engine(DB_URL)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


Menu_model = Table(
    "menu",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('title', String, nullable=False, unique=True),
    Column("description", String, nullable=False),
)

Submenu_model = Table(
    'submenu',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('title', String, nullable=False, unique=True),
    Column('description', String, nullable=False),
    Column('from_menu', Integer, ForeignKey("menu.id")),
)

Dish_model = Table(
    'dish',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('title', String, nullable=False, unique=True),
    Column('description', String, nullable=False),
    Column('price', Float, nullable=False),
    Column('from_submenu', Integer, ForeignKey("submenu.id")),
)
