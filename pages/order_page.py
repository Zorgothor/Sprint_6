
import allure

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from constants import BASE_URL
from pages.base_page import BasePage


class OrderPage(BasePage):

    # Первый экран
    NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    SURNAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    # Второй экран
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_DROPDOWN = (By.CLASS_NAME, "Dropdown-control")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    BACK_BUTTON = (By.XPATH, "//button[text()='Назад']")
    ORDER_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'Order_Buttons')]//button[text()='Заказать']"
    )

    # Цвет самоката
    BLACK_COLOR = (By.ID, "black")
    GREY_COLOR = (By.ID, "grey")

    # Модальные окна
    CONFIRM_MODAL = (By.CLASS_NAME, "Order_Modal__YZ-d3")
    CONFIRM_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'Order_Modal')]//button[text()='Да']"
    )
    SUCCESS_MODAL = (
        By.XPATH,
        "//div[contains(@class, 'Order_Modal')]"
        "[.//*[contains(text(), 'Заказ оформлен')]]"
    )

    # Баннер cookie
    COOKIE_BANNER = (By.CLASS_NAME, "App_CookieConsent__1yUIN")

    @allure.step("Инициализация страницы оформления заказа")
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Открыть страницу оформления заказа")
    def open(self):
        self.open_url(BASE_URL)

    @allure.step("Закрыть баннер cookie, если он отображается")
    def close_cookie_banner(self):
        banners = self.find_elements(self.COOKIE_BANNER)

        if banners and self.is_web_element_displayed(banners[0]):
            buttons = self.find_child_elements(
                banners[0],
                By.TAG_NAME,
                "button"
            )

            if buttons:
                self.click_web_element(buttons[0])

    @allure.step("Заполнить данные заказчика")
    def fill_customer_data(self, data):
        self.enter_text(self.NAME_INPUT, data["name"])
        self.enter_text(self.SURNAME_INPUT, data["surname"])
        self.enter_text(self.ADDRESS_INPUT, data["address"])

        self.close_cookie_banner()

        self.click_element(self.METRO_INPUT)
        self.enter_text(self.METRO_INPUT, data["metro"])

        metro_option = (
            By.XPATH,
            "//button[contains(@class, 'select-search__option') "
            f"and normalize-space(.)='{data['metro']}']"
        )

        self.click_element(metro_option)

        self.enter_text(self.PHONE_INPUT, data["phone"])
        self.click_element(self.NEXT_BUTTON)

    @allure.step("Заполнить данные аренды")
    def fill_rental_data(self, data):
        self.click_element(self.DATE_INPUT)
        self.send_keys(self.DATE_INPUT, data["date"])
        self.send_keys(self.DATE_INPUT, Keys.ESCAPE)

        self.wait_until_invisible(
            (By.CLASS_NAME, "react-datepicker")
        )

        self.scroll_to_element(self.RENTAL_DROPDOWN)
        self.click_element(self.RENTAL_DROPDOWN)

        rental_option = (
            By.XPATH,
            f"//*[contains(@class, 'Dropdown-option') "
            f"and normalize-space()='{data['rental_period']}']"
        )

        self.click_element(rental_option)

        if data["color"] == "black":
            self.click_element(self.BLACK_COLOR)
        else:
            self.click_element(self.GREY_COLOR)

        self.enter_text(self.COMMENT_INPUT, data["comment"])

    @allure.step("Отправить заказ")
    def submit_order(self):
        self.click_element(self.ORDER_BUTTON)

    @allure.step("Подтвердить оформление заказа")
    def confirm_order(self):
        self.wait_for_element(self.CONFIRM_MODAL)
        self.click_element(self.CONFIRM_BUTTON)

    @allure.step("Получить сообщение об успешном оформлении заказа")
    def get_success_message(self):
        return self.get_element_text(self.SUCCESS_MODAL)
