
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    @allure.step("Инициализация базовой страницы")
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть страницу: {url}")
    def open_url(self, url):
        self.driver.get(url)

    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator):
        return self.driver.find_element(*locator)

    @allure.step("Найти все элементы: {locator}")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Найти вложенные элементы")
    def find_child_elements(self, element, by, value):
        return element.find_elements(by, value)

    @allure.step("Дождаться появления элемента: {locator}")
    def wait_for_element(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Дождаться кликабельности элемента: {locator}")
    def wait_for_clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Дождаться появления списка элементов: {locator}")
    def wait_for_all_elements(self, locator):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )

    @allure.step("Дождаться исчезновения элемента: {locator}")
    def wait_until_invisible(self, locator):
        return self.wait.until(
            EC.invisibility_of_element_located(locator)
        )

    @allure.step("Нажать на элемент: {locator}")
    def click_element(self, locator):
        self.wait_for_clickable(locator).click()

    @allure.step("Нажать на элемент по индексу: {index}")
    def click_element_by_index(self, locator, index):
        elements = self.wait_for_all_elements(locator)
        element = elements[index]

        self.scroll_element_into_view(element)

        self.wait.until(
            lambda driver: element.is_displayed() and element.is_enabled()
        )

        element.click()

    @allure.step("Прокрутить страницу к элементу")
    def scroll_element_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

    @allure.step("Прокрутить страницу к элементу: {locator}")
    def scroll_to_element(self, locator):
        element = self.wait_for_element(locator)
        self.scroll_element_into_view(element)
        return element

    @allure.step("Ввести текст в поле: {locator}")
    def enter_text(self, locator, text):
        field = self.wait_for_element(locator)
        field.clear()
        field.send_keys(text)

    @allure.step("Отправить клавиши в элемент: {locator}")
    def send_keys(self, locator, keys):
        element = self.wait_for_element(locator)
        element.send_keys(keys)

    @allure.step("Получить текст элемента: {locator}")
    def get_element_text(self, locator):
        return self.find_element(locator).text

    @allure.step("Проверить отображение элемента")
    def is_element_displayed(self, locator):
        return self.wait_for_element(locator).is_displayed()

    @allure.step("Проверить отображение найденного элемента")
    def is_web_element_displayed(self, element):
        return element.is_displayed()

    @allure.step("Нажать на найденный WebElement")
    def click_web_element(self, element):
        element.click()

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Получить открытые вкладки браузера")
    def get_window_handles(self):
        return self.driver.window_handles

    @allure.step("Дождаться открытия новой вкладки")
    def wait_for_new_window(self, old_handles):
        self.wait.until(
            EC.new_window_is_opened(old_handles)
        )

    @allure.step("Переключиться на новую вкладку")
    def switch_to_new_window(self, old_handles):
        new_handle = next(
            handle
            for handle in self.driver.window_handles
            if handle not in old_handles
        )

        self.driver.switch_to.window(new_handle)

    @allure.step("Дождаться появления URL: {url_part}")
    def wait_for_url_contains(self, url_part):
        self.wait.until(
            EC.url_contains(url_part)
        )
