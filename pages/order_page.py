
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import BASE_URL


class OrderPage:

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
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(BASE_URL)

    def close_cookie_banner(self):
        banners = self.driver.find_elements(*self.COOKIE_BANNER)

        if banners and banners[0].is_displayed():
            buttons = banners[0].find_elements(By.TAG_NAME, "button")

            if buttons:
                buttons[0].click()

    def enter_text(self, locator, text):
        field = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        field.clear()
        field.send_keys(text)

    def fill_customer_data(self, data):
        self.enter_text(self.NAME_INPUT, data["name"])
        self.enter_text(self.SURNAME_INPUT, data["surname"])
        self.enter_text(self.ADDRESS_INPUT, data["address"])

        self.close_cookie_banner()

        self.enter_text(self.METRO_INPUT, data["metro"])

        metro_option = (
            By.XPATH,
            f"//button[contains(@class, 'select-search__option') "
            f"and .//div[normalize-space()='{data['metro']}']]"
        )

        self.wait.until(
            EC.visibility_of_element_located(metro_option)
        )

        self.close_cookie_banner()

        self.wait.until(
            EC.element_to_be_clickable(metro_option)
        ).click()

        self.enter_text(self.PHONE_INPUT, data["phone"])

        self.wait.until(
            EC.element_to_be_clickable(self.NEXT_BUTTON)
        ).click()

    def fill_rental_data(self, data):
        date_field = self.wait.until(
            EC.visibility_of_element_located(self.DATE_INPUT)
        )

        date_field.click()
        date_field.send_keys(data["date"])
        date_field.send_keys(Keys.ESCAPE)

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CLASS_NAME, "react-datepicker")
            )
        )

        dropdown = self.wait.until(
            EC.element_to_be_clickable(self.RENTAL_DROPDOWN)
        )

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

        self.wait.until(
            EC.element_to_be_clickable(rental_option)
        ).click()

        if data["color"] == "black":
            self.wait.until(
                EC.element_to_be_clickable(self.BLACK_COLOR)
            ).click()
        else:
            self.wait.until(
                EC.element_to_be_clickable(self.GREY_COLOR)
            ).click()

        self.enter_text(self.COMMENT_INPUT, data["comment"])

    def submit_order(self):
        self.wait.until(
            EC.element_to_be_clickable(self.ORDER_BUTTON)
        ).click()

    def confirm_order(self):
        self.wait.until(
            EC.visibility_of_element_located(self.CONFIRM_MODAL)
        )

        self.wait.until(
            EC.element_to_be_clickable(self.CONFIRM_BUTTON)
        ).click()

    def get_success_message(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.SUCCESS_MODAL)
        ).text
