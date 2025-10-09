from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import helpers


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Route fields (IDs exist)
    ADDRESS_FROM = (By.ID, "from")
    ADDRESS_TO = (By.ID, "to")

    # Call taxi button (text-based)
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Call a taxi')]")

    # Tariff cards / selected plan
    SUPPORTIVE_PLAN = (By.XPATH, "//div[text()='Supportive']/..")
    SELECTED_PLAN = (By.CSS_SELECTOR, ".tcard.active .tcard-title")

    # Phone flow
    PHONE_BUTTON = (By.CSS_SELECTOR, ".np-button")  # the button that reveals phone form
    PHONE_INPUT = (By.ID, "phone")
    NEXT_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Next')]")
    SMS_INPUT = (By.ID, "code")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Confirm')]")

    # Payment / card flow
    PAYMENT_METHOD = (By.CSS_SELECTOR, '.pp-button')
    PAYMENT_TEXT = (By.CSS_SELECTOR, '.pp-value-text')
    ADD_CARD_BUTTON = (By.CSS_SELECTOR, '.pp-plus')
    CARD_FORM = (By.XPATH, "//div[contains(@class,'section') and .//div[contains(normalize-space(),'Adding a card')]]//form")

    card_number_input = (By.ID, 'number')
    card_code_input = (By.XPATH, "//input[@placeholder='12']")

    LINK_BUTTON = (By.XPATH, '//button[@type="submit"][text()="Link"]')
    CLOSE_PAYMENT_METHOD_LOCATOR = (By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    CARD_PLC_LOCATOR = (By.CSS_SELECTOR, '.plc')

    # Driver comment
    COMMENT_INPUT = (By.ID, "comment")

    # Blanket & handkerchief toggles -> click the slider element
    BLANKET_SLIDER = (By.XPATH,"//div[contains(@class, 'r-sw-container') and .//div[contains(normalize-space(), 'Blanket and handkerchiefs')]]//span[contains(@class,'slider')]")
    BLANKET_INPUT = (By.XPATH,"//div[contains(@class, 'r-sw-container') and .//div[contains(normalize-space(), 'Blanket and handkerchiefs')]]//input")

    # Ice cream controls: plus button and counter value
    ICE_CREAM_PLUS_BUTTON = (By.CLASS_NAME, "counter-plus")
    ICE_CREAM_VALUE = (By.CLASS_NAME, "counter-value")

    ORDER_BUTTON = (By.CSS_SELECTOR, ".smart-button")

    ORDER_TAXI_POPUP = (By.CSS_SELECTOR, ".order-header-title")
    CAR_SEARCH_MODAL = (By.CSS_SELECTOR, "div.car-search, div.order-modal")


    # --- Route ---
    def set_route(self, address_from, address_to):
        el_from = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ADDRESS_FROM))
        el_from.send_keys(address_from)

        el_to = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ADDRESS_TO))
        el_to.send_keys(address_to)

    def get_from(self):
        return self.driver.find_element(*self.ADDRESS_FROM).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.ADDRESS_TO).get_attribute("value")

    # --- Plan ---
    def select_supportive_plan(self):
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN)).click()

    def get_selected_plan(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SELECTED_PLAN)).text

    # --- Phone helpers (used across tests) ---
    def fill_phone_number(self, phone):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.PHONE_BUTTON)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PHONE_INPUT)).send_keys(phone)

    def get_phone_number(self):
        """Return current phone input value (used in tests)"""
        return self.driver.find_element(*self.PHONE_BUTTON).text

    def click_call_taxi_button(self):
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def click_next_button(self):
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

    def enter_sms_code(self, code):
        el = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SMS_INPUT))
        el.send_keys(code)

    def click_confirm_phone(self):
        confirm_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CONFIRM_BUTTON))
        confirm_button.click()

    def wait_for_sms_code(self) -> str:
        code = helpers.retrieve_phone_code(self.driver)
        return code

    # --- Card (payment) ---
    def add_card(self, number, code):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PAYMENT_METHOD)).click()
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.card_number_input)).send_keys(number)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.card_code_input)).send_keys(code)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.LINK_BUTTON)).click()
        self.driver.find_element(*self.CLOSE_PAYMENT_METHOD_LOCATOR).click()

    def is_card_linked(self):
        return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.PAYMENT_METHOD)).text == "Card"

    # --- Driver comment ---
    def write_comment_for_driver(self, message):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.COMMENT_INPUT))

    def get_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute("value")

    # --- Blanket & handkerchiefs ---
    def toggle_blanket_and_handkerchiefs(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.BLANKET_SLIDER)).click()

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_INPUT).get_attribute("checked")

    # --- Ice cream ---
    def order_ice_creams(self, quantity):
        for count in range(quantity):
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON)).click()

    def get_ice_cream_quantity(self):
        return WebDriverWait(self.driver, 7).until(EC.visibility_of_element_located(self.ICE_CREAM_VALUE)).text

    # --- Car search / Order ---
    def place_taxi_order(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()

    def is_order_taxi_popup(self):
        car_search_modal_appears = self.wait.until(EC.presence_of_element_located(self.ORDER_TAXI_POPUP))
        return car_search_modal_appears.is_displayed()