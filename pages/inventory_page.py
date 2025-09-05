from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


class InventoryPage:
    """Страница товаров."""

    def __init__(self, driver: WebDriver) -> None:
        """Инициализируй страницу."""
        self.driver = driver

    def is_opened(self) -> bool:
        """Проверь, что страница товаров открыта."""
        return bool(
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "inventory_list")),
            ),
        )

    def logout(self) -> None:
        """Выйди из аккаунта."""
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.ID, "logout_sidebar_link")),
        ).click()
