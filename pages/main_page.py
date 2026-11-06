
import allure

from selenium.webdriver.common.by import By

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

    @allure.step("Инициализация главной страницы")
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Открыть главную страницу")
    def open(self):
        self.open_url(BASE_URL)

    @allure.step("Открыть вопрос FAQ с индексом {index}")
    def click_faq_question(self, index):
        question_locator = (
            By.ID,
            f"accordion__heading-{index}"
        )

        self.scroll_to_element(question_locator)
        self.click_element(question_locator)

        answer_locator = (
            By.ID,
            f"accordion__panel-{index}"
        )

        self.wait_for_element(answer_locator)

    @allure.step("Получить ответ FAQ с индексом {index}")
    def get_faq_answer(self, index):
        answer_locator = (
            By.ID,
            f"accordion__panel-{index}"
        )

        return self.get_element_text(answer_locator)

    @allure.step("Нажать на кнопку заказа с индексом {button_index}")
    def click_order_button(self, button_index):
        self.click_element_by_index(
            self.ORDER_BUTTONS,
            button_index
        )

    @allure.step("Нажать на логотип Самоката")
    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    @allure.step("Нажать на логотип Яндекса и перейти на новую вкладку")
    def click_yandex_logo(self):
        old_handles = self.get_window_handles()

        self.click_element(self.YANDEX_LOGO)
        self.wait_for_new_window(old_handles)
        self.switch_to_new_window(old_handles)
        self.wait_for_url_contains("dzen.ru")
