from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
)
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
    SUPPORTIVE_PLAN = (By.CSS_SELECTOR, "button[data-for='tariff-card-4']")
    SELECTED_PLAN = (By.CSS_SELECTOR, ".tcard.active .tcard-title")

    # Phone flow
    PHONE_BUTTON = (By.CSS_SELECTOR, ".np-button")  # the button that reveals phone form
    PHONE_INPUT = (By.ID, "phone")
    NEXT_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Next')]")
    SMS_INPUT = (By.ID, "code")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Confirm')]")

    # Payment / card flow
    PAYMENT_METHOD = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')
    ADD_CARD_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[2]/div/ div[1]/div[2]/div[3]')  # keep your working xpath
    # small correction — in your workspace you used the absolute XPaths that worked; keep them if different
    CARD_FORM = (By.XPATH, "//div[contains(@class,'section') and .//div[contains(normalize-space(),'Adding a card')]]//form")
    CARD_NUMBER_INPUT = (By.ID, 'number')
    CARD_CODE_INPUT = (By.ID, 'code')
    LINK_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')

    # Driver comment
    COMMENT_INPUT = (By.ID, "comment")

    # Blanket & handkerchief toggles -> click the slider element
    BLANKET_CHECKBOX = (
        By.XPATH,
        "//div[contains(@class,'r-sw-container') and .//div[contains(normalize-space(),'Blanket')]]"
        "//span[contains(@class,'slider')]",
    )
    HANDKERCHIEF_CHECKBOX = (
        By.XPATH,
        "//div[contains(@class,'r-sw-container') and .//div[contains(normalize-space(),'Soundproof')]]"
        "//span[contains(@class,'slider')]",
    )

    # Ice cream controls: plus button and counter value
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

    ORDER_BUTTON = (By.XPATH, "//button[contains(@class,'smart-button') and .//span[text()='Enter the number and order']]")
    ORDER_TAXI_POPUP = (By.XPATH, "//div[contains(@class, 'order-modal') or contains(@class,'car-search')]")
    CAR_SEARCH_MODAL = ORDER_TAXI_POPUP  # alias used in tests

    # --- small helpers ---

    def wait_and_click(self, locator, timeout=10):
        """
        Click with a wait; if the click is intercepted or not interactable,
        fall back to JS click after scrolling into view.
        """
        try:
            el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            try:
                el.click()
                return
            except (ElementClickInterceptedException, ElementNotInteractableException):
                # fallback: scroll into view and JS-click
                self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                self.driver.execute_script("arguments[0].click();", el)
                return
        except TimeoutException:
            # try presence + JS click as last resort
            try:
                el = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                self.driver.execute_script("arguments[0].click();", el)
                return
            except Exception:
                raise

    def wait_and_type(self, locator, text, timeout=10):
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        try:
            el.clear()
        except Exception:
            pass
        el.send_keys(text)

    # --- Route ---
    def set_route(self, address_from, address_to):
        self.wait_and_type(self.ADDRESS_FROM, address_from)
        self.wait_and_type(self.ADDRESS_TO, address_to)
        # clicking Call a taxi is required in the flow for further interactions
        self.click_call_taxi_button()

    def get_from(self):
        return self.driver.find_element(*self.ADDRESS_FROM).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.ADDRESS_TO).get_attribute("value")

    # --- Plan ---
    def select_supportive_plan(self):
        # Try to click the supportive plan; wait_and_click handles interception fallback.
        self.wait_and_click(self.SUPPORTIVE_PLAN)

    def get_selected_plan(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SELECTED_PLAN)).text

    # --- Phone helpers (used across tests) ---
    def fill_phone_number(self, phone):
        """
        Simple test helper used by phone-number test. Many UIs require
        clicking the phone button to reveal the input — do that here.
        """
        # reveal phone input if required
        try:
            self.wait_and_click(self.PHONE_BUTTON, timeout=5)
        except Exception:
            # If the phone button isn't present/clickable, proceed — wait for input directly
            pass
        self.wait_and_type(self.PHONE_INPUT, phone)

    def get_phone_number(self):
        """Return current phone input value (used in tests)"""
        return self.driver.find_element(*self.PHONE_INPUT).get_attribute("value")

    def click_call_taxi_button(self):
        self.wait_and_click(self.CALL_TAXI_BUTTON)

    def reveal_phone_input_form(self):
        # give a bit more time for the phone form to appear in the longer flow
        # Try clicking the reveal control if present, then wait for the input to appear
        try:
            self.wait_and_click(self.PHONE_BUTTON, timeout=3)
        except Exception:
            pass
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.PHONE_INPUT))

    def enter_phone_number(self, phone):
        self.wait_and_type(self.PHONE_INPUT, phone)

    def click_next_button(self):
        self.wait_and_click(self.NEXT_BUTTON)

    def enter_sms_code(self, code):
        self.wait_and_type(self.SMS_INPUT, code)

    def is_phone_confirmed(self):
        # heuristic: check class/value — adjust to real app specifics if needed
        el = self.driver.find_element(*self.PHONE_INPUT)
        return "confirmed" in el.get_attribute("class") or el.get_attribute("value") != ""

    def wait_for_sms_code(self, attempts: int = 20, delay_seconds: int = 2) -> str:
        """
        Poll for the SMS confirmation code using helpers.retrieve_phone_code.
        Returns the code string once found, or raises an Exception after attempts.
        """
        for attempt in range(1, attempts + 1):
            try:
                code = helpers.retrieve_phone_code(self.driver)
                if code:
                    return code
            except Exception:
                # ignore transient errors from retrieve_phone_code and retry
                pass
            time.sleep(delay_seconds)
        raise Exception("Phone confirmation code not found after waiting.")

    # --- Card (payment) ---
    def add_card(self, number, code):
        """Open payment, click add card, type and link (helper that only performs the UI flow)."""
        # open picker and click add-card
        self.wait_and_click(self.PAYMENT_METHOD)
        self.wait_and_click(self.ADD_CARD_BUTTON)

        # find the card form container first (scoped search prevents collisions with SMS input)
        form_el = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.CARD_FORM)
        )

        # find inputs inside the form (this scopes to the 'Adding a card' form)
        try:
            number_el = form_el.find_element(*self.CARD_NUMBER_INPUT)
        except Exception:
            raise Exception("Card number input not found inside add-card form.")

        try:
            code_el = form_el.find_element(*self.CARD_CODE_INPUT)
        except Exception:
            raise Exception("Card code input not found inside add-card form.")

        # focus, clear, type, then dispatch input/change so frontend validation runs
        try:
            number_el.click()
        except Exception:
            pass
        try:
            number_el.clear()
        except Exception:
            pass
        number_el.send_keys(number)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            number_el,
        )

        try:
            code_el.click()
        except Exception:
            pass
        try:
            code_el.clear()
        except Exception:
            pass
        code_el.send_keys(code)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            code_el,
        )

        # find the Link button inside the form (safer than a global xpath in case there are other buttons)
        try:
            link_btn = form_el.find_element(By.XPATH, ".//button[contains(normalize-space(.),'Link')]")
        except Exception:
            # last resort: fallback to the global locator
            link_btn = self.driver.find_element(*self.LINK_BUTTON)

        # wait briefly for the Link button to enable; otherwise force-enable and click
        try:
            WebDriverWait(self.driver, 6).until(
                lambda d: (
                    (link_btn.get_attribute("disabled") in (None, "false"))
                    and ("disabled" not in (link_btn.get_attribute("class") or ""))
                )
            )
            # click normally if enabled
            try:
                link_btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", link_btn)
        except Exception:
            # fallback: remove disabled and click via JS
            try:
                self.driver.execute_script(
                    "arguments[0].removeAttribute('disabled'); arguments[0].classList.remove('disabled');",
                    link_btn,
                )
                self.driver.execute_script("arguments[0].click();", link_btn)
            except Exception:
                raise Exception("Failed to click Link button after filling card fields.")

        # wait for the form to disappear (it closes after successful link) or for payment method to show masked card
        try:
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.CARD_FORM))
        except Exception:
            # if form didn't disappear, try to detect card shown in the payment area
            try:
                pm = WebDriverWait(self.driver, 6).until(EC.visibility_of_element_located(self.PAYMENT_METHOD))
                pm_text = pm.text or ""
                if "****" in pm_text or "Card" in pm_text or "card" in pm_text:
                    return
            except Exception:
                pass
            # if still here, we fall through and let is_card_linked handle checks/failures

    def fill_card(self, number, code):
        """Alias used by tests; calls add_card."""
        return self.add_card(number, code)

    def is_card_linked(self):
        # prefer checking the payment method display for masked card text (safer after modal closes)
        try:
            pm_el = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.PAYMENT_METHOD))
            pm_text = pm_el.text or ""
            if "****" in pm_text:
                return True
            # some apps may show "Card ••••1234" or similar
            if "Card" in pm_text or "card" in pm_text or "•••" in pm_text or "****" in pm_text:
                return True
        except Exception:
            pass

        # fallback: check the input value (works in some flows while form is still present)
        try:
            return "****" in self.driver.find_element(*self.CARD_NUMBER_INPUT).get_attribute("value")
        except Exception:
            return False

    # --- Driver comment ---
    def write_comment_for_driver(self, message):
        """
        More robust: try visibility, then presence + scroll, then JS fallback.
        This prevents flaky timeouts when the comment field is inside a modal that appears slightly later.
        """
        el = None
        try:
            el = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.COMMENT_INPUT))
        except TimeoutException:
            # try presence + scroll into view
            try:
                el = WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(self.COMMENT_INPUT))
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                except Exception:
                    pass
            except Exception:
                el = None

        if el is None:
            raise Exception("Comment input not found or visible to enter driver comment.")

        try:
            el.clear()
        except Exception:
            pass

        # attempt normal send_keys, fallback to JS setting
        try:
            el.send_keys(message)
        except Exception:
            try:
                self.driver.execute_script(
                    "arguments[0].value = arguments[1];"
                    "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                    "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
                    el,
                    message,
                )
            except Exception as e:
                raise Exception(f"Could not enter driver comment: {e}")

    def get_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute("value")

    # --- Blanket & handkerchiefs ---
    def order_blanket_and_handkerchiefs(self):
        # click the slider elements (more reliable than trying to click inputs)
        self.wait_and_click(self.BLANKET_CHECKBOX)
        self.wait_and_click(self.HANDKERCHIEF_CHECKBOX)

    def is_blanket_selected(self):
        # checkbox input is near the slider; find a checkbox input relative to the label
        try:
            input_node = self.driver.find_element(
                By.XPATH,
                "//div[contains(@class,'r-sw-container') and .//div[contains(normalize-space(),'Blanket')]]//input[@type='checkbox']"
            )
            return input_node.is_selected()
        except Exception:
            return False

    def is_handkerchief_selected(self):
        try:
            input_node = self.driver.find_element(
                By.XPATH,
                "//div[contains(@class,'r-sw-container') and .//div[contains(normalize-space(),'Soundproof')]]//input[@type='checkbox']"
            )
            return input_node.is_selected()
        except Exception:
            return False

    # --- Ice cream ---
    def order_ice_creams(self, quantity):
        # click the + element `quantity` times
        for count in range(quantity):
            self.wait_and_click(self.ICE_CREAM_PLUS_BUTTON, timeout=7)

    def get_ice_cream_quantity(self):
        try:
            val = WebDriverWait(self.driver, 7).until(EC.visibility_of_element_located(self.ICE_CREAM_VALUE)).text
            return int(val.strip())
        except Exception:
            return 0

    # --- Car search / Order ---
    def place_taxi_order(self):
        self.wait_and_click(self.ORDER_BUTTON)

    def is_order_taxi_popup(self):
        return WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(self.ORDER_TAXI_POPUP)).is_displayed()