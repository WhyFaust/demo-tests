import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    URL = "https://www.saucedemo.com/"
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открываем страницу логина")
    def open(self):
        self.driver.get(self.URL)

    @allure.step("Логинимся пользователем: {username}")
    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    @allure.step("Проверяем, что форма логина отображается")
    def is_displayed(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )
        return self.driver.current_url == self.URL
    
    @allure.step("Получаем сообщение об ошибке")
    def get_error_message(self) -> str:
        return self.driver.find_element(*self.ERROR_MESSAGE).text
