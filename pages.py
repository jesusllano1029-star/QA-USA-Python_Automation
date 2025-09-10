from selenium.webdriver.common.by import By
import data

class UrbanRoutesPage:
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    SUPPORTIVE_PLAN = (By.ID, "supportive-plan")
    SELECTED_PLAN = (By.ID, "selected-plan")
    PHONE_INPUT = (By.ID, "phone")
    CARD_NUMBER_INPUT = (By.ID, "card-number")
    CARD_CODE_INPUT = (By.ID, "card-code")
    CARD_CONFIRM = (By.ID, "card-confirm")
    DRIVER_COMMENT_INPUT = (By.ID, "driver-comment")
    BLANKET_CHECKBOX = (By.ID, "blanket")
    HANDKERCHIEF_CHECKBOX = (By.ID, "handkerchief")
    ICE_CREAM_INPUT = (By.ID, "ice-cream")
    ORDER_BUTTON = (By.ID, "order-button")
    ORDER_TAXI_POPUP = (By.ID, "order-popup")

    def __init__(self, driver):
        self.driver = driver

    def open(self, base_url):
        self.driver.get(base_url)

    # Route
    def set_route(self, address_from, address_to):
        self.driver.find_element(*self.FROM_INPUT).send_keys(address_from)
        self.driver.find_element(*self.TO_INPUT).send_keys(address_to)

    def get_from(self):
        return self.driver.find_element(*self.FROM_INPUT).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.TO_INPUT).get_attribute("value")

    # Plan
    def select_supportive_plan(self):
        self.driver.find_element(*self.SUPPORTIVE_PLAN).click()

    def get_selected_plan(self):
        return self.driver.find_element(*self.SELECTED_PLAN).text

    # Phone
    def fill_phone_number(self, phone):
        self.driver.find_element(*self.PHONE_INPUT).send_keys(phone)

    def get_phone_number(self):
        return self.driver.find_element(*self.PHONE_INPUT).get_attribute("value")

    # Card
    def fill_card(self, number, code):
        self.driver.find_element(*self.CARD_NUMBER_INPUT).send_keys(number)
        self.driver.find_element(*self.CARD_CODE_INPUT).send_keys(code)
        self.driver.find_element(*self.CARD_CONFIRM).click()

    def is_card_linked(self):
        return "****" in self.driver.find_element(*self.CARD_NUMBER_INPUT).get_attribute("value")

    # Driver comment
    def write_comment_for_driver(self, message):
        self.driver.find_element(*self.DRIVER_COMMENT_INPUT).send_keys(message)

    def get_driver_comment(self):
        return self.driver.find_element(*self.DRIVER_COMMENT_INPUT).get_attribute("value")

    # Blanket & handkerchiefs
    def order_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.BLANKET_CHECKBOX).click()
        self.driver.find_element(*self.HANDKERCHIEF_CHECKBOX).click()

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).is_selected()

    def is_handkerchief_selected(self):
        return self.driver.find_element(*self.HANDKERCHIEF_CHECKBOX).is_selected()

    # Ice cream
    def order_ice_creams(self, quantity):
        self.driver.find_element(*self.ICE_CREAM_INPUT).clear()
        self.driver.find_element(*self.ICE_CREAM_INPUT).send_keys(str(quantity))

    def get_ice_cream_quantity(self):
        return int(self.driver.find_element(*self.ICE_CREAM_INPUT).get_attribute("value"))

    # Car search
    def place_taxi_order(self):
        self.driver.find_element(*self.ORDER_BUTTON).click()

    def is_order_taxi_popup(self):
        return self.driver.find_element(*self.ORDER_TAXI_POPUP).is_displayed()