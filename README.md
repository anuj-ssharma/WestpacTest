[![Build Status](https://travis-ci.com/anuj-ssharma/WestpacTest.svg?branch=master)](https://travis-ci.com/anuj-ssharma/WestpacTest)

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

# Running tests on Travis CI (Linux)

The tests can be executed on the Travis CI server as well, however this only works for Chrome (at the moment). Click on the `build` button at the top of this
README page to view the results of the latest execution. 


# Running tests locally (Windows x64)

1. Install Python 3.8 from https://www.python.org/downloads/
2. Clone the project `git clone https://github.com/anuj-ssharma/WestpacTest.git`
3. Within the project root directory, run `pip install -r requirements.txt`. 
    * if pip is not installed, install using the instructions at (https://pip.pypa.io/en/stable/installing/)
4. If chrome browser is not already installed, install from https://www.google.com/chrome/. Ensure that the chrome browser is on major version 81  
6. Within the project directory,
    * To run on Chrome, run `set BROWSER=chrome` on the command line. To run on Firefox, run `set BROWSER=firefox`
    * To run headless, run `set HEADLESS=1`.
    * Run `python -m unittest test\test_kiwisaver.py` to run all tests.
    * To run a single test, run `python -m unittest test.test_kiwisaver.KiwiSaverCalculator.<name_of_test_method>`, e.g., `python -m unittest test.test_kiwisaver.KiwiSaverCalculator.test_calculation_for_employed`
    * In case of a test failure, screenshot of the full page will be saved to the `screenshots` directory.
    * By default, the tests will run in non-headless mode. 
    
 
