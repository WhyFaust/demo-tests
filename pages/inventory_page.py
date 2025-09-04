from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def is_opened(self) -> bool:
        return "inventory.html" in self.driver.current_url

    def logout(self) -> None:
        self.driver.find_element(*self.MENU_BUTTON).click()
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.LOGOUT_LINK)
        ).click()