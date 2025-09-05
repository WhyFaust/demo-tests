from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


class LoginPage:
    """Страница логина."""

    def __init__(self, driver: WebDriver) -> None:
        """Инициализируй страницу логина."""
        self.driver = driver

    @allure.step("Открыть страницу логина")
    def open(self) -> None:
        """Открой страницу логина."""
        self.driver.get("https://www.saucedemo.com/")

    @allure.step("Выполнить вход")
    def login(self, username: str, password: str) -> None:
        """Выполни вход c заданными логином и паролем."""  # латинская c
        self.driver.find_element(By.ID, "user-name").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()

    @allure.step("Проверить отображение формы логина")
    def is_displayed(self) -> bool:
        """Проверь, что форма логина отображается."""
        return bool(
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.ID, "login-button")),
            ),
        )

    @allure.step("Получаем сообщение ошибки")
    def get_error_message(self) -> str:
        element = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        return element.text if element else ""
