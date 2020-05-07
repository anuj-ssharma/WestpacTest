from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class KiwiSaverCalcPage():
    """
    Class to maintain the various actions of the Kiwisaver calculator page
    """
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.westpac.co.nz/kiwisaver/calculators/kiwisaver-calculator/"

    def load(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 20).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div#widget-loading-mask")))

    def is_title_matches(self):
        return "KiwiSaver Retirement Calculator - Westpac NZ" in self.driver.title

    def switch_to_calculator(self):
        iframe = KSCalcPageElement(driver=self.driver, css_locator=".calculator-embed > iframe").element()
        self.driver.switch_to.frame(iframe)

    def enter_details(self, current_age, emp_status, pir, risk_profile, current_balance=None, vol_contribs_amount=None, vol_contribs_frequency=None, annual_income=None, member_contrib=None, savings_goal=None):
        KSCalcPageElement(driver=self.driver, field_name="current-age").set_field_value(current_age)
        KSCalcPageElement(driver=self.driver, field_name="employment-status").select_dropdown_value(emp_status)
        if annual_income is not None:
            KSCalcPageElement(driver=self.driver, field_name="annual-income").set_field_value(annual_income)
        if member_contrib is not None:
            KSCalcPageElement(driver=self.driver, field_name="kiwisaver-member-contribution").select_radio_button(member_contrib)
        KSCalcPageElement(driver=self.driver, field_name="pir-rate").select_dropdown_value(pir)
        if current_balance is not None:
            KSCalcPageElement(driver=self.driver, field_name="kiwi-saver-balance").set_field_value(current_balance)

        if vol_contribs_amount is not None:
            KSCalcPageElement(driver=self.driver, field_name="voluntary-contributions").set_field_value(vol_contribs_amount)
            KSCalcPageElement(driver=self.driver, field_name="voluntary-contributions").select_dropdown_value(vol_contribs_frequency)
        KSCalcPageElement(driver=self.driver, field_name="risk-profile").select_radio_button(risk_profile)
        if savings_goal is not None:
            KSCalcPageElement(driver=self.driver, field_name="savings-goal").set_field_value(savings_goal)

    def view_projections(self):
        results_btn = KSCalcPageElement(driver=self.driver, css_locator="button.btn-results-reveal").element()
        results_btn.click()



class KSCalcPageElement():
    """
    Class to maintain the elements on the Kiwisaver calculations page
    """
    def __init__(self, driver, field_name=None, css_locator=None):
        """
        Use either the field_name or the css_locator to find an element.
        :param driver:
        :param field_name: This is based on the field name on the page and uses the locator pre-defined in the methods
        :param css_locator: This is based on finding an element based on the css locator
        """
        self.driver = driver
        self.field_name = field_name
        self.locator = css_locator

    def wait_for_element_to_be_visible(self, css_locator):
        self.wait_for_loading_widget()

        element = WebDriverWait(self.driver, 20).until \
            (EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, css_locator)))
        return element

    def wait_for_elements_to_be_visible(self, css_locator):
        self.wait_for_loading_widget()

        elements = WebDriverWait(self.driver, 20).until \
            (EC.visibility_of_any_elements_located(
                    (By.CSS_SELECTOR, css_locator)))
        return elements

    def wait_for_loading_widget(self):
        # Wait for a couple of seconds if the loading widget is visible
        try:
            WebDriverWait(self.driver, 2).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div#widget-loading-mask")))
        except Exception:
            # We don't want to do anything here
            pass

    def info_icon(self):
        """
        :return: Information icon for the field on the page
        """
        element = self.wait_for_element_to_be_visible(".wpnib-field-{} div.field-info button".format(self.field_name))
        return element

    def info_text(self):
        """
        :return: Information icon text for the field on the page.
        """
        element = self.wait_for_element_to_be_visible("div.wpnib-field-{}.field-group div.message-info p".format(self.field_name))
        return element.text

    def set_field_value(self, value):
        """
        Set the value of a field on the page
        :param value:
        :return:
        """
        element = self.wait_for_element_to_be_visible(".wpnib-field-{} input".format(self.field_name))
        element.clear()
        element.send_keys(value)

    def element(self):
        """
        :return: WebDriver element based on the css locator
        """
        element = self.wait_for_element_to_be_visible(self.locator)
        return element

    def has_element(self):
        """
        :return: True if the element is displayed on the page otherwise False
        """
        return self.wait_for_element_to_be_visible(self.locator)

    def select_dropdown_value(self, option_text):
        """
        Select a value from a dropdown field
        :param option_text: The value to be selected
        :return:
        """
        element = self.wait_for_element_to_be_visible(".wpnib-field-{} div.select-control".format(self.field_name))
        element.click()
        self.wait_for_element_to_be_visible(".wpnib-field-{} div.dropdown ul.option-list".format(self.field_name))
        dropdown_options = self.driver.find_elements_by_css_selector(".wpnib-field-{} div.dropdown li".format(self.field_name))
        for option in dropdown_options:
            if option.text == option_text:
                option.click()
                break

    def select_radio_button(self, option_to_select):
        """
        Select a radio button option for a field
        :param option_to_select: The option text to be selected
        :return: 
        """
        member_contribution_options = self.wait_for_elements_to_be_visible(".wpnib-field-{} div.radio-control".format(self.field_name))
        for option in member_contribution_options:
            if option.text == option_to_select:
                option.find_element_by_tag_name("input").click()
                break