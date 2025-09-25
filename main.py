import time
import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        print("Step 2: Setting route addresses...")
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        print("Step 3: Verifying route addresses...")
        assert data.ADDRESS_FROM == page.get_from(), f"Expected from '{data.ADDRESS_FROM}', got '{page.get_from()}'"
        assert data.ADDRESS_TO == page.get_to(), f"Expected to '{data.ADDRESS_TO}', got '{page.get_to()}'"
        print("Route verified successfully.")

    def test_select_plan(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        print("Step 2: Setting route addresses...")
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        print("Step 3: Selecting the Supportive Plan...")
        page.select_supportive_plan()
        time.sleep(2)

        print("Step 4: Verifying selected plan...")
        assert page.get_selected_plan() == "Supportive"
        print("Plan verified successfully.")

    def test_fill_phone_number(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        print("Step 2: Setting route addresses...")
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        print(f"Step 3: Entering phone number: {data.PHONE_NUMBER}...")
        # keep this interaction in the page object where UI details belong
        page.fill_phone_number(data.PHONE_NUMBER)
        page.click_next_button()
        print("Phone number entered.")

        # use the page helper that already encapsulates polling logic
        code = page.wait_for_sms_code()
        print(f"Step 4: Received SMS code: {code}")

        # enter and verify the phone input value
        page.enter_sms_code(code)
        actual_phone = page.get_phone_number()
        assert data.PHONE_NUMBER == actual_phone, f"Expected '{data.PHONE_NUMBER}', got '{actual_phone}'"
        print("Phone number verified.")

    def test_fill_card(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        print("Step 2: Setting route addresses...")
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        print("Step 3: Entering card details...")
        page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        time.sleep(2)
        print("Card details entered.")

        print("Step 4: Verifying card link...")
        assert page.is_card_linked(), "Card was not linked successfully"
        print("Card linked successfully.")

    def test_comment_for_driver(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        print("Step 2: Setting route addresses...")
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        print(f"Step 3: Writing comment for driver: '{data.MESSAGE_FOR_DRIVER}'...")
        page.write_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        time.sleep(2)
        print("Comment entered.")

        print("Step 4: Verifying driver comment...")
        actual_comment = page.get_driver_comment()
        assert data.MESSAGE_FOR_DRIVER == actual_comment, f"Expected '{data.MESSAGE_FOR_DRIVER}', got '{actual_comment}'"
        print("Driver comment verified.")

    def test_order_blanket_and_handkerchiefs(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        # --- Setup: route, call taxi, choose tariff, and confirm phone ---
        print("Step 2: Setting route addresses...")
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_supportive_plan()
        page.confirm_phone(data.PHONE_NUMBER)
        print("Preconditions done: route set, tariff selected, phone confirmed.")

        # --- Place the blanket/handkerchief order ---
        print("Step 3: Ordering blanket and handkerchiefs...")
        page.order_blanket_and_handkerchiefs()
        time.sleep(0.6)

        print("Step 4: Verifying order...")
        assert page.is_blanket_selected(), "Blanket was not selected"
        assert page.is_handkerchief_selected(), "Handkerchief was not selected"
        print("Order verified successfully.")

    def test_order_2_ice_creams(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        print("Step 2: Setting route addresses...")
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(1)

        # --- important: select the Supportive tariff so extras are active ---
        print("Step 3: Selecting the Supportive Plan (required for extras)...")
        page.select_supportive_plan()
        time.sleep(0.6)

        print("Step 4: Ordering 2 ice creams...")
        page.order_ice_creams(2)
        time.sleep(0.6)
        print("Ice creams ordered.")

        print("Step 5: Verifying ice cream quantity...")
        actual_quantity = page.get_ice_cream_quantity()
        assert actual_quantity == 2, f"Expected 2, got {actual_quantity}"
        print("Ice cream order verified.")

    def test_car_search_modal_appears(self):
        print("Step 1: Setting addresses ...")
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.set_route("East 2nd Street, 601", "1300 1st St")
        print("Addresses set successfully.")

        print("Step 2: Clicking 'Call a Taxi' button ...")
        page.click_call_taxi_button()
        print("'Call a Taxi' button clicked.")

        print("Step 3: Selecting the Supportive Plan ...")
        page.select_supportive_plan()
        print("Supportive Plan selected.")

        print("Step 4: Confirming phone (page helper flow)...")
        page.confirm_phone(data.PHONE_NUMBER)
        print("Phone confirmed.")

        print(f"Step 5: Entering driver comment: {data.MESSAGE_FOR_DRIVER} ...")
        page.write_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        print("Driver comment entered.")

        print("Step 6: Placing taxi order via page helper ...")
        page.place_taxi_order()
        print("Order button clicked.")

        print("Step 7: Verifying that the car search modal appears ...")
        assert page.is_order_taxi_popup(), "Car search modal did not appear after placing order"
        print("Car search modal is displayed successfully.")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()