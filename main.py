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
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        print("Step 2: Setting route addresses...")
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        print("Step 3: Verifying route addresses...")
        assert data.ADDRESS_FROM == routes_page.get_from()
        assert data.ADDRESS_TO == routes_page.get_to()
        print("Route verified successfully.")

    def test_select_plan(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        print("Step 2: Setting route addresses...")
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(2)

        print("Step 3: Selecting the Supportive Plan...")
        routes_page.select_supportive_plan()
        time.sleep(2)

        print("Step 4: Verifying selected plan...")
        assert routes_page.get_selected_plan() == "Supportive"
        print("Plan verified successfully.")

    def test_add_phone_number(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        print("Step 2: Adding phone number...")
        routes_page.add_phone_number(data.PHONE_NUMBER)
        time.sleep(2)

        print("Step 3: Verifying phone number confirmation...")
        assert routes_page.is_phone_confirmed(), "Phone number was not confirmed"
        print("Phone number confirmed successfully.")

    def test_add_card(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        print("Step 2: Adding card...")
        routes_page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        time.sleep(2)

        print("Step 3: Verifying card link...")
        assert routes_page.is_card_linked(), "Card was not linked successfully"
        print("Card linked successfully.")

    def test_comment_for_driver(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        print("Step 2: Writing comment for driver...")
        routes_page.write_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        time.sleep(2)

        print("Step 3: Verifying driver comment...")
        assert data.MESSAGE_FOR_DRIVER == routes_page.get_driver_comment()
        print("Driver comment verified successfully.")

    def test_order_blanket_and_handkerchiefs(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        print("Step 2: Ordering blanket and handkerchiefs...")
        routes_page.order_blanket_and_handkerchiefs()
        time.sleep(2)

        print("Step 3: Verifying order...")
        assert routes_page.is_blanket_selected()
        assert routes_page.is_handkerchief_selected()
        print("Order verified successfully.")

    def test_order_2_ice_creams(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        print("Step 2: Ordering 2 ice creams...")
        routes_page.order_ice_creams(2)
        time.sleep(2)

        print("Step 3: Verifying ice cream quantity...")
        assert routes_page.get_ice_cream_quantity() == 2
        print("Ice cream order verified successfully.")

    def test_car_search_model_appears(self):
        print("Step 1: Opening Urban Routes URL...")
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        print("Step 2: Placing taxi order...")
        routes_page.place_taxi_order()
        time.sleep(2)

        print("Step 3: Verifying taxi popup...")
        assert routes_page.is_order_taxi_popup(), "Order taxi popup did not appear"
        print("Taxi popup verified successfully.")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()