import unittest
from parameterized import parameterized
from selenium import webdriver
from pages.kiwisaver_calculator import KiwiSaverCalcPage, KSCalcPageElement

class KiwiSaverCalculator(unittest.TestCase):
    def setUp(self) -> None:
        """
        Load Chromedriver and go to the Kiwisaver calculator page.
        Validate that the correct page is lpaded by verifying the title of the page.
        :return:
        """
        self.driver = webdriver.Chrome()
        self.ks_calc_page = KiwiSaverCalcPage(self.driver)
        self.ks_calc_page.load()
        assert self.ks_calc_page.is_title_matches(), "Could not load Kiwisaver Calculator page"
        # Switch to the iframe that contains all the calculation fields.
        self.ks_calc_page.switch_to_calculator()


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
    def test_info_icons(self, test_name, field_name, field_info_text):
        """
        This is testing the following user story:
        As a Product Owner
        I want that while using the KiwiSaver Retirement Calculator all fields in the calculator have got the information icon present
        So that
        The user is able to get a clear understanding of what needs to be entered in the field .

        :param test_name: Name of the test, can be anything.
        :param field_name: The field for which the info icon is being tested.
        :param field_info_text: the text that needs to be validated when the user clicks on the info icon.
        :return:
        """
        if(test_name == "annual_income" or test_name == "member_contrib"):
            # To display these fields
            KSCalcPageElement(driver=self.driver, locator="employment-status").select_dropdown("Employed")
        element = KSCalcPageElement(driver=self.driver, locator=field_name)
        element.info_button().click()
        self.assertEqual(element.info_text(), field_info_text)

    def test_calculation_employed(self):
        """
        This is the testing the following user story for a person who is employed:
        As a Product Owner
        I want that the KiwiSaver Retirement Calculator users are able to calculate what their KiwiSaver projected balance would be at retirement
        So that
        The users are able to plan their investments better.

        :return:
        """
        self.ks_calc_page.enter_details(current_age=30, emp_status="Employed", annual_income=82000, member_contrib="4%", pir="17.5%", risk_profile="High")
        self.ks_calc_page.view_projections()

        self.assertEqual(KSCalcPageElement(self.driver, "span.result-title").element().text,
                         "At age 65, your KiwiSaver balance is estimated to be:")
        self.assertEqual(KSCalcPageElement(self.driver, "span.result-value").element().text,
                         "$\n279,558")
        self.assertTrue(KSCalcPageElement(self.driver, "div.results-graph").has_element())

    def test_calcuation_self_employed(self):
        """
        This is the testing the following user story for a person who is self employed:
        As a Product Owner
        I want that the KiwiSaver Retirement Calculator users are able to calculate what their KiwiSaver projected balance would be at retirement
        So that
        The users are able to plan their investments better.

        :return:
        """
        self.ks_calc_page.enter_details(current_age=45, emp_status="Self-employed", pir="10.5%", current_balance=100000,
                                        vol_contribs_amount=90, vol_contribs_frequency="Fortnightly",
                                        risk_profile="Medium", savings_goal=290000)
        self.ks_calc_page.view_projections()

        self.assertEqual(KSCalcPageElement(self.driver, "span.result-title").element().text,
                         "At age 65, your KiwiSaver balance is estimated to be:")
        self.assertEqual(KSCalcPageElement(self.driver, "span.result-value").element().text,
                         "$\n212,440")
        self.assertTrue(KSCalcPageElement(self.driver, "div.results-graph").has_element())

    def test_calculation_not_employed(self):
        """
        This is the testing the following user story for a person who is not employed:
        As a Product Owner
        I want that the KiwiSaver Retirement Calculator users are able to calculate what their KiwiSaver projected balance would be at retirement
        So that
        The users are able to plan their investments better.

        :return:
        """
        self.ks_calc_page.enter_details(current_age=55, emp_status="Not employed", pir="10.5%", current_balance=140000,
                                        vol_contribs_amount=10, vol_contribs_frequency="Annually", risk_profile="Medium",
                                        savings_goal=200000)
        self.ks_calc_page.view_projections()

        self.assertEqual(KSCalcPageElement(self.driver, "span.result-title").element().text,
                         "At age 65, your KiwiSaver balance is estimated to be:")
        self.assertEqual(KSCalcPageElement(self.driver, "span.result-value").element().text,
                         "$\n168,425")
        self.assertTrue(KSCalcPageElement(self.driver, "div.results-graph").has_element())


    def tearDown(self) -> None:
        """
        Close and Quit the driver once test completes
        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()