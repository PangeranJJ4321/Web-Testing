from selenium.webdriver.common.by import By


def test_example_domain_title_and_h1(driver):
    driver.get("https://example.com/")

    title = driver.title
    h1_text = driver.find_element(By.TAG_NAME, "h1").text

    assert title == "Example Domain"
    assert h1_text == "Example Domain"
