import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from typing import Generator, Optional, Any

# Сброс системных прокси
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default="chrome", help="Браузер: chrome или firefox")
    parser.addoption("--browser-version", action="store", default=None, help="Версия браузера")

@pytest.fixture
def browser(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    """Фикстура для инициализации браузера"""
    browser_name: str = request.config.getoption("--browser")
    driver: Optional[WebDriver] = None

    if browser_name == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--guest")
        driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    elif browser_name == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--disable-blink-features=AutomationControlled")
        firefox_options.add_argument("--disable-notifications")
        firefox_options.add_argument("--disable-popup-blocking")
        firefox_options.add_argument("--no-default-browser-check")
        firefox_options.add_argument("--no-first-run")
        firefox_options.add_argument("--guest")
        driver = webdriver.Firefox(service=FirefoxService(), options=firefox_options)
    else:
        raise ValueError(f"Неизвестный браузер: {browser_name}")

    assert driver is not None
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Any, call: "pytest.CallInfo[None]") -> Generator[None, None, None]:
    """Hook для скриншотов при падении теста"""
    outcome: Any = yield  # mypy не знает точный тип
    rep: Any = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver: Optional[WebDriver] = None
        try:
            driver = item.getfixturevalue("browser")
        except Exception:
            pass

        if driver:
            screenshot: bytes = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )