# Overview
* This repository contains the tests requested as part of the technical test from Westpac NZ. 
* The tests are defined in the `test/test_kiwisaver.py`. There are a total of 12 tests when the suite is executed. 
    * `setUp` Step - Loads the chrome driver and goes to the page under test.
    * test_info_icons - Tests for the user story as follows:
        > As a Product Owner
          I want that while using the KiwiSaver Retirement Calculator all fields in the calculator have got the information icon present
        So that
        The user is able to get a clear understanding of what needs to be entered in the field .
    * Kiwisaver calculation tests - Tests for the user story as follows:
        >    As a Product Owner
        I want that the KiwiSaver Retirement Calculator users are able to calculate what their KiwiSaver projected balance would be at retirement
        So that
        The users are able to plan their investments better.
        * test_calculation_employed
        * test_calculation_self_employed
        * test_calculation_not_employed

# Running tests locally (Windows x64)

1. Install Python 3.8 from https://www.python.org/downloads/
2. Clone the project `git clone https://github.com/anuj-ssharma/WestpacTest.git`
3. Within the project root directory, run `pip install -r requirements.txt`. 
    * if pip is not installed, install using the instructions at (https://pip.pypa.io/en/stable/installing/)
4. If chrome browser not already installed, install from https://www.google.com/chrome/. Ensure that the chrome browser is on major version 81
    * For the purposes of this test, the chromedriver is within this repo itself in `drivers` directory. In the real world, this would be managed via a package manager.  
4. Within the project directory, run `python -m unittest test\test_kiwisaver.py` to run all tests.
    * To run a single test, run `python -m unittest test.test_kiwisaver.KiwiSaverCalculator.<name_of_test_method>`, e.g., `python -m unittest test.test_kiwisaver.KiwiSaverCalculator.test_calculation_for_employed`
    * In case of a test failure, screenshot of the full page will be saved to the `screenshots` directory.
    * By default, the tests will run in non-headless mode. 
    
 
