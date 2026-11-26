import pytest

from pages.article_page import ArticlePage
from tests.helpers import require_wikimedia_response


@pytest.mark.smoke
def test_TC10_article_heading(driver):
    """TC10: Article heading matches the requested page."""
    page = ArticlePage(driver).load("Software_testing")
    require_wikimedia_response(driver)
    assert page.heading_text == "Software testing"


@pytest.mark.regression
def test_TC11_article_title_contains_wikipedia(driver):
    """TC11: Browser tab title ends with '- Wikipedia'."""
    page = ArticlePage(driver).load("Software_testing")
    require_wikimedia_response(driver)
    assert "Wikipedia" in page.title


@pytest.mark.regression
def test_TC12_infobox_present(driver):
    """TC12: A biographical article contains an infobox."""
    page = ArticlePage(driver).load("Albert_Einstein")
    require_wikimedia_response(driver)
    assert page.is_present(page.INFOBOX)


@pytest.mark.regression
def test_TC13_references_present(driver):
    """TC13: A long article has a references list."""
    page = ArticlePage(driver).load("Software_testing")
    require_wikimedia_response(driver)
    assert page.is_present(page.REFERENCES)


@pytest.mark.regression
def test_TC14_article_has_sections(driver):
    """TC14: Article has multiple section headings."""
    page = ArticlePage(driver).load("Software_testing")
    require_wikimedia_response(driver)
    assert len(page.section_names()) >= 3


@pytest.mark.regression
def test_TC15_article_has_images(driver):
    """TC15: Article contains at least one image."""
    page = ArticlePage(driver).load("Albert_Einstein")
    require_wikimedia_response(driver)
    assert len(page.find_all(page.IMAGES)) > 0


@pytest.mark.regression
def test_TC16_nonexistent_article(driver):
    """TC16: Visiting a non-existent page shows the 'no article' message."""
    page = ArticlePage(driver).load("Thispagedoesnotexist_xyz_98765")
    require_wikimedia_response(driver)
    assert page.missing_article_message_visible()


@pytest.mark.regression
def test_TC17_article_tabs(driver):
    """TC17: Talk, Edit/View-source and History tabs are available."""
    page = ArticlePage(driver).load("Software_testing")
    require_wikimedia_response(driver)
    assert page.is_present(page.TALK_TAB)
    assert page.is_present(page.EDIT_TAB)
    assert page.is_present(page.HISTORY_TAB)
