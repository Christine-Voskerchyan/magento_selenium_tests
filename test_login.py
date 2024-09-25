import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import allure

LOGIN_URL = "https://magento.softwaretestingboard.com/customer/account/login/"
ACCOUNT_URL = "https://magento.softwaretestingboard.com/customer/account/"
EMAIL = "christine.voskerchyan@gmail.com"
PASSWORD = "12345.ABCDEabcde"
NEW_PASSWORD = "12345.ABCDEabcde"

@pytest.fixture(scope="module")
def driver():

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no_sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.mark.regression
@allure.feature('User Authentication')
@allure.suite('Login Tests')
@allure.title('Invalid Login Test')
@allure.description('This test verifies that the user cannot log in with invalid credentials and receives an appropriate error message.')
@allure.severity(allure.severity_level.CRITICAL)
def test_invalid_login(driver):
    with allure.step("Navigate to login page"):
        driver.get(LOGIN_URL)

    with allure.step("Enter invalid email"):
        email_input = driver.find_element(By.ID, 'email')
        email_input.send_keys("invalidmail@gmail.com")

    with allure.step("Enter invalid password"):
        password_input = driver.find_element(By.ID, 'pass')
        password_input.send_keys('invalidpassword')

    with allure.step("Click the login button"):
        login_button = driver.find_element(By.ID, 'send2')
        login_button.click()

    with allure.step("Wait for error message"):
        time.sleep(3)

    with allure.step("Verify the error message is displayed"):
        error_message = driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div[2]/div/div/div')
        assert "Please wait and try again later." in error_message.text

@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('User Authentication')
@allure.suite('Login Tests')
@allure.title('Valid Login Test')
@allure.description('This test verifies that the user can log in with valid credentials and is redirected to the account page.')
@allure.severity(allure.severity_level.BLOCKER)
def test_login(driver):
    with allure.step("Navigate to login page"):
        driver.get(LOGIN_URL)

    with allure.step("Enter valid email"):
        email_input = driver.find_element(By.ID, 'email')
        email_input.send_keys(EMAIL)

    with allure.step("Enter valid password"):
        password_input = driver.find_element(By.ID, 'pass')
        password_input.send_keys(PASSWORD)

    with allure.step("Click the login button"):
        login_button = driver.find_element(By.ID, 'send2')
        login_button.click()

    with allure.step("Wait for page load"):
        time.sleep(3)

    with allure.step("Verify user is redirected to the account page"):
        assert driver.current_url == ACCOUNT_URL

@pytest.mark.regression
@allure.feature('User Account Management')
@allure.suite('Password Management')
@allure.title('Change Password with Incorrect Current Password')
@allure.description('This test verifies that a user cannot change their password using an incorrect current password.')
@allure.severity(allure.severity_level.NORMAL)
def test_change_password_incorrect_current(driver):
    with allure.step("Navigate to the account page"):
        driver.get(ACCOUNT_URL)

    with allure.step("Click on 'Change Password' link"):
        change_password_link = driver.find_element(By.LINK_TEXT, 'Change Password')
        change_password_link.click()

    with allure.step("Enter incorrect current password"):
        current_password_input = driver.find_element(By.ID, 'current-password')
        current_password_input.send_keys("incorrectpassword")

    with allure.step("Enter new password and confirm it"):
        new_password_input = driver.find_element(By.ID, 'password')
        new_password_input.send_keys(NEW_PASSWORD)

        confirm_password_input = driver.find_element(By.ID, 'password-confirmation')
        confirm_password_input.send_keys(NEW_PASSWORD)

    with allure.step("Click the save button to attempt to change the password"):
        save_button = driver.find_element(By.XPATH, '//*[@id="form-validate"]/div/div[1]/button')
        save_button.click()

    with allure.step("Wait for error message to appear"):
        time.sleep(3)

    with allure.step("Verify the error message is displayed when using an incorrect current password"):
        error_message = driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[1]/div[2]/div/div/div')
        assert 'Verify the password and try again' in error_message.text

@pytest.mark.regression
@allure.feature('User Account Management')
@allure.suite('Password Management')
@allure.title('Change Password with Mismatched Confirmation')
@allure.description('This test verifies that the user cannot change their password if the new password and confirmation password do not match.')
@allure.severity(allure.severity_level.NORMAL)
def test_change_password_mismatch(driver):
    with allure.step("Navigate to the account page"):
        driver.get(ACCOUNT_URL)

    with allure.step("Click on 'Change Password' link"):
        change_password_link = driver.find_element(By.LINK_TEXT, 'Change Password')
        change_password_link.click()

    with allure.step("Enter current password"):
        current_password_input = driver.find_element(By.ID, 'current-password')
        current_password_input.send_keys(PASSWORD)

    with allure.step("Enter new password"):
        new_password_input = driver.find_element(By.ID, 'password')
        new_password_input.send_keys(NEW_PASSWORD)

    with allure.step("Enter mismatched confirmation password"):
        confirm_password_input = driver.find_element(By.ID, 'password-confirmation')
        confirm_password_input.send_keys('mismatchedpassword')

    with allure.step("Click the save button to attempt to change the password"):
        save_button = driver.find_element(By.XPATH, "//button[@title='Save']")
        save_button.click()

    with allure.step("Wait for error message to appear"):
        time.sleep(3)

    with allure.step("Verify the error message is displayed when the confirmation password does not match"):
        error_message = driver.find_element(By.ID, 'password-confirmation-error')
        assert "Please enter the same value again." in error_message.text

@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('User Account Management')
@allure.suite('Password Management')
@allure.title('Change Password Successfully')
@allure.description('This test verifies that a user can change their password successfully when all fields are entered correctly.')
@allure.severity(allure.severity_level.CRITICAL)
def test_change_password(driver):
    with allure.step("Navigate to the account page"):
        driver.get(ACCOUNT_URL)

    with allure.step("Click on 'Change Password' link"):
        change_password_link = driver.find_element(By.LINK_TEXT, 'Change Password')
        change_password_link.click()

    with allure.step("Enter current password"):
        current_password_input = driver.find_element(By.ID, 'current-password')
        current_password_input.send_keys(PASSWORD)

    with allure.step("Enter new password"):
        new_password_input = driver.find_element(By.ID, 'password')
        new_password_input.send_keys(NEW_PASSWORD)

    with allure.step("Confirm new password"):
        confirm_password_input = driver.find_element(By.ID, 'password-confirmation')
        confirm_password_input.send_keys(NEW_PASSWORD)

    with allure.step("Click the save button to update password"):
        save_button = driver.find_element(By.XPATH, "//button[@title='Save']")
        save_button.click()

    with allure.step("Wait for success message to appear"):
        time.sleep(3)

    with allure.step("Verify the success message is displayed"):
        success_message = driver.find_element(By.XPATH, "//div[contains(@class, 'message-success')]")
        assert "You saved the account information." in success_message.text