import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print ('Connected to the Urban Routes server')
        else:
            print ('Cannot connect to Urban Routes. Check the server is on and still running')

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)

        assert data.ADDRESS_FROM == page.get_from(), f"Expected from '{data.ADDRESS_FROM}', got '{page.get_from()}'"
        assert data.ADDRESS_TO == page.get_to(), f"Expected to '{data.ADDRESS_TO}', got '{page.get_to()}'"

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_supportive_plan()

        assert page.get_selected_plan() == "Supportive"

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_supportive_plan()
        page.fill_phone_number(data.PHONE_NUMBER)
        page.click_next_button()

        code = page.wait_for_sms_code()
        page.enter_sms_code(code)
        page.click_confirm_phone()

        actual_phone = page.get_phone_number()
        assert data.PHONE_NUMBER == actual_phone, f"Expected '{data.PHONE_NUMBER}', got '{actual_phone}'"

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_supportive_plan()
        page.add_card(data.CARD_NUMBER, data.CARD_CODE)

        assert page.is_card_linked(), "Card was not linked successfully"

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.write_comment_for_driver(data.MESSAGE_FOR_DRIVER)

        actual_comment = page.get_driver_comment()
        assert data.MESSAGE_FOR_DRIVER == actual_comment, f"Expected '{data.MESSAGE_FOR_DRIVER}', got '{actual_comment}'"

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_supportive_plan()

        page.toggle_blanket_and_handkerchiefs()

        assert page.is_blanket_selected(), "Blanket and Handkerchiefs option was not selected"

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_supportive_plan()
        page.order_ice_creams(2)

        actual_quantity = page.get_ice_cream_quantity()
        assert actual_quantity == 2, f"Expected 2, got {actual_quantity}"

    def test_car_search_modal_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_supportive_plan()
        page.write_comment_for_driver(data.MESSAGE_FOR_DRIVER)

        page.place_taxi_order()
        assert page.is_order_taxi_popup(), "Car search modal did not appear after placing order"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()