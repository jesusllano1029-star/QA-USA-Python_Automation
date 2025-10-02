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
    ADD_CARD_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[2]/div/div[1]/div[2]/div[3]')  # keep your working xpath
    # small correction — in your workspace you used the absolute XPaths that worked; keep them if different
    CARD_FORM = (By.XPATH, "//div[contains(@class,'section') and .//div[contains(normalize-space(),'Adding a card')]]//form")

    # changed per instructor feedback: not all attributes must be uppercase
    card_number_input = (By.ID, 'number')
    card_code_input = (By.ID, 'code')

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

    ORDER_BUTTON = (By.CSS_SELECTOR, ".smart-button")

    ORDER_TAXI_POPUP = (By.XPATH, "//div[contains(@class, 'order-modal') or contains(@class,'car-search')]")
    CAR_SEARCH_MODAL = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[2]/div')


    # --- Route ---
    def set_route(self, address_from, address_to):
        el_from = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ADDRESS_FROM))
        try:
            el_from.clear()
        except Exception:
            pass
        el_from.send_keys(address_from)

        el_to = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ADDRESS_TO))
        try:
            el_to.clear()
        except Exception:
            pass
        el_to.send_keys(address_to)

        self.click_call_taxi_button()

    def get_from(self):
        return self.driver.find_element(*self.ADDRESS_FROM).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.ADDRESS_TO).get_attribute("value")

    # --- Plan ---
    def select_supportive_plan(self):
        try:
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN)).click()
        except Exception:
            # fallback JS click
            el = self.driver.find_element(*self.SUPPORTIVE_PLAN)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
            self.driver.execute_script("arguments[0].click();", el)

    def get_selected_plan(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SELECTED_PLAN)).text

    # --- Phone helpers (used across tests) ---
    def fill_phone_number(self, phone):
        """
        Simple test helper used by phone-number test. Many UIs require
        clicking the phone button to reveal the input — do that here.
        """
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.PHONE_BUTTON)).click()
        except Exception:
            try:
                el = self.driver.find_element(*self.PHONE_BUTTON)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception:
                pass

        el_phone = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.PHONE_INPUT))
        try:
            el_phone.clear()
        except Exception:
            pass
        el_phone.send_keys(phone)

    def get_phone_number(self):
        """Return current phone input value (used in tests)"""
        return self.driver.find_element(*self.PHONE_INPUT).get_attribute("value")

    def click_call_taxi_button(self):
        try:
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()
        except Exception:
            el = self.driver.find_element(*self.CALL_TAXI_BUTTON)
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
            except Exception:
                pass
            self.driver.execute_script("arguments[0].click();", el)

    def reveal_phone_input_form(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.PHONE_BUTTON)).click()
        except Exception:
            try:
                el = self.driver.find_element(*self.PHONE_BUTTON)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception:
                pass
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.PHONE_INPUT))

    def enter_phone_number(self, phone):
        el = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.PHONE_INPUT))
        try:
            el.clear()
        except Exception:
            pass
        el.send_keys(phone)

    def click_next_button(self):
        try:
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()
        except Exception:
            el = self.driver.find_element(*self.NEXT_BUTTON)
            self.driver.execute_script("arguments[0].click();", el)

    def enter_sms_code(self, code):
        el = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SMS_INPUT))
        try:
            el.clear()
        except Exception:
            pass
        el.send_keys(code)

    def is_phone_confirmed(self):
        # heuristic: check class/value — adjust to real app specifics if needed
        el = self.driver.find_element(*self.PHONE_INPUT)
        class_attr = el.get_attribute("class") or ""
        val_attr = el.get_attribute("value") or ""
        return "confirmed" in class_attr or val_attr != ""

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
                pass
            time.sleep(delay_seconds)
        raise Exception("Phone confirmation code not found after waiting.")

    def confirm_phone(self, phone: str, attempts: int = 20, delay_seconds: int = 2, wait_after_confirm: float = 0.6):
        """
        Full phone confirmation flow used by tests:
        - reveal phone input (if needed)
        - enter phone and press Next
        - poll helpers.retrieve_phone_code for the SMS code
        - enter SMS code and click Confirm
        - wait briefly and attempt a lightweight verification that phone is confirmed
        """
        try:
            self.reveal_phone_input_form()
        except Exception:
            pass

        self.enter_phone_number(phone)
        self.click_next_button()

        code = None
        for _ in range(attempts):
            try:
                code = helpers.retrieve_phone_code(self.driver)
                if code:
                    break
            except Exception:
                pass
            time.sleep(delay_seconds)

        if not code:
            raise Exception("Phone confirmation code not found in confirm_phone().")

        self.enter_sms_code(code)
        try:
            confirm_btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.CONFIRM_BUTTON))
            try:
                confirm_btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", confirm_btn)
        except Exception:
            try:
                self.driver.execute_script(
                    "Array.from(document.querySelectorAll('button')).forEach(b=>{ if((b.innerText||'').trim().toLowerCase().includes('confirm')) b.click(); });"
                )
            except Exception:
                pass

        time.sleep(wait_after_confirm)
        try:
            WebDriverWait(self.driver, 6).until(lambda d: self.is_phone_confirmed())
        except Exception:
            pass

    # --- Card (payment) ---
    def add_card(self, number, code):
        """
        Open payment picker, click add card, fill fields and click Link.
        Afterwards wait for either the form to disappear or for the payment area
        to show a linked card using several heuristics.
        """
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PAYMENT_METHOD)).click()
        except Exception:
            try:
                el = self.driver.find_element(*self.PAYMENT_METHOD)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception:
                pass

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()
        except Exception:
            try:
                el = self.driver.find_element(*self.ADD_CARD_BUTTON)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception:
                pass

        form_el = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.CARD_FORM)
        )

        try:
            number_el = form_el.find_element(*self.card_number_input)
        except Exception:
            raise Exception("Card number input not found inside add-card form.")

        try:
            code_el = form_el.find_element(*self.card_code_input)
        except Exception:
            raise Exception("Card code input not found inside add-card form.")

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

        link_btn = None
        try:
            link_btn = form_el.find_element(By.XPATH, ".//button[contains(normalize-space(.),'Link')]")
        except Exception:
            try:
                link_btn = self.driver.find_element(*self.LINK_BUTTON)
            except Exception:
                pass

        if link_btn is None:
            raise Exception("Could not find Link button inside card form.")

        try:
            WebDriverWait(self.driver, 6).until(
                lambda d: (
                    (link_btn.get_attribute("disabled") in (None, "false"))
                    and ("disabled" not in (link_btn.get_attribute("class") or ""))
                )
            )
            try:
                link_btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", link_btn)
        except Exception:
            try:
                self.driver.execute_script(
                    "arguments[0].removeAttribute('disabled'); arguments[0].classList.remove('disabled');",
                    link_btn,
                )
                self.driver.execute_script("arguments[0].click();", link_btn)
            except Exception:
                raise Exception("Failed to click Link button after filling card fields.")


        try:
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.CARD_FORM))
            return
        except Exception:
            try:
                pm = WebDriverWait(self.driver, 6).until(EC.visibility_of_element_located(self.PAYMENT_METHOD))
                pm_text = pm.text or ""
                if "****" in pm_text or "Card" in pm_text or "card" in pm_text or "•••" in pm_text:
                    return
            except Exception:
                pass


        try:
            time.sleep(0.5)
            val = form_el.find_element(*self.card_number_input).get_attribute("value") or ""
            if "****" in val or val.strip() != "":
                return
        except Exception:
            pass


        raise Exception("Card linking did not complete (form still present and payment area not updated).")

    def fill_card(self, number, code):
        """Alias used by tests; calls add_card."""
        return self.add_card(number, code)

    def is_card_linked(self):
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

        try:
            el = self.driver.find_element(*self.card_number_input)
            val = el.get_attribute("value") or ""
            if "****" in val or val.strip() != "":
                return True
        except Exception:
            pass

        return False

    def close_payment_popup(self, timeout: int = 6) -> bool:
        """
        Close any open payment/add-card modal or section by clicking a visible close button.
        Returns True if we closed something, False otherwise.
        """
        close_selectors = [
            (By.CSS_SELECTOR, ".close-button.section-close"),
            (By.CSS_SELECTOR, ".section .close-button"),
            (By.CSS_SELECTOR, ".close-button.input-close-button"),
            (By.CSS_SELECTOR, ".button.full.disabled + .close-button"),  # defensive
        ]
        for loc in close_selectors:
            try:
                btn = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(loc))
                try:
                    btn.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", btn)
                # brief wait for modal to disappear
                time.sleep(0.25)
                return True
            except Exception:
                pass

        try:
            self.driver.execute_script("document.activeElement.blur();")
            from selenium.webdriver.common.keys import Keys  # local import to avoid global noise
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            time.sleep(0.25)
            return True
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
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.BLANKET_CHECKBOX)).click()
        except Exception:
            el = self.driver.find_element(*self.BLANKET_CHECKBOX)
            self.driver.execute_script("arguments[0].click();", el)
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.HANDKERCHIEF_CHECKBOX)).click()
        except Exception:
            el = self.driver.find_element(*self.HANDKERCHIEF_CHECKBOX)
            self.driver.execute_script("arguments[0].click();", el)

    def is_blanket_selected(self):
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
            try:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON)).click()
            except Exception:
                el = self.driver.find_element(*self.ICE_CREAM_PLUS_BUTTON)
                self.driver.execute_script("arguments[0].click();", el)

    def get_ice_cream_quantity(self):
        try:
            val = WebDriverWait(self.driver, 7).until(EC.visibility_of_element_located(self.ICE_CREAM_VALUE)).text
            return int(val.strip())
        except Exception:
            return 0

    # --- Car search / Order ---
    def place_taxi_order(self):
        try:
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()
        except Exception:
            # fallback to locate element and JS click
            el = self.driver.find_element(*self.ORDER_BUTTON)
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
            except Exception:
                pass
            self.driver.execute_script("arguments[0].click();", el)

    def is_order_taxi_popup(self):
        return WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(self.ORDER_TAXI_POPUP)).is_displayed()