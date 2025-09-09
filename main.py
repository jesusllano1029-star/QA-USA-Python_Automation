import time
import data
import helpers
from selenium import webdriver
import pages

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
        pages.set_route(self.driver, data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)
        actual_from = pages.get_from(self.driver)
        actual_to = pages.get_to(self.driver)
        assert data.ADDRESS_FROM == actual_from, f"Expected from '{data.ADDRESS_FROM}', got '{actual_from}'"
        assert data.ADDRESS_TO == actual_to, f"Expected to '{data.ADDRESS_TO}', got '{actual_to}'"

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        pages.select_supportive_plan(self.driver)
        time.sleep(2)
        selected_plan = pages.get_selected_plan(self.driver)
        expected_plan = "Supportive"
        assert expected_plan in selected_plan, f"Expected '{expected_plan}' in '{selected_plan}'"

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        pages.fill_phone_number(self.driver, data.PHONE_NUMBER)
        time.sleep(2)
        actual_phone = pages.get_phone_number(self.driver)
        assert data.PHONE_NUMBER == actual_phone, f"Expected '{data.PHONE_NUMBER}', got '{actual_phone}'"

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        pages.fill_card(self.driver, data.CARD_NUMBER, data.CARD_CODE)
        time.sleep(2)
        actual_card = pages.get_card_number(self.driver)
        actual_code = pages.get_card_code(self.driver)
        assert data.CARD_NUMBER == actual_card, f"Expected '{data.CARD_NUMBER}', got '{actual_card}'"
        assert data.CARD_CODE == actual_code, f"Expected '{data.CARD_CODE}', got '{actual_code}'"

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        pages.write_comment_for_driver(self.driver, data.MESSAGE_FOR_DRIVER)
        time.sleep(2)
        actual_comment = pages.get_driver_comment(self.driver)
        assert data.MESSAGE_FOR_DRIVER == actual_comment, f"Expected '{data.MESSAGE_FOR_DRIVER}', got '{actual_comment}'"

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        pages.order_blanket_and_handkerchiefs(self.driver)
        time.sleep(2)
        blanket_selected = pages.is_blanket_selected(self.driver)
        handkerchief_selected = pages.is_handkerchief_selected(self.driver)
        assert blanket_selected, "Blanket was not selected"
        assert handkerchief_selected, "Handkerchief was not selected"

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        for i in range(2):
            pages.order_ice_cream(self.driver)
            time.sleep(2)
        actual_quantity = pages.get_ice_cream_quantity(self.driver)
        assert actual_quantity == 2, f"Expected 2 ice creams, got {actual_quantity}"

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        pages.place_taxi_order(self.driver)
        time.sleep(2)
        model_appears = pages.is_car_model_visible(self.driver)
        assert model_appears, "Car model did not appear after placing order"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()