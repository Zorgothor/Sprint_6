
import allure

from pages.main_page import MainPage
from pages.order_page import OrderPage
from constants import BASE_URL


class TestLogo:

    @allure.title("Проверка возврата на главную страницу по логотипу Самоката")
    def test_scooter_logo_returns_to_main_page(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        main_page.click_order_button(0)

        main_page.click_scooter_logo()

        assert driver.current_url == BASE_URL

    @allure.title("Проверка открытия Дзена по логотипу Яндекса")
    def test_yandex_logo_opens_dzen_in_new_tab(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        original_handles = driver.window_handles

        main_page.click_yandex_logo()

        assert len(driver.window_handles) == len(original_handles) + 1
        assert "dzen.ru" in driver.current_url
