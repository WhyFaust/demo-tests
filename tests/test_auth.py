import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"


def test_login(browser: WebDriver) -> None:
    browser.get(URL)

    browser.find_element(By.ID, "user-name").send_keys(USERNAME)
    browser.find_element(By.ID, "password").send_keys(PASSWORD)
    browser.find_element(By.ID, "login-button").click()

    products_title = browser.find_element(By.CLASS_NAME, "title").text
    assert products_title == "Products"
    assert len(browser.find_elements(By.CLASS_NAME, "inventory_item")) > 0

def test_logout(browser: WebDriver) -> None:
    browser.get(URL)

    browser.find_element(By.ID, "user-name").send_keys(USERNAME)
    browser.find_element(By.ID, "password").send_keys(PASSWORD)
    browser.find_element(By.ID, "login-button").click()

    browser.find_element(By.ID, "react-burger-menu-btn").click()
    browser.find_element(By.ID, "logout_sidebar_link").click()

    assert browser.current_url == URL
    assert browser.find_element(By.ID, "login-button").is_displayed()
