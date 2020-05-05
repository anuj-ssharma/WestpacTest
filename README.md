# Overview
* This repository contains the tests requested as part of the technical tests from Westpac NZ. 
* The tests are defined in the `test/test_kiwisaver.py` file. There are a total of 12 tests when the suite is executed. 
    * Setup Step - Loads the chrome driver and goes to the page under test.
    * test_info_icons - Tests for the first user story. Please refer to the comments in the test
    * Calculation tests - Please refer to the comments in the test
        * test_calculation_employed
        * test_calculation_self_employed
        * test_calculation_not_employed

# Test Execution (Travis CI)
TODO

# Running tests locally

1. Install Python 3.8
2. Clone the project `git clone https://github.com/anuj-ssharma/WestpacTest.git`
3. Within the project, run `pip install -r requirements.txt`. 
    * if pip is not installed, install using the instructions at (https://pip.pypa.io/en/stable/installing/)
4. Within the project directory, run `python -m unittest test\test_kiwisaver.py`
 
