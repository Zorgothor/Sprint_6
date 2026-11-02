
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import BASE_URL


class MainPage:

    FAQ_BUTTONS = (By.CSS_SELECTOR, ".accordion__button")

    ORDER_BUTTONS = (
        By.CSS_SELECTOR,
        "button.Button_Button__ra12g:not(.Header_Button__28dPO)"
    )

    SCOOTER_LOGO = (
        By.CSS_SELECTOR,
        "a.Header_LogoScooter__3lsAR"
    )

    YANDEX_LOGO = (
        By.CSS_SELECTOR,
        "a.Header_LogoYandex__3TSOI"
    )

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(BASE_URL)

    def click_faq_question(self, index):
        questions = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located(self.FAQ_BUTTONS)
        )

        question = questions[index]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            question
        )

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, f"accordion__heading-{index}")
            )
        )

        question.click()

        answer_locator = (
            By.ID,
            f"accordion__panel-{index}"
        )

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(answer_locator)
        )

    def get_faq_answer(self, index):
        answer_locator = (
            By.ID,
            f"accordion__panel-{index}"
        )

        return self.driver.find_element(*answer_locator).text

    def click_order_button(self, button_index):
        buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.ORDER_BUTTONS)
        )

        button = buttons[button_index]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        WebDriverWait(self.driver, 10).until(
            lambda driver: button.is_displayed() and button.is_enabled()
        )

        button.click()

    def click_scooter_logo(self):
        logo = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SCOOTER_LOGO)
        )
        logo.click()

    def click_yandex_logo(self):
        old_handles = self.driver.window_handles

        logo = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.YANDEX_LOGO)
        )
        logo.click()

        WebDriverWait(self.driver, 10).until(
            EC.new_window_is_opened(old_handles)
        )

        new_handle = next(
            handle
            for handle in self.driver.window_handles
            if handle not in old_handles
        )

        self.driver.switch_to.window(new_handle)

        WebDriverWait(self.driver, 20).until(
            EC.url_contains("dzen.ru")
        )
