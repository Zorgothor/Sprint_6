from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def wait_for_element(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    def click_element(self, locator):
        self.wait_for_clickable(locator).click()

    def enter_text(self, locator, text):
        field = self.wait_for_element(locator)
        field.clear()
        field.send_keys(text)