"""Pytest fixtures and hooks shared by all tests."""
import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="chrome or firefox")
    parser.addoption("--headless", action="store_true", help="Run without a visible browser")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    if browser == "firefox":
        opts = FirefoxOptions()
        if headless:
            opts.add_argument("-headless")
        drv = webdriver.Firefox(options=opts)
    else:
        opts = ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--disable-notifications")
        drv = webdriver.Chrome(options=opts)

    # Keep all element synchronization explicit and put an upper bound on a
    # navigation.  Wikipedia is a live site; without this, a slow response can
    # leave an entire pytest run stuck indefinitely.
    drv.implicitly_wait(0)
    drv.set_page_load_timeout(45)
    drv.set_script_timeout(30)
    drv.set_window_size(1920, 1080)

    try:
        yield drv
    finally:
        # A failed setup/navigation must not leave a browser process behind.
        drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take a screenshot automatically when a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs("screenshots", exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"screenshots/{item.name}_{stamp}.png"
            drv.save_screenshot(path)
            print(f"\nScreenshot saved: {path}")
