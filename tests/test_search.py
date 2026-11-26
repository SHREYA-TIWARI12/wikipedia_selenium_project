import pytest

from pages.article_page import ArticlePage
from pages.home_page import HomePage
from tests.helpers import require_wikimedia_response


@pytest.mark.smoke
def test_TC05_search_opens_expected_article(driver):
    """TC05: Searching from the main page opens the requested article."""
    home = HomePage(driver).load()
    require_wikimedia_response(driver)
    home.search("Selenium (software)")
    require_wikimedia_response(driver)

    assert ArticlePage(driver).heading_text == "Selenium (software)"


@pytest.mark.regression
@pytest.mark.parametrize(
    "query, expected_heading",
    [
        ("Python (programming language)", "Python (programming language)"),
        ("Selenium (software)", "Selenium (software)"),
        ("Software testing", "Software testing"),
    ],
)
def test_TC06_data_driven_search(driver, query, expected_heading):
    """TC06: Each data-driven search opens its corresponding article."""
    home = HomePage(driver).load()
    require_wikimedia_response(driver)
    home.search(query)
    require_wikimedia_response(driver)

    assert ArticlePage(driver).heading_text == expected_heading


@pytest.mark.regression
def test_TC07_search_autocomplete(driver):
    """TC07: Typing a query displays at least one autocomplete suggestion."""
    home = HomePage(driver).load()
    require_wikimedia_response(driver)
    home.type_in_search("Selenium")
    assert home.get_suggestions(), "No autocomplete suggestions were displayed."


@pytest.mark.regression
def test_TC08_invalid_search_shows_no_results(driver):
    """TC08: An unmatchable query displays Wikipedia's no-results message."""
    driver.get(
        "https://en.wikipedia.org/wiki/Special:Search?search=codex_nonexistent_987654321"
    )
    require_wikimedia_response(driver)

    article = ArticlePage(driver)
    assert article.is_present(article.NO_SEARCH_RESULTS), (
        "The expected no-results message was not displayed."
    )


@pytest.mark.regression
def test_TC09_search_results_list(driver):
    """TC09: A broad query returns a list of search results."""

    driver.get(
        "https://en.wikipedia.org/wiki/Special:Search?search=software&fulltext=1&ns0=1"
    )
    require_wikimedia_response(driver)

    article = ArticlePage(driver)

    results = article.find_all(article.SEARCH_RESULTS)

    assert len(results) > 0, "No search results were displayed."
