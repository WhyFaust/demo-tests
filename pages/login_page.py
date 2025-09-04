import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    URL: str = "https://www.saucedemo.com/"
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    @allure.step("Открываем страницу логина")
    def open(self) -> None:
        self.driver.get(self.URL)

    @allure.step("Логинимся пользователем: {username}")
    def login(self, username: str, password: str) -> None:
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    @allure.step("Проверяем, что форма логина отображается")
    def is_displayed(self) -> bool:
        """Проверка, что форма логина отображается"""
        return bool(
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.USERNAME_INPUT)
            )
        )

    @allure.step("Получаем сообщение об ошибке")
    def get_error_message(self) -> str:
        element = self.driver.find_element(*self.ERROR_MESSAGE)
        return element.text if element else ""