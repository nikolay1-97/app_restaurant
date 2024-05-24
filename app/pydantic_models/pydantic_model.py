"""Модуль со схемами данных запрсов и ответов."""
from decimal import Decimal
from pydantic import BaseModel


class MenuModel(BaseModel):
    """Модель данных создания меню для сужности меню."""

    title: str
    description: str


class MenuModelResp(BaseModel):
    """Модель данных ответа для сущности меню."""

    id: int
    title: str
    description: str


class MenuModelRespGetItem(BaseModel):
    """Модель данных запроса определенного меню."""

    id: int
    title: str
    description: str
    count_of_submenu: int
    count_of_dishs: int


class SubmenuModel(BaseModel):
    """Модель данных создания подменю для сущности подменю."""

    title: str
    description: str


class SubmenuModelResp(BaseModel):
    """Модель данных ответа для сущности подменю."""

    id: int
    title: str
    description: str


class SubmenuModelRespGetItem(BaseModel):
    """Модель данных запроса определенного подменю для сущности подменю."""

    id: int
    title: str
    description: str
    count_of_dishs: int


class DishModel(BaseModel):
    """Модель данных создания позиции блюда для сущности блюдо."""

    title: str
    description: str
    price: str
