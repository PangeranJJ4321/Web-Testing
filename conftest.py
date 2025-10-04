import os
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


def _is_headless() -> bool:
    return os.getenv("HEADLESS", "0") in ("1", "true", "True")


def _create_chrome_driver():
    """Create Chrome WebDriver with optimized settings"""
    headless = _is_headless()
    
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    
    # Optimized Chrome settings
    options.add_argument("--window-size=1280,800")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), 
        options=options
    )


@pytest.fixture(scope="function")
def driver():
    """WebDriver fixture - Chrome only"""
    drv = _create_chrome_driver()
    drv.implicitly_wait(10)
    yield drv
    drv.quit()
