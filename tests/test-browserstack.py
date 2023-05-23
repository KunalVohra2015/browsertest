import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture(scope="module")
def driver(request):
    # Define BrowserStack credentials
    bs_username = "kunalvohra_scwMkP"
    bs_access_key = "uvbxNz3gCsKc6Ada4C2T"

    # Define BrowserStack capabilities for different browsers
    browsers = [
        {
            "os": "Windows",
            "os_version": "10",
            "browser": "Chrome",
            "browser_version": "latest",
            "local": "false"
        },
        {
            "os": "OS X",
            "os_version": "Ventura",
            "browser": "Firefox",
            "browser_version": "latest",
            "local": "false"
        },
        {
            "device": "Samsung Galaxy S22",
            "real_mobile": "true",
            "os_version": "12.0",
            "local": "false"
        },
    ]

    # Define options for running tests on BrowserStack
    bs_options = {
        "browserstack.user": bs_username,
        "browserstack.key": bs_access_key,
        "name": "BrowserStack Test"
    }

    # Initialize WebDriver with capabilities and options
    capabilities = browsers[request.param]
    capabilities.update(bs_options)
    driver = webdriver.Remote(
        command_executor="https://hub-cloud.browserstack.com/wd/hub",
        desired_capabilities=capabilities
    )

    # Wait for page to load
    driver.implicitly_wait(10)

    # Return the driver to the test
    yield driver

    # Quit the driver after the test
    driver.quit()


def test_browserstack_login_logout(driver):
    # Open BrowserStack login page
    driver.get("https://www.browserstack.com/users/sign_in")

    # Log in using trial credentials
    username = "Kunal.Vohra2015@gmail.com"
    password = "Tacos123"
    driver.find_element(By.ID, "user_email_login").send_keys(username)
    driver.find_element(By.ID, "user_password").send_keys(password)
    driver.find_element(By.NAME, "commit").click()

    # Assert that the homepage includes a link to Invite Users
    invite_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Invite Users"))
    )
    assert invite_link is not None

    # Retrieve the link's URL
    invite_url = invite_link.get_attribute("href")
    print("Invite Users URL:", invite_url)

    # Log out of BrowserStack
    driver.find_element(By.CSS_SELECTOR, ".header-user-dropdown").click()
    driver.find_element(By.CSS_SELECTOR, ".header-user-logout").click()

    # Verify successful logout
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Log In"))
    )
    assert login_button is not None


if __name__ == "__main__":
    pytest.main(["-v", "-s", "--driver", "Chrome", "--driver", "Firefox", "--driver", "SamsungGalaxyS22"])
