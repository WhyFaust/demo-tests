import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_login(browser):
    login_page = LoginPage(browser)
    inventory_page = InventoryPage(browser)

    # открываем страницу логина
    login_page.open()

    # логинимся
    login_page.login("standard_user", "secret_sauce")

    # проверяем, что открылась страница товаров
    assert inventory_page.is_opened()


def test_logout(browser):
    login_page = LoginPage(browser)
    inventory_page = InventoryPage(browser)

    # логинимся
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert inventory_page.is_opened()

    # разлогиниваемся
    inventory_page.logout()

    # проверяем, что снова открылась форма логина
    assert login_page.is_displayed()