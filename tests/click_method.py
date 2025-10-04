from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://www.saucedemo.com/"


def login_as_standard_user(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "user-name")))
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 20).until(EC.url_contains("inventory"))


def js_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)


def click_when_clickable(driver, locator):
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator))
    js_click(driver, el)

