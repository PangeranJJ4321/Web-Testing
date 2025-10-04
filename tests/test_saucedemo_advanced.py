from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    ElementClickInterceptedException, WebDriverException, StaleElementReferenceException
)
from click_method import js_click, click_when_clickable, fill_input_with_js
import time

BASE_URL = "https://www.saucedemo.com/"


def login_as_standard_user(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "user-name")))
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 20).until(EC.url_contains("inventory"))


def test_login_form_validation(driver):
    """Test login form validation with empty fields and invalid credentials"""
    driver.get(BASE_URL)
    
    # Test empty username
    driver.find_element(By.ID, "login-button").click()
    error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    assert "Username is required" in error.text
    
    # Test empty password
    driver.find_element(By.ID, "user-name").send_keys("test")
    driver.find_element(By.ID, "login-button").click()
    error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    assert "Password is required" in error.text
    
    # Test invalid credentials
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "user-name").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    assert "Username and password do not match" in error.text

    login_as_standard_user(driver)


def test_product_sorting(driver):
    """Test product sorting functionality"""
    test_login_form_validation(driver)
    
    # Get initial product names
    initial_products = [el.text for el in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    
    # Test sorting by Name (A to Z)
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_value("az")
    
    WebDriverWait(driver, 5).until(
        lambda d: d.find_elements(By.CLASS_NAME, "inventory_item_name")[0].text == sorted(initial_products)[0]
    )
    
    sorted_products = [el.text for el in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    assert sorted_products == sorted(initial_products)
    
    # Test sorting by Name (Z to A)
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_value("za")
    
    WebDriverWait(driver, 5).until(
        lambda d: d.find_elements(By.CLASS_NAME, "inventory_item_name")[0].text == sorted(initial_products, reverse=True)[0]
    )
    
    reverse_sorted_product = [el.text for el in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    assert reverse_sorted_product == sorted(initial_products, reverse=True)
    
    # Test sorting by Price (low to high)
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_value("lohi")
    
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_price"))
    )
    
    prices = [float(el.text.replace("$", "")) for el in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
    assert prices == sorted(prices)

    # Test sorting by Price (High to Low)
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_value("hilo")
    
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_price"))
    )
    
    reverse_sorted_price = [float(el.text.replace("$", "")) for el in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
    assert reverse_sorted_price == sorted(prices, reverse=True)  


def test_add_multiple_items_and_verify_cart(driver):
    test_product_sorting(driver)
    # test_login_form_validation(driver)

    # ambil 3 tombol pertama
    add_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[id^='add-to-cart']"))
    )

    print(len(add_buttons))

    for button in add_buttons:
        click_when_clickable(driver, button)

    # masuk cart

    # Open cart and verify item present (avoid relying on badge)
    click_when_clickable(driver, (By.CLASS_NAME, "shopping_cart_link"))
    cart_items = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "cart_item"))
    )
    
    print(len(cart_items))

    assert len(cart_items) == 6


def test_remove_items_from_cart(driver):
    """Test removing items from cart"""
    # login_as_standard_user(driver)
    
    # Add 2 items
    test_add_multiple_items_and_verify_cart(driver)
    
    # Go to cart
    # click_when_clickable(driver, (By.CLASS_NAME, "shopping_cart_link"))
    # WebDriverWait(driver, 20).until(
    #     EC.visibility_of_element_located((By.ID, "remove-sauce-labs-backpack"))
    # )
    
    # Remove first item
    click_when_clickable(driver, (By.ID, "remove-sauce-labs-backpack"))
    
    # Verify only 1 item remains
    cart_items = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "cart_item"))
    )
    assert len(cart_items) == 5

   
def test_checkout_flow(driver):
    """Test complete checkout flow"""
    test_remove_items_from_cart(driver)

    # Navigate to checkout
    click_when_clickable(driver, (By.ID, "checkout"))

    # Wait for form load
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    )

    # Cancel once
    click_when_clickable(driver, (By.ID, "cancel"))

    # Back to cart, then checkout again
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "checkout"))
    )
    click_when_clickable(driver, (By.ID, "checkout"))

    # Wait for checkout form again
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    )

    # Isi form (ambil element fresh!)
    jar = driver.find_element(By.ID, "first-name")
    jar.clear()
    driver.execute_script("arguments[0].scrollIntoView(true);", jar)
    jar.send_keys("Jar")

    last_name = driver.find_element(By.ID, "last-name")
    last_name.clear()
    last_name.send_keys("ganteng")

    code = driver.find_element(By.ID, "postal-code")
    code.clear()
    code.send_keys("1234")

    # Assertion
    assert jar.get_attribute("value") == "Jar"
    assert last_name.get_attribute("value") == "ganteng"
    assert code.get_attribute("value") == "1234"

    # Continue to overview
    click_when_clickable(driver, (By.ID, "continue"))

    # Tunggu tombol Finish
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )

    # Klik Finish
    click_when_clickable(driver, (By.ID, "finish"))

    # Tunggu Thank You page
    thank_you_header = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    )

    

