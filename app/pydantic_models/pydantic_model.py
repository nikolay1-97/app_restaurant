"""Модуль со схемами данных запрсов и ответов."""
from decimal import Decimal

from pydantic import BaseModel


class MenuModel(BaseModel):
    """
    Модель для данных о меню.

    Модель для данных о меню.
    """

    title: str
    description: str

class MenuModelUpdate(BaseModel):
    """
    Модель для данных о меню.

    Модель для данных о меню.
    """

    menu_name: str
    new_menu_name: str


class SubmenuModel(BaseModel):
    """
    Модель для данных о меню.

    Модель для данных о меню.
    """

    title: str
    description: str


class SubmenuModelUpdate(BaseModel):
    """
    Модель для данных о подменю.

    Модель для данных о подменю.
    """

    submenu_name: str
    submenu_new_name: str
    new_from_menu: int


class DishModel(BaseModel):
    """
    Модель для данных о наименованиях блюд.

    Модель для данных о наименованиях блюд.
    """

    title: str
    description: str
    price: str


class DishModelUpdate(BaseModel):
    """
    Модель для данных о наименованиях блюд.

    Модель для данных о наименованиях блюд.
    """

    name: str
    new_name: str
    new_price: float
    new_from_submenu: int
