from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class DriverExtended:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
        self.email_address_scrambled = None
        self.user_name_scrambled = None
        self.email_address_unscrambled = None
        self.user_name_unscrambled = None

    def wait_and_find_by_xpath(self, xpath):
        self.wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
        return self.driver.find_element_by_xpath(xpath)

    def wait_and_find_and_click_by_xpath(self, xpath):
        element = self.wait_and_find_by_xpath(xpath)
        element.click()

    def wait_and_find_and_send_keys(self, xpath, value):
        element = self.wait_and_find_by_xpath(xpath)
        element.send_keys(value)

    def read_and_unscramble_email(self):
        self.email_address_scrambled = self.wait_and_find_by_xpath('//span[@id="email-widget"]').text
        self.wait_and_find_and_click_by_xpath('//input[@name="alias"]')
        self.email_address_unscrambled = self.wait_and_find_by_xpath('//span[@id="email-widget"]').text
        self.user_name_scrambled = self.email_address_scrambled.split("@")[0]
        self.user_name_unscrambled = self.email_address_unscrambled.split("@")[0]

    # actions
    def click_send(self):
        self.wait_and_find_and_click_by_xpath('//input[@type="submit"][@value="Send"]')

    def click_reply(self):
        self.wait_and_find_and_click_by_xpath('//a[@id="reply_link"]')

    def click_email_by_subject(self, subject):
        self.wait_and_find_and_click_by_xpath(f'//td[text()[contains(.,"{subject}")]]')

    def fill_recipient(self, recipient):
        self.wait_and_find_and_send_keys('//input[@name="to"]', recipient)

    def fill_subject(self, subject):
        self.wait_and_find_and_send_keys('//input[@name="subject"]', subject)

    def fill_body(self, body):
        self.wait_and_find_and_send_keys('//textarea[@name="body"]', body)

    # navigation
    def go_to_inbox(self):
        self.wait_and_find_and_click_by_xpath('//a[@title="Email"]')

    def go_to_send(self):
        self.wait_and_find_and_click_by_xpath('//a[@title="Compose"]')
