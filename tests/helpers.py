import pytest
from selenium.webdriver.common.by import By


def require_wikimedia_response(driver):
    """Skip a test when Wikimedia's temporary HTTP 429 page is displayed."""
    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    if "too many requests" in body_text:
        pytest.skip("Wikimedia returned HTTP 429; retry after the rate limit clears")
