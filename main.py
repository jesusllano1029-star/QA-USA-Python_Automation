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
        page.fill_phone_number(data.PHONE_NUMBER)
        page.click_next_button()
        print("Phone number entered.")

        code = None
        for _ in range(20):
            try:
                code = helpers.retrieve_phone_code(self.driver)
                if code:
                    break
            except Exception:
                time.sleep(3)
                if not code:
                    raise Exception("Phone confirmation code not found.")

        print("Step 4: Verifying phone number field...")
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

        print("Step 2: Setting route addresses...")
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        print("Step 3: Ordering blanket and handkerchiefs...")
        page.order_blanket_and_handkerchiefs()
        time.sleep(2)
        print("Blanket and handkerchiefs ordered.")

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
        time.sleep(2)

        print("Step 3: Ordering 2 ice creams...")
        page.order_ice_creams(2)
        time.sleep(2)
        print("Ice creams ordered.")

        print("Step 4: Verifying ice cream quantity...")
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

        print("Step 4: Revealing phone input form ...")
        page.reveal_phone_input_form()
        print("Phone input form revealed.")

        print(f"Entering phone number: {data.PHONE_NUMBER} ...")
        page.enter_phone_number(data.PHONE_NUMBER)
        page.click_next_button()
        print("Phone number entered and Next button clicked.")

        print("Step 5: Verifying phone number...")
        code = None
        for _ in range(20):
            try:
                code = helpers.retrieve_phone_code(self.driver)
                if code:
                    break
            except Exception:
                time.sleep(3)
                if not code:
                    raise Exception("Phone confirmation code not found.")

        print(f"Step 6: Entering SMS code: {code} ...")
        page.enter_sms_code(code)
        print("SMS code entered.")

        print("Step 7: Clicking Confirm button ...")
        wait = WebDriverWait(self.driver, timeout=15)
        confirm_btn = wait.until(EC.element_to_be_clickable(page.CONFIRM_BUTTON))
        confirm_btn.click()
        print("Confirm button clicked.")

        print(f"Step 8: Entering driver comment: {data.MESSAGE_FOR_DRIVER} ...")
        page.write_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        print("Driver comment entered.")

        print("Step 9: Clicking Order button ...")
        WebDriverWait(self.driver, timeout=15).until(
            EC.element_to_be_clickable(page.ORDER_BUTTON)
        ).click()
        print("Order button clicked.")

        print("Step 10: Verifying that the car search modal appears ...")
        print("CAR_SEARCH_MODAL Locator:", page.CAR_SEARCH_MODAL)
        time.sleep(1)  # buffer for animations
        wait = WebDriverWait(self.driver, timeout=20)
        modal = wait.until(EC.visibility_of_element_located(self.page.CAR_SEARCH_MODAL))
        assert modal.is_displayed(), "Car search modal did not appear after placing order"
        print("Car search modal is displayed successfully.")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()