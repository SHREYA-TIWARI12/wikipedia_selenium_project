import pytest
from selenium.webdriver.common.by import By


def require_wikimedia_response(driver):
    """Skip a test when Wikimedia temporarily rejects an automated request."""
    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    transient_responses = ("too many requests", "wikimedia error")
    if any(message in body_text for message in transient_responses):
        pytest.skip("Wikimedia temporarily rejected the automated request")
