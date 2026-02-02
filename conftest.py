import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def browser_driver():
    # Ye line automatically sahi chromedriver download karegi
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # Background mein chalane ke liye
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()