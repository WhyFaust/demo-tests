from __future__ import annotations

import contextlib
import os
from typing import TYPE_CHECKING, Any

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

if TYPE_CHECKING:
    from collections.abc import Generator

    from selenium.webdriver.remote.webdriver import WebDriver


os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Добавь параметры командной строки."""
    parser.addoption("--browser", action="store", default="chrome", help="Браузер: chrome или firefox")
    parser.addoption("--browser-version", action="store", default=None, help="Версия браузера")


@pytest.fixture
def browser(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    """Создай браузер и верни драйвер."""
    browser_name: str = request.config.getoption("--browser")
    driver: WebDriver

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
        driver = webdriver.Firefox(service=FirefoxService(), options=firefox_options)
    else:
        raise ValueError(f"Неизвестный браузер: {browser_name}")

    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Any, call: pytest.CallInfo[None]) -> Generator[None, None, None]:  # noqa: ARG001
    """Сделай скриншот при падении теста."""
    outcome: Any = yield
    rep: Any = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = None
        with contextlib.suppress(Exception):
            driver = item.getfixturevalue("browser")
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="screenshot",
                attachment_type=allure.AttachmentType.PNG,
            )
