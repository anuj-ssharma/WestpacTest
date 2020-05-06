from datetime import datetime
import os
import unittest
from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.kiwisaver_calculator import KiwiSaverCalcPage, KSCalcPageElement

class KiwiSaverCalculator(unittest.TestCase):
    def setUp(self) -> None:
        """
        Load Chromedriver and go to the Kiwisaver calculator page.
        Validate that the correct page is loaded by verifying the title of the page.
        :return:
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)

        self.kiwisaver_calc_page = KiwiSaverCalcPage(self.driver)
        self.kiwisaver_calc_page.load()
        assert self.kiwisaver_calc_page.is_title_matches(), "Could not load Kiwisaver Calculator page"
        # Switch to the iframe that contains all the calculation fields.
        self.kiwisaver_calc_page.switch_to_calculator()


    @parameterized.expand([
    ["current_age", "current-age", "This calculator has an age limit of 84 years old."],
    ["employment_status", "employment-status", "If you are earning a salary or wage, select ‘Employed’. Your employer contributions will be automatically calculated at a rate of 3% of your before-tax salary or wages. You can also select ‘Self-employed’ or ‘Not employed’ and then enter below (in the Voluntary contributions field), the amount and frequency of any contributions that you wish to make."],
    ["pir_rate", "pir-rate", "This is your prescribed investor rate (PIR) for tax purposes. If you don't know what your PIR is, click on the ‘Find My Rate’ button."],
    ["kiwi_saver_balance", "kiwi-saver-balance", "If you do not have a KiwiSaver account, then leave this field blank."],
    ["voluntary_contributions", "voluntary-contributions", "If you are 'Self-Employed' or 'Not employed', you can make direct contributions to your KiwiSaver account. If you are 'Employed', you can make voluntary contributions in addition to your regular employee contributions."],
    ["risk_profile", "risk-profile", "The risk profile affects your potential investment returns:"],
    ["savings_goal", "savings-goal", "Enter the amount you would like to have saved when you reach your intended retirement age. If you aren’t sure what this amount is, you can leave it blank or use the Sorted Retirement Planner"],
    ["annual_income", "annual-income", "Only include your total annual income that is paid to you by your employer(s). Other income sources such as rental income or dividends should not be included."],
    ["member_contrib", "kiwisaver-member-contribution", "You can choose to contribute a regular amount equal to 3%, 4%, 6%, 8% or 10% of your before-tax salary or wage. If you do not select a rate, your rate will be 3%."]
    ])
    def test_info_icons(self, test_name, field_name, expected_field_info_text):
        """
        :param test_name: Name of the test that will be used for reporting purposes
        :param field_name: The field for which the info icon is being tested.
        :param expected_field_info_text: the expected text to be displayed when the user clicks on the info icon.
        :return:
        """
        if(test_name == "annual_income" or test_name == "member_contrib"):
            # The fields annual income and member contribution are only shown when the user selects
            # the 'Employed' status for Employment status.
            KSCalcPageElement(driver=self.driver, field_name="employment-status").select_dropdown_value("Employed")

        field = KSCalcPageElement(driver=self.driver, field_name=field_name)
        field.info_icon().click()
        self.assertEqual(field.info_text(), expected_field_info_text)


    def test_calculation_for_employed(self):
        self.kiwisaver_calc_page.enter_details(current_age=30, emp_status="Employed", annual_income=82000, member_contrib="4%",
                                               pir="17.5%", risk_profile="High")
        self.kiwisaver_calc_page.view_projections()

        self.assertEqual(KSCalcPageElement(self.driver, css_locator="span.result-title").element().text,
                         "At age 65, your KiwiSaver balance is estimated to be:")
        self.assertEqual(KSCalcPageElement(self.driver, css_locator="span.result-value").element().text,
                         "$\n279,558")
        self.assertTrue(KSCalcPageElement(self.driver, css_locator="div.results-graph").has_element())


    def test_calcuation_for_self_employed(self):
        self.kiwisaver_calc_page.enter_details(current_age=45, emp_status="Self-employed", pir="10.5%", current_balance=100000,
                                               vol_contribs_amount=90, vol_contribs_frequency="Fortnightly",
                                               risk_profile="Medium", savings_goal=290000)
        self.kiwisaver_calc_page.view_projections()

        self.assertEqual(KSCalcPageElement(self.driver, css_locator="span.result-title").element().text,
                         "At age 65, your KiwiSaver balance is estimated to be:")
        self.assertEqual(KSCalcPageElement(self.driver, css_locator="span.result-value").element().text,
                         "$\n212,440")
        self.assertTrue(KSCalcPageElement(self.driver, css_locator="div.results-graph").has_element())


    def test_calculation_for_not_employed(self):
        self.kiwisaver_calc_page.enter_details(current_age=55, emp_status="Not employed", pir="10.5%", current_balance=140000,
                                               vol_contribs_amount=10, vol_contribs_frequency="Annually",
                                               risk_profile="Medium", savings_goal=200000)
        self.kiwisaver_calc_page.view_projections()

        self.assertEqual(KSCalcPageElement(self.driver, css_locator="span.result-title").element().text,
                         "At age 65, your KiwiSaver balance is estimated to be:")
        self.assertEqual(KSCalcPageElement(self.driver, css_locator="span.result-value").element().text,
                         "$\n168,425")
        self.assertTrue(KSCalcPageElement(self.driver, css_locator="div.results-graph").has_element())


    def tearDown(self) -> None:
        """
        Take a full page screenshot if the test fails.
        Finally close and Quit the driver.
        :return:
        """
        for method, error in self._outcome.errors:
            if error:
                S = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
                self.driver.set_window_size(S('Width'), S('Height'))
                if not os.path.exists("screenshots"):
                    os.makedirs("screenshots")
                filename = "{}-{}".format(self._testMethodName,datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
                self.driver.find_element_by_tag_name('body').screenshot('screenshots/{}.png'.format(filename))
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()