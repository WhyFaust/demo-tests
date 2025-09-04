import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

USERS = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
]

PASSWORD = "secret_sauce"

@allure.feature("Авторизация")
@pytest.mark.parametrize("username", USERS)
def test_login_users(browser, username):
    login_page = LoginPage(browser)
    inventory_page = InventoryPage(browser)

    login_page.open()
    login_page.login(username, PASSWORD)

    if username == "locked_out_user":
        with allure.step("Проверяем сообщение об ошибке"):
            error_msg = login_page.get_error_message()
            assert "locked out" in error_msg.lower()
    else:
        with allure.step("Проверяем, что открыта страница товаров"):
            assert inventory_page.is_opened()

@allure.feature("Логаут")
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