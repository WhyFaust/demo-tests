import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Сброс системных прокси
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default="chrome", help="Браузер: chrome или firefox")
    parser.addoption("--browser-version", action="store", default=None, help="Версия браузера (для Selenoid)")


@pytest.fixture
def browser(request: pytest.FixtureRequest):
    browser_name = request.config.getoption("--browser")

    if browser_name == "chrome":
        options = ChromeOptions()
        driver = webdriver.Chrome(service=ChromeService(), options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        driver = webdriver.Firefox(service=FirefoxService(), options=options)
    else:
        raise ValueError(f"Неизвестный браузер: {browser_name}")

    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()
