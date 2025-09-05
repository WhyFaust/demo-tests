import allure
import pytest
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from selenium.webdriver.remote.webdriver import WebDriver

USERS = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
]

PASSWORD = "secret_sauce"  # тестовый пароль


@allure.feature("Авторизация")
@pytest.mark.parametrize("username", USERS)
def test_login_users(browser: WebDriver, username: str) -> None:
    """Протестируй авторизацию для всех пользователей."""
    login_page = LoginPage(browser)
    inventory_page = InventoryPage(browser)

    login_page.open()
    login_page.login(username, PASSWORD)

    if username == "locked_out_user":
        with allure.step("Проверяем сообщение ошибки"):  # type: ignore[attr-defined]
            error_msg = login_page.get_error_message()
            assert "locked out" in error_msg.lower()
    else:
        with allure.step("Проверяем, что открыта страница товаров"):  # type: ignore[attr-defined]
            assert inventory_page.is_opened()


@allure.feature("Авторизация")
def test_logout(browser: WebDriver) -> None:
    """Протестируй выход из аккаунта."""
    login_page = LoginPage(browser)
    inventory_page = InventoryPage(browser)

    login_page.open()
    login_page.login("standard_user", PASSWORD)
    inventory_page.logout()

    assert login_page.is_displayed()
