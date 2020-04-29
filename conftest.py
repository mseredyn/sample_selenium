import pytest
import configparser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os



@pytest.fixture(scope="session", autouse=False)
def get_config():
    config = configparser.ConfigParser()
    config.read("./config/config.ini")
    yield config


@pytest.fixture(scope="session", autouse=False)
def get_driver_factory():
    class DriverFactory(object):
        def __init__(self):
            self.drivers = []
        def __del__(self):
            for driver in self.drivers:
                driver.close()
        def create_driver(self, url):
            options = webdriver.ChromeOptions()
            options.add_argument("start-maximized")
            options.add_argument('disable-infobars')
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.get(url)
            self.drivers.append(driver)
            return driver

    return DriverFactory()


