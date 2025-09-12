import time
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
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)
        actual_from = routes_page.get_from()
        actual_to = routes_page.get_to()
        assert data.ADDRESS_FROM == actual_from, f"Expected from '{data.ADDRESS_FROM}', got '{actual_from}'"
        assert data.ADDRESS_TO == actual_to, f"Expected to '{data.ADDRESS_TO}', got '{actual_to}'"

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)
        routes_page.select_supportive_plan()
        time.sleep(2)
        selected_plan = routes_page.get_selected_plan()
        expected_plan = "Supportive"
        assert expected_plan == selected_plan, f"Expected '{expected_plan}', got '{selected_plan}'"

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        time.sleep(2)
        actual_phone = routes_page.get_phone_number()
        assert data.PHONE_NUMBER == actual_phone, f"Expected '{data.PHONE_NUMBER}', got '{actual_phone}'"

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)
        routes_page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        time.sleep(2)
        assert routes_page.is_card_linked(), "Card was not linked successfully"

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)
        routes_page.write_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        time.sleep(2)
        actual_comment = routes_page.get_driver_comment()
        assert data.MESSAGE_FOR_DRIVER == actual_comment, f"Expected '{data.MESSAGE_FOR_DRIVER}', got '{actual_comment}'"

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)
        routes_page.order_blanket_and_handkerchiefs()
        time.sleep(2)
        assert routes_page.is_blanket_selected(), "Blanket was not selected"
        assert routes_page.is_handkerchief_selected(), "Handkerchief was not selected"

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)
        routes_page.order_ice_creams(2)
        time.sleep(2)
        actual_quantity = routes_page.get_ice_cream_quantity()
        assert actual_quantity == 2, f"Expected 2, got {actual_quantity}"

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)
        routes_page.place_taxi_order()
        time.sleep(2)
        assert routes_page.is_order_taxi_popup(), "Order taxi popup did not appear"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()