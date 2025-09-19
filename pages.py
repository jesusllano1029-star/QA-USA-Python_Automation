from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import data


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators (kept conservative; prefer text/XPath where IDs don't exist)
    ADDRESS_FROM = (By.ID, "from")
    ADDRESS_TO = (By.ID, "to")

    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Call a taxi')]")

    # tariff card button that selects the "Supportive" plan
    SUPPORTIVE_PLAN = (By.CSS_SELECTOR, "button[data-for='tariff-card-4']")
    # the visible title inside the active tariff card (to read the selected plan)
    SELECTED_PLAN = (By.CSS_SELECTOR, ".tcard.active .tcard-title")

    # Phone flow
    PHONE_INPUT = (By.ID, "phone")
    NEXT_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Next')]")
    SMS_INPUT = (By.ID, "code")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Confirm')]")

    # Payment / Card flow
    PAYMENT_METHOD = (By.XPATH, "//div[contains(normalize-space(.), 'Payment method')]")
    ADD_CARD_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Add card')]")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.ID, "code")
    LINK_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Link')]")

    # Driver comment
    COMMENT_INPUT = (By.ID, "comment")

    # Blanket and "soundproof curtain" switches — located by their labels
    BLANKET_CHECKBOX = (
        By.XPATH,
        "//div[contains(@class,'r-sw-label') and normalize-space() = 'Blanket and handkerchiefs']"
        "/following::input[@type='checkbox'][1]",
    )
    HANDKERCHIEF_CHECKBOX = (
        By.XPATH,
        "//div[contains(@class,'r-sw-label') and normalize-space() = 'Soundproof curtain']"
        "/following::input[@type='checkbox'][1]",
    )

    # Ice cream counter — use the plus button to increase and read the counter-value for quantity
    ICE_CREAM_PLUS_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'r-group-title') and normalize-space() = 'Ice cream bucket']"
        "/following::div[contains(@class,'counter-plus')][1]"
    )
    ICE_CREAM_VALUE = (
        By.XPATH,
        "//div[contains(@class,'r-group-title') and normalize-space() = 'Ice cream bucket']"
        "/following::div[contains(@class,'counter-value')][1]"
    )

    ORDER_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Order')]")
    ORDER_TAXI_POPUP = (By.XPATH, "//div[contains(@class, 'order-modal') or contains(@class,'car-search')]")
    CAR_SEARCH_MODAL = ORDER_TAXI_POPUP  # alias used in main.py

    # tiny helpers
    def wait_and_click(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()

    def wait_and_type(self, locator, text, timeout=10):
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        try:
            el.clear()
        except Exception:
            pass
        el.send_keys(text)

    # Route
    def set_route(self, address_from, address_to):
        """Enter addresses and click the 'Call a taxi' button as part of the route flow."""
        self.wait_and_type(self.ADDRESS_FROM, address_from)
        self.wait_and_type(self.ADDRESS_TO, address_to)
        # Clicking Call a taxi is required for many subsequent interactions
        self.click_call_taxi_button()

    def get_from(self):
        return self.driver.find_element(*self.ADDRESS_FROM).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.ADDRESS_TO).get_attribute("value")

    # Plan
    def select_supportive_plan(self):
        self.wait_and_click(self.SUPPORTIVE_PLAN)

    def get_selected_plan(self):
        return self.wait.until(EC.visibility_of_element_located(self.SELECTED_PLAN)).text

    # Phone (different helper entry points used by tests)
    def fill_phone_number(self, phone):
        """Simple helper used by the phone-number test (does not complete SMS confirmation)."""
        # ensure the phone input is visible (Call a taxi should have been clicked via set_route)
        self.wait_and_type(self.PHONE_INPUT, phone)

    # Methods used in the longer car search flow
    def click_call_taxi_button(self):
        self.wait_and_click(self.CALL_TAXI_BUTTON)

    def reveal_phone_input_form(self):
        # wait for the phone input to appear (some pages don't wrap it in a modal)
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(self.PHONE_INPUT))

    def enter_phone_number(self, phone):
        self.wait_and_type(self.PHONE_INPUT, phone)

    def click_next_button(self):
        self.wait_and_click(self.NEXT_BUTTON)

    def enter_sms_code(self, code):
        self.wait_and_type(self.SMS_INPUT, code)

    def is_phone_confirmed(self):
        # heuristic: check the phone input's class or value to infer confirmation; adjust if needed
        el = self.driver.find_element(*self.PHONE_INPUT)
        return "confirmed" in el.get_attribute("class") or el.get_attribute("value") != ""

    # Card (both alias names supported)
    def add_card(self, number, code):
        self.wait_and_click(self.PAYMENT_METHOD)
        self.wait_and_click(self.ADD_CARD_BUTTON)
        self.wait_and_type(self.CARD_NUMBER_INPUT, number)
        self.wait_and_type(self.CARD_CODE_INPUT, code)
        self.wait_and_click(self.LINK_BUTTON)

    def fill_card(self, number, code):
        """Alias used by tests that call fill_card(...)"""
        return self.add_card(number, code)

    def is_card_linked(self):
        return "****" in self.driver.find_element(*self.CARD_NUMBER_INPUT).get_attribute("value")

    # Driver comment
    def write_comment_for_driver(self, message):
        self.wait_and_type(self.COMMENT_INPUT, message)

    def get_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute("value")

    # Blanket & handkerchiefs
    def order_blanket_and_handkerchiefs(self):
        # toggles the two switches found on the page
        self.wait_and_click(self.BLANKET_CHECKBOX)
        self.wait_and_click(self.HANDKERCHIEF_CHECKBOX)

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).is_selected()

    def is_handkerchief_selected(self):
        return self.driver.find_element(*self.HANDKERCHIEF_CHECKBOX).is_selected()

    # Ice cream
    def order_ice_creams(self, quantity):
        # Click the + button `quantity` times (some UIs use a counter without an input)
        for _ in range(quantity):
            self.wait_and_click(self.ICE_CREAM_PLUS_BUTTON)

    def get_ice_cream_quantity(self):
        # read the counter-value text and convert to int; fallback to 0 on parse failure
        try:
            val = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_VALUE)).text
            return int(val.strip())
        except Exception:
            return 0

    # Car search / Order
    def place_taxi_order(self):
        self.wait_and_click(self.ORDER_BUTTON)

    def is_order_taxi_popup(self):
        return self.wait.until(EC.visibility_of_element_located(self.ORDER_TAXI_POPUP)).is_displayed()