
"""Page object for Wikipedia articles and search-result pages."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
)

from .base_page import BasePage


class ArticlePage(BasePage):

    BASE = "https://en.wikipedia.org"

    HEADING = (By.ID, "firstHeading")
    # Vector's current layout no longer assigns ``mw-content-text`` to the
    # article body.  The page's semantic main region is stable across Vector
    # variants and contains the parser output.
    CONTENT = (By.CSS_SELECTOR, "main#content, main")
    INFOBOX = (By.CSS_SELECTOR, "table.infobox")
    REFERENCES = (By.CSS_SELECTOR, "ol.references")
    TOC = (By.CSS_SELECTOR, "#vector-toc, #toc, nav.vector-toc")

    FIRST_INTERNAL_LINK = (
        By.CSS_SELECTOR,
        # MediaWiki currently emits both /wiki/Title and ./Title links,
        # depending on the parser/skin.  Restrict this to article content and
        # exclude namespace links such as File:, Help:, and Category:.
        "main#content a[href^='/wiki/']:not([href*=':']):not(.mw-file-description), "
        "main#content a[href^='./']:not([href*=':']):not(.mw-file-description), "
        "main a[href^='/wiki/']:not([href*=':']):not(.mw-file-description), "
        "main a[href^='./']:not([href*=':']):not(.mw-file-description)"
    )

    NO_ARTICLE = (By.CSS_SELECTOR, ".noarticletext, #noarticletext")
    NO_SEARCH_RESULTS = (By.CSS_SELECTOR, ".mw-search-nonefound")

    # MediaWiki has used both a result class and a list wrapper across skins.
    SEARCH_RESULTS = (
        By.CSS_SELECTOR,
        ".mw-search-result, .mw-search-results > li",
    )

    SECTION_HEADINGS = (By.CSS_SELECTOR, "main#content h2, main h2")
    EDIT_TAB = (By.CSS_SELECTOR, "#ca-edit, #ca-viewsource")
    HISTORY_TAB = (By.ID, "ca-history")
    TALK_TAB = (By.CSS_SELECTOR, "#ca-talk")
    IMAGES = (By.CSS_SELECTOR, "main#content img, main img")

    def load(self, title):
        self.open(f"{self.BASE}/wiki/{title}")
        self._wait_for_article_or_rate_limit()
        return self

    def open_random(self):
        self.open(f"{self.BASE}/wiki/Special:Random")
        self._wait_for_article_or_rate_limit()
        return self

    def _wait_for_article_or_rate_limit(self):
        self.wait.until(
            lambda driver: driver.find_elements(*self.HEADING)
            or "too many requests"
            in driver.find_element(By.TAG_NAME, "body").text.lower()
        )

    @property
    def heading_text(self):
        return self.wait.until(
            lambda driver: (
                driver.find_element(*self.HEADING).text.strip() or False
            )
        )

    def missing_article_message_visible(self):
        self.wait.until(EC.presence_of_element_located(self.HEADING))

        body_text = self.driver.find_element(
            By.TAG_NAME, "body"
        ).text.lower()

        phrases = (
            "wikipedia does not have an article with this exact name",
            "you can create this page",
            "there is currently no text in this page",
        )

        return (
            any(phrase in body_text for phrase in phrases)
            or self.is_present(self.NO_ARTICLE)
        )

    def click_first_internal_link(self):
        def find_clickable_article_link(driver):
            current_url = driver.current_url.rstrip("/")
            # Query the rendered main region rather than relying on one
            # skin-specific content wrapper.  ``href`` here is fully resolved
            # by the browser, so this accepts both ./Title and /wiki/Title.
            return driver.execute_script(
                """
                const current = arguments[0];
                return [...document.querySelectorAll('main a[href]')].find(link => {
                    const href = link.href;
                    return link.offsetParent !== null && link.innerText.trim()
                        && href.includes('/wiki/') && !href.includes('#')
                        && !href.split('/wiki/')[1].includes(':')
                        && href.replace(/\\/$/, '') !== current;
                }) || false;
                """,
                current_url,
            )

        link = self.wait.until(find_clickable_article_link)
        link_text = link.text.strip()

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            link
        )

        try:
            link.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", link)

        return link_text

    def section_names(self):
        return [
            heading.text
            for heading in self.find_all(self.SECTION_HEADINGS)
            if heading.text.strip()
        ]
