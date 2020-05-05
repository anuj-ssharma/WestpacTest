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
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector(".calculator-embed > iframe"))

    def enter_details(self, current_age, emp_status, pir, risk_profile, current_balance=None, vol_contribs_amount=None, vol_contribs_frequency=None, annual_income=None, member_contrib=None, savings_goal=None):
        KSCalcPageElement(driver=self.driver, locator="current-age").set(current_age)
        KSCalcPageElement(driver=self.driver, locator="employment-status").select_dropdown(emp_status)
        KSCalcPageElement(driver=self.driver, locator="pir-rate").select_dropdown(pir)
        KSCalcPageElement(driver=self.driver, locator="risk-profile").select_radio_button(risk_profile)
        # Optional fields
        if current_balance is not None:
            KSCalcPageElement(driver=self.driver, locator="kiwi-saver-balance").set(current_balance)
        if vol_contribs_amount is not None:
            KSCalcPageElement(driver=self.driver, locator="voluntary-contributions").set(vol_contribs_amount)
            KSCalcPageElement(driver=self.driver, locator="voluntary-contributions").select_dropdown(vol_contribs_frequency)
        if annual_income is not None:
            KSCalcPageElement(driver=self.driver, locator="annual-income").set(annual_income)
        if member_contrib is not None:
            KSCalcPageElement(driver=self.driver, locator="kiwisaver-member-contribution").select_radio_button(member_contrib)
        if savings_goal is not None:
            KSCalcPageElement(driver=self.driver, locator="savings-goal").set(savings_goal)

    def view_projections(self):
        results_btn = WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_css_selector(
                    "button.btn-results-reveal"))
        results_btn.click()



class KSCalcPageElement():
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    def info_button(self):
        WebDriverWait(self.driver, 20).until(
                lambda driver: self.driver.find_element_by_css_selector(
                        ".wpnib-field-{} div.field-info button".format(self.locator)))
        element = self.driver.find_element_by_css_selector(
            ".wpnib-field-{} div.field-info button".format(self.locator))
        return element

    def info_text(self):
        WebDriverWait(self.driver, 20).until(
                lambda driver: self.driver.find_element_by_css_selector(
                        "div.wpnib-field-{}.field-group div.message-info p".format(self.locator)))
        element = self.driver.find_element_by_css_selector(
                "div.wpnib-field-{}.field-group div.message-info p".format(self.locator))
        return element.text

    def set(self, value):
        WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_css_selector(".wpnib-field-{} input".format(self.locator)))
        self.driver.find_element_by_css_selector(".wpnib-field-{} input".format(self.locator)).clear()
        self.driver.find_element_by_css_selector(".wpnib-field-{} input".format(self.locator)).send_keys(value)

    def element(self):
        return WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_css_selector(self.locator))

    def has_element(self):
        return WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_css_selector(self.locator).is_displayed())

    def select_dropdown(self, option_text):
        element = WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_css_selector(".wpnib-field-{} div.select-control".format(self.locator)))
        element.click()

        dropdown_options = WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_elements_by_css_selector(".wpnib-field-{} div.dropdown li".format(self.locator)))
        for option in dropdown_options:
            if option.text == option_text:
                option.click()
                break

    def select_radio_button(self, contribution):
        member_contribution_options = WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_elements_by_css_selector(
                    ".wpnib-field-{} div.radio-control".format(self.locator)))
        for option in member_contribution_options:
            if option.text == contribution:
                option.find_element_by_tag_name("input").click()
                break