
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from constants import BASE_URL
from pages.base_page import BasePage


class MainPage(BasePage):

    FAQ_BUTTONS = (By.CSS_SELECTOR, ".accordion__button")

    ORDER_BUTTONS = (
        By.XPATH,
        "//button[contains(@class, 'Button_Button') "
        "and normalize-space(.)='Заказать']"
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
        super().__init__(driver)

    def open(self):
        self.driver.get(BASE_URL)

    def click_faq_question(self, index):
        questions = self.wait.until(
            EC.presence_of_all_elements_located(self.FAQ_BUTTONS)
        )

        question = questions[index]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            question
        )

        question = self.wait_for_clickable(
            (By.ID, f"accordion__heading-{index}")
        )

        question.click()

        answer_locator = (
            By.ID,
            f"accordion__panel-{index}"
        )

        self.wait_for_element(answer_locator)

    def get_faq_answer(self, index):
        answer_locator = (
            By.ID,
            f"accordion__panel-{index}"
        )

        return self.find_element(answer_locator).text

    def click_order_button(self, button_index):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.ORDER_BUTTONS)
        )

        button = buttons[button_index]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        self.wait.until(
            lambda driver: button.is_displayed() and button.is_enabled()
        )

        button.click()

    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    def click_yandex_logo(self):
        old_handles = self.driver.window_handles

        self.click_element(self.YANDEX_LOGO)

        self.wait.until(
            EC.new_window_is_opened(old_handles)
        )

        new_handle = next(
            handle
            for handle in self.driver.window_handles
            if handle not in old_handles
        )

        self.driver.switch_to.window(new_handle)

        self.wait.until(
            EC.url_contains("dzen.ru")
        )
