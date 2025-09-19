from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import data


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver.get(data.URBAN_ROUTES_URL)

    # Locators
    ADDRESS_FROM = (By.ID, "from")
    ADDRESS_TO = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(text(), 'Call a taxi')]")
    SUPPORTIVE_PLAN = (By.CSS_SELECTOR, "button[data-for='tariff-card-4']")
    SELECTED_PLAN = (By.CSS_SELECTOR, "button.tcard.active")
    PHONE_INPUT = (By.ID, "phone")
    PHONE_MODAL = (By.XPATH, "//div[contains(@class, 'modal') and .//input[@id='phone']]")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Next')]")
    SMS_INPUT = (By.ID, "code")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirm')]")
    PAYMENT_METHOD = (By.XPATH, "//div[contains(text(), 'Payment method')]")
    ADD_CARD_BUTTON = (By.XPATH, "//button[contains(text(), 'Add card')]")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.ID, "code")
    LINK_BUTTON = (By.XPATH, "//button[contains(text(), 'Link')]")
    COMMENT_INPUT = (By.ID, "comment")
    BLANKET_CHECKBOX = (By.ID, "blanket")
    HANDKERCHIEF_CHECKBOX = (By.ID, "handkerchiefs")
    ICE_CREAM_INPUT = (By.CSS_SELECTOR, "input[name='ice-cream']")
    ICE_CREAM_PLUS_BUTTON = (By.XPATH, "//button[contains(@class,'counter-plus')]")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Order')]")
    ORDER_TAXI_POPUP = (By.XPATH, "//div[contains(@class, 'order-modal')]")
    CAR_SEARCH_MODAL = (By.XPATH, "//div[contains(@class,'order-body')]")  # added for modal verification

    # Helpers
    def wait_and_click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def wait_and_type(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    # Route
    def set_route(self, address_from, address_to):
        self.wait_and_type(self.ADDRESS_FROM, address_from)
        self.wait_and_type(self.ADDRESS_TO, address_to)

    def get_from(self):
        return self.driver.find_element(*self.ADDRESS_FROM).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.ADDRESS_TO).get_attribute("value")

    # Plan
    def select_supportive_plan(self):
        self.wait_and_click(self.SUPPORTIVE_PLAN)

    def get_selected_plan(self):
        return self.driver.find_element(*self.SELECTED_PLAN).text

    # Phone (step-by-step, matching main.py)
    def click_call_taxi_button(self):
        self.wait_and_click(self.CALL_TAXI_BUTTON)

    def reveal_phone_input_form(self):
        self.wait.until(EC.visibility_of_element_located(self.PHONE_MODAL))

    def enter_phone_number(self, phone):
        self.wait_and_type(self.PHONE_INPUT, phone)

    def click_next_button(self):
        self.wait_and_click(self.NEXT_BUTTON)

    def enter_sms_code(self, code):
        self.wait_and_type(self.SMS_INPUT, code)

    # Card (full flow)
    def add_card(self, number, code):
        self.wait_and_click(self.PAYMENT_METHOD)
        self.wait_and_click(self.ADD_CARD_BUTTON)
        self.wait_and_type(self.CARD_NUMBER_INPUT, number)
        self.wait_and_type(self.CARD_CODE_INPUT, code)
        self.wait_and_click(self.LINK_BUTTON)

    def is_card_linked(self):
        return "****" in self.driver.find_element(*self.CARD_NUMBER_INPUT).get_attribute("value")

    # Driver comment
    def write_comment_for_driver(self, message):
        self.wait_and_type(self.COMMENT_INPUT, message)

    def get_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute("value")

    # Blanket & handkerchiefs
    def order_blanket_and_handkerchiefs(self):
        self.wait_and_click(self.BLANKET_CHECKBOX)
        self.wait_and_click(self.HANDKERCHIEF_CHECKBOX)

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).is_selected()

    def is_handkerchief_selected(self):
        return self.driver.find_element(*self.HANDKERCHIEF_CHECKBOX).is_selected()

    # Ice cream
    def order_ice_creams(self, quantity):
        self.wait_and_type(self.ICE_CREAM_INPUT, str(quantity))

    def get_ice_cream_quantity(self):
        return int(self.driver.find_element(*self.ICE_CREAM_INPUT).get_attribute("value"))

    # Car search
    def place_taxi_order(self):
        self.wait_and_click(self.ORDER_BUTTON)

    def is_order_taxi_popup(self):
        return self.wait.until(EC.visibility_of_element_located(self.ORDER_TAXI_POPUP)).is_displayed()