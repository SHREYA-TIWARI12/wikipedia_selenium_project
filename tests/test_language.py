import pytest

from pages.home_page import PortalPage


@pytest.mark.regression
def test_TC23_portal_loads(driver):
    """TC23: Wikipedia portal loads with a search box."""
    portal = PortalPage(driver).load()
    assert "Wikipedia" in portal.title
    assert portal.is_present(portal.SEARCH_INPUT)


@pytest.mark.regression
@pytest.mark.parametrize("code, domain", [
    ("en", "en.wikipedia.org"),
    ("es", "es.wikipedia.org"),
    ("de", "de.wikipedia.org"),
    ("fr", "fr.wikipedia.org"),
])
def test_TC24_language_links(driver, code, domain):
    """TC24: Language links on the portal open the right Wikipedia edition."""
    portal = PortalPage(driver).load()
    portal.click_language(code)
    portal.wait.until(lambda d: domain in d.current_url)
    assert domain in portal.url
