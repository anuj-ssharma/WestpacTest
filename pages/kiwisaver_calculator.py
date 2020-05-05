from selenium.webdriver.support.wait import WebDriverWait


class KiwiSaverCalcPage():
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.westpac.co.nz/kiwisaver/calculators/kiwisaver-calculator/"

    def load(self):
        self.driver.get(self.url)

    def is_title_matches(self):
        return "KiwiSaver Retirement Calculator - Westpac NZ" in self.driver.title

    def switch_to_calculator(self):
        iframe = KSCalcPageElement(driver=self.driver, locator=".calculator-embed > iframe").element()
        self.driver.switch_to.frame(iframe)

    def enter_details(self, current_age, emp_status, pir, risk_profile, current_balance=None, vol_contribs_amount=None, vol_contribs_frequency=None, annual_income=None, member_contrib=None, savings_goal=None):
        KSCalcPageElement(driver=self.driver, field_name="current-age").set_field_value(current_age)
        KSCalcPageElement(driver=self.driver, field_name="employment-status").select_dropdown(emp_status)
        KSCalcPageElement(driver=self.driver, field_name="pir-rate").select_dropdown(pir)
        KSCalcPageElement(driver=self.driver, field_name="risk-profile").select_radio_button(risk_profile)
        # Optional fields
        if current_balance is not None:
            KSCalcPageElement(driver=self.driver, field_name="kiwi-saver-balance").set_field_value(current_balance)
        if vol_contribs_amount is not None:
            KSCalcPageElement(driver=self.driver, field_name="voluntary-contributions").set_field_value(vol_contribs_amount)
            KSCalcPageElement(driver=self.driver, field_name="voluntary-contributions").select_dropdown(vol_contribs_frequency)
        if annual_income is not None:
            KSCalcPageElement(driver=self.driver, field_name="annual-income").set_field_value(annual_income)
        if member_contrib is not None:
            KSCalcPageElement(driver=self.driver, field_name="kiwisaver-member-contribution").select_radio_button(member_contrib)
        if savings_goal is not None:
            KSCalcPageElement(driver=self.driver, field_name="savings-goal").set_field_value(savings_goal)

    def view_projections(self):
        results_btn = WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_css_selector(
                    "button.btn-results-reveal"))
        results_btn.click()



class KSCalcPageElement():
    def __init__(self, driver, field_name=None, locator=None):
        self.driver = driver
        self.field_name = field_name
        self.locator = locator

    def info_icon(self):
        WebDriverWait(self.driver, 20).until(
                lambda driver: self.driver.find_element_by_css_selector(
                        ".wpnib-field-{} div.field-info button".format(self.field_name)))
        element = self.driver.find_element_by_css_selector(
            ".wpnib-field-{} div.field-info button".format(self.field_name))
        return element

    def info_text(self):
        WebDriverWait(self.driver, 20).until(
                lambda driver: self.driver.find_element_by_css_selector(
                        "div.wpnib-field-{}.field-group div.message-info p".format(self.field_name)))
        element = self.driver.find_element_by_css_selector(
                "div.wpnib-field-{}.field-group div.message-info p".format(self.field_name))
        return element.text

    def set_field_value(self, value):
        WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_css_selector(".wpnib-field-{} input".format(self.field_name)))
        self.driver.find_element_by_css_selector(".wpnib-field-{} input".format(self.field_name)).clear()
        self.driver.find_element_by_css_selector(".wpnib-field-{} input".format(self.field_name)).send_keys(value)

    def element(self):
        return WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_css_selector(self.locator))

    def has_element(self):
        return WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_css_selector(self.locator).is_displayed())

    def select_dropdown(self, option_text):
        element = WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_css_selector(".wpnib-field-{} div.select-control".format(self.field_name)))
        element.click()

        dropdown_options = WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_elements_by_css_selector(".wpnib-field-{} div.dropdown li".format(self.field_name)))
        for option in dropdown_options:
            if option.text == option_text:
                option.click()
                break

    def select_radio_button(self, contribution):
        member_contribution_options = WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_elements_by_css_selector(
                    ".wpnib-field-{} div.radio-control".format(self.field_name)))
        for option in member_contribution_options:
            if option.text == contribution:
                option.find_element_by_tag_name("input").click()
                break