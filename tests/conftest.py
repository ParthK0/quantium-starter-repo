import pytest
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


@pytest.hookimpl(tryfirst=True)
def pytest_setup_options():
    """
    Configure Chrome options for Dash testing.
    This hook is called by dash.testing to configure the browser.
    """
    # Download ChromeDriver if not already present
    chromedriver_path = ChromeDriverManager().install()
    
    # Add ChromeDriver to PATH
    chromedriver_dir = os.path.dirname(chromedriver_path)
    if chromedriver_dir not in os.environ['PATH']:
        os.environ['PATH'] = chromedriver_dir + os.pathsep + os.environ['PATH']
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    return options
