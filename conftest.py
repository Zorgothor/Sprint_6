
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("-width=1920")
    options.add_argument("-height=1080")

    browser = webdriver.Firefox(options=options)

    browser.maximize_window()

    yield browser

    browser.quit()
