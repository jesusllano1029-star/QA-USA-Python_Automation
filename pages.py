from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import data

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver.get(data.URBAN_ROUTES_URL)

    ADDRESS_FROM = (By.ID, "from")
    ADDRESS_TO = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(text(), 'Call a taxi')]")
    SUPPORTIVE_PLAN = (By.CSS_SELECTOR, "button[data-for='tariff-card-4']")
    PHONE_INPUT = (By.ID, "phone")
    PHONE_MODAL = (By.XPATH, "//div[contains(@class, 'modal') and .//input[@id='phone']]")
    SMS_INPUT = (By.ID, "code")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Next')]")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirm')]")
    PAYMENT_METHOD = (By.XPATH, "//div[contains(text(), 'Payment method')]")
    ADD_CARD_BUTTON = (By.XPATH, "//button[contains(text(), 'Add card')]")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.ID, "code")
    LINK_BUTTON = (By.XPATH, "//button[contains(text(), 'Link')]")
    COMMENT_INPUT = (By.ID, "comment")
    BLANKET_HANDKERCHIEFS_SLIDER = (By.XPATH, "//input[@type='checkbox' and @id='blanket']")
    ICE_CREAM_PLUS_BUTTON = (By.XPATH, "//button[contains(@class,'counter-plus')]")
    ICE_CREAM_SUMMARY = (By.XPATH, "//div[contains(@class,'ice-cream-summary')]")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Order')]")
    CAR_SEARCH_MODAL = (By.XPATH, "//div[contains(@class, 'order-modal')]")

    def __init__(self, driver):
        self.driver = driver

    def open(self, base_url):
        self.driver.get(base_url)

    # Route
    def set_route(self, address_from, address_to):
        self.driver.find_element(*self.FROM_INPUT).send_keys(address_from)
        self.driver.find_element(*self.TO_INPUT).send_keys(address_to)
        self.click_call_taxi_button()

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

    def click_call_taxi_button(self):
        WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of_element_located(self.CALL_TAXI_BUTTON)
        )
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    # Car search
    def place_taxi_order(self):
        self.driver.find_element(*self.ORDER_BUTTON).click()

    def is_order_taxi_popup(self):
        return self.driver.find_element(*self.ORDER_TAXI_POPUP).is_displayed()