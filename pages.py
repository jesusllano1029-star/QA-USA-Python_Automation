from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver

    ROUTE_FROM_INPUT = (By.ID, "from")
    ROUTE_TO_INPUT = (By.ID, "to")
    SUPPORTIVE_PLAN = (By.XPATH, "//div[@class='tcard-title' and text()='Supportive']")
    PHONE_INPUT = (By.ID, "phone")
    SMS_CODE_INPUT = (By.ID, "sms")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.ID, "code")
    COMMENT_INPUT = (By.ID, "comment")
    BLANKET_LABEL = (By.XPATH, "//div[@class='r-sw-label' and text()='Blanket and handkerchiefs']")
    BLANKET_CHECKBOX = (By.CLASS_NAME, "switch-input")
    ICE_CREAM_LABEL = (By.XPATH, "//div[@class='r-counter-label' and text()='Ice cream']")
    ICE_CREAM_PLUS = (By.CLASS_NAME, "counter-plus")
    ICE_CREAM_VALUE = (By.CLASS_NAME, "counter-value")
    CAR_SEARCH_MODAL = (By.CLASS_NAME, "car-search-modal")

    def open(self, base_url):
        self.driver.get(base_url)

    def set_route(self, address_from, address_to):
        self.driver.find_element(*self.ROUTE_FROM_INPUT).send_keys(address_from)
        self.driver.find_element(*self.ROUTE_TO_INPUT).send_keys(address_to)

    def select_supportive_plan(self):
        plan_el = self.driver.find_element(*self.SUPPORTIVE_PLAN)
        plan_el.click()

    def fill_phone_number(self, phone_number):
        phone_el = self.driver.find_element(*self.PHONE_INPUT)
        phone_el.clear()
        phone_el.send_keys(phone_number)

    def enter_sms_code(self, code):
        sms_el = self.driver.find_element(*self.SMS_CODE_INPUT)
        sms_el.clear()
        sms_el.send_keys(code)

    def fill_card(self, card_number, card_code):
        self.driver.find_element(*self.CARD_NUMBER_INPUT).send_keys(card_number)
        self.driver.find_element(*self.CARD_CODE_INPUT).send_keys(card_code)

    def write_comment_for_driver(self, comment):
        comment_el = self.driver.find_element(*self.COMMENT_INPUT)
        comment_el.clear()
        comment_el.send_keys(comment)

    def order_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.BLANKET_LABEL).click()

        # Verify the checkbox is now selected
        checkbox = self.driver.find_element(*self.BLANKET_CHECKBOX)
        assert checkbox.is_selected(), "Blanket and handkerchiefs checkbox was not selected!"

    def order_ice_creams(self, quantity=2):
        for _ in range(quantity):
            plus_btn = self.driver.find_element(*self.ICE_CREAM_PLUS)
            if "disabled" not in plus_btn.get_attribute("class"):
                plus_btn.click()
            else:
                break  # stop if button is disabled
        # Optional: verify quantity
        value_el = self.driver.find_element(*self.ICE_CREAM_VALUE)
        assert int(value_el.text) == quantity, f"Ice cream quantity expected {quantity}, got {value_el.text}"

    def place_taxi_order(self):
        self.driver.find_element(*self.ORDER_TAXI_BUTTON).click()

        # Verify the car search modal appears
        modal = self.driver.find_element(*self.CAR_SEARCH_MODAL)
        assert modal.is_displayed(), "Car search modal did not appear!"