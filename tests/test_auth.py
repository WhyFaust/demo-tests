import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from selenium.webdriver.remote.webdriver import WebDriver

USERS = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
]

PASSWORD = "secret_sauce"

@allure.feature("Авторизация") # type: ignore
@pytest.mark.parametrize("username", USERS)
def test_login_users(browser: WebDriver, username: str) -> None:
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

@allure.feature("Логаут") # type: ignore
def test_logout(browser: WebDriver) -> None:
    login_page = LoginPage(browser)
    inventory_page = InventoryPage(browser)

    login_page.open()
    login_page.login("standard_user", PASSWORD)
    assert inventory_page.is_opened()

    inventory_page.logout()
    assert login_page.is_displayed()