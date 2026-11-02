
import pytest
import allure

from pages.main_page import MainPage
from pages.order_page import OrderPage
from constants import ORDER_DATA


class TestOrder:

    @pytest.mark.parametrize("button_index", [0, 1])
    @allure.title("Проверка перехода к оформлению заказа через кнопку {button_index}")
    def test_order_button_opens_form(self, driver, button_index):
        main_page = MainPage(driver)
        main_page.open()

        main_page.click_order_button(button_index)

        order_page = OrderPage(driver)

        assert driver.find_element(
            *order_page.NAME_INPUT
        ).is_displayed()

    @pytest.mark.parametrize("data", ORDER_DATA)
    @allure.title("Проверка полного оформления заказа")
    def test_successful_order(self, driver, data):
        main_page = MainPage(driver)
        main_page.open()

        main_page.click_order_button(0)

        order_page = OrderPage(driver)

        order_page.fill_customer_data(data)
        order_page.fill_rental_data(data)
        order_page.submit_order()
        order_page.confirm_order()

        success_message = order_page.get_success_message()

        assert "Заказ оформлен" in success_message
        assert "Номер заказа" in success_message
