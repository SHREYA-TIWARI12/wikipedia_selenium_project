import pytest

from pages.article_page import ArticlePage
from pages.home_page import HomePage


@pytest.mark.smoke
def test_TC01_main_page_title(driver):
    """TC01: Main page loads with correct title."""
    home = HomePage(driver).load()
    assert "Wikipedia" in home.title


@pytest.mark.smoke
def test_TC02_main_page_url(driver):
    """TC02: Main page URL is the English Wikipedia domain."""
    home = HomePage(driver).load()
    assert home.url.startswith("https://en.wikipedia.org")


@pytest.mark.regression
def test_TC03_main_page_sections_visible(driver):
    """TC03: Featured article, In the news and Did you know sections exist."""
    home = HomePage(driver).load()
    assert home.find(home.FEATURED_ARTICLE).is_displayed()
    assert home.find(home.NEWS_SECTION).is_displayed()
    assert home.find(home.DID_YOU_KNOW).is_displayed()


@pytest.mark.regression
def test_TC04_logo_returns_to_main_page(driver):
    """TC04: Clicking the logo from an article returns to the main page."""
    ArticlePage(driver).load("Python_(programming_language)")
    home = HomePage(driver)
    home.click(home.LOGO)
    home.wait.until(
        lambda d: "Main_Page" in d.current_url
        or d.current_url.rstrip("/") == "https://en.wikipedia.org"
    )
    assert "Main_Page" in home.url or home.url.rstrip("/") == "https://en.wikipedia.org"
