from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver

    def logout(self):
        self.driver.find_element(*self.BURGER_MENU).click()
        self.driver.find_element(*self.LOGOUT_LINK).click()

    def is_opened(self):
        """Проверка, что мы на странице товаров"""
        return WebDriverWait(self.driver, 5).until(
            EC.url_contains("/inventory.html")
        )