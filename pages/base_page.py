"""Base page: reusable Selenium helpers with explicit, stale-safe waits."""
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    TIMEOUT = 20

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver, self.TIMEOUT,
            ignored_exceptions=(StaleElementReferenceException,),
        )

    def open(self, url):
        self.driver.get(url)
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )
        return self

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text):
        # Wikipedia may replace its progressively enhanced search input while
        # it is being focused. Reacquire it once if that render occurs.
        for attempt in range(2):
            try:
                element = self.wait.until(EC.visibility_of_element_located(locator))
                # clear() is inconsistent on Wikipedia's progressively enhanced
                # search input; selecting all works works for both input forms.
                element.send_keys(Keys.CONTROL, "a")
                element.send_keys(Keys.BACKSPACE)
                element.send_keys(text)
                return element
            except StaleElementReferenceException:
                if attempt:
                    raise

    def is_present(self, locator, timeout=5):
        try:
            WebDriverWait(
                self.driver, timeout,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    @property
    def title(self):
        return self.driver.title

    @property
    def url(self):
        return self.driver.current_url
