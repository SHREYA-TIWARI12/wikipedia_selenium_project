import pytest

from pages.article_page import ArticlePage
from tests.helpers import require_wikimedia_response


@pytest.mark.smoke
def test_TC18_random_article(driver):
    """TC18: Special:Random loads some article with a heading."""
    page = ArticlePage(driver)
    page.open_random()
    require_wikimedia_response(driver)
    assert page.heading_text.strip() != ""


@pytest.mark.regression
def test_TC19_click_internal_link(driver):
    """TC19: Clicking an internal link navigates to a different article."""
    page = ArticlePage(driver).load("Software_testing")
    old_url = page.url
    page.click_first_internal_link()
    page.wait.until(lambda d: d.current_url != old_url)
    assert page.url != old_url
    assert "/wiki/" in page.url


@pytest.mark.regression
def test_TC20_browser_back_forward(driver):
    """TC20: Browser back and forward buttons work."""
    page = ArticlePage(driver).load("Software_testing")
    first_url = page.url
    page.open(f"{ArticlePage.BASE}/wiki/Selenium_(software)")
    second_url = page.url
    driver.back()
    assert page.url == first_url
    driver.forward()
    assert page.url == second_url


@pytest.mark.regression
def test_TC21_page_refresh(driver):
    """TC21: Refreshing keeps the same page."""
    page = ArticlePage(driver).load("Software_testing")
    url = page.url
    driver.refresh()
    assert page.url == url
    assert page.heading_text == "Software testing"


@pytest.mark.regression
def test_TC22_history_tab_opens(driver):
    """TC22: Clicking the History tab opens the revision history."""
    page = ArticlePage(driver).load("Software_testing")
    page.click(page.HISTORY_TAB)
    assert "action=history" in page.url
