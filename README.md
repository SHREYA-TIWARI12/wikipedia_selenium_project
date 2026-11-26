# Wikipedia Test Automation using Selenium

A software testing project that automates functional testing of
[Wikipedia](https://www.wikipedia.org) with **Selenium WebDriver**, **Python** and **pytest**,
using the **Page Object Model (POM)** design pattern.

## 1. Project Overview
| Item | Details |
|---|---|
| Application Under Test | Wikipedia (en.wikipedia.org, www.wikipedia.org) |
| Testing Type | Functional / UI automation testing (black-box) |
| Tool | Selenium WebDriver 4 |
| Language | Python 3.9+ |
| Framework | pytest + pytest-html |
| Design Pattern | Page Object Model |
| Browsers | Chrome (default), Firefox |

## 2. Objectives
- Verify the main features of Wikipedia: search, article display, navigation and language selection.
- Reduce manual effort through automation and reusable page objects.
- Generate an HTML report and capture screenshots for failed tests.

## 3. Project Structure
```
wikipedia_selenium_project/
├── conftest.py          # driver fixture, CLI options, screenshot-on-failure hook
├── pytest.ini           # pytest config + HTML report + markers
├── requirements.txt
├── pages/               # Page Object classes
│   ├── base_page.py     # reusable Selenium helpers (waits, click, type)
│   ├── home_page.py     # PortalPage and HomePage
│   └── article_page.py  # ArticlePage
├── tests/               # test cases
│   ├── test_homepage.py   (TC01-TC04)
│   ├── test_search.py     (TC05-TC09)
│   ├── test_article.py    (TC10-TC17)
│   ├── test_navigation.py (TC18-TC22)
│   └── test_language.py   (TC23-TC24)
├── screenshots/         # auto-saved on failure
└── reports/report.html  # generated after each run
```

## 4. Setup
```bash
# 1. Install Python 3.9+ and Google Chrome
# 2. Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / Mac

# 3. Install dependencies
pip install -r requirements.txt
```
Selenium 4.6+ downloads the correct browser driver automatically (Selenium Manager), so no manual chromedriver setup is needed.

## 5. Running the Tests
```bash
pytest                                  # run everything (Chrome)
pytest --headless                       # without opening a browser window
pytest --browser=firefox                # run on Firefox
pytest -m smoke                         # only smoke tests
pytest tests/test_search.py             # one file
pytest -k "TC05"                        # one test case
```
Open `reports/report.html` in a browser to see the results.

## 6. Test Cases
| ID | Module | Description | Expected Result |
|---|---|---|---|
| TC01 | Home | Main page title | Title contains "Wikipedia" |
| TC02 | Home | Main page URL | URL starts with en.wikipedia.org |
| TC03 | Home | Main page sections | Featured article, news, DYK visible |
| TC04 | Home | Logo click | Returns to main page |
| TC05 | Search | Search "Selenium (software)" | Article opens with correct heading |
| TC06 | Search | Data-driven search (3 terms) | Each article heading matches |
| TC07 | Search | Autocomplete | Suggestions appear while typing |
| TC08 | Search | Invalid search term | "No results" message shown |
| TC09 | Search | Broad search | List of results shown |
| TC10 | Article | Heading check | Heading equals "Software testing" |
| TC11 | Article | Page title | Contains "Wikipedia" |
| TC12 | Article | Infobox | Infobox present on biography page |
| TC13 | Article | References | Reference list present |
| TC14 | Article | Sections | At least 3 section headings |
| TC15 | Article | Images | At least 1 image |
| TC16 | Article | Non-existent page | "No article" message shown |
| TC17 | Article | Tabs | Talk, Edit, History tabs present |
| TC18 | Navigation | Random article | Article with heading opens |
| TC19 | Navigation | Internal link | Navigates to a new article |
| TC20 | Navigation | Back / Forward | URLs restore correctly |
| TC21 | Navigation | Refresh | Same page remains |
| TC22 | Navigation | History tab | URL contains action=history |
| TC23 | Language | Portal loads | Title and search box present |
| TC24 | Language | EN/ES/DE/FR links | Correct Wikipedia edition opens |

Total: 24 test case IDs (29 executed tests including parameterized runs).

## 7. Key Concepts Demonstrated
- Locators: ID, NAME, CSS selector
- Explicit waits (`WebDriverWait` + `expected_conditions`)
- Page Object Model
- pytest fixtures, markers and parameterization (data-driven testing)
- Automatic screenshots on failure
- HTML test reporting
- Cross-browser testing (Chrome / Firefox)

## 8. Limitations and Future Scope
- Tests depend on live Wikipedia, so layout changes can break locators.
- Future work: CI with GitHub Actions, Selenium Grid, login and edit tests, API tests.

## 9. Conclusion
The project automates core Wikipedia user flows with Selenium, showing how a maintainable, data-driven framework can replace repetitive manual testing.
