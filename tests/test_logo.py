
import allure

from pages.main_page import MainPage
from constants import BASE_URL


class TestLogo:

    @allure.title("Проверка возврата на главную страницу по логотипу Самоката")
    def test_scooter_logo_returns_to_main_page(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        main_page.click_order_button(0)
        main_page.click_scooter_logo()

        assert main_page.get_current_url() == BASE_URL

    @allure.title("Проверка открытия Дзена по логотипу Яндекса")
    def test_yandex_logo_opens_dzen_in_new_tab(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        original_handles = main_page.get_window_handles()

        main_page.click_yandex_logo()

        current_handles = main_page.get_window_handles()

        assert len(current_handles) == len(original_handles) + 1
        assert "dzen.ru" in main_page.get_current_url()
