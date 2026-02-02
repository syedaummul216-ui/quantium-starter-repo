import pytest
import multiprocessing
import time
import selenium.webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from app import app  # Ensure karein aapki file ka naam app.py hai

# 1. Purane Selenium versions ka error fix karne ke liye hack
if not hasattr(selenium.webdriver, 'PhantomJS'):
    selenium.webdriver.PhantomJS = lambda *args, **kwargs: None


# 2. Server ko background mein chalane ka function
def run_server():
    # Naye Dash versions mein app.run use hota hai
    app.run(debug=False, port=8050)


@pytest.fixture(scope="module")
def driver():
    # Server start karein
    p = multiprocessing.Process(target=run_server)
    p.start()
    time.sleep(5)  # App ko load hone ke liye thoda extra time (5s) dein

    # Chrome setup (Headless takay background mein chale)
    options = Options()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    # Test khatam hone par cleanup
    driver.quit()
    p.terminate()


# 3. Actual Tests
def test_header_exists(driver):
    driver.get("http://127.0.0.1:8050")
    time.sleep(2)

    # H1 tag check kar rahe hain
    header = driver.find_element(By.TAG_NAME, "h1")
    assert "Pink Morsel" in header.text


def test_visualization_exists(driver):
    driver.get("http://127.0.0.1:8050")
    time.sleep(2)

    # Aapki app.py wali sahi ID: 'sales-line-chart'
    graph = driver.find_element(By.ID, "sales-line-chart")
    assert graph.is_displayed()