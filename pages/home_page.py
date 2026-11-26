"""Page objects for the Wikipedia portal and the English main page."""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base_page import BasePage


class PortalPage(BasePage):
    """https://www.wikipedia.org  (the language-selection portal)"""
    URL = "https://www.wikipedia.org"
    SEARCH_INPUT = (By.ID, "searchInput")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LANG_SELECT = (By.ID, "searchLanguage")

    def load(self):
        self.open(self.URL)
        return self

    def link_for_language(self, code):
        return (By.ID, f"js-link-box-{code}")

    def click_language(self, code):
        self.click(self.link_for_language(code))


class HomePage(BasePage):
    """https://en.wikipedia.org  (English Wikipedia main page)"""
    URL = "https://en.wikipedia.org/wiki/Main_Page"
    SEARCH_INPUT = (By.NAME, "search")
    SUGGESTIONS = (
        By.CSS_SELECTOR,
        "[role='listbox'] [role='option'], .cdx-menu-item, .suggestions-result",
    )
    LOGO = (By.CSS_SELECTOR, "a.mw-logo")
    FEATURED_ARTICLE = (By.ID, "mp-tfa")
    NEWS_SECTION = (By.ID, "mp-itn")
    DID_YOU_KNOW = (By.ID, "mp-dyk")

    def load(self):
        self.open(self.URL)
        return self

    def search(self, text):
        self.type(self.SEARCH_INPUT, text)
        # The input can be replaced after typing; the focused replacement is
        # the reliable target for submitting the search.
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)

    def type_in_search(self, text):
        self.type(self.SEARCH_INPUT, text)

    def get_suggestions(self):
        return [e.text for e in self.find_all(self.SUGGESTIONS) if e.text.strip()]
