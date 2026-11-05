
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        self.driver.get(BASE_URL)

    def close_cookie_banner(self):
        banners = self.driver.find_elements(*self.COOKIE_BANNER)

        if banners and banners[0].is_displayed():
            buttons = banners[0].find_elements(By.TAG_NAME, "button")

            if buttons:
                buttons[0].click()

    def fill_customer_data(self, data):
        self.enter_text(self.NAME_INPUT, data["name"])
        self.enter_text(self.SURNAME_INPUT, data["surname"])
        self.enter_text(self.ADDRESS_INPUT, data["address"])

        self.close_cookie_banner()

        metro_field = self.wait_for_element(self.METRO_INPUT)
        metro_field.click()
        metro_field.clear()
        metro_field.send_keys(data["metro"])

        metro_option = (
            By.XPATH,
            "//button[contains(@class, 'select-search__option') "
            f"and normalize-space(.)='{data['metro']}']"
        )

        metro_button = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(metro_option)
        )

        metro_button.click()

        self.enter_text(self.PHONE_INPUT, data["phone"])
        self.click_element(self.NEXT_BUTTON)

    def fill_rental_data(self, data):
        date_field = self.wait_for_element(self.DATE_INPUT)

        date_field.click()
        date_field.send_keys(data["date"])
        date_field.send_keys(Keys.ESCAPE)

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CLASS_NAME, "react-datepicker")
            )
        )

        dropdown = self.wait_for_clickable(self.RENTAL_DROPDOWN)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            dropdown
        )

        dropdown.click()

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

    def submit_order(self):
        self.click_element(self.ORDER_BUTTON)

    def confirm_order(self):
        self.wait_for_element(self.CONFIRM_MODAL)
        self.click_element(self.CONFIRM_BUTTON)

    def get_success_message(self):
        return self.wait_for_element(self.SUCCESS_MODAL).text
